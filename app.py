from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from config import Config
from controllers.task_controller import task_bp
from controllers.schedule_controller import schedule_bp
from controllers.page_controller import page_bp

def create_app():
    app = Flask(
        __name__,
        static_folder="views/static",
        template_folder="views/templates"
    )
    app.config.from_object(Config)

    # API blueprints
    app.register_blueprint(task_bp, url_prefix='/tasks')
    app.register_blueprint(schedule_bp, url_prefix='/schedule')
    # Page blueprint (renders HTML)
    app.register_blueprint(page_bp, url_prefix='')

    return app

if __name__ == '__main__':
    app = create_app()
    # turn off the reloader but keep debug on
    app.run(debug=True, use_reloader=False)
