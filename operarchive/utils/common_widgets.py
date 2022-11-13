import time
from typing import Iterable, TypeVar

import streamlit as st
from streamlit_toggle import st_toggle_switch

from operarchive.database.deta_interface import Collection
from operarchive.database.models import DBModel


def text_with_existing_options_but_also_new_input_option(
    label: str,
    options: Iterable[str],
    check_on_lefthand_side: bool = True,
    value: str | None = "",
) -> str:
    ratios = (0.3, 0.7) if check_on_lefthand_side else (0.7, 0.3)
    if check_on_lefthand_side:
        col_check, col_text = st.columns(ratios)
    else:
        col_text, col_check = st.columns(ratios)

    with col_check:
        # is_new = st.checkbox("New value", key=f"{label}_box")
        is_new = (
            st_toggle_switch("New Value", key=f"{label}_box", label_after=True)
            or len(options) == 0
        )

    with col_text:
        if is_new:
            value = st.text_input(label, key=f"{label}_new", value=value)
        else:
            try:
                index_to_show = list(options).index(value)
            except ValueError:
                index_to_show = 0
            value = st.selectbox(
                label, options, key=f"{label}_existing", index=index_to_show
            )

    assert isinstance(value, str)

    return value


T = TypeVar("T", bound=DBModel)


def _sleep_half_time_if_not_none(fake_wait_time: float | None) -> None:
    # return
    if fake_wait_time is not None:
        time.sleep(fake_wait_time / 2)


def upload_item_to_db_widget(
    db: Collection[T],
    element: T,
    fake_wait_time: float | None = None,
    button_promt: str = "Upload",
) -> None:
    if st.button(button_promt):
        with st.spinner("Uploading..."):
            _sleep_half_time_if_not_none(fake_wait_time)
            db.add_item(element)
        st.success("Upload successful")
        _sleep_half_time_if_not_none(fake_wait_time)
        st.experimental_rerun()


def delete_item_from_db_widget(
    db: Collection[T],
    element: T,
    confirm_string: str,
    confirm_prompt: str,
    fake_wait_time: float | None = None,
) -> None:
    with st.expander("Delete entry"):
        st.warning(
            "This action cannot be undone! It will delete the entry from the database.",
            icon="🛑",
        )

        # st.write("hello")

        with st.form("delete_entry", clear_on_submit=True):
            st.markdown(
                f"##### Are you sure you want to delete this entry? {confirm_prompt}"
            )
            user_confirmation = st.text_input("Confirm")

            if st.form_submit_button("Delete"):
                if user_confirmation.strip() != confirm_string.strip():
                    st.error("Incorrect confirmation string")
                else:

                    with st.spinner("Deleting..."):

                        _sleep_half_time_if_not_none(fake_wait_time)
                        db.remove_item(element)
                        st.success("Deletion successful")
                        _sleep_half_time_if_not_none(fake_wait_time)
                        st.experimental_rerun()
