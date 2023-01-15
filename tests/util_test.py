import json

import pytest
from src.util import (AppStoreCategories, AppStoreCollections,
                                     AppStoreUtils)


def test_category_exists():
    category = AppStoreCategories()
    assert category.BOOKS == 6018


def test_category_does_not_exist():
    category = AppStoreCategories()
    with pytest.raises(AttributeError, match="'AppStoreCategories' object has no attribute 'METHOD'"):
        category.METHOD


def test_collection_exists():
    collection = AppStoreCollections()
    assert collection.NEW_IOS == "newapplications"


def test_collection_does_not_exist():
    collection = AppStoreCollections()
    with pytest.raises(AttributeError, match="'AppStoreCollections' object has no attribute 'NOTHING'"):
        collection.NOTHING


def test_app_utils():
    utils = AppStoreUtils()
    json_object = json.loads(utils.get_entries(AppStoreCollections()))
    assert "names" in json_object
