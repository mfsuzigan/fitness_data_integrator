import json
import os
from flask import Flask, request, jsonify, render_template
from service import save_to_stats_spreadsheet, save_to_requests_log, update_weight_in_diet_spreadsheet, \
    load_diet_spreadsheet, load_diet_properties

app = Flask(__name__)
config_type = os.getenv('FLASK_ENV', 'production')

if config_type.lower() == 'test':
    app.config.from_object('config_test.TestConfig')
    app.logger.warning("⚠️  Running TEST environment️")

else:
    app.config.from_object('config.Config')


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/measurement', methods=['POST'])
def save_measurement():
    input_data = request.get_json()
    app.logger.info(input_data)
    save_to_requests_log(json.dumps(input_data))

    load_diet_spreadsheet(app.config['DIET_SPREADSHEET_ID'])
    load_diet_properties()
    save_to_stats_spreadsheet(input_data, app.config['STATS_SPREADSHEET_ID'])
    update_weight_in_diet_spreadsheet(input_data)

    return jsonify({'message': 'Measurements received successfully'})


if __name__ == "__main__":
    app.run(debug=True, port=8888, host="0.0.0.0")
