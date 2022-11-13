#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import streamlit as st

from operarchive.modes.edit_database.add_modify_performance import (
    run as run_add_performance,
)
from operarchive.modes.edit_database.add_modify_production import (
    run as run_add_production,
)
from operarchive.modes.edit_database.add_modify_stage_producer import (
    run as run_add_stage_producer,
)
from operarchive.modes.edit_database.add_modify_work import run as run_add_work

EDIT_DATABASE = {
    "Work Database": run_add_work,
    "Performance Database": run_add_performance,
    "Production Database": run_add_production,
    "Stage/Producer Database": run_add_stage_producer,
}


def render_page() -> None:
    """Render the "Edit Database" page."""
    st.markdown("# Edit Database")

    with st.sidebar:
        key = st.radio("Select Database", EDIT_DATABASE.keys())
        run = EDIT_DATABASE[key]
    run()
