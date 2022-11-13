from datetime import date

import streamlit as st
from streamlit_toggle import st_toggle_switch

from operarchive.database import WorkDatabase
from operarchive.database.models import WorkModel, WorkType
from operarchive.utils.common_widgets import (
    delete_item_from_db_widget,
    text_with_existing_options_but_also_new_input_option,
    upload_item_to_db_widget,
)


def run() -> None:

    modify_work = st.checkbox("Modify existing work")

    page_title = "Add Work" if not modify_work else "Modify Work"
    st.markdown(f"## {page_title}")

    if modify_work:
        work = st.selectbox(
            "Select work",
            sorted(WorkDatabase.data, key=lambda x: x.title),
            format_func=lambda x: " - ".join([x.composer, x.title]),
        )

        assert work is not None

        default_work_type_index = list(t.name for t in WorkType).index(
            work.work_type.name
        )
        default_composer = work.composer
        default_title = work.title
        default_premier_year = work.world_premiere_year
        default_written_year = work.written_year
        default_version_year = work.version_year
        default_main_roles = "\n".join(work.main_roles)
        default_key = work.key
    else:
        default_work_type_index = 0
        default_composer = ""
        default_title = ""
        default_premier_year = date.today().year
        default_written_year = default_premier_year
        default_version_year = default_premier_year
        default_main_roles = ""
        default_key = None

    st.session_state["modify_or_add_work"] = modify_work

    column_left, column_right = st.columns(2)
    with column_left:

        title = st.text_input("Title", value=default_title).strip()
        premiere_year = st.number_input(
            "World Premiere Year",
            min_value=1500,
            max_value=2999,
            value=default_premier_year,
            step=1,
        )
        if not modify_work:
            show_options_for_written_version_years = st_toggle_switch(
                "Explicit written and version years"
            )
        else:
            show_options_for_written_version_years = True
        if show_options_for_written_version_years:

            written_year = st.number_input(
                "Written Year",
                min_value=1500,
                max_value=2999,
                value=default_written_year,
                step=1,
            )
            version_year = st.number_input(
                "Version Year",
                min_value=1500,
                max_value=2999,
                value=default_version_year,
                step=1,
            )
        else:
            written_year = premiere_year
            version_year = premiere_year

    with column_right:
        known_composers = {work.composer for work in WorkDatabase.data}
        composer = text_with_existing_options_but_also_new_input_option(
            "Composer",
            known_composers,
            value=default_composer,
        ).strip()
        work_type = st.selectbox(
            "Work Type",
            WorkType,
            format_func=lambda x: x.name.title(),
            index=default_work_type_index,
        )

    st.markdown("### Roles")

    roles = st.text_area(
        "Role",
        help="Separate roles with a new line",
        value=default_main_roles,
        height=(len(default_main_roles.splitlines()) + 10) * 20,
    )

    button_text = "Submit " + ("new work" if not modify_work else "changes")

    number_of_existing_works = sum(
        1
        for work in WorkDatabase.data
        if work.composer == composer and work.title == title
    )
    if number_of_existing_works > 0 and not modify_work:
        st.warning(
            f"Work with composer '{composer}' and title '{title}' already exists in the database.",
            icon="🔔",
        )
    roles_list = roles.splitlines()

    st.write(work_type)
    new_work = WorkModel(
        key=default_key,
        title=title,
        work_type=work_type.value,
        composer=composer,
        written_year=written_year,
        world_premiere_year=premiere_year,
        version_year=version_year,
        main_roles=roles_list,
    )
    upload_item_to_db_widget(WorkDatabase, new_work, 1, button_text)

    if modify_work and work is not None:
        delete_item_from_db_widget(
            WorkDatabase,
            work,
            work.title,
            "Enter the title of the work to confirm.",
            1.0,
        )


if __name__ == "__main__":
    from collections import defaultdict

    all_entered_works = sorted(WorkDatabase.data, key=lambda x: x.title)
    d: list[WorkModel] = defaultdict(list)
    # print(len(all_entered_works), len(all_unique_works))
    for work in all_entered_works:
        d[work.title].append(work)

    for title, works in d.items():
        if len(works) > 1:
            print(title)
    # for work in all_entered_works:
    #     print(work.title)
