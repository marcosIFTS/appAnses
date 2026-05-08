import csv


def save_file(filename, enc, cursor, header=0, footer=0):
    with open(f"{filename}", 'w', newline='', encoding=enc) as csv_file:
        csv_writer = csv.writer(csv_file, 
                                quotechar='\\', quoting=csv.QUOTE_NONE,
                                delimiter='|')
        if header != 0:
            csv_writer.writerow([header])
        csv_writer.writerows(cursor)
        if footer != 0:
            csv_writer.writerow([footer])
