import os.path

import gspread
import gspread_formatting
import pickle
from gspread.utils import ValueInputOption

SPREADSHEET_ID = "1mukK9oAWguKaMmlnI_lzaqBBxs1Z2UbCCCr9vCwFldY"
COLUMN_COUNT = 33

formula_by_column_name = {
    "A": "%SINGLE_VALUE%",
    "B": "=DATEDIF(\"1987-11-17\";A%N%;\"y\")",
    "F": "=C%N%-E%N%",
    "G": "=F%N%/E%N%",
    "K": "=AVERAGE%TUPLE%",
    "L": "=(K%N%-K%PREVIOUS_ROW_NUM%)*100",
    "M": "=(K%N%/K%PREVIOUS_ROW_NUM%)-1",
    "N": "=K%N%/POWER(1,67;2)",
    "O": "=AVERAGE%TUPLE%",
    "P": "=AVERAGE%TUPLE%",
    "Q": "=AVERAGE%TUPLE%",
    "R": "=AVERAGE%TUPLE%",
    "S": "%SINGLE_VALUE%",
    "T": "=K128-(K%N%*O%N%/100)",
    "U": "=(T%N%/T%PREVIOUS_ROW_NUM%)-1",
    "V": "=K%N%-T%N%",
    "W": "=(V%N%/V%PREVIOUS_ROW_NUM%)-1",
    "X": "=T%N%/(1,67^2)",
    "Y": "=X%N%/S%N%",
    "Z": "=(U%N%-W%N%)*100",
    "AA": "=AVERAGE%TUPLE%",
    "AB": "=AVERAGE%TUPLE%",
    "AC": "=AVERAGE%TUPLE%",
}

property_by_column_name = {
    "A": "date",
    "K": "weight",
    "O": "fat_perc",
    "P": "musc_perc",
    "Q": "vfat_perc",
    "R": "body_age",
    "S": "waist",
    "AA": "systolic_bp",
    "AB": "diastolic_bp",
    "AC": "heart_rate"
}

cell_formats_by_range = {
    "A:A": "date_normal_gray",
    "K:X": "decimal2_normal_white",
    "Q:S": "decimal1_normal_white",
    "AA:AG": "integer_normal_white",
    "B:J": "integer_bold_gray",
    "F:F": "integer_bold_grayer",
    "D:D": "decimal1_bold_gray",
    "G:G": "signaledpercentage2_bold_grayer",
    "L:L": "signaledinteger_normal_white",
    "M:M": "signaledpercentage2_normal_white",
    "U:U": "signaledpercentage2_normal_white",
    "W:W": "signaledpercentage2_normal_white",
    "Y:Y": "decimal3_normal_white",
    "Z:Z": "signaleddecimal2_normal_white"
}


def save_to_file(request):
    with open("requests.log", "a") as file_log:
        file_log.writelines(f"\n{request}")


def save_to_spreadsheet(input_data):
    worksheet = get_worksheet()
    # save_row_format_to_disk(worksheet)

    last_row_number = len(worksheet.col_values(1))
    new_row_number = last_row_number + 1

    apply_row_formatting(worksheet, new_row_number)

    new_row_values = build_new_row(input_data, last_row_number, COLUMN_COUNT)
    worksheet.update([new_row_values], f"{new_row_number}:{new_row_number}",
                     value_input_option=ValueInputOption.user_entered)


def save_row_format_to_disk(worksheet):
    for _range in cell_formats_by_range:
        if not os.path.exists(f"cell_formats/{cell_formats_by_range[_range]}"):
            cell_format = gspread_formatting.get_user_entered_format(worksheet, f"{_range.split(':')[0]}127")
            save_cell_format_to_disk(cell_format, cell_formats_by_range[_range])


def save_cell_format_to_disk(cell_format, name):
    os.makedirs("cell_formats", exist_ok=True)
    with open(f"cell_formats/{name}.format", "wb") as file:
        pickle.dump(cell_format, file)


def load_cell_format_from_disk(name):
    with open(f"cell_formats/{name}.format", "rb") as file:
        return pickle.load(file)


def build_new_row(input_data, last_row_number, column_count):
    new_row_number = last_row_number + 1
    new_row_values = []

    for column_index in range(1, column_count):
        column_name = get_column_name_by_index(column_index)

        if column_name in formula_by_column_name:
            cell_value = (formula_by_column_name[column_name]
                          .replace("%PREVIOUS_ROW_NUM%", f"{last_row_number}")
                          .replace("%N%", f"{new_row_number}"))

            if column_name in property_by_column_name:
                _property_name = property_by_column_name[column_name]

                if formula_by_column_name[column_name] == "%SINGLE_VALUE%":
                    cell_value = cell_value.replace("%SINGLE_VALUE%", input_data[_property_name])

                else:
                    _tuple = str(tuple(input_data[_property_name])).replace(",", ";")
                    cell_value = cell_value.replace("%TUPLE%", f"{_tuple}")
        else:
            cell_value = ""

        cell_value = cell_value.replace(".", ",")
        new_row_values.append(cell_value)

    return new_row_values


def apply_row_formatting(worksheet, new_row_number):
    for original_range in cell_formats_by_range:
        applicable_cell_format = load_cell_format_from_disk(cell_formats_by_range[original_range])
        range_parts = original_range.split(":")
        applied_range = f"{range_parts[0]}{new_row_number}:{range_parts[1]}{new_row_number}"
        gspread_formatting.format_cell_range(worksheet, applied_range, applicable_cell_format)


def get_column_name_by_index(index):
    column_name = ""

    while index > 0:
        index, remainder = divmod(index - 1, 26)
        column_name = chr(65 + remainder) + column_name

    return column_name


def get_worksheet():
    gc = gspread.service_account(filename="resources/creds.json")
    return gc.open_by_key(SPREADSHEET_ID).sheet1
