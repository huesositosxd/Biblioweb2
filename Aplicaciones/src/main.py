import sqlite3
import pandas as pd
import os
from datetime import datetime
from openpyxl import load_workbook
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header

# Función para enviar el correo
def enviar_correo(subject, body, to_email, attachment_path):
    try:
        from_email = "biblioparque0@gmail.com"
        password = "prdwwteddfqvccub"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email

        # Asegurar que el asunto esté correctamente codificado en UTF-8
        msg['Subject'] = Header(subject, 'utf-8')

        # Asegurar que el cuerpo del mensaje esté en UTF-8
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # Abrir el archivo adjunto y adjuntarlo al correo
        with open(attachment_path, "rb") as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(attachment_path)}")
            msg.attach(part)

        # Conectar al servidor SMTP y enviar el correo
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())

        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Ruta base del script
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "../../BiblioParque.db")
output_folder = os.path.join(base_dir, "../Reportes")

# Verificar si la carpeta de salida existe, si no, crearla
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Conectar a la base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Obtener la fecha de hoy en formato YYYY-MM-DD
fecha_hoy = datetime.today().strftime('%Y-%m-%d')

# Consulta SQL para obtener registros de visitas de hoy
query = """
SELECT * FROM Visitas_registrovisita
WHERE fecha_hora BETWEEN ? AND ?
"""
cursor.execute(query, (f"{fecha_hoy} 00:00:00", f"{fecha_hoy} 23:59:59"))

# Obtener los resultados de la consulta
rows = cursor.fetchall()
col_names = [description[0] for description in cursor.description]

# Cerrar la conexión a la base de datos
conn.close()

# Si no hay registros, mostrar un mensaje
if not rows:
    print(f"No hay registros para hoy: {fecha_hoy}")
else:
    # Crear el DataFrame de Pandas con los resultados
    df = pd.DataFrame(rows, columns=col_names)

    # Generar el nombre del archivo con la fecha de hoy
    nombre_archivo = os.path.join(output_folder, f"{fecha_hoy}.xlsx")

    # Guardar los datos en un archivo Excel
    df.to_excel(nombre_archivo, index=False, engine="openpyxl")

    # Ajustar el ancho de las columnas del archivo Excel
    wb = load_workbook(nombre_archivo)
    ws = wb.active
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter  # Obtener la letra de la columna
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = max_length + 2  # Ajustar el ancho con un margen

    # Guardar el archivo Excel con los cambios
    wb.save(nombre_archivo)
    print(f"Archivo guardado en: {nombre_archivo}")

    # Enviar el archivo generado por correo
    subject = "Reporte Diario de Visitas"
    body = "Adjunto el archivo Excel con el reporte de visitas de hoy."
    to_email = "josueegremi@gmail.com"

    # Llamar a la función para enviar el correo
    enviar_correo(subject, body, to_email, nombre_archivo)
