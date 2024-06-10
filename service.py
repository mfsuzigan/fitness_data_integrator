import gspread
import gspread_formatting
from gspread.utils import ValueInputOption

SPREADSHEET_ID = "1mukK9oAWguKaMmlnI_lzaqBBxs1Z2UbCCCr9vCwFldY"

formula_by_column_name = {
    "A": "%SINGLE_VALUE%",
    "B": "=DATEDIF(\"1987-11-17\";A%ROW_NUM%;\"y\")",
    "F": "=C%ROW_NUM%-E%ROW_NUM%",
    "G": "=F%ROW_NUM%/E%ROW_NUM%",
    "K": "=AVERAGE%TUPLE%",
    "L": "=(K%ROW_NUM%-K%PREVIOUS_ROW_NUM%)*100",
    "M": "=(K%ROW_NUM%/K%PREVIOUS_ROW_NUM%)-1",
    "N": "=K%ROW_NUM%/POWER(1,67;2)",
    "O": "=AVERAGE%TUPLE%",
    "P": "=AVERAGE%TUPLE%",
    "Q": "=AVERAGE%TUPLE%",
    "R": "=AVERAGE%TUPLE%",
    "S": "%SINGLE_VALUE%",
    "T": "=K128-(K%ROW_NUM%*O%ROW_NUM%/100)",
    "U": "=(T%ROW_NUM%/T%PREVIOUS_ROW_NUM%)-1",
    "V": "=K%ROW_NUM%-T%ROW_NUM%",
    "W": "=(V%ROW_NUM%/V%PREVIOUS_ROW_NUM%)-1",
    "X": "=T%ROW_NUM%/(1,67^2)",
    "Y": "=X%ROW_NUM%/S%ROW_NUM%",
    "Z": "=(U42-W42)*100",
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

        if column_name in formula_by_column_name:
            cell_value = (formula_by_column_name[column_name]
                          .replace("%PREVIOUS_ROW_NUM%", f"{last_row_number}")
                          .replace("%ROW_NUM%", f"{new_row_number}"))

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
