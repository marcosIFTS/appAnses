from openpyxl import Workbook


def save_xlsx(header, rows, filename):
    workbook = Workbook()
    sheet = workbook.active

    sheet.append(header)

    line = 2
    for row in rows:
        sheet[f'A{line}'] = row[0]
        sheet[f'B{line}'] = row[1]
        sheet[f'C{line}'] = row[2]
        sheet[f'D{line}'] = row[3]
        sheet[f'E{line}'] = row[4]
        sheet[f'F{line}'] = row[5]
        sheet[f'G{line}'] = row[6]
        sheet[f'H{line}'] = row[7]
        sheet[f'I{line}'] = row[8]
        sheet[f'J{line}'] = row[9]
        sheet[f'K{line}'] = row[10]
        sheet[f'L{line}'] = row[11]
        sheet[f'M{line}'] = row[12]
        sheet[f'N{line}'] = row[13]
        sheet[f'O{line}'] = row[14]
        line += 1

    workbook.save(f'{filename}')
