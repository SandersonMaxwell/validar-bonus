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
st.sidebar.info("As colunas esperadas são: **Client ID**, **Accrual Date** e **bonus Amount**.")

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
                total = len(df)
                dup_total = duplicated['Client ID'].nunique()
                perc = round((dup_total / total) * 100, 2)

                st.warning(f"⚠️ Foram encontrados {dup_total} IDs duplicados ({perc}% do total).")

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
            ids_comuns = set(df1['Client ID']).intersection(set(df2['Client ID']))

            if not ids_comuns:
                st.info("🎉 Nenhum ID em comum foi encontrado entre as duas planilhas.")
            else:
                # Filtra apenas IDs em comum
                df1_common = df1[df1['Client ID'].isin(ids_comuns)].copy()
                df2_common = df2[df2['Client ID'].isin(ids_comuns)].copy()

                # Adiciona coluna indicando origem
                df1_common["Origem"] = "Planilha 1"
                df2_common["Origem"] = "Planilha 2"

                # Junta os dois dataframes
                resultado = pd.concat([df1_common, df2_common], ignore_index=True)

                resultado = resultado[['Client ID', 'Accrual Date', 'bonus Amount', 'Origem']] \
                    .sort_values(by=['Client ID', 'Origem', 'Accrual Date']) \
                    .reset_index(drop=True)

                st.subheader("📋 IDs encontrados em ambas as planilhas")
                st.dataframe(resultado, use_container_width=True)

                st.markdown(f"**Total de IDs em comum:** {len(ids_comuns)}")

                # Baixar CSV
                csv_download = resultado.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 Baixar relatório de IDs em comum (CSV)",
                    data=csv_download,
                    file_name="ids_em_comum.csv",
                    mime="text/csv"
                )
    else:
        st.info("👆 Envie os dois arquivos CSV para comparar.")
