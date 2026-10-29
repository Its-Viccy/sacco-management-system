from django.db.backends.base.base import BaseDatabaseWrapper

# Allow Django 5.1 to run on XAMPP's MariaDB 10.4.32
BaseDatabaseWrapper.check_database_version_supported = lambda self: None