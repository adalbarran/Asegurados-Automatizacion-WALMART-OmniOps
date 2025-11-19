# Archivo: app.py (En la carpeta raíz del proyecto)

import streamlit as st
import pandas as pd
from src.logic_functions import procesar_lote # Importa la lógica

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Automatización Asegurados Walmart",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- TÍTULO Y DESCRIPCIÓN ---
st.title("Automatización de Pago Asegurados (MVP)")
st.caption("Carga de Lotes: Validar si los asegurados cumplen con la condicion de pago, y calcular Valor a Pagar.")

# --- FORMULARIO DE ENTRADA ---
with st.form("input_form"):
    
    # 1. INPUT DE ARCHIVO (Carga del Zonal)
    uploaded_file = st.file_uploader(
        "1. Subir Archivo de ASEGURADOS, 'Con Formato Predeterminado a seguir' (.xlsx o .csv)",
        type=['xlsx', 'csv']
    )
    
    # 2. INPUT DE TARIFA (Única variable manual que define el valor)
    tarifa_base = st.number_input(
        "2. Ingresar Tarifa Base de Pago por Asegurado ($)",
        min_value=1,
        value=15000,
        step=1000,
        help="Este monto se multiplicará por la Cant. Asegurados si el registro es APROBADO."
    )
    
    # Botón de Ejecución
    submitted = st.form_submit_button("3. VALIDAR y CALCULAR PAGOS")

# --- LÓGICA DE PROCESAMIENTO ---
if submitted:
    if uploaded_file is not None:
        try:
            # Leer el archivo subido
            if uploaded_file.name.endswith('.csv'):
                df_input = pd.read_csv(uploaded_file)
            else:
                df_input = pd.read_excel(uploaded_file)
            
            # Procesar el lote (llama a la lógica central)
            df_aprobados, df_completo = procesar_lote(df_input, tarifa_base)
            
            st.success(f"✅ Procesamiento Completo. Total de Registros Analizados: {len(df_input)}")

            # --- RESULTADOS PARA EL ZONAL ---
            st.header("📋 Resumen de Resultados y Reportes Generados")
            
            # Resumen de Métricas
            total_aprobados = len(df_aprobados)
            total_rechazados = len(df_completo) - total_aprobados
            valor_total_calculado = df_aprobados['Valor_Calculado'].sum()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Aprobados", total_aprobados)
            col2.metric("Rechazados", total_rechazados)
            col3.metric("💰 Valor Total a Pagar", f"${valor_total_calculado:,.0f}")
            
            st.subheader("Reporte Completo de Validación (Para Zonal - Trazabilidad)")
            st.dataframe(df_completo, use_container_width=True)

            # --- ENTREGABLE PARA FINANZAS ---
            if not df_aprobados.empty:
                st.subheader("⭐ Reporte Final de Pagos (Para Finanzas)")
                st.dataframe(df_aprobados, use_container_width=True)

                # Botón de Descarga
                st.download_button(
                    label="⬇️ Descargar Reporte Aprobados (.csv)",
                    data=df_aprobados.to_csv(index=False).encode('utf-8'),
                    file_name='Reporte_Pagos_Aprobados_FINAL.csv',
                    mime='text/csv'
                )

        except Exception as e:
            st.error(f"❌ Error al procesar el archivo. Asegúrese de que las columnas 'Flota (%)', 'Ventana (%)', 'OTEA (%)', 'N2H (%)' y 'Cant. Asegurados' existen y contienen números. Error: {e}")

    else:
        st.warning("Por favor, suba un archivo para comenzar la validación.")