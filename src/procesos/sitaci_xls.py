from openpyxl import load_workbook
from datetime import datetime
import os
import sys

# Ensure project root is on sys.path so 'src' imports work
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

def xls_modification(filename, lon, filerows, desc='', fecha=1,
                     row_to_write=12, file= os.path.join(ROOT, 'src', 'xls', 'SITACIE_Entrada.xlsx')):
    workbook = load_workbook(filename=file)
    sheet = workbook.active

    today = datetime.now()
    if fecha == 1:
        sheet['A5'] = f'Fecha: {today.strftime("%d/%m/%Y")}'

    sheet[f'B{row_to_write}'] = filename
    sheet[f'C{row_to_write}'] = lon
    sheet[f'D{row_to_write}'] = filerows
    sheet[f'F{row_to_write}'] = desc

    workbook.save(f'SITACIE_Entrada-{today.strftime("%Y-%m-%d")}.xlsx')

    return f'SITACIE_Entrada-{today.strftime("%Y-%m-%d")}.xlsx'
