import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta

# --- CREDENCIAIS ---
URL_NUVEM = "https://gcgmztsqtqgqhsvqzncz.supabase.co"
KEY_NUVEM = "sb_publishable_MfxiCv7gYIk-kJvD1xjlZw_9q2Jvz9A"
supabase = create_client(URL_NUVEM, KEY_NUVEM)

st.set_page_config(page_title="G-AUTO Cloud", page_icon="☁️")
st.title("☁️ G-AUTO Cloud")
st.write("Insira os dados da oficina. Eles serão guardados na nuvem até abrir o PC no escritório.")

with st.form("form_cloud"):
    oficina = st.text_input("Nome da Oficina / Cliente")
    servico = st.selectbox("Tipo de Serviço", ["Manutenção Preventiva", "Reparação Urgente", "Montagem"])
    notas = st.text_area("Notas / Observações")
    
    if st.form_submit_button("ENVIAR PARA O ESCRITÓRIO"):
        if oficina:
            data_alerta = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
            try:
                supabase.table("elevadores_nuvem").insert({
                    "cliente": oficina,
                    "estado": servico,
                    "data_alerta": data_alerta,
                    "observacoes": f"NUVEM: {notas}"
                }).execute()
                st.success(f"✅ Sucesso! {oficina} enviado. Pode desligar.")
            except Exception as e:
                st.error(f"Erro ao enviar: {e}")
        else:
            st.error("Por favor, indique o nome da oficina.")

st.divider()
st.subheader("Pendentes na Nuvem")
try:
    res = supabase.table("elevadores_nuvem").select("cliente, estado").execute()
    if res.data:
        for r in res.data:
            st.write(f"• {r['cliente']} ({r['estado']})")
    else:
        st.write("Nuvem limpa.")
except:
    pass