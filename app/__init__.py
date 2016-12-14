from flask import Flask
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
toolbar = DebugToolbarExtension()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  bootstrap.init_app(app)
  toolbar.init_app(app)
  mail.init_app(app)
  moment.init_app(app)
  db.init_app(app)

  if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
    from flask_sslify import SSLify
    sslify = SSLify(app)

  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  from .api_1_0 import api as api_1_0_blueprint
  app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

  return app
