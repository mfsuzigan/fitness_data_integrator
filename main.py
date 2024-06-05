from flask import Flask, request, jsonify
import gspread

SPREADSHEET_ID = "1ETe9O2qX36aRx6243qzYNMNChQKZmxvWdRMt7htPLaM"
app = Flask(__name__)


@app.route('/measures', methods=['OPTIONS'])
def measures():
    if request.is_json:
        try:
            measures_data = request.get_json()
            weight_measures = measures_data.get('weight')
            fat_measures = measures_data.get('fat%')
            return jsonify({'message': 'Measures received successfully'}), 200

        except Exception as e:
            return jsonify({'error': 'Invalid JSON format'}), 400
    else:
        return jsonify({'error': 'Request must contain JSON data'}), 400


def main():
    gc = gspread.service_account(filename="creds.json")
    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1
    row = ["=average(2, 2, 1)", "2", "3", "4"]
    sheet.append_row(row, value_input_option="USER_ENTERED")


if __name__ == "__main__":
    app.run(debug=True)
