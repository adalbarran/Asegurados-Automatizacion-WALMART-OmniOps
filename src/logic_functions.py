import pandas as pd
from datetime import date
import os

# --- RUTAS DE ARCHIVOS (Ajusta esto en tu proyecto) ---
# Este archivo será el REPORTE FINAL que tú usarás para saber a quién pagar.
RUTA_REPORTE_FINAL = 'data/Reporte_Final_Asegurados_Aprobados.xlsx'
NOMBRE_HOJA_REPORTE = 'Aprobados_Pagos'


def validar_elegibilidad(flota_pct, ventana_pct, otea_pct, n2h_pct):
    """
    Verifica si un asegurado cumple con los 4 KPIs (Reglas de Pago).
    Se asume que los porcentajes se pasan como valores decimales (ej: 0.98 para 98%).
    """
    try:
        reglas = {
            "Flota (<= 100%)": flota_pct <= 1.00,
            "Ventana (<= 60%)": ventana_pct <= 0.60,
            "OTEA (>= 98%)": otea_pct >= 0.98,
            "N2H (>= 70%)": n2h_pct >= 0.70
        }
        
        es_aprobado = all(reglas.values())
        
        if es_aprobado:
            return True, "APROBADO: Cumple con todos los KPIs."
        else:
            fallas = [k for k, v in reglas.items() if v is False]
            return False, f"NO ELEGIBLE: Falló en las siguientes reglas: {', '.join(fallas)}"

    except TypeError:
        return False, "Error: Asegúrate de que todos los valores de KPI sean números."


def registrar_aprobado_en_reporte(datos_ingresados, nombre_zonal):
    """
    Adjunta un nuevo registro al Reporte Final de Aprobados.
    """
    
    # 1. Crear el nuevo registro (DataFrame) con la estructura del Excel final
    nuevo_registro = pd.DataFrame({
        'Responsable': [nombre_zonal],
        'Local': [datos_ingresados['Local']],
        'Fecha': [datos_ingresados['Fecha']],
        'Proveedor': [datos_ingresados['Proveedor']],
        'AM/PM': [datos_ingresados['AM/PM']],
        'Motivo': [datos_ingresados['Motivo']],
        'Modelo': [datos_ingresados['Modelo']],
        'Q Shoppers/Pickers': [datos_ingresados['Q Shoppers/Pickers']],
        'Comentario': [datos_ingresados['Comentario']],
        'CHECK': ['OK'] # Marcado automático como APROBADO
    })
    
    try:
        # Intenta leer el archivo existente (si no existe, lo creamos)
        if os.path.exists(RUTA_REPORTE_FINAL):
            df_existente = pd.read_excel(RUTA_REPORTE_FINAL, sheet_name=NOMBRE_HOJA_REPORTE)
        else:
            df_existente = pd.DataFrame() # DataFrame vacío si es la primera vez que se ejecuta
            
        # 2. Concatenar (Adjuntar) el nuevo registro
        df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)
        
        # 3. Sobrescribir/Guardar el archivo
        df_actualizado.to_excel(RUTA_REPORTE_FINAL, sheet_name=NOMBRE_HOJA_REPORTE, index=False)
        
        return True, f"Registro de {datos_ingresados['Proveedor']} añadido al Reporte Final de Pagos."
        
    except Exception as e:
        return False, f"Error crítico al escribir en el Excel de Reporte Final: {e}"