from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="sqlite:///blogchain.sqlite.db",
    )
    
    from .models import db
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .routes.home import home_bp
    from .routes.create import create_bp
    from .routes.auth import auth_bp
    from .routes.viewPost import viewPost_bp
    from .routes.profile import profile_bp
    from .routes.delete import delete_bp
    from .routes.settings import settings_bp

    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect(app) # for logout form which does not use WTForm

    from flask_moment import Moment
    moment = Moment(app)

    app.register_blueprint(home_bp, csrf=csrf)
    app.register_blueprint(create_bp, url_prefix='/create')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(viewPost_bp, url_prefix='/users')
    app.register_blueprint(profile_bp, url_prefix='/users')
    app.register_blueprint(delete_bp)
    app.register_blueprint(settings_bp, url_prefix='/settings')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()