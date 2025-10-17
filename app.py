import streamlit as st
import pandas as pd

st.set_page_config(page_title="Validação de IDs Duplicados", layout="wide")

st.title("🔍 Validação de IDs Duplicados")

st.write("""
Envie um arquivo CSV com as colunas **Client ID**, **Accrual Date** e **Bonus Amount**  
para identificar IDs duplicados e gerar um relatório para download.
""")

# Upload do arquivo
uploaded_file = st.file_uploader("📂 Escolha o arquivo CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Verifica se as colunas necessárias existem
    required_cols = {'Client ID', 'Accrual Date', 'Bonus Amount'}
    if not required_cols.issubset(df.columns):
        st.error("O CSV precisa conter as colunas: 'Client ID', 'Accrual Date' e 'Bonus Amount'.")
    else:
        st.success("✅ CSV carregado com sucesso!")

        # Identifica duplicados com base apenas no Client ID
        duplicated = df[df.duplicated(subset=['Client ID'], keep=False)]

        if duplicated.empty:
            st.info("🎉 Nenhum ID duplicado encontrado!")
        else:
            st.warning(f"⚠️ Foram encontrados {duplicated['Client ID'].nunique()} IDs de clientes duplicados!")

            # Mantém apenas as colunas necessárias e ordena
            duplicated = (
                duplicated[['Client ID', 'Accrual Date', 'Bonus Amount']]
                .sort_values(by=['Client ID', 'Accrual Date'], ascending=True)
                .reset_index(drop=True)
            )

            st.subheader("📋 IDs Duplicados (em ordem crescente)")
            st.dataframe(duplicated, use_container_width=True)

            # Cria o CSV em memória para download
            csv_download = duplicated.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="💾 Baixar relatório de duplicados (CSV)",
                data=csv_download,
                file_name="duplicated_clients.csv",
                mime="text/csv"
            )
