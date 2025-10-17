import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Validação de Duplicados", layout="wide")

st.title("🔍 Validação de IDs Duplicados - Bônus")

st.write("Envie um arquivo CSV contendo as colunas **Client ID** e **Accrual Date** para verificar duplicidades de clientes.")

# Upload do CSV
uploaded_file = st.file_uploader("Escolha o arquivo CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Verifica colunas necessárias
    if 'Client ID' not in df.columns or 'Accrual Date' not in df.columns:
        st.error("O CSV precisa conter as colunas 'Client ID' e 'Accrual Date'.")
    else:
        st.success("✅ CSV carregado com sucesso!")

        # Identificar duplicados com base apenas no Client ID
        duplicated_ids = df[df.duplicated(subset=['Client ID'], keep=False)]

        if duplicated_ids.empty:
            st.info("🎉 Nenhum ID duplicado encontrado!")
        else:
            st.warning(f"⚠️ Foram encontrados {duplicated_ids['Client ID'].nunique()} IDs de clientes duplicados!")

            # Exibe tabela com os duplicados
            st.subheader("📋 Lista de IDs Duplicados")
            st.dataframe(duplicated_ids)

            # Quantidade de duplicações por ID
            duplicates_count = (
                duplicated_ids.groupby('Client ID')
                .size()
                .reset_index(name='Ocorrências')
                .sort_values(by='Ocorrências', ascending=False)
            )

            st.subheader("📊 Quantidade de Ocorrências por Client ID")
            chart = alt.Chart(duplicates_count).mark_bar().encode(
                x=alt.X('Client ID:N', sort='-y'),
                y='Ocorrências:Q',
                tooltip=['Client ID', 'Ocorrências']
            ).properties(height=400)
            
            st.altair_chart(chart, use_container_width=True)
