import gspread
from gspread.utils import ValueInputOption

SPREADSHEET_ID = "1ETe9O2qX36aRx6243qzYNMNChQKZmxvWdRMt7htPLaM"


def save_data(raw_data):
    record = build_record(raw_data)
    worksheet = get_worksheet()
    duplicate_worksheet_last_row(worksheet)


def build_record(data):
    record = [data["created_at_formatted"]]
    record.extend(["", "", "", "", "", "", "", "", ""])
    record.append(f"=average{tuple(data['weight'])}")
    record.extend(["", "", ""])
    record.append(f"=average{tuple(data['fat_perc'])}")
    return record


def duplicate_worksheet_last_row(worksheet):
    row_count = len(worksheet.col_values(1))
    last_row = worksheet.row_values(row_count)
    next_row = row_count + 1
    worksheet.update([last_row], f"{next_row}:{next_row}")

    # for col in range(1, len(last_row)):
    #     cell_formats.append(spreadsheet.get_formatted_value(7, col))
    #
    # spreadsheet.update_row(8, last_row)
    #
    # for i, cell_format in enumerate(cell_formats):
    #     spreadsheet.format(f"B{8 + 1}", cell_format)


def get_worksheet():
    gc = gspread.service_account(filename="resources/creds.json")
    return gc.open_by_key(SPREADSHEET_ID).sheet1

# def send_to_spreadsheet(record):
#     sheet.append_row(record, value_input_option=ValueInputOption.user_entered)
