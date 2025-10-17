import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Validação de Bônus", layout="wide")

st.title("Validação de IDs de Jogadores e Data de Bônus")

# Upload do CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Verifica colunas esperadas
    if 'Client ID' not in df.columns:
        st.error(CSV precisa conter as colunas 'Client ID')
    else:
        st.success("CSV carregado com sucesso!")

        # Duplicados
        duplicates = df[df.duplicated(subset=['Client ID'], keep=False)]

        if duplicates.empty:
            st.info("Nenhum jogador duplicado encontrado com a mesma data de bônus!")
        else:
            st.warning(f"Foram encontrados {duplicates['Client ID'].nunique()} jogadores com IDs duplicados!")
            st.dataframe(duplicates)

            # Visualização: quantidade de duplicados por data
            chart_data = duplicates.groupby('Accrual Date')['Client ID'].nunique().reset_index()
            chart_data.rename(columns={'Client ID': 'duplicated_players'}, inplace=True)

            st.subheader("Duplicados por Data de Bônus")
            chart = alt.Chart(chart_data).mark_bar().encode(
                x='Accrual Date',
                y='duplicated_players',
                tooltip=['Accrual Date', 'duplicated_players']
            )
            st.altair_chart(chart, use_container_width=True)

