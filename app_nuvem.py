import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta

# --- LIGAÇÃO SUPABASE ---
URL_NUVEM = "https://gcgmztsqtqgqhsvqzncz.supabase.co"
KEY_NUVEM = "sb_publishable_MfxiCv7gYIk-kJvD1xjlZw_9q2Jvz9A"
supabase = create_client(URL_NUVEM, KEY_NUVEM)

st.set_page_config(page_title="RSF Cloud", page_icon="📸")
st.title("🔧 RSF CRM Mobile")

# O programa procura se o MacroDroid enviou algum número no link
numero_chamada = st.query_params.get("telefone", "")

with st.form("form_oficina"):
    telefone = st.text_input("Telefone do Cliente", value=numero_chamada)
    oficina = st.text_input("Nome da Oficina / Cliente*")
    servico = st.selectbox("Serviço", ["Manutenção Preventiva", "Reparação Urgente", "Montagem", "Orçamento"])
    
    st.write("---")
    foto = st.camera_input("📸 Tirar Foto ao Autocolante (Opcional)") 
    notas = st.text_area("Observações")
    
    if st.form_submit_button("ENVIAR PARA O ESCRITÓRIO"):
        if oficina: 
            try:
                # 1. Guarda o telefone para o PC conseguir extrair
                obs_final = f"TEL: {telefone} | " if telefone else "TEL: S/N | "
                
                # 2. SE VEIO DE UMA CHAMADA, REGISTA A HORA!
                if numero_chamada:
                    # Regista a hora exata em que o formulário está a ser enviado
                    hora_atual = datetime.now().strftime('%H:%M')
                    obs_final += f"📞 Chamada às {hora_atual} | "
                
                # 3. Trata das fotos e das notas
                if foto:
                    nome_f = f"{oficina.replace(' ','_')}_{datetime.now().strftime('%H%M%S')}.jpg"
                    supabase.storage.from_("fotos-gauto").upload(nome_f, foto.getvalue())
                    obs_final += f"FOTO_PENDENTE:{nome_f} | {notas}"
                else:
                    obs_final += f"SEM FOTO | {notas}"

                # 4. Envia para a Base de Dados
                supabase.table("elevadores_nuvem").insert({
                    "cliente": oficina,
                    "estado": servico,
                    "data_alerta": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                    "observacoes": obs_final
                }).execute()
                
                st.success("✅ Guardado! O PC vai descarregar tudo.")
            except Exception as e:
                st.error(f"Erro ao enviar: {e}")
        else:
            st.error("⚠️ O Nome da oficina é obrigatório!")
