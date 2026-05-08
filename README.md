# ANSES Envíos - Generador de Pagos PAS

## 📋 Descripción

Sistema automatizado para la generación, validación y exportación de datos de pagos del programa **PAS (Pensiones a Adultos Mayores)** de ANSES (Administración Nacional de la Seguridad Social de Argentina).

Este proyecto gestiona el flujo completo de datos desde la base de datos SQL Server hasta la generación de archivos de envío en múltiples formatos, incluyendo validaciones de integridad y generación de reportes de seguimiento.

---

## 🎯 Funcionalidades Principales

### 1. **Generación de Datos**
- Conexión a base de datos SQL Server
- Ejecución de procedimiento almacenado `gen_PagosANSeS`
- Selección de período de procesamiento
- Generación de tabla temporal de liquidación

### 2. **Exportación de Archivos**
- **TXT ANSI**: Codificación CP1252 (compatibilidad legacy)
- **TXT UTF-8**: Formato moderno con codificación estándar
- **XLSX**: Archivo Excel con estructura definida

### 3. **Validación de Archivos**
- Verificación de longitud de líneas
- Consistencia de formato
- Reporte de errores de validación

### 4. **Seguimiento y Auditoría**
- Generación de archivos SITACIE de entrada
- Registro de fechas y horas de procesamiento
- Información de características del archivo (tamaño, cantidad de registros)

---

## 📊 Estructura del Proyecto

```
anses-envios/
├── gui.py                      # Interfaz gráfica Tkinter (NUEVO)
├── pagos_hf.py                 # Script principal de ejecución (legacy)
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Este archivo
├── correrAnsesBajasNegativas.txt # Configuración/notas de ejecución
│
├── src/
│   ├── __init__.py
│   ├── defs/
│   │   ├── __init__.py
│   │   └── pagos_hf.py        # Especificaciones de estructura de archivo
│   │
│   ├── procesos/
│   │   ├── __init__.py
│   │   ├── checks.py          # Validación de archivos
│   │   ├── export_csv.py      # Exportación TXT delimitado
│   │   ├── export_xlsx.py     # Exportación Excel
│   │   └── sitaci_xls.py      # Generación de archivos SITACIE
│   │
│   ├── sql/
│   │   ├── __init__.py
│   │   └── hf_ppc.py          # Configuración de conexión SQL Server
│   │
│   ├── img/
│   │   ├── datosPAS_pie.png   # Imagen de pie de página para GUI
│   │   └── anses-logo.ico     # Icono para ejecutable
│   │
│   └── xls/
│       └── SITACIE_Entrada.xlsx # Plantilla de seguimiento
│
└── output/
    └── (archivos generados)
        ├── ansiPASestadosAAAAAAAA.txt
        ├── utf-8PASestadosAAAAAAAA.txt
        ├── ansiPASestadosAAAAAAAA.txt.zip
        ├── utf-8PASestadosAAAAAAAA.txt.zip
        ├── PASestadosAAAAAAAA.xlsx
        └── SITACIE_Entrada-YYYY-MM-DD-HHMM.xlsx
```

---

## 🏗️ Especificación de Formato PAS

El archivo de salida contiene registros con los siguientes campos (longitud total: **703 caracteres**):

| Campo | Longitud | Posición | Descripción |
|-------|----------|----------|-------------|
| Programa | 3 | 1-3 | Código PAS |
| Apellidos | 100 | 4-103 | Apellido del beneficiario |
| Nombres | 100 | 104-203 | Nombre del beneficiario |
| DNI | 8 | 204-211 | Número de DNI |
| CUIT | 11 | 212-222 | Código CUIT |
| Provincia | 100 | 223-322 | Descripción de la provincia |
| Municipio | 100 | 323-422 | Descripción del municipio |
| Sucursal | 100 | 423-522 | Descripción de la sucursal |
| Mes Alta | 6 | 523-528 | Mes de alta (YYYYMM) |
| Período | 6 | 529-534 | Período de procesamiento (YYYYMM) |
| Estado | 50 | 535-584 | Estado del pago |
| Aviso | 100 | 585-684 | Información adicional/avisos |
| Fecha Cobro | 10 | 685-694 | Fecha de cobro (YYYY-MM-DD) |
| Haber | 9 | 695-703 | Monto depositado en cuenta |

---

## 🔧 Requisitos Técnicos

### Dependencias

```
pandas>=1.0.0
openpyxl>=3.0.0
sqlalchemy>=1.3.0
pyodbc>=4.0.0
PyInstaller>=5.0.0
Pillow>=8.0.0
```

### Requisitos del Sistema

