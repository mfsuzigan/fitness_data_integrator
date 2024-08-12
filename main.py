import os

import gspread

from app import create_app
from exceptions import MissingEnvironmentVariableError

GOOGLE_API_CREDENTIALS_FILE_PATH = "resources/credentials.json"


def main():
    service_account = get_service_account()
    app = create_app(service_account)
    set_flask_env(app)
    app.run(debug=True, port=8888, host="0.0.0.0")


def set_flask_env(app):
    config_type = os.getenv('FLASK_ENV', default='production')

    if config_type.lower() == 'test':
        app.config.from_object('config_test.TestConfig')
        app.logger.warning("⚠️  Running TEST environment️")

    else:
        app.config.from_object('config.Config')


def get_service_account():
    if not os.path.exists(GOOGLE_API_CREDENTIALS_FILE_PATH):
        raise MissingEnvironmentVariableError("Google service account credentials not set")

    return gspread.service_account(filename=GOOGLE_API_CREDENTIALS_FILE_PATH)


if __name__ == "__main__":
    main()
