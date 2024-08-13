import os

import gspread

from app import create_app
from exceptions import MissingEnvironmentVariableError

GOOGLE_API_CREDENTIALS_FILE_PATH = "resources/credentials.json"

flask_configuration_by_environment = {
    "test": {
        "object": "config_test.TestConfig",
        "message": "⚠️  Running TEST environment️"
    },
    "production": {
        "object": "config.Config",
        "message": None
    }
}


def main():
    service_account = get_service_account()
    app = create_app(service_account)
    set_flask_env(app)
    app.run(debug=True, port=8888, host="0.0.0.0")


def set_flask_env(app):
    flask_env = os.getenv("FLASK_ENV", default="production").lower()
    app.config.from_object(flask_configuration_by_environment[flask_env]["object"])
    app.logger.warning(flask_configuration_by_environment[flask_env]["message"])


def get_service_account():
    if not os.path.exists(GOOGLE_API_CREDENTIALS_FILE_PATH):
        raise MissingEnvironmentVariableError("Google service account credentials not set")

    return gspread.service_account(filename=GOOGLE_API_CREDENTIALS_FILE_PATH)


if __name__ == "__main__":
    main()
