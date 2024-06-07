from flask import Flask, request, jsonify, render_template
import gspread
from gspread.utils import ValueInputOption

SPREADSHEET_ID = "1ETe9O2qX36aRx6243qzYNMNChQKZmxvWdRMt7htPLaM"
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/measurement', methods=['POST'])
def save_measurement():
    raw_data = request.get_json()
    app.logger.info(raw_data)
    send_to_spreadsheet(build_record(raw_data))

    return jsonify({'message': 'Measures received successfully'})


def build_record(data):
    record = [data["created_at_formatted"]]
    record.extend(["", "", "", "", "", "", "", "", ""])
    record.append(f"=average{tuple(data['weight'])}")
    record.extend(["", "", ""])
    record.append(f"=average{tuple(data['fat_perc'])}")
    return record


def send_to_spreadsheet(record):
    gc = gspread.service_account(filename="resources/creds.json")
    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1
    sheet.append_row(record, value_input_option=ValueInputOption.user_entered)


if __name__ == "__main__":
    app.run(debug=True, port=8888, host="0.0.0.0")
