import gspread
import gspread_formatting
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
    last_row_number = len(worksheet.col_values(1))
    last_row_values = worksheet.row_values(last_row_number)

    next_row_number = last_row_number + 1
    worksheet.update([last_row_values], f"{next_row_number}:{next_row_number}",
                     value_input_option=ValueInputOption.user_entered)

    column_count = len(worksheet.row_values(1))

    for column_number in range(1, column_count):
        column_name = chr(ord('@') + column_number)
        cell_format = gspread_formatting.get_user_entered_format(worksheet, f"{column_name}{last_row_number}")
        gspread_formatting.format_cell_range(worksheet, f"{column_name}{next_row_number}", cell_format)

    # TODO:
    # 1. column names for: "AA", "AB" etc
    # 2. preserve formulas at copying


def get_worksheet():
    gc = gspread.service_account(filename="resources/creds.json")
    return gc.open_by_key(SPREADSHEET_ID).sheet1

# def send_to_spreadsheet(record):
#     sheet.append_row(record, value_input_option=ValueInputOption.user_entered)
