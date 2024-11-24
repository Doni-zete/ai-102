import streamlit as st
from services.blob_service import upload_blob
from services.credit_card_service import analize_credit_card


def configure_inteface():
    st.title("Upload de Arquivos em script python")
    uploaded_file = st.file_uploader(
        "Escolha um arquivo", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        fileName = uploaded_file.name
        # Enviar para azurage
        blob_url = upload_blob(uploaded_file, fileName)
        if blob_url:
            st.write(f"Arquivo {fileName} enviado com sucesso para Azure")
            # Chamar a função de detecção de cartão
            credit_card_info = analize_credit_card(blob_url)
            show_image_and_validadtion(blob_url, credit_card_info)
        else:
            st.write(f"Erro ao enviar o arquivo {fileName} para o Azure")


def show_image_and_validadtion(blob_url, credit_card_info):
    st.image(blob_url, caption="Imagem enviada", use_column_width=True)
    st.write("Resultado da validação: ")
    if credit_card_info and credit_card_info["card_name"]:
        st.markdown(f"<h1 style='color: green;'> Cartão valido</h1>",
                    unsafe_allow_html=True)
        st.write(f"Nome do Titular: {credit_card_info['card_name']}")
        st.write(f"Banco Emissor: {credit_card_info['bank_name']}")
        st.write(f"Data de Validade: {credit_card_info['expiry_date']}")
    else:
        st.markdown(f"<h1 style='color: red;'> Cartão Invalido </h1>",
                    unsafe_allow_html=True)
        st.write("Este não é um cartão de crédito válido.")


if __name__ == "__main__":
    configure_inteface()
