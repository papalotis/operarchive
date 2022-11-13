from datetime import date

import streamlit as st

from operarchive.database import (
    ProductionsDatabase,
    StageProducerDatabase,
    WorkDatabase,
)
from operarchive.database.deta_interface import Collection
from operarchive.database.models import ProductionModel
from operarchive.utils.common_widgets import (
    delete_item_from_db_widget,
    upload_item_to_db_widget,
)


def find_index_of_item_with_key_return_0_if_not_found_or_key_is_none(
    collection: Collection, key: str | None
) -> int:
    if key is None:
        return 0
    try:
        return collection.find_index_of_item_with_key(key)
    except ValueError:
        return 0


def production_to_show_string(production: ProductionModel) -> str:
    work = WorkDatabase[production.work_key]
    producer = StageProducerDatabase[production.producer_key]
    return f"{work.title} - {production.premiere_year} - {producer.short_name} - {production.disambiguation}"


def run() -> None:
    if len(ProductionsDatabase.data) == 0:
        modify_production = False
    else:
        modify_production = st.checkbox("Modify production")

    page_title = "Add Production" if not modify_production else "Modify Production"
    st.markdown(f"## {page_title}")

    if modify_production:

        production = st.selectbox(
            "Select production",
            ProductionsDatabase.data,
            format_func=production_to_show_string,
        )

        assert production is not None

        default_producer_key = production.producer_key
        default_work_key = production.work_key
        default_disambiguation = production.disambiguation
        default_premiere_year = production.premiere_year
        default_key = production.key

    else:
        default_producer_key = None
        default_work_key = None
        default_disambiguation = ""
        default_premiere_year = date.today().year
        default_key = None
        production = None

    index_producer = find_index_of_item_with_key_return_0_if_not_found_or_key_is_none(
        StageProducerDatabase, default_producer_key
    )
    producer = st.selectbox(
        "Producer",
        StageProducerDatabase.data,
        index=index_producer,
        format_func=lambda x: x.name,
    )

    index_work = find_index_of_item_with_key_return_0_if_not_found_or_key_is_none(
        WorkDatabase, default_work_key
    )
    work = st.selectbox(
        "Work",
        WorkDatabase.data,
        index=index_work,
        format_func=lambda x: f"{x.title} - {x.composer}",
    )

    premiere_year = st.number_input(
        "Premiere year",
        min_value=1500,
        max_value=2999,
        value=default_premiere_year,
        step=1,
    )

    disambiguation = st.text_input("Disambiguation", value=default_disambiguation)

    new_production = ProductionModel(
        key=default_key,
        producer_key=producer.key,
        work_key=work.key,
        premiere_year=premiere_year,
        disambiguation=disambiguation,
    )

    upload_item_to_db_widget(ProductionsDatabase, new_production, fake_wait_time=0.3)
    if production is not None:
        delete_item_from_db_widget(
            ProductionsDatabase,
            production,
            confirm_string="Yes delete this production",
            confirm_prompt='Please type "Yes delete this production" to confirm.',
        )

    # if modify_stage_production:
    #     delete_item_from_db_widget(
    #         StageProductionDatabase,
    #         production,
    #         production.name,
    #         "Type the full name of the stage/production.",
    #     )
    #     st.experimental_rerun()
