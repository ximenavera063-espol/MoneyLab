
import streamlit as st

st.set_page_config(
    page_title="MoneyLab",
    page_icon="💰",
    layout="wide"
)

st.title("💰 MoneyLab")
st.write("Finanzas inteligentes para estudiantes universitarios")

opcion = st.sidebar.radio(
    "Elige una herramienta",
    [
        "Inicio",
        "Mi presupuesto",
        "Mi meta de ahorro",
        "Calculadora de crédito",
        "Comparar créditos"
    ]
)

if opcion == "Inicio":
    st.header("Aprende a tomar mejores decisiones financieras")

    st.write("""
    MoneyLab es una herramienta educativa creada para ayudar
    a estudiantes universitarios a practicar conceptos básicos
    de finanzas personales.
    """)

elif opcion == "Mi presupuesto":

    st.header("💰 Construye tu presupuesto")

    ingresos = st.number_input(
        "Ingreso mensual ($)",
        min_value=0.0,
        value=300.0
    )

    transporte = st.number_input(
        "Transporte ($)",
        min_value=0.0,
        value=40.0
    )

    alimentacion = st.number_input(
        "Alimentación ($)",
        min_value=0.0,
        value=80.0
    )

    universidad = st.number_input(
        "Universidad ($)",
        min_value=0.0,
        value=30.0
    )

    entretenimiento = st.number_input(
        "Entretenimiento ($)",
        min_value=0.0,
        value=35.0
    )

    otros = st.number_input(
        "Otros gastos ($)",
        min_value=0.0,
        value=20.0
    )

    if st.button("Calcular mi presupuesto"):

        gastos = (
            transporte
            + alimentacion
            + universidad
            + entretenimiento
            + otros
        )

        saldo = ingresos - gastos

        col1, col2, col3 = st.columns(3)

        col1.metric("Ingresos", f"${ingresos:.2f}")
        col2.metric("Gastos", f"${gastos:.2f}")
        col3.metric("Saldo", f"${saldo:.2f}")

        if saldo > 0:
            st.success(
                f"Tienes ${saldo:.2f} disponibles después de tus gastos."
            )

        elif saldo == 0:
            st.warning(
                "Estás utilizando todos tus ingresos."
            )

        else:
            st.error(
                f"Tus gastos superan tus ingresos en ${abs(saldo):.2f}."
            )

elif opcion == "Mi meta de ahorro":
    st.header("🎯 Mi meta de ahorro")

elif opcion == "Calculadora de crédito":
    st.header("💳 Calculadora de crédito")

elif opcion == "Comparar créditos":
    st.header("⚖️ Comparar créditos")
