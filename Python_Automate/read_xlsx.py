import openpyxl
wb = openpyxl.load_workbook('/Users/weizheng/PycharmProjects/football/result.xlsx')
print(wb.get_sheet_names())