from django.core.management.base import BaseCommand
from Aplicaciones.Visitas.models import RegistroVisita, Visitausuario
from django.utils.timezone import now
import pandas as pd
from django.core.mail import EmailMessage
from django.conf import settings
import os
import openpyxl

class Command(BaseCommand):
    help = 'Genera y envía reporte diario de visitas'

    def handle(self, *args, **kwargs):
        hoy = now().date()

        # --- REGISTROS ANÓNIMOS (RegistroVisita) ---
        visitas_anonimas = RegistroVisita.objects.filter(fecha_hora__date=hoy)
        df_anonimas = pd.DataFrame(list(visitas_anonimas.values()))
        df_anonimas["tipo_visita"] = "anónima"
        df_anonimas.rename(columns={"fecha_hora": "fecha_visita"}, inplace=True)

        # --- REGISTROS USUARIOS AUTENTICADOS (Visitausuario) ---
        visitas_usuarios = Visitausuario.objects.filter(fecha_visita__date=hoy)
        df_usuarios = pd.DataFrame(list(visitas_usuarios.values()))
        df_usuarios["tipo_visita"] = "usuario"

        # --- UNIFICAR CAMPOS COMUNES ---
        campos_comunes = [
            "nombre", "fecha_nacimiento", "edad", "sexo",
            "colonia", "discapacidad", "actividad", "estado_nacimiento",
            "fecha_visita", "tipo_visita"
        ]
        df_anonimas = df_anonimas[[c for c in campos_comunes if c in df_anonimas.columns]]
        df_usuarios = df_usuarios[[c for c in campos_comunes if c in df_usuarios.columns]]

        df_final = pd.concat([df_anonimas, df_usuarios], ignore_index=True)

        # Quitar zonas horarias si existieran
        if pd.api.types.is_datetime64tz_dtype(df_final["fecha_visita"]):
            df_final["fecha_visita"] = df_final["fecha_visita"].dt.tz_localize(None)

        # --- DEFINIR RUTA ---
        nombre_archivo = f"reporte_visitas_{hoy}.xlsx"
        ruta = os.path.join(settings.BASE_DIR, nombre_archivo)

        # --- GUARDAR EXCEL ---
        df_final.to_excel(ruta, index=False, engine="openpyxl")

        # --- AJUSTAR ANCHO DE COLUMNAS ---
        wb = openpyxl.load_workbook(ruta)
        ws = wb.active

        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter  # letra de la columna, ej. 'A'
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = max_length + 2
            ws.column_dimensions[column].width = adjusted_width

        wb.save(ruta)

        # --- ENVIAR POR CORREO ---
        asunto = "Reporte Diario de Visitas"
        cuerpo = "Se adjunta el reporte de visitas del día de hoy."
        destinatarios = ["josueegremi@gmail.com"]

        email = EmailMessage(
            asunto,
            cuerpo,
            settings.DEFAULT_FROM_EMAIL,
            destinatarios,
        )
        email.attach_file(ruta)
        email.send()

        self.stdout.write(self.style.SUCCESS(f"Reporte generado y enviado correctamente: {nombre_archivo}"))
