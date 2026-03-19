import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta

# --- LIGAÇÃO SUPABASE ---
URL_NUVEM = "https://gcgmztsqtqgqhsvqzncz.supabase.co"
KEY_NUVEM = "sb_publishable_MfxiCv7gYIk-kJvD1xjlZw_9q2Jvz9A"
supabase = create_client(URL_NUVEM, KEY_NUVEM)

st.set_page_config(page_title="G-AUTO Cloud", page_icon="📸")
st.title("🔧 G-AUTO CRM Mobile")

with st.form("form_oficina"):
    oficina = st.text_input("Nome da Oficina")
    servico = st.selectbox("Serviço", ["Manutenção", "Reparação", "Montagem"])
    
    st.write("---")
    # ESTA É A LINHA QUE CRIA O BOTÃO DA FOTO:
    foto = st.camera_input("📸 Tirar Foto ao Autocolante") 
    
    notas = st.text_area("Observações")
    
    if st.form_submit_button("ENVIAR PARA O ESCRITÓRIO"):
        if oficina and foto:
            try:
                nome_f = f"{oficina.replace(' ','_')}_{datetime.now().strftime('%H%M%S')}.jpg"
                supabase.storage.from_("fotos-gauto").upload(nome_f, foto.getvalue())
                
                supabase.table("elevadores_nuvem").insert({
                    "cliente": oficina,
                    "estado": servico,
                    "data_alerta": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                    "observacoes": f"FOTO_PENDENTE:{nome_f} | {notas}"
                }).execute()
                st.success("✅ Enviado com sucesso!")
            except Exception as e:
                st.error(f"Erro: {e}")
        else:
            st.error("⚠️ Nome da oficina e Foto são obrigatórios!")
