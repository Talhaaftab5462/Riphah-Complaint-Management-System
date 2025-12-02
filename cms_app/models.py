from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Complaints submitted BY this user
    complaints = db.relationship(
        "Complaint",
        foreign_keys="Complaint.user_id",
        backref="owner",
        lazy=True
    )

    # Complaints assigned TO this user (staff/admin)
    assigned_complaints = db.relationship(
        "Complaint",
        foreign_keys="Complaint.assigned_to",
        backref="assigned_staff",
        lazy=True
    )

    # Comments made by this user
    comments = db.relationship("Comment", back_populates="user", lazy=True)

    # Notifications for this user
    notifications = db.relationship('Notification', back_populates='user', lazy=True)


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(10), nullable=True)
    attachment = db.Column(db.String(100), nullable=True)  # store file path
    status = db.Column(db.String(20), default="Pending")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Complaints assigned to an admin/staff
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    assigned_user = db.relationship(
        'User',
        foreign_keys=[assigned_to],
        overlaps="assigned_complaints,assigned_staff"
    )

    # Relationship to comments
    comments = db.relationship(
        'Comment',
        back_populates='complaint',
        cascade='all, delete-orphan'
    )


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    complaint = db.relationship('Complaint', back_populates='comments')
    user = db.relationship('User', back_populates='comments')


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Use back_populates to avoid backref conflict
    user = db.relationship('User', back_populates='notifications')
