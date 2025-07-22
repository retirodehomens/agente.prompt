import streamlit as st
import openai

# Configurar sua API Key da OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

def gerar_prompts_por_nivel(tema):
    niveis = {
        1: f"Crie um prompt simples sobre: {tema}.",
        2: f"Crie um prompt com mais direcionamento sobre: {tema}.",
        3: f"Crie um prompt com parâmetros específicos para o tema: {tema}.",
        4: f"Crie um prompt com exemplos ou estilo desejado sobre: {tema}.",
        5: f"Crie um prompt com contexto, público e objetivo claros sobre: {tema}.",
        6: f"Crie um prompt nota 10, no mais alto nível de engenharia, sobre: {tema}. O prompt deve:\n"
           "- Instruir o modelo a agir como um especialista no assunto\n"
           "- Definir claramente o público-alvo\n"
           "- Definir estrutura, tom e formato da resposta\n"
           "- Incluir restrições ou objetivos específicos\n"
           "- Ser otimizado para performance máxima\n"
           "- Estimular criatividade, profundidade e utilidade"
    }

    resultados = {}
    for nivel, instrucoes in niveis.items():
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista em engenharia de prompts."},
                {"role": "user", "content": instrucoes}
            ],
            temperature=0.8
        )
        resultados[nivel] = resposta.choices[0].message.content.strip()

    return resultados

st.set_page_config(page_title="Agente Neural de Prompts", layout="wide")
st.title("🤖 Agente Neural: Geração de Prompts em 6 Níveis")
tema = st.text_input("Digite o tema-base do prompt:")

if st.button("Gerar Prompts"):
    if tema.strip() == "":
        st.warning("Digite um tema antes de gerar.")
    else:
        st.info("Gerando prompts, aguarde...")
        resultados = gerar_prompts_por_nivel(tema)
        for nivel in range(1, 7):
            cor = "#38b000" if nivel == 6 else "#1f77b4"
            st.markdown(f"### 🎯 Nível {nivel} de complexidade")
            st.code(resultados[nivel], language="markdown")
            if nivel == 6:
                st.markdown(f"🟢 **Avaliação:** Nota **10/10** – Prompt de excelência.")
      
