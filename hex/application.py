from flask import Flask
import flask_profiler
from hex.configuration import configure_inject, configure_application, configure_profiler
from hex.web.post_blueprint import create_post_blueprint


def create_application() -> Flask:
    application = Flask(__name__)
    configure_application(application)
    configure_inject(application)
    configure_profiler(application)

    application.register_blueprint(create_post_blueprint(), url_prefix='/api')

    flask_profiler.init_app(application)

    return application
