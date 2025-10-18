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

            # IDs únicos
            ids1 = set(df1['Client ID'])
            ids2 = set(df2['Client ID'])

            # Classificar origem de cada ID
            ids_ambos = ids1.intersection(ids2)
            ids_apenas_1 = ids1 - ids2
            ids_apenas_2 = ids2 - ids1

            # Criar dataframe consolidado
            lista = []

            for i in ids_ambos:
                lista.append({"Client ID": i, "Origem": "Ambas"})
            for i in ids_apenas_1:
                lista.append({"Client ID": i, "Origem": "Planilha 1"})
            for i in ids_apenas_2:
                lista.append({"Client ID": i, "Origem": "Planilha 2"})

            resultado = pd.DataFrame(lista).sort_values(by="Client ID").reset_index(drop=True)

            st.subheader("📋 Resultado da Comparação")
            st.dataframe(resultado, use_container_width=True)

            total_1 = len(df1)
            total_2 = len(df2)
            total_comum = len(ids_ambos)
            perc_comum = round((total_comum / ((len(ids1 | ids2))) * 100), 2)

            st.markdown(f"""
            - 📄 **Planilha 1:** {total_1} registros  
            - 📄 **Planilha 2:** {total_2} registros  
            - 🔁 **IDs em comum:** {total_comum}  
            - 📊 **Percentual de IDs em comum:** {perc_comum}%
            """)

            # Baixar CSV
            csv_download = resultado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="💾 Baixar relatório de comparação (CSV)",
                data=csv_download,
                file_name="comparacao_ids.csv",
                mime="text/csv"
            )

    else:
        st.info("👆 Envie os dois arquivos CSV para comparar.")
