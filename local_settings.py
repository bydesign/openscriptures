
# Include your preferred database settings in local_settings.py
DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'... 
DATABASE_NAME = 'openscriptures'             # Or path to database file if using sqlite3.
DATABASE_USER = 'openscriptures'             # Not used with sqlite3.
DATABASE_PASSWORD = 'john316'         # Not used with sqlite3.
DATABASE_HOST = '127.0.0.1'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '3306'             # Set to empty string for default. Not used with sqlite3.

SECRET_KEY = 'Pka69bVfISbdZm' #Define this in local_settings.py

TIME_ZONE = 'America/Chicago'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/Users/jleineweber/Sites/open-scriptures/openscriptures/core/templates",
    "/Users/jleineweber/Sites/open-scriptures/openscriptures/debug_toolbar/templates",
)
CACHE_BACKEND = 'locmem:///'

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)