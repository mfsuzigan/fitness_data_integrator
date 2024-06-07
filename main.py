from flask import Flask, request, jsonify, render_template
import gspread
from gspread.utils import ValueInputOption

SPREADSHEET_ID = "1ETe9O2qX36aRx6243qzYNMNChQKZmxvWdRMt7htPLaM"
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/measures', methods=['POST'])
def measures():
    measures_data = request.get_json()
    app.logger.info(measures_data)

    weight_measures = measures_data.get('weight')
    fat_measures = measures_data.get('fat_perc')

    send_data_to_spreadsheet(weight_measures)

    return jsonify({'message': 'Measures received successfully'}), 200


def send_data_to_spreadsheet(weight_measures):
    gc = gspread.service_account(filename="resources/creds.json")
    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1
    row = [f"=average{tuple(weight_measures)}", "test", "test", "test"]
    sheet.append_row(row, value_input_option=ValueInputOption.user_entered)


if __name__ == "__main__":
    app.run(debug=True, port=8888, host="0.0.0.0")
