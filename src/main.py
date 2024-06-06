from flask import Flask, request, jsonify
import gspread
from gspread.utils import ValueInputOption

SPREADSHEET_ID = "1ETe9O2qX36aRx6243qzYNMNChQKZmxvWdRMt7htPLaM"
app = Flask(__name__)


@app.route('/measures', methods=['POST'])
def measures():
    measures_data = request.get_json()
    weight_measures = measures_data.get('weight')
    fat_measures = measures_data.get('fat%')
    return jsonify({'message': 'Measures received successfully'}), 200


@app.route('/', methods=['OPTIONS'])
def preflight():
    return jsonify()


def main():
    gc = gspread.service_account(filename="resources/creds.json")
    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1
    row = ["=average(2, 2, 1)", "2", "3", "4"]
    sheet.append_row(row, value_input_option=ValueInputOption.user_entered)


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


app.after_request(add_cors_headers)

if __name__ == "__main__":
    app.run(debug=True)
