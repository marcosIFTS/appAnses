import os
import sys
import threading
import codecs
import zipfile
from datetime import date
import tkinter as tk
from tkinter import messagebox

# Ensure project root is on sys.path so 'src' imports work
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

# In PyInstaller onefile, bundled resources are extracted under sys._MEIPASS.
BASE_PATH = getattr(sys, '_MEIPASS', ROOT)


def resource_path(*parts):
    return os.path.join(BASE_PATH, *parts)

from src.sql.hf_ppc import conn
from src.defs.pagos_hf import file_specs
from src.procesos.sitaci_xls import xls_modification
from src.procesos.export_csv import save_file
from src.procesos.export_xlsx import save_xlsx

import pyodbc


class PagosApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ANSES - Generador Archivos de Pagos PAS')
        self.geometry('760x360')

        self.cnxn = None
        self.cursor = None
        self.mod_file = None
        self.footer_image = None

        self._build()

    def _build(self):
        row = 0
        tk.Label(self, text='Conexión a base de datos').grid(column=0, row=row, sticky='w', padx=10, pady=6)
        self.btn_connect = tk.Button(self, text='Conectar DB', width=20, command=self._threaded(self.connect_db))
        self.btn_connect.grid(column=1, row=row, padx=10, pady=6)

        row += 1
        tk.Label(self, text='Período (YYYYMM)').grid(column=0, row=row, sticky='w', padx=10, pady=6)
        self.period_var = tk.StringVar()
        self.entry_period = tk.Entry(self, textvariable=self.period_var)
        self.entry_period.grid(column=1, row=row, padx=10, pady=6)

        row += 1
        self.btn_generate = tk.Button(self, text='Generar tabla (gen_PagosANSeS)', width=30, command=self._threaded(self.generate_table))
        self.btn_generate.grid(column=0, row=row, columnspan=2, padx=10, pady=6)
        self.btn_generate.config(state='disabled')

        row += 1
        self.btn_export = tk.Button(self, text='Exportar TXT - ansi / utf-8', width=30, command=self._threaded(self.export_files))
        self.btn_export.grid(column=0, row=row, columnspan=2, padx=10, pady=6)
        self.btn_export.config(state='disabled')

        row += 1
        tk.Label(self, text='Estado:').grid(column=0, row=row, sticky='w', padx=10, pady=6)
        self.status_var = tk.StringVar(value='Desconectado')
        self.lbl_status = tk.Label(self, textvariable=self.status_var, fg='blue')
        self.lbl_status.grid(column=1, row=row, sticky='w')

        row += 1
        tk.Label(self, text='Mensajes:').grid(column=0, row=row, sticky='nw', padx=10, pady=6)
        self.txt_messages = tk.Text(self, height=4, width=60, state='disabled')
        self.txt_messages.grid(column=0, row=row, columnspan=2, padx=10, pady=6)

        row += 1
        footer = tk.Frame(self, bd=1, relief='sunken')
        footer.grid(column=0, row=row, columnspan=2, sticky='ew', padx=10, pady=(8, 6))
        self._build_footer(footer)

    def _build_footer(self, parent):
        image_path = resource_path('src', 'img', 'datosPAS_pie.png')
        if not os.path.exists(image_path):
            tk.Label(parent, text='Imagen de pie no encontrada', fg='gray').pack(padx=8, pady=6)
            return

        try:
            img = tk.PhotoImage(file=image_path)
            max_w = 620
            max_h = 70

            sub_x = max(1, (img.width() + max_w - 1) // max_w)
            sub_y = max(1, (img.height() + max_h - 1) // max_h)
            img = img.subsample(sub_x, sub_y)

            self.footer_image = img
            tk.Label(parent, image=self.footer_image).pack(fill='x', padx=4, pady=4)
        except Exception as e:
            tk.Label(parent, text=f'No se pudo cargar imagen de pie: {e}', fg='gray').pack(padx=8, pady=6)

    def _threaded(self, fn):
        def wrapper():
            t = threading.Thread(target=fn, daemon=True)
            t.start()
        return wrapper

    def _log(self, msg):
        self.txt_messages.config(state='normal')
        self.txt_messages.insert('end', f'{msg}\n')
        self.txt_messages.see('end')
        self.txt_messages.config(state='disabled')

    def _zip_single_file(self, file_path):
        zip_path = f'{file_path}.zip'
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(file_path, arcname=os.path.basename(file_path))
        return zip_path

    def connect_db(self):
        try:
            self.status_var.set('Conectando...')
            self._log('Intentando conexión a SQL Server...')
            self.cnxn = pyodbc.connect(conn())
            self.cursor = self.cnxn.cursor()
            self._log('Conectado a la base de datos')
            self.status_var.set('Conectado')
            self.btn_generate.config(state='normal')
        except Exception as e:
            self._log(f'Error al conectar: {e}')
            self.status_var.set('Error de conexión')
            messagebox.showerror('Error', f'No se pudo conectar a la base de datos: {e}')

    def generate_table(self):
        periodo = self.period_var.get().strip()
        if not periodo:
            messagebox.showwarning('Período requerido', 'Ingrese un período válido (YYYYMM)')
            return

        if not self.cursor:
            messagebox.showwarning('No conectado', 'Primero conecte a la base de datos')
            return

        try:
            self.status_var.set('Generando tabla...')
            self._log(f'Ejecutando gen_PagosANSeS para periodo {periodo}...')
            # Ejecutar procedimiento almacenado
            self.cursor.execute(f'exec [dbo].[gen_PagosANSeS] @p = {periodo}')
            self.cnxn.commit()

            # Contar filas en la tabla temporal
            tbl = file_specs['table']
            self.cursor.execute(f"select count(*) from dbo.{tbl}")
            rows = self.cursor.fetchall()[0][0]
            self._log(f'Tabla generada. Registros: {rows}')
            self.status_var.set('Tabla generada')
            self.btn_export.config(state='normal')
        except Exception as e:
            self._log(f'Error generando tabla: {e}')
            self.status_var.set('Error')
            messagebox.showerror('Error', f'Error al generar tabla: {e}')

    def export_files(self):
        if not self.cursor:
            messagebox.showwarning('No conectado', 'Conecte a la base de datos primero')
            return

        try:
            self.status_var.set('Exportando...')
            self._log('Iniciando exportación de archivos...')

            today = date.today().strftime('%Y%m%d')
            filename = file_specs['filename'].replace('AAAAAAAA', today)

            # Generar SITACIE (modifica plantilla y devuelve ruta de archivo)
            lon = file_specs['lon']
            tbl = file_specs['table']
            desc = file_specs.get('desc', '')

            # Contar registros de nuevo para pasar a xls_modification
            self.cursor.execute(f"select count(*) from dbo.{tbl}")
            rows = self.cursor.fetchall()[0][0]

            sitacie_template = resource_path('src', 'xls', 'SITACIE_Entrada.xlsx')

            self._log('Generando archivo SITACIE...')
            self.mod_file = xls_modification(f'ansi{filename}', lon, rows, desc, file=sitacie_template)

            # Otra llamada similar a la del script original (opcional)
            xls_modification(f'utf-8{filename}', lon, rows, desc, 0, 13, self.mod_file)

            # Exporto txt ANSI
            self._log('Exportando TXT ANSI...')
            self.cursor.execute(f"select * from dbo.{tbl}")
            save_file(f'ansi{filename}.txt', 'cp1252', self.cursor)

            # Exporto txt UTF-8
            self._log('Convirtiendo a UTF-8...')
            with codecs.open(f'ansi{filename}.txt', 'r', encoding='cp1252') as f:
                lines = f.read()
            with codecs.open(f'utf-8{filename}.txt', 'w', encoding='utf-8') as f:
                f.write(lines)

            #comprimiendo archivos ansi y utf-8
            self._log('Comprimiendo TXT ANSI...')
            ansi_zip = self._zip_single_file(f'ansi{filename}.txt')
            self._log(f'ZIP creado: {ansi_zip}')

            self._log('Comprimiendo TXT UTF-8...')
            utf8_zip = self._zip_single_file(f'utf-8{filename}.txt')
            self._log(f'ZIP creado: {utf8_zip}')

            self._log('Exportación finalizada')
            self.status_var.set('Exportación completa')
        except Exception as e:
            self._log(f'Error en exportación: {e}')
            self.status_var.set('Error')
            messagebox.showerror('Error', f'Error durante exportación: {e}')


if __name__ == '__main__':
    app = PagosApp()
    app.mainloop()