- **Python**: 3.7 o superior
- **SQL Server**: 2016 o superior
- **Conectividad**: Acceso a base de datos HF_PPC en servidor 10.80.5.17:21433
- **Permisos**: Windows Authentication con acceso a procedimiento `gen_PagosANSeS`

---

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd anses-envios
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 📦 Compilación a Ejecutable (`.exe`)

Puedes generar un único archivo ejecutable que incluya todo el proyecto sin necesidad de Python instalado.

### Requisitos Previos
- PyInstaller instalado (incluido en `requirements.txt`)
- Icono disponible en `src/img/anses-logo.ico`

### Pasos para Generar el `.exe`

#### 1. Asegurar que todas las dependencias estén instaladas
```bash
pip install -r requirements.txt
```

#### 2. Generar el ejecutable con el icono
```bash
PyInstaller --onefile --windowed --icon=src/img/anses-logo.ico --name="ANSES-PagosPAS" --add-data "src;src" --add-data "src/img;src/img" --add-data "src/xls;src/xls" gui.py
```

**Parámetros explicados:**
- `--onefile`: Crea un único archivo ejecutable (en lugar de una carpeta)
- `--windowed`: Oculta la consola de comandos (modo GUI limpio)
- `--icon=src/img/anses-logo.ico`: Asigna el icono ANSES al ejecutable
- `--name="ANSES-PagosGUI"`: Nombre del ejecutable generado

#### 3. Localizar el archivo generado
El ejecutable se encontrará en:
```
dist/ANSES-PagosGUI.exe
```

### Distribución del Ejecutable

El archivo `ANSES-PagosGUI.exe` es **autónomo** y puede distribuirse a otros usuarios sin requerir:
- Python instalado
- Dependencias de Python
- Archivos del proyecto

**Nota:** El ejecutable **requiere** acceso de red a:
- Servidor SQL Server: `10.80.5.17:21433`
- Base de datos: `HF_PPC`
- Windows Authentication configurada

### Optimizaciones Adicionales (Opcional)

Si deseas reducir el tamaño del ejecutable:

```bash
pyinstaller --onefile --windowed --icon=src/img/anses-logo.ico --name="ANSES-PagosGUI" --exclude-module matplotlib --exclude-module numpy gui.py
```

Para incluir recursos adicionales (imágenes, plantillas):

```bash
pyinstaller --onefile --windowed --icon=src/img/anses-logo.ico --name="ANSES-PagosGUI" --add-data "src;src" --add-data "src/img;src/img" --add-data "src/xls;src/xls" gui.py
```

### Troubleshooting del `.exe`

| Problema | Solución |
|----------|----------|
| Error "módulo no encontrado" | Ejecutar: `pyinstaller --collect-all <modulo> ...` |
| El icono no aparece | Verificar ruta `src/img/anses-logo.ico` existe |
| Archivo muy grande | Usar `--exclude-module` para remover librerías innecesarias |
| Antivirus bloquea el exe | El archivo es legítimo; excepcionar en el antivirus |

---

## 🚀 Uso

### Opción 1: Interfaz Gráfica (Recomendado)

```bash
python gui.py
```

**Interfaz interactiva con:**
- Botón "Conectar DB" para establecer conexión con SQL Server
- Campo de entrada para período (YYYYMM)
- Botón "Generar tabla" para ejecutar procedimiento almacenado
- Botón "Exportar TXT / XLSX" para generar archivos de salida
- Registro en tiempo real de operaciones
- Pie de página con logo institucional

**Archivos generados automáticamente en `output/`:**
- `ansiPASestadosAAAAAAAA.txt` (encoding CP1252)
- `utf-8PASestadosAAAAAAAA.txt` (encoding UTF-8)
- `ansiPASestadosAAAAAAAA.txt.zip`
- `utf-8PASestadosAAAAAAAA.txt.zip`
- `PASestadosAAAAAAAA.xlsx`
- `SITACIE_Entrada-YYYY-MM-DD-HHMM.xlsx` (archivo de seguimiento)

### Opción 2: Ejecutable Compilado (Sin Python)

```bash
ANSES-PagosGUI.exe
```

Ver sección **Compilación a Ejecutable** para generar el `.exe` desde el código fuente.

### Opción 3: Script de Línea de Comandos (Legacy)

```bash
python pagos_hf.py
```

**Proceso:**
1. Se solicita el período a procesar (formato: YYYYMM)
2. Se conecta a la base de datos SQL Server
3. Ejecuta el procedimiento almacenado `gen_PagosANSeS`
4. Genera tabla temporal con datos de liquidación
5. Exporta en múltiples formatos:
   - TXT ANSI (CP1252)
   - TXT UTF-8
   - XLSX
6. Crea archivo de seguimiento SITACIE
7. Reporta tiempo total de ejecución

