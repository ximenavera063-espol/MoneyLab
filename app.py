import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Configuración inicial de la página
st.set_page_config(
    page_title="MoneyLab | Finanzas Inteligentes",
    page_icon="💰",
    layout="wide"
)

# --- CONTROL DE SESIÓN ---
if "registrado" not in st.session_state:
    st.session_state["registrado"] = False
if "nombre_usuario" not in st.session_state:
    st.session_state["nombre_usuario"] = ""

# PANTALLA 1: SI EL USUARIO NO SE HA REGISTRADO TODAVÍA
if not st.session_state["registrado"]:
    col_welcome, col_form = st.columns([1.2, 1])
    
    with col_welcome:
        st.title("💰 Bienvenidos a MoneyLab")
        st.subheader("Finanzas inteligentes para estudiantes universitarios")
        st.markdown(
            """
            **MoneyLab** es una plataforma educativa diseñada para ayudarte a tomar el control 
            de tus finanzas personales.
            
            Para acceder a las herramientas interactivas de presupuesto, metas de ahorro y test financiero, 
            por favor identifícate a continuación.
            """
        )
        st.info("📌 Registro rápido para habilitar tu sesión personalizada.")

    with col_form:
        st.subheader("🔑 Ingreso de Usuario")
        with st.form("form_registro"):
            nombre_input = st.text_input("Nombre y Apellido:*", placeholder="Ej. Ana García")
            carrera_input = st.text_input("Carrera:*", placeholder="Ej. Economía")
            edad_input = st.text_input("Edad:*", placeholder="Ej. 20")
            
            btn_ingresar = st.form_submit_button("Ingresar a MoneyLab 🚀")
            
            if btn_ingresar:
                nombre_clean = nombre_input.strip()
                carrera_clean = carrera_input.strip()
                edad_clean = edad_input.strip()
                
                palabras_nombre = nombre_clean.split()
                
                # --- VALIDACIONES OBLIGATORIAS ---
                if not nombre_clean:
                    st.error("⚠️️ Por favor, ingresa tu Nombre y Apellido.")
                elif len(palabras_nombre) < 2:
                    st.error("⚠️ Debes ingresar al menos **un nombre y un apellido** (Ej. Ana García).")
                elif not carrera_clean:
                    st.error("⚠️ Por favor, ingresa tu Carrera.")
                elif not edad_clean:
                    st.error("⚠️ Por favor, ingresa tu Edad.")
                elif not edad_clean.isdigit():
                    st.error("⚠️ Por favor, ingresa una Edad válida en números (Ej. 20).")
                else:
                    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # 1. Guardar en la sesión activa
                    st.session_state["registrado"] = True
                    st.session_state["nombre_usuario"] = nombre_clean
                    st.session_state["carrera_usuario"] = carrera_clean
                    st.session_state["edad_usuario"] = edad_clean
                    
   # 2. Guardar automáticamente en Google Sheets mediante st.secrets
                    try:
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        
                        nuevo_registro = pd.DataFrame([{
                            "Fecha": fecha_actual,
                            "Nombre": nombre_clean,
                            "Carrera": carrera_clean,
                            "Edad": edad_clean
                        }])
                        
                        # Intentar leer datos previos o crear una lista limpia
                        try:
                            df_existente = conn.read(worksheet="Hoja 1", ttl=0)
                            df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)
                        except Exception:
                            df_actualizado = nuevo_registro

                        # Guardar en Google Sheets
                        conn.update(worksheet="Hoja 1", data=df_actualizado)
                        st.toast("✅ Registro guardado con éxito en Google Sheets")
                    except Exception as e:
                        st.warning(f"Nota: No se pudo actualizar Google Sheets: {e}")
                        
                    st.success(f"¡Bienvenid@, {nombre_clean}! Cargando herramientas...")
                    st.rerun()

