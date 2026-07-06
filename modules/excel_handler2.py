import win32com.client
import pythoncom
import time

class ExcelHandler:

    def __init__(self, workbook_name):

        pythoncom.CoInitialize()

        print("Waiting for Excel...")

        self.excel = None

        for i in range(30):

            try:
                # Attach to an already running Excel instance
                self.excel = win32com.client.GetActiveObject("Excel.Application")
                print(type(self.excel))
                print(self.excel)
                break

            except Exception as e:
                print(type(e))
                print(e)
                print(f"Waiting for Excel... ({i+1}/30)")
                #time.sleep(1)

        if self.excel is None:
            raise Exception("Could not connect to the running Excel instance.")

        print(f"Found {self.excel.Workbooks.Count} open workbook(s).")

        self.workbook = None

        for wb in self.excel.Workbooks:

            print("Workbook:", wb.Name)

            if wb.Name.lower() == workbook_name.lower():

                self.workbook = wb
                break

        if self.workbook is None:
            raise Exception(f"{workbook_name} is not open.")

        print("Connected to:", self.workbook.Name)

        #self.sheet = self.workbook.ActiveSheet
        self.sheet = self.workbook.Worksheets("Jul 05")

        print("Worksheet:", self.sheet.Name)

    def get_phone_numbers(self):

        numbers = []

        row = 3

        while True:

            value = self.sheet.Cells(row, 2).Value   # Column A (MSISDN)

            if value is None:
                break

            # Excel returns numbers as floats
            phone = str(int(value))

            numbers.append((row, phone))

            row += 1

        return numbers

    def write_offer(self, row, column, value):

        
        print(
                f"WRITING {value} TO {column}{row}"
            )

        self.sheet.Range(
            f"{column}{row}"
        ).Value = value

    def save(self):

        self.workbook.Save()

        print("Workbook saved successfully.")

    def close(self):

        self.workbook.Close(SaveChanges=True)