### Parámetros Disponibles

Según `correrAnsesBajasNegativas.txt`:
```bash
python pagos_hf.py -ne -t -ch
```

**Opciones:**
- `-ne`: No exportar (?)
- `-t`: Usar tablas temporales
- `-ch`: Ejecutar validaciones (checks)

---

## 📋 Módulos

### `src/defs/pagos_hf.py`
Define la estructura y especificaciones del archivo PAS:
- Nombre de archivo con timestamp
- Tabla base de datos asociada
- Descripción de campos y sus posiciones
- Codificación y longitud de línea

### `src/sql/hf_ppc.py`
Gestiona la conexión a SQL Server:
- Configuración de servidor
- Parámetros de conexión
- Autenticación Windows

### `src/procesos/checks.py`
Valida la integridad de archivos:
- Verifica longitud de cada línea (debe ser 703 caracteres)
- Reporta líneas con error
- Confirma validación exitosa

### `src/procesos/export_csv.py`
Exporta datos a archivo TXT delimitado:
- Delimitador de campo: `|`
- Comillas de escape: `\`
- Soporta encabezados y pies de página

### `src/procesos/export_xlsx.py`
Genera archivos Excel:
- Crea libro de trabajo nuevo
- Inserta encabezados en primera fila
- Mapea 15 columnas de datos

### `src/procesos/sitaci_xls.py`
Genera archivos de seguimiento SITACIE:
- Modifica plantilla base
- Inserta fecha de procesamiento
- Registra características del archivo (nombre, longitud, cantidad de registros)
- Genera con timestamp para trazabilidad

---

## 📊 Flujo de Procesamiento

```
Inicio
   ↓
Solicitar período
   ↓
Conectar SQL Server
   ↓
Ejecutar gen_PagosANSeS
   ↓
Contar registros
   ↓
├─→ Generar TXT ANSI (CP1252)
├─→ Generar TXT UTF-8
├─→ Generar XLSX
└─→ Generar SITACIE
   ↓
Comprimir archivos TXT
   ↓
Fin (con tiempo transcurrido)
```

---

## 🔒 Seguridad

- **Autenticación**: Windows Authentication (requiere credenciales del dominio)
- **Conexión**: SQL Server con encriptación recomendada
- **Acceso**: Limitado a procedimiento almacenado específico
- **Auditoría**: Registro de archivos generados con timestamps

---

## 🐛 Solución de Problemas

### Conexión a BD rechazada
- Verificar acceso de red a 10.80.5.17:21433
- Confirmar credenciales Windows
- Validar instalación de SQL Server Driver

### Error de codificación
- Asegurar que los archivos origen están en codificación correcta
- Verificar que CP1252 y UTF-8 estén disponibles en el sistema

### Archivo generado con longitud incorrecta
- Ejecutar `checks.py` para identificar líneas problemáticas
- Revisar especificaciones en `src/defs/pagos_hf.py`

### Permisos insuficientes
- Confirmar ejecución con cuenta que tenga acceso a HF_PPC
- Verificar permisos de escritura en carpeta `output/`

### GUI no carga imagen de pie de página
- Verificar que `src/img/datosPAS_pie.png` existe
- Confirmar ruta relativa correcta desde raíz del proyecto

### PyInstaller no encuentra módulos
- Ejecutar: `pyinstaller --collect-all pyodbc gui.py`
- Asegurar que todas las dependencias están instaladas

---

## 📝 Mantenimiento

### Actualización de Especificaciones
Modificar `src/defs/pagos_hf.py` si cambian:
- Estructura de campos
- Posiciones de datos
- Nombres de tablas o procedimientos

### Cambio de Servidor
Actualizar `src/sql/hf_ppc.py`:
```python
server = (r"Driver={SQL Server};" + "Server=<nuevo_servidor>,<puerto>;" +
          f"Database=<nueva_db>;Trusted_Connection=yes")
```

### Agregar Nuevos Formatos
Crear nuevo módulo en `src/procesos/` e integrar en `gui.py` o `pagos_hf.py`

---

## 📞 Contacto y Soporte

Para consultas sobre:
- Especificaciones PAS: Contactar a ANSES
- Errores de base de datos: Consultar administrador SQL Server
- Desarrollo: Revisar logs en terminal durante ejecución

---

## 📄 Licencia

Proyecto desarrollado para ANSES - Sistema de Seguridad Social Argentina

---

## 📅 Historial de Cambios

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 2.0 | 2026-05-08 | Interfaz GUI Tkinter, compilación a EXE, compresión de archivos |
| 1.0 | 2026-05-05 | Documentación inicial |

---

**Última actualización**: 2026-05-08
