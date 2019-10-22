import pymysql
pymysql.install_as_MySQLdb()

DEV = True
DEBUG = True
# THUMBNAIL_DEBUG = True
CACHING = False
DB_USER = 'root'
DB_PASS = ''
SECRET_KEY = 'somesecretkey'
ADMIN_EMAIL = SERVER_EMAIL = 'marketing@unilexicon.com'
INTERNAL_IPS = ('127.0.0.1',)

# imap
EMAIL_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = 'marketing@unilexicon.com'
EMAIL_PASSWORD = ''

# smtp
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = EMAIL_ACCOUNT
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD

PAY_PAYPAL_EMAIL = PAY_RECEIPT_EMAIL = 'marketing@unilexicon.com'
