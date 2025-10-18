import streamlit as st
import pandas as pd

st.set_page_config(page_title="Validação e Comparação de IDs", layout="wide")

st.title("🔍 Validação e Comparação de IDs de Clientes")

st.sidebar.title("⚙️ Opções da Aplicação")
modo = st.sidebar.radio(
    "Escolha o modo de operação:",
    ["Verificar Duplicados", "Comparar Dois Arquivos"]
)

st.sidebar.write("---")
st.sidebar.info("Certifique-se de que seu CSV contém as colunas: **Client ID**, **Accrual Date** e **bonus Amount**.")

def validar_colunas(df):
    required_cols = {'Client ID', 'Accrual Date', 'bonus Amount'}
    return required_cols.issubset(df.columns)

# ---------------------------
# 🧾 MODO 1 - Verificar duplicados
# ---------------------------
if modo == "Verificar Duplicados":
    st.subheader("🧾 Verificação de IDs Duplicados")

    uploaded_file = st.file_uploader("📂 Escolha o arquivo CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

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
                    mime="text/csv"
                )

# ---------------------------
# 🔁 MODO 2 - Comparar dois arquivos
# ---------------------------
elif modo == "Comparar Dois Arquivos":
    st.subheader("🔁 Comparar IDs entre dois arquivos CSV")

    uploaded_file1 = st.file_uploader("📂 Escolha o primeiro arquivo CSV", type="csv", key="file1")
    uploaded_file2 = st.file_uploader("📂 Escolha o segundo arquivo CSV", type="csv", key="file2")

    if uploaded_file1 and uploaded_file2:
        df1 = pd.read_csv(uploaded_file1)
        df2 = pd.read_csv(uploaded_file2)

        if not validar_colunas(df1) or not validar_colunas(df2):
            st.error("Ambos os arquivos precisam conter as colunas: 'Client ID', 'Accrual Date' e 'bonus Amount'.")
        else:
            st.success("✅ Ambos os arquivos carregados com sucesso!")

            # IDs em comum
            common_ids = pd.merge(df1, df2, on='Client ID', suffixes=('_File1', '_File2'))

            if common_ids.empty:
                st.info("✅ Nenhum ID em comum encontrado entre os dois arquivos.")
            else:
                st.warning(f"⚠️ Encontrados {common_ids['Client ID'].nunique()} IDs presentes em ambos os arquivos!")

                resultado = (
                    common_ids[['Client ID', 'Accrual Date_File1', 'bonus Amount_File1',
                                'Accrual Date_File2', 'bonus Amount_File2']]
                    .sort_values(by='Client ID')
                    .reset_index(drop=True)
                )

                st.subheader("📋 IDs que aparecem em ambos os arquivos")
                st.dataframe(resultado, use_container_width=True)

                csv_download = resultado.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 Baixar relatório de IDs em comum (CSV)",
                    data=csv_download,
                    file_name="common_clients.csv",
                    mime="text/csv"
                )

    else:
        st.info("👆 Envie os dois arquivos CSV para comparar.")
