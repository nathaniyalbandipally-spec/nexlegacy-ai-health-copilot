
import streamlit as st
from supabase import create_client


def create_supabase_client(access_token=None, refresh_token=None):
    """Create a Supabase client for the current user session."""

    client = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

    if access_token and refresh_token:
        client.auth.set_session(access_token, refresh_token)

    return client