# PANTALLA 2: UNA VEZ QUE EL USUARIO YA INGRESÓ SUS DATOS
else:
    # --- MENÚ LATERAL ---
    st.sidebar.title("💰 MoneyLab")
    st.sidebar.success(f"👤 Usuario: **{st.session_state['nombre_usuario']}**")
    
    if st.sidebar.button("Cerrar Sesión / Cambiar Usuario"):
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")
    opcion = st.sidebar.radio(
        "Elige una herramienta:",
        [
            "Inicio", 
            "Mi presupuesto", 
            "Mi meta de ahorro", 
            "Test de salud financiera"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("MoneyLab | Plataforma de Educación Financiera")

    # --- SECCIÓN: INICIO ---
    if opcion == "Inicio":
        st.title(f"👋 ¡Hola, {st.session_state['nombre_usuario']}!")
        st.subheader("Aprende a tomar mejores decisiones financieras")
        st.write("---")
        st.write(
            """
            MoneyLab te ayuda a practicar conceptos básicos de finanzas personales, 
            gestionar tus presupuestos y planificar metas de ahorro de forma práctica.
            
            Usa el menú lateral de la izquierda para navegar entre las distintas herramientas.
            """
        )

    # --- SECCIÓN: MI PRESUPUESTO ---
    elif opcion == "Mi presupuesto":
        st.title("💰 Construye tu presupuesto")
        st.write("Ingresa tus datos para analizar la distribución de tus finanzas mensuales.")

        col_inputs, col_results = st.columns([1, 1])

        with col_inputs:
            ingreso = st.number_input("Ingreso mensual ($)", min_value=0.0, value=300.0, step=10.0)
            
            st.subheader("Gastos")
            transporte = st.number_input("Transporte ($)", min_value=0.0, value=40.0, step=5.0)
            alimentacion = st.number_input("Alimentación ($)", min_value=0.0, value=80.0, step=5.0)
            universidad = st.number_input("Universidad ($)", min_value=0.0, value=30.0, step=5.0)
            entretenimiento = st.number_input("Entretenimiento / Otros ($)", min_value=0.0, value=50.0, step=5.0)

        total_gastos = transporte + alimentacion + universidad + entretenimiento
        saldo = ingreso - total_gastos

        with col_results:
            st.subheader("Resumen Financiero")
            
            m1, m2 = st.columns(2)
            m1.metric("Total Gastos", f"${total_gastos:.2f}")
            m2.metric("Disponible / Saldo", f"${saldo:.2f}")

            if saldo < 0:
                st.error("⚠️ Tus gastos superan tus ingresos. Revisa tus gastos no esenciales.")
            elif saldo == 0:
                st.warning("⚖️ Estás en punto de equilibrio. Intenta ajustar para generar margen de ahorro.")
            else:
                st.success(f"🎉 Te quedan ${saldo:.2f} disponibles para tu meta de ahorro.")

            df_gastos = pd.DataFrame({
                "Categoría": ["Transporte", "Alimentación", "Universidad", "Entretenimiento"],
                "Monto ($)": [transporte, alimentacion, universidad, entretenimiento]
            })
            
            df_gastos = df_gastos[df_gastos["Monto ($)"] > 0]
            
            if not df_gastos.empty:
                st.write("### Distribución de tus Gastos")
                st.bar_chart(df_gastos.set_index("Categoría"))

    # --- SECCIÓN: MI META DE AHORRO ---
    elif opcion == "Mi meta de ahorro":
        st.title("🎯 Mi Meta de Ahorro")
        st.write("Planifica tus objetivos financieros a corto y mediano plazo.")

        col_inputs, col_results = st.columns([1, 1.2])

        with col_inputs:
            st.subheader("1. Configura tu Meta")
            nombre_meta = st.text_input("¿Qué quieres lograr?", value="Fondo para Laptop / Titulación")
            monto_objetivo = st.number_input("Monto total objetivo ($):", min_value=10.0, value=500.0, step=25.0)
            ahorro_actual = st.number_input("Ahorro actual acumulado ($):", min_value=0.0, value=50.0, step=10.0)
            
            st.markdown("---")
            st.subheader("2. Estrategia")
            tipo_calculo = st.radio(
                "¿Cómo prefieres calcularlo?",
                ["Definir mi aporte mensual", "Definir plazo en meses"]
            )

            if tipo_calculo == "Definir mi aporte mensual":
                aporte_mensual = st.number_input("Aporte mensual ($):", min_value=1.0, value=50.0, step=5.0)
                monto_faltante = max(0.0, monto_objetivo - ahorro_actual)
                meses_necesarios = int(np.ceil(monto_faltante / aporte_mensual)) if aporte_mensual > 0 else 0
            else:
                plazo_meses = st.number_input("Plazo deseado (meses):", min_value=1, value=6, step=1)
                monto_faltante = max(0.0, monto_objetivo - ahorro_actual)
                aporte_mensual = monto_faltante / plazo_meses if plazo_meses > 0 else 0.0
                meses_necesarios = plazo_meses

        with col_results:
            st.subheader(f"📊 Proyección: {nombre_meta}")

            progreso = min(1.0, ahorro_actual / monto_objetivo) if monto_objetivo > 0 else 0
            st.write(f"**Progreso actual:** {progreso*100:.1f}%")
            st.progress(progreso)

            kpi1, kpi2 = st.columns(2)
            kpi1.metric("Aporte Mensual", f"${aporte_mensual:.2f}")
            kpi2.metric("Tiempo Estimado", f"{meses_necesarios} meses")

            if meses_necesarios > 0:
                meses_list = list(range(0, meses_necesarios + 1))
                acumulado_list = []
                
                saldo_temp = ahorro_actual
                for m in meses_list:
                    if m == 0:
                        acumulado_list.append(ahorro_actual)
                    else:
                        saldo_temp = min(monto_objetivo, saldo_temp + aporte_mensual)
                        acumulado_list.append(saldo_temp)

                df_ahorro = pd.DataFrame({
                    "Mes": meses_list,
                    "Monto Acumulado ($)": acumulado_list
                })

                st.write("### Crecimiento de tu ahorro")
                st.line_chart(df_ahorro.set_index("Mes"))

                if progreso >= 1.0:
                    st.balloons()
                    st.success("🎉 ¡Felicidades! Has alcanzado tu meta de ahorro.")
                else:
                    st.info(f"💡 Te faltan **${monto_faltante:.2f}** para completar tu objetivo.")

    # --- SECCIÓN: TEST DE SALUD FINANCIERA ---
    elif opcion == "Test de salud financiera":
        st.title("🩺 Diagnóstico de Salud Financiera")
        st.write("Responde estas 3 preguntas breves para evaluar tus hábitos económicos.")
        
        with st.form("quiz_form"):
            p1 = st.radio("1. ¿Llevas un registro de tus ingresos y gastos mensuales?", ["No", "A veces", "Sí, siempre"])
            p2 = st.radio("2. ¿Tienes un ahorro o fondo guardado para emergencias?", ["No tengo", "En proceso", "Sí, suficiente"])
            p3 = st.radio("3. ¿Sueles gastar más de lo que recibes al mes?", ["Frecuentemente", "Ocasionalmente", "Casi nunca"])
            
            submit = st.form_submit_button("Evaluar Mi Salud Financiera")
            
        if submit:
            puntos = 0
            puntos += 0 if p1 == "No" else (1 if p1 == "A veces" else 2)
            puntos += 0 if p2 == "No tengo" else (1 if p2 == "En proceso" else 2)
            puntos += 0 if p3 == "Frecuentemente" else (1 if p3 == "Ocasionalmente" else 2)
            
            st.write("---")
            st.subheader("Tu Diagnóstico:")
            if puntos <= 2:
                st.error(f"Puntaje: {puntos}/6 — **Nivel Inicial**: Es recomendado empezar a registrar tus gastos diarios.")
            elif puntos <= 4:
                st.warning(f"Puntaje: {puntos}/6 — **Nivel Intermedio**: Vas por buen camino. Enfócate en tu meta de ahorro.")
            else:
                st.success(f"Puntaje: {puntos}/6 — **Nivel Avanzado**: ¡Excelente disciplina financiera!")
