

import streamlit as st
from supabase import create_client


def create_supabase_client():
    """Create a client for the current Streamlit session."""
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
