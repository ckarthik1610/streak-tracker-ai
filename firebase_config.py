import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate({
            "type": st.secrets["firebase_key"]["type"],
            "project_id": st.secrets["firebase_key"]["project_id"],
            "private_key_id": st.secrets["firebase_key"]["private_key_id"],
            "private_key": st.secrets["firebase_key"]["private_key"],
            "client_email": st.secrets["firebase_key"]["client_email"],
            "client_id": st.secrets["firebase_key"]["client_id"],
            "auth_uri": st.secrets["firebase_key"]["auth_uri"],
            "token_uri": st.secrets["firebase_key"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase_key"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase_key"]["client_x509_cert_url"]
        })
        firebase_admin.initialize_app(cred)
    return firestore.client()
