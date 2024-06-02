import gspread

SPREADSHEET_ID = "1ETe9O2qX36aRx6243qzYNMNChQKZmxvWdRMt7htPLaM"


def main():
    gc = gspread.service_account(filename="creds.json")
    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1
    row = ["1", "2", "3", "4"]
    sheet.append_row(row)


if __name__ == "__main__":
    main()
