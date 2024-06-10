import gspread
import gspread_formatting
from gspread.utils import ValueInputOption

SPREADSHEET_ID = "1mukK9oAWguKaMmlnI_lzaqBBxs1Z2UbCCCr9vCwFldY"

formula_by_column_name = {
    "B": "=DATEDIF(\"1987-11-17\";A%ROW%;\"y\")",
    "F": "=C%ROW%-E%ROW%",
    "G": "=F%ROW%/E%ROW%",
    "K": "=AVERAGE%VALUE_TUPLE%",
    "L": "=(K%ROW%-K%PREVIOUS_ROW%)*100",
    "M": "=(K%ROW%/K%PREVIOUS_ROW%)-1",
    "N": "=K%ROW%/POWER(1,67;2)",
    "O": "=AVERAGE%VALUE_TUPLE%",
    "P": "=AVERAGE%VALUE_TUPLE%",
    "Q": "=AVERAGE%VALUE_TUPLE%",
    "R": "=AVERAGE%VALUE_TUPLE%",
    "U": "=(T%ROW%/T%ROW%)-1",
    "V": "=K%ROW%-T%ROW%",
    "W": "=(V%ROW%/V%PREVIOUS_ROW%)-1",
    "X": "=T%ROW%/(1,67^2)",
    "Y": "=X%ROW%/S%ROW%",
    "Z": "=(U42-W42)*100",
    "AA": "=AVERAGE%VALUE_TUPLE%",
    "AB": "=AVERAGE%VALUE_TUPLE%",
    "AC": "=AVERAGE%VALUE_TUPLE%",
}

property_by_column_name = {
    "K": "weight",
    "O": "fat_perc",
    "P": "musc_perc",
    "Q": "vfat_perc",
    "R": "body_age",
    "AA": "systolic_bp",
    "AB": "diastolic_bp",
    "AC": "heart_rate"
}


def save_data(input_data):
    worksheet = get_worksheet()
    last_row_number = len(worksheet.col_values(1))
    copy_last_row_formatting(worksheet, last_row_number)

    last_row_values = worksheet.row_values(last_row_number)
    new_row_number = last_row_number + 1

    worksheet.update([build_new_row(input_data, last_row_number, last_row_values)],
                     f"{new_row_number}:{new_row_number}",
                     value_input_option=ValueInputOption.user_entered)


def build_new_row(input_data, last_row_number, last_row_values):
    new_row_number = last_row_number + 1
    new_row_values = []

    for index, old_value in enumerate(last_row_values):
        column_name = get_column_name_by_index(index + 1)

        if index == 0:
            cell_value = input_data["date"]

        elif column_name in formula_by_column_name:
            cell_value = (formula_by_column_name[column_name]
                          .replace("%PREVIOUS_ROW%", f"{last_row_number}")
                          .replace("%ROW%", f"{new_row_number}"))

            if column_name in property_by_column_name:
                _tuple = str(tuple(input_data[property_by_column_name[column_name]])).replace(",", ";")
                cell_value = cell_value.replace("%VALUE_TUPLE%", f"{_tuple}")
        else:
            cell_value = ""

        new_row_values.append(cell_value)

    return new_row_values


def copy_last_row_formatting(worksheet, last_row_number):
    column_count = len(worksheet.row_values(1))

    for column_number in range(1, column_count + 1):
        column_name = get_column_name_by_index(column_number)
        cell_format = gspread_formatting.get_user_entered_format(worksheet, f"{column_name}{last_row_number}")
        gspread_formatting.format_cell_range(worksheet, f"{column_name}{last_row_number + 1}", cell_format)


def get_column_name_by_index(index):
    column_name = ""

    while index > 0:
        index, remainder = divmod(index - 1, 26)
        column_name = chr(65 + remainder) + column_name

    return column_name


def get_worksheet():
    gc = gspread.service_account(filename="resources/creds.json")
    return gc.open_by_key(SPREADSHEET_ID).sheet1
