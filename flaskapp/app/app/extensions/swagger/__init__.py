from flask import Blueprint, jsonify
main = Blueprint('main', __name__)

from flask_swagger_ui import get_swaggerui_blueprint
from .spec import spec

SWAGGER_URL = '/api/docs'
API_URL = "/static/swagger.json"

# Call factory function to create our blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My App"
    }
)


def init_app(app):
    """
    Init swagger ui.

    with app.test_request_context():
        for fn_name in app.view_functions:
            if fn_name == 'static':
                print("static function {0}".format(fn_name))
                continue
            view_fn = app.view_functions[fn_name]
            spec.path(view=view_fn)

    format_swagger_json(app)
    """
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


def format_swagger_json(app):
    # Create tables if they do not exist already
    @app.route("/api/swagger.json")
    def create_swagger_spec():
        """
        Swagger API definition.
        """
        return jsonify(spec.to_dict())
