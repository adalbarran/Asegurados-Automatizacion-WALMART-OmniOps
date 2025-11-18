import pandas as pd
import os

# --- 1. FUNCIÓN DE LÓGICA CENTRAL ---
def validar_elegibilidad_y_calcular_pago(
    nombre_asegurado,
    kpi_flota_perc,       # Cumplimiento Flota (ej: 95.0)
    kpi_ventana_perc,     # Ocupación Ventana (ej: 55.0)py 
    kpi_otea_perc,        # OTEA (ej: 99.0)
    kpi_n2h_perc,         # N2H (ej: 75.0)
    num_asegurados,       # Cantidad para el cálculo (ej: 10)
    tarifa_base           # Valor por unidad (ej: 15000)
):
    """
    Valida las 4 reglas de negocio y calcula el valor a pagar si es aprobado.
    """
    
    # 🚨 NOTA: Las reglas usan el porcentaje en formato 0-100.
    
    # Reglas de Negocio (Requisitos estrictos de APROBACIÓN)
    reglas_fallidas = []

    if kpi_flota_perc > 100.0:
        reglas_fallidas.append("Flota > 100%")
    
    if kpi_ventana_perc > 60.0:
        reglas_fallidas.append("Ocupación Ventana > 60%")
    
    if kpi_otea_perc < 98.0:
        reglas_fallidas.append("OTEA < 98%")
        
    if kpi_n2h_perc < 70.0:
        reglas_fallidas.append("N2H < 70%")

    es_aprobado = len(reglas_fallidas) == 0
    
    # --- CÁLCULO DE VALOR Y REGISTRO ---
    
    if es_aprobado:
        valor_a_pagar = num_asegurados * tarifa_base
        estado = "APROBADO"
    else:
        valor_a_pagar = 0
        estado = "RECHAZADO"

    # Preparar el registro para el archivo Excel
    registro = {
        'Asegurado': nombre_asegurado,
        'Flota (%)': kpi_flota_perc,
        'Ventana (%)': kpi_ventana_perc,
        'OTEA (%)': kpi_otea_perc,
        'N2H (%)': kpi_n2h_perc,
        'Estado': estado,
        'Valor a Pagar': valor_a_pagar,
        'Reglas Fallidas': ", ".join(reglas_fallidas) if reglas_fallidas else "N/A"
    }

    return registro


# --- 2. PRUEBAS DE CASOS Y REGISTRO ---

def ejecutar_pruebas():
    print("--- Ejecutando Pruebas de Lógica de Pago ---")
    
    # Caso 1: APROBADO (Cumple las 4 reglas)
    registro_aprobado = validar_elegibilidad_y_calcular_pago(
        nombre_asegurado="Proveedor_A",
        kpi_flota_perc=95.0,
        kpi_ventana_perc=50.0,
        kpi_otea_perc=98.5,
        kpi_n2h_perc=75.0,
        num_asegurados=10,
        tarifa_base=15000
    )
    print(f"\nCaso 1 - {registro_aprobado['Asegurado']}: {registro_aprobado['Estado']} (Valor: {registro_aprobado['Valor a Pagar']})")
    
    # Caso 2: RECHAZADO (Falla Flota y N2H)
    registro_rechazado = validar_elegibilidad_y_calcular_pago(
        nombre_asegurado="Proveedor_B",
        kpi_flota_perc=105.0, # Falla aquí (>100)
        kpi_ventana_perc=55.0,
        kpi_otea_perc=99.0,
        kpi_n2h_perc=65.0, # Falla aquí (<70)
        num_asegurados=5,
        tarifa_base=15000
    )
    print(f"\nCaso 2 - {registro_rechazado['Asegurado']}: {registro_rechazado['Estado']}")
    print(f"   Motivo: {registro_rechazado['Reglas Fallidas']}")
    
    # Consolidar resultados (simulando el reporte Excel)
    df_resultados = pd.DataFrame([registro_aprobado, registro_rechazado])
    
    # Guardar en Excel (requiere pandas y openpyxl, que deberías tener)
    ruta_reporte = 'Reporte_de_Pruebas_Logica.xlsx'
    
    if not os.path.exists(ruta_reporte):
         df_resultados.to_excel(ruta_reporte, index=False)
         print(f"\nReporte inicial creado en: {ruta_reporte}")
    else:
         # Simular cómo Streamlit agregaría la fila al final
         df_actual = pd.read_excel(ruta_reporte)
         df_final = pd.concat([df_actual, df_resultados], ignore_index=True)
         df_final.to_excel(ruta_reporte, index=False)
         print(f"\nReporte de pruebas actualizado en: {ruta_reporte}")


# Ejecutar la simulación
if __name__ == "__main__":
    # Necesitas que pandas y openpyxl estén instalados desde tu requirements.txt
    # Si la red no te deja, intenta solo la función 'validar_elegibilidad_y_calcular_pago'
    try:
        ejecutar_pruebas()
    except Exception as e:
        print(f"\nError al ejecutar la simulación (probablemente falta pandas/openpyxl): {e}")
        print("Puedes probar la lógica sin la parte del Excel, imprimiendo solo los resultados de la función.")


### 2. Ejecutar la Prueba en la Terminal

# Asegúrate de estar en tu entorno virtual (`(venv)` activado), y ejecuta el *script*:

# ```powershell
# (venv) PS C:\ruta\al\proyecto> python src/test_logic.py