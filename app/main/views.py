from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response
from flask_sqlalchemy import get_debug_queries
from . import main
from .. import db
from ..models import Permission, Role, User
from ..decorators import admin_required, permission_required


@main.after_app_request
def after_request(response):
  for query in get_debug_queries():
    if query.duration >= current_app.config['IPRM_SLOW_DB_QUERY_TIME']:
      current_app.logger.warning(
        'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
        % (query.statement, query.parameters, query.duration, query.context))
  return response


@main.route('/shutdown')
def server_shutdown():
  if not current_app.testing:
    abort(404)
  shutdown = request.environ.get('werkzeug.server.shutdown')
  if not shutdown:
    abort(500)
  shutdown()
  return 'Shutting down...'

@main.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@main.route("/", methods=['GET', 'POST'])
def index():
  form = nForm = nameForm()
  ipForm = IPForm()
  if nForm.validate_on_submit():
      old_name = session.get('name')
      if old_name is not None and old_name != nForm.name.data:
          flash('Looks like you have changed your IP query')
      session['name'] = nForm.name.data
      nForm.name.data = ''
      return redirect(url_for('index'))
  return render_template('index.html', form=nForm, ipForm=IPForm, name=session.get('name'), current_time=datetime.utcnow())

@main.route("/ip")
def ip():
  return render_template('ip.html', ips=ips(), current_time=datetime.utcnow())

@main.route('/user/<username>')
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('user.html', user=user)
