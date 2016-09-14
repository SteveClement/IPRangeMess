import os
basedir = os.path.abspath(os.path.dirname(__file__))

try:
  from app.secrets import *
except ImportError:
  sys.exit("Please create a file with a config dictionary in: secrets.py")

class Config:
  # Flask-WTF Config
  SECRET_KEY =  os.environ.get('SECRET_KEY') or 'H4rd t0 gu3ss $tr1ng -> Ch4nge M3!!!'
  SSL_DISABLE = False
  SQLALCHEMY_COMMIT_ON_TEARDOWN = True
  SQLALCHEMY_RECORD_QUERIES = True
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  MAIL_SERVER = 'mail.mbox.lu'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  IPRM_MAIL_SUBJECT_PREFIX = '[IPRangeMess]'
  IPRM_MAIL_SENDER = 'IPRangeMess Admin <iprm@example.com>'
  IPRM_ADMIN = os.environ.get('IPRM_ADMIN')
  IPRM_SLOW_DB_QUERY_TIME=0.5


  @staticmethod
  def init_app(app):
    pass

class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
  WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

  @classmethod
  def init_app(cls, app):
    Config.init_app(app)

    # Email errrors to admin
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    secure = None
    if getattr(cls, 'MAIL_USERNAME', None) is not None:
      credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
      if getattr(cls, 'MAIL_USE_TLS', None):
        secure = ()
    mail_handler = SMTPHandler(
      mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
      fromaddr=cls.IPRM_MAIL_SENDER,
      toaddrs=[cls.IPRM_ADMIN],
      subject=cls.IPRM_MAIL_SUBJECT_PREFIX + ' Application Error',
      credentials=credentials,
      secure=secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

class UnixConfig(ProductionConfig):
  @classmethod
  def init_app(cls, app):
    ProducitonConfig.init_app(app)

    # log to syslog
    import logging
    from logging.handlers import SysLogHandler
    syslog_handler = SysLogHandler()
    syslog_handler.setLevel(logging.WARNING)
    app.logger.addHandler(syslog_handler)

config = {
  'development' : DevelopmentConfig,
  'testing' : TestingConfig,
  'production' : ProductionConfig,
  'unix' : UnixConfig,

  'default' : DevelopmentConfig
}
