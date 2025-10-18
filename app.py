import streamlit as st
import pandas as pd

st.set_page_config(page_title="Validação e Comparação de IDs", layout="wide")

st.title("🔍 Validação e Comparação de IDs de Clientes")

st.write("""
Envie **um ou dois arquivos CSV** contendo as colunas **Client ID**, **Accrual Date** e **bonus Amount**.  
Você poderá verificar duplicados dentro de um arquivo e também identificar IDs que aparecem **em ambos os arquivos**.
""")

# Upload de até dois arquivos
uploaded_file1 = st.file_uploader("📂 Escolha o primeiro arquivo CSV", type="csv", key="file1")
uploaded_file2 = st.file_uploader("📂 Escolha o segundo arquivo CSV (opcional)", type="csv", key="file2")

def validar_colunas(df):
    required_cols = {'Client ID', 'Accrual Date', 'bonus Amount'}
    return required_cols.issubset(df.columns)

# Caso 1: Apenas um arquivo (verificar duplicados)
if uploaded_file1 and not uploaded_file2:
    df = pd.read_csv(uploaded_file1)

    if not validar_colunas(df):
        st.error("O CSV precisa conter as colunas: 'Client ID', 'Accrual Date' e 'bonus Amount'.")
    else:
        st.success("✅ CSV carregado com sucesso!")

        duplicated = df[df.duplicated(subset=['Client ID'], keep=False)]

        if duplicated.empty:
            st.info("🎉 Nenhum ID duplicado encontrado!")
        else:
            st.warning(f"⚠️ Foram encontrados {duplicated['Client ID'].nunique()} IDs de clientes duplicados!")

            duplicated = (
                duplicated[['Client ID', 'Accrual Date', 'bonus Amount']]
                .sort_values(by=['Client ID', 'Accrual Date'])
                .reset_index(drop=True)
            )

            st.subheader("📋 IDs Duplicados (em ordem crescente)")
            st.dataframe(duplicated, use_container_width=True)

            csv_download = duplicated.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="💾 Baixar relatório de duplicados (CSV)",
                data=csv_download,
                file_name="duplicated_clients.csv",
