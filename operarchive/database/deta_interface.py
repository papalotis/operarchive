from typing import Any, Generic, TypeVar

import streamlit as st
from deta import Deta
from deta.base import _Base
from fastapi.encoders import jsonable_encoder

from operarchive.database.models import DBModel


def load_project_key() -> str:
    key: str = st.secrets["project_key"]
    return key


def load_project_id() -> str:
    project_id: str = st.secrets["project_id"]
    return project_id


deta = Deta(load_project_key())


def get_base(name: str) -> _Base:
    return deta.Base(name)


@st.experimental_memo
def load_data_from_base(name: str) -> list[Any]:

    import time

    tic = time.time()
    base = get_base(name)
    data = base.fetch().items
    toc = time.time()
    print(f'Loaded {len(data)} items from "{name}" in {toc - tic:.2f} seconds.')
    return data


T = TypeVar("T", bound=DBModel)


class Collection(Generic[T]):
    def __init__(self, database_name: str, datatype: type[T]) -> None:
        self.database_name = database_name
        self.datatype = datatype

        self.key_to_index: dict[str, int] = {}

    @property
    def data(self) -> list[T]:
        items = load_data_from_base(self.database_name)
        return [self.datatype(**values) for values in items]

    @property
    def base(self) -> _Base:
        return get_base(self.database_name)

    def add_item(self, item: T) -> None:
        self.base.put(jsonable_encoder(item))
        load_data_from_base.clear()

    def remove_item(self, item: T) -> None:
        self.base.delete(item.key)
        load_data_from_base.clear()

    def find_index_of_item_with_key(self, key: str) -> int:
        for i, item in enumerate(self.data):
            if item.key == key:
                return i
        raise ValueError(f"Could not find item with key {key}")

    def __getitem__(self, key: str) -> T:
        return self._get_by_key(key)

    def _get_by_key(self, key: str) -> T:
        if key not in self.key_to_index:
            self.key_to_index[key] = self.find_index_of_item_with_key(key)

        return self.data[self.key_to_index[key]]
