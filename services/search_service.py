import streamlit as st
from tavily import TavilyClient


@st.cache_resource
def get_tavily():
    return TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])


def buscar_info(query: str):
    try:
        tavily = get_tavily()
        resultado = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=6,
            include_answer=True
        )
        textos, fuentes = [], []
        if resultado.get("answer"):
            textos.append(resultado["answer"])
        for r in resultado.get("results", []):
            textos.append(f"- {r['title']}: {r['content'][:400]}")
            fuentes.append(f"• [{r['title']}]({r.get('url', '')})")
        return "\n".join(textos), fuentes
    except Exception as e:
        return f"Error al buscar: {e}", []
