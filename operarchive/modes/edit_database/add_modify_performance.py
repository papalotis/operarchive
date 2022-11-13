from datetime import date

import streamlit as st

from operarchive.database import (
    StageProducerDatabase,
    WorkDatabase,
)
from operarchive.database.models import DateType


def run() -> None:

    seen_work = st.selectbox(
        "Select work",
        WorkDatabase.data,
        format_func=lambda x: " - ".join([x.composer, x.title]),
    )

    date_type = st.radio(
        "Date type", list(DateType), format_func=lambda x: x.value, horizontal=True
    )

    if date_type == DateType.EXACT:
        earliest = st.date_input(
            "Date", min_value=date(1500, 1, 1), max_value=date(2999, 12, 31)
        )
        latest = earliest
    elif date_type == DateType.RANGE:
        col_left, col_right = st.columns(2)
        with col_left:
            earliest = st.date_input(
                "Earliest date",
                min_value=date(1500, 1, 1),
                max_value=date(2999, 12, 31),
            )
        with col_right:
            latest = st.date_input(
                "Latest date",
                min_value=date(1500, 1, 1),
                max_value=date(2999, 12, 31),
            )
    elif date_type == DateType.UNKNOWN:
        earliest = None
        latest = None
    else:
        raise ValueError("Unreachable code")

    stage = st.selectbox(
        "Stage",
        StageProducerDatabase.data,
        format_func=lambda x: " - ".join([x.name, x.short_name]),
    )

    st.write("hello")
