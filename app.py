import json
from flask import Flask, render_template, request, jsonify

from service import *


def create_app(service_account):
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route('/measurement', methods=['POST'])
    def save_measurement():
        input_data = request.get_json()
        app.logger.info(input_data)
        log_request(json.dumps(input_data))

        diet_spreadsheet = service_account.open_by_key(app.config['DIET_SPREADSHEET_ID'])
        load_diet_properties(input_data["diet_worksheet_scheme"], diet_spreadsheet)

        stats_worksheet = service_account.open_by_key(app.config['STATS_SPREADSHEET_ID']).sheet1
        save_to_stats_spreadsheet(input_data, stats_worksheet)

        update_weight_in_diet_spreadsheet(input_data, diet_spreadsheet)

        return jsonify({'message': 'Stats received successfully'})

    return app
