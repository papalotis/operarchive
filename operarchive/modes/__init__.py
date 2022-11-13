from enum import Enum
from typing import Callable

import streamlit as st

from operarchive.modes.edit_database import \
    render_page as render_edit_database_page
from operarchive.modes.explore_performances import \
    render_page as render_explore_performances_page
from operarchive.modes.search import render_page as render_search_page


class Mode(str, Enum):
    EXPLORE_PERFORMANCES = "Explore Performances"
    SEARCH = "Search"
    EDIT_DATABASE = "Edit Database"


MODE_TO_RENDER_PAGE_FUNCTION = {
    Mode.EXPLORE_PERFORMANCES: render_explore_performances_page,
    Mode.SEARCH: render_search_page,
    Mode.EDIT_DATABASE: render_edit_database_page,
}


def select_render_function() -> Callable[[], None]:
    """Select a mode."""
    st.markdown("## Modes")
    mode = st.radio(
        "Select mode",
        options=MODE_TO_RENDER_PAGE_FUNCTION.keys(),
        format_func=lambda mode: mode.value,
    )

    assert mode is not None

    return MODE_TO_RENDER_PAGE_FUNCTION[mode]
