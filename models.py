"""
models.py — Database Models
----------------------------
Defines SQLAlchemy ORM models for:
  - ContactMessage : stores visitor contact form submissions with sync and notification tracking
  - AdminUser      : stores admin login credentials (hashed passwords)
  - Project        : stores portfolio project data
"""

from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class ContactMessage(db.Model):
    """
    Stores messages submitted via the contact form.
    Each record represents one visitor enquiry.
    Tracks status, Google Sheets synchronization, and email notification delivery.
    """
    __tablename__ = 'contact_messages'

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    email        = db.Column(db.String(150), nullable=False)
    subject      = db.Column(db.String(200), nullable=False)
    message      = db.Column(db.Text, nullable=False)
    
    # Submission Date & Time
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) # Legacy compatibility

    # Management Status: 'New' | 'Read' | 'Replied'
    status       = db.Column(db.String(20), default='New', nullable=False)
    is_read      = db.Column(db.Boolean, default=False)

    # Google Sheets Synchronization Tracking
    sheets_synced    = db.Column(db.Boolean, default=False)
    sheets_synced_at = db.Column(db.DateTime, nullable=True)
    sheets_error     = db.Column(db.Text, nullable=True)

    # Email Notification Delivery Tracking
    email_sent       = db.Column(db.Boolean, default=False)
    email_sent_at    = db.Column(db.DateTime, nullable=True)
    email_error      = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<ContactMessage #{self.id} from {self.name} ({self.email}) [{self.status}]>'

    def mark_as_read(self):
        """Mark this message as read."""
        self.is_read = True
        if self.status == 'New':
            self.status = 'Read'
        db.session.commit()

    def mark_as_replied(self):
        """Mark this message as replied."""
        self.is_read = True
        self.status = 'Replied'
        db.session.commit()

    def mark_as_new(self):
        """Reset this message status to New."""
        self.is_read = False
        self.status = 'New'
        db.session.commit()

    def to_dict(self):
        """Serialize contact message to dictionary for JSON APIs and admin dashboard."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'submitted_at': (self.submitted_at or self.created_at).strftime('%Y-%m-%d %H:%M:%S'),
            'formatted_date': (self.submitted_at or self.created_at).strftime('%d %b %Y, %I:%M %p'),
            'status': self.status,
            'is_read': self.is_read,
            'sheets_synced': self.sheets_synced,
            'sheets_synced_at': self.sheets_synced_at.strftime('%Y-%m-%d %H:%M:%S') if self.sheets_synced_at else None,
            'sheets_error': self.sheets_error,
            'email_sent': self.email_sent,
            'email_sent_at': self.email_sent_at.strftime('%Y-%m-%d %H:%M:%S') if self.email_sent_at else None,
            'email_error': self.email_error
        }


class AdminUser(db.Model):
    """
    Stores admin user accounts.
    Passwords are NEVER stored in plain text — always hashed.
    """
    __tablename__ = 'admin_users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Hash and store the given password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Return True if the given password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser {self.username}>'


class Project(db.Model):
    """
    Stores portfolio projects.
    Can be managed from the admin dashboard.
    """
    __tablename__ = 'projects'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack  = db.Column(db.String(300))        # Comma-separated technologies
    github_url  = db.Column(db.String(300))        # Optional GitHub link
    live_url    = db.Column(db.String(300))        # Optional live demo link
    image_file  = db.Column(db.String(200))        # Filename in static/images/
    category    = db.Column(db.String(100))        # e.g. "AI/ML", "Web", "Database"
    featured    = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def tech_list(self):
        """Return tech_stack as a Python list."""
        if self.tech_stack:
            return [t.strip() for t in self.tech_stack.split(',')]
        return []

    def __repr__(self):
        return f'<Project {self.title}>'
