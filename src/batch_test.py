
import pandas as pd
import os

# --- VARIABLES CRÍTICAS ---
# NOTA: En el script final, la Tarifa Base sería un input de Streamlit.
TARIFA_BASE_PAGO = 15000  # Placeholder: $15,000 por asegurado aprobado

# --- FUNCIÓN DE LÓGICA CENTRAL ---
def validar_registro(row, tarifa):
    """Aplica las 4 reglas de negocio y calcula el pago para una sola fila (registro)."""
    
    # Mapeo de columnas de entrada (AJUSTAR ESTO A LA COLUMNA REAL DE TU REPORTE ZONAL)
    kpi_flota_perc = row['Flota (%)']
    kpi_ventana_perc = row['Ventana (%)']
    kpi_otea_perc = row['OTEA (%)']
    kpi_n2h_perc = row['N2H (%)']
    num_asegurados = row['Cant. Asegurados'] # Dato necesario para el cálculo
    
    reglas_fallidas = []

    # Aplicación de las Reglas
    if kpi_flota_perc > 100.0:
        reglas_fallidas.append("I. Flota > 100%")
    if kpi_ventana_perc > 60.0:
        reglas_fallidas.append("II. Ocupación Ventana > 60%")
    if kpi_otea_perc < 98.0:
        reglas_fallidas.append("III. OTEA < 98%")
    if kpi_n2h_perc < 70.0:
        reglas_fallidas.append("IV. N2H < 70%")

    es_aprobado = len(reglas_fallidas) == 0
    
    # --- CÁLCULO DE VALOR ---
    if es_aprobado:
        valor_a_pagar = num_asegurados * tarifa
        estado = "APROBADO"
    else:
        valor_a_pagar = 0
        estado = "RECHAZADO"

    # Retorna un diccionario con los nuevos campos de resultado
    return {
        'Estado_Final': estado,
        'Valor_Calculado': valor_a_pagar,
        'Reglas_Fallidas': ", ".join(reglas_fallidas) if reglas_fallidas else "N/A"
    }

# --- FUNCIÓN PRINCIPAL DE PROCESAMIENTO DE LOTE ---
def procesar_lote_y_generar_reporte(archivo_entrada, tarifa):
    print(f"Iniciando procesamiento del archivo: {archivo_entrada}")
    
    # 1. Carga del Archivo (Simulando la carga del Zonal)
    try:
        df = pd.read_excel(archivo_entrada)
        print(f"Archivo cargado. Se encontraron {len(df)} registros.")
    except FileNotFoundError:
        print(f"ERROR: Archivo no encontrado en la ruta: {archivo_entrada}")
        return

    # 2. Aplicación de la Lógica a cada fila (Máxima Automatización)
    # Aplica la función 'validar_registro' a cada fila del DataFrame y crea nuevas columnas
    resultados = df.apply(
        lambda row: validar_registro(row, tarifa),
        axis=1, result_type='expand'
    )

    # 3. Consolidar resultados en el DataFrame original
    df = pd.concat([df, resultados], axis=1)

    # 4. Generación de Reporte Final (Solo aprobados para Finanzas)
    df_aprobados = df[df['Estado_Final'] == 'APROBADO']
    
    ruta_salida = 'Reporte_Pagos_Aprobados_FINAL.xlsx'
    
    if not df_aprobados.empty:
        # Aquí se simula la escritura del reporte final para Finanzas
        df_aprobados.to_excel(ruta_salida, index=False)
        print("\n----------------------------------------------------")
        print(f"✅ PROCESO COMPLETADO. Reporte de Pagos generado en: {ruta_salida}")
        print(f"  Total Aprobados: {len(df_aprobados)}")
        print(f"  Valor Total a Pagar: ${df_aprobados['Valor_Calculado'].sum():,.0f}")
        print("----------------------------------------------------")
    else:
        print("\n----------------------------------------------------")
        print("⚠️ Advertencia: No se encontraron registros elegibles para pago.")
        print("----------------------------------------------------")
        
    # Opcional: Guardar el reporte completo (con rechazados y motivos)
    df.to_excel('Reporte_Completo_Validacion.xlsx', index=False)
    print("Reporte completo de la validación (incluye rechazados) guardado.")


# --- EJECUCIÓN DEL SCRIPT DE PRUEBA ---
if __name__ == "__main__":
    # La ruta del archivo de entrada debe ser relativa a donde ejecutas el script
    # Asumimos que 'datos_asegurados_prueba.xlsx' está en la carpeta raíz del proyecto.
    archivo_entrada = '../datos_asegurados_prueba.xlsx' 
    
    # La Tarifa Base es la única variable que la Zonal debería ingresar fácilmente
    procesar_lote_y_generar_reporte(archivo_entrada, TARIFA_BASE_PAGO)