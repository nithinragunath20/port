"""
extensions.py — Flask Extensions
----------------------------------
Initialises Flask extensions without binding them to a specific app instance.
This pattern (Application Factory) prevents circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# SQLAlchemy instance — shared across all models
db = SQLAlchemy()

# CSRF protection instance
csrf = CSRFProtect()
