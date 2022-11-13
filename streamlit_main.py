import streamlit as st

from operarchive.modes import select_render_function

with st.sidebar:
    st.markdown("# Vangelis OperArchive")

    render_func = select_render_function()

render_func()
