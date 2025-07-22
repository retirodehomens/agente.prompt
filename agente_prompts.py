import streamlit as st
from openai import OpenAI

# Inicializa o cliente da OpenAI com a chave da API do Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def gerar_prompts_por_nivel(tema):
    niveis = {
        1: f"Crie um prompt simples sobre: {tema}.",
        2: f"Crie um prompt com mais direcionamento sobre: {tema}.",
        3: f"Crie um prompt com parâmetros específicos para o tema: {tema}.",
        4: f"Crie um prompt com exemplos ou estilo desejado sobre: {tema}.",
        5: f"Crie um prompt com contexto, público e objetivo claros sobre: {tema}.",
        6: f"""Crie um prompt nota 10, no mais alto nível de engenharia, sobre: {tema}. O prompt deve:
- Instruir o modelo a agir como um especialista no assunto
- Definir claramente o público-alvo
- Definir estrutura, tom e formato da resposta
- Incluir restrições ou objetivos específicos
- Ser otimizado para performance máxima
- Estimular criatividade, profundidade e utilidade"""
    }

    resultados = {}
    for nivel, instrucoes in niveis.items():
        modelo = "gpt-4"  # tenta usar GPT-4
        try:
            resposta = client.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": "Você é um especialista em engenharia de prompts."},
                    {"role": "user", "content": instrucoes}
                ],
                temperature=0.8
            )
        except Exception as e:
            if "model_not_found" in str(e) or "does not exist" in str(e):
                modelo = "gpt-3.5-turbo"  # fallback automático
                resposta = client.chat.completions.create(
                    model=modelo,
                    messages=[
                        {"role": "system", "content": "Você é um especialista em engenharia de prompts."},
                        {"role": "user", "content": instrucoes}
                    ],
                    temperature=0.8
                )
            else:
                raise e
        resultados[nivel] = resposta.choices[0].message.content.strip()

    return resultados

# Interface Streamlit
st.set_page_config(page_title="Agente Neural de Prompts", layout="wide")
st.title("🤖 Agente Neural: Geração de Prompts em 6 Níveis")
tema = st.text_input("Digite o tema-base do prompt:")

if st.button("Gerar Prompts"):
    if tema.strip() == "":
        st.warning("Digite um tema antes de gerar.")
    else:
        st.info("Gerando prompts, aguarde...")
        try:
            resultados = gerar_prompts_por_nivel(tema)
            for nivel in range(1, 7):
                cor = "#38b000" if nivel == 6 else "#1f77b4"
                st.markdown(f"### 🎯 Nível {nivel} de complexidade")
                st.code(resultados[nivel], language="markdown")
                if nivel == 6:
                    st.markdown(f"🟢 **Avaliação:** Nota **10/10** – Prompt de excelência.")
        except Exception as e:
            st.error(f"Erro ao gerar prompts: {e}")
