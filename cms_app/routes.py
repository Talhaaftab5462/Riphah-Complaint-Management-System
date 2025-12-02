from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user, logout_user
from . import db, login_manager
from .models import User, Complaint, Comment, Notification
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from cms_app.forms import ComplaintForm
from cms_app.models import Complaint
from sqlalchemy import func
import os

main = Blueprint("main", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        flash("Invalid credentials")
    return render_template("login.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@main.route('/dashboard')
@login_required
def dashboard():

    if current_user.is_admin:
        complaints = Complaint.query.all()
        user_filter = True  # Means “no filter”
    else:
        complaints = Complaint.query.filter_by(user_id=current_user.id).all()
        user_filter = Complaint.user_id == current_user.id

    # Statistics
    total_complaints = len(complaints)

    pending_count = Complaint.query.filter(
        Complaint.status == 'Pending',
        user_filter
    ).count()

    in_progress_count = Complaint.query.filter(
        Complaint.status == 'In Progress',
        user_filter
    ).count()

    resolved_count = Complaint.query.filter(
        Complaint.status == 'Resolved',
        user_filter
    ).count()

    approved_count = Complaint.query.filter(
        Complaint.status == 'Approved',
        user_filter
    ).count()

    denied_count = Complaint.query.filter(
        Complaint.status == 'Denied',
        user_filter
    ).count()

    # Complaints by category
    if current_user.is_admin:
        category_counts = Complaint.query.with_entities(
            Complaint.category,
            func.count(Complaint.id)
        ).group_by(Complaint.category).all()
    else:
        category_counts = Complaint.query.with_entities(
            Complaint.category,
            func.count(Complaint.id)
        ).filter(
            Complaint.user_id == current_user.id
        ).group_by(Complaint.category).all()

    users = User.query.filter_by(is_admin=True).all() if current_user.is_admin else []

    return render_template(
        'dashboard.html',
        complaints=complaints,
        total_complaints=total_complaints,
        pending_count=pending_count,
        in_progress_count=in_progress_count,
        resolved_count=resolved_count,
        approved_count=approved_count,
        denied_count=denied_count,
        category_counts=category_counts,
        users=users
    )


@main.route("/submit_complaint", methods=["GET", "POST"])
@login_required
def submit_complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        # Handle file upload
        file = request.files.get("attachment")
        filename = None
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.root_path, "static/uploads")
            os.makedirs(upload_path, exist_ok=True)  # Ensure folder exists
            file.save(os.path.join(upload_path, filename))

        new_complaint = Complaint(
            title=form.title.data,
            category=form.category.data,
            priority=form.priority.data,
            description=form.description.data,
            user_id=current_user.id,
            attachment=filename  # Save filename in DB
        )
        db.session.add(new_complaint)
        db.session.commit()
        flash("Complaint submitted successfully!", "success")
        return redirect(url_for("main.dashboard"))
    
    return render_template("complaint_form.html", form=form)

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered.")
            return redirect(url_for("main.register"))

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for("main.login"))

    return render_template("register.html")

@main.route("/update_status/<int:complaint_id>/<string:status>")
@login_required
def update_status(complaint_id, status):
    if not current_user.is_admin:
        flash("Unauthorized", "danger")
        return redirect(url_for("main.dashboard"))

    complaint = Complaint.query.get_or_404(complaint_id)
    if status not in ["Pending", "Approved", "Denied", "In Progress", "Resolved"]:
        flash("Invalid status", "danger")
        return redirect(url_for("main.dashboard"))

    complaint.status = status
    db.session.commit()

    # Create a notification for the complaint owner
    from .models import Notification
    notif_message = f"Your complaint '{complaint.title}' status has been updated to '{status}'."
    notification = Notification(user_id=complaint.owner.id, message=notif_message)
    db.session.add(notification)
    db.session.commit()

    flash(f"Complaint status updated to {status}.", "success")
    return redirect(url_for("main.dashboard"))

@main.route("/complaint/<int:complaint_id>", methods=["GET", "POST"])
@login_required
def view_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)

    # POST handling
    if request.method == "POST":
        # Normal users can only comment on their own complaints
        if not current_user.is_admin and complaint.user_id != current_user.id:
            flash("You cannot comment on this complaint.", "danger")
            return redirect(url_for("main.view_complaint", complaint_id=complaint.id))

        # Admins/staff can only comment if assigned
        if current_user.is_admin and complaint.assigned_to != current_user.id:
            flash("You are not assigned to this complaint. You can only view it.", "danger")
            return redirect(url_for("main.view_complaint", complaint_id=complaint.id))

        # Block comments if complaint is resolved or denied
        if complaint.status in ["Resolved", "Denied"]:
            flash("You cannot comment on this complaint.", "danger")
            return redirect(url_for("main.view_complaint", complaint_id=complaint.id))

        # Add the comment
        comment_text = request.form.get("comment")
        if comment_text:
            comment = Comment(
                complaint_id=complaint.id,
                user_id=current_user.id,
                text=comment_text
            )
            db.session.add(comment)
            db.session.commit()
            flash("Comment added.", "success")
            return redirect(url_for("main.view_complaint", complaint_id=complaint.id))

    return render_template("view_complaint.html", complaint=complaint)

@main.route('/assign/<int:complaint_id>', methods=['POST'])
@login_required
def assign_complaint(complaint_id):

    if not current_user.is_admin:
        return "Unauthorized", 403

    complaint = Complaint.query.get_or_404(complaint_id)
    staff_id = request.form.get("staff_id")

    if not staff_id:
        return "No staff selected", 400

    complaint.assigned_to = staff_id
    db.session.commit()

    return redirect(url_for('main.dashboard'))

@main.route('/notification/read/<int:id>')
@login_required
def read_notification(id):
    notification = Notification.query.get_or_404(id)
    
    # Make sure the current user owns this notification
    if notification.user_id != current_user.id:
        flash("You cannot access this notification.", "danger")
        return redirect(url_for('main.dashboard'))
    
    # Mark as read
    notification.is_read = True
    db.session.commit()
    
    # Redirect wherever you want, e.g., dashboard or complaint view
    return redirect(url_for('main.dashboard'))