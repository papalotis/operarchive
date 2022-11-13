import streamlit as st

from operarchive.database import StageProducerDatabase
from operarchive.database.models import StageProducerModel
from operarchive.utils.common_widgets import (
    delete_item_from_db_widget,
    upload_item_to_db_widget,
)


def run() -> None:

    if len(StageProducerDatabase.data) == 0:
        modify_stage_producer = False
    else:
        modify_stage_producer = st.checkbox("Modify existing stage/producer")

    page_title = (
        "Add Stage/Producer" if not modify_stage_producer else "Modify Stage/Producer"
    )
    st.markdown(f"## {page_title}")

    if modify_stage_producer:

        stage_producer = st.selectbox(
            "Select stage producer",
            StageProducerDatabase.data,
            format_func=lambda x: " - ".join([x.name, x.short_name]),
        )

        assert stage_producer is not None

        default_name = stage_producer.name
        default_short_name = stage_producer.short_name
        default_key = stage_producer.key

    else:
        default_name = ""
        default_short_name = ""
        default_key = None

    name = st.text_input("Name", value=default_name).strip()
    short_name = st.text_input("Short Name", value=default_short_name).strip()
    new_stage_producer = StageProducerModel(
        key=default_key,
        name=name,
        short_name=short_name,
    )

    upload_item_to_db_widget(
        StageProducerDatabase,
        new_stage_producer,
        fake_wait_time=0.5,
    )

    if modify_stage_producer:
        delete_item_from_db_widget(
            StageProducerDatabase,
            stage_producer,
            stage_producer.name,
            "Type the full name of the stage/producer.",
        )


# if __name__ == "__main__":
#     from tqdm import tqdm

#     from operarchive.database.deta_interface import Collection

#     old_prod = Collection("stages_productions", StageProducerModel)
#     new_prod = StageProducerDatabase

#     for el in tqdm(old_prod.data):
#         new_prod.add_item(el)
