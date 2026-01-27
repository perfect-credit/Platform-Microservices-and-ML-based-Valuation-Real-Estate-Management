import json
import os

import jsonlines
import pandas as pd
from pymongo import MongoClient

from schemas import Building, Floor, Property, Owner, Unit

client = MongoClient(os.getenv("MONGO_URI"))
db = client['SPM']


def push_owner_data():
    with open("static/processed/person_property_box.json", "r", encoding="utf-8") as reader:
        owners = json.loads(reader.read())

    data = []
    for owner in owners:
        data.append(Owner(**owner).model_dump())

    collection = db["owners"]
    collection.insert_many(data)


def push_floor_data():
    with open("static/processed/building_floors.json", "r", encoding="utf-8") as reader:
        floors = json.loads(reader.read())

    data = []
    for floor in floors:
        data.append(Floor(**floor).model_dump())

    collection = db["floors"]
    collection.insert_many(data)


def push_building_data():
    collection = db["floors"]
    floor_data = list(collection.find({}))

    building_floors = {}
    for floor in floor_data:
        if floor["building_id"] not in building_floors:
            building_floors[floor["building_id"]] = []
        building_floors[floor["building_id"]].append({"$ref": "floors", "$id": floor["_id"]})

    with open("static/processed/building_box.json", "r", encoding="utf-8") as reader:
        buildings = json.loads(reader.read())

    for building in buildings:
        building["floor_data"] = building_floors.get(building["building_id"], [])

    data = []
    for building in buildings:
        data.append(Building(**building).model_dump())

    collection = db["buildings"]
    collection.insert_many(data)


def push_unit_data():
    with open("static/processed/units.json", "r", encoding="utf-8") as reader:
        units = json.loads(reader.read())

    with open("static/processed/prediction_data.json", "r", encoding="utf-8") as reader:
        pred_data = json.loads(reader.read())

    preds = {}
    for item in pred_data:
        preds[item["unit_id"]] = item

    data = []
    for unit in units:
        if unit["unit_id"] in preds:
            if not unit["index_id"]:
                continue
            unit.update(preds[unit["unit_id"]])
            data.append(Unit(**unit).model_dump())

    collection = db["units"]
    collection.insert_many(data)

    with open("static/processed/unit-update.json", "w", encoding="utf-8") as writer:
        writer.write(json.dumps(list(collection.find({}, {"_id": 0, "created_at": 0, "updated_at": 0})), indent=4))


def push_property_data():
    collection = db["buildings"]
    building_data = list(collection.find({}))

    collection = db["owners"]
    owner_data = list(collection.find({}))

    collection = db["units"]
    unit_data = list(collection.find({}))

    property_buildings = {}
    for building in building_data:
        if building["property_id_nma"] not in property_buildings:
            property_buildings[building["property_id_nma"]] = []
        property_buildings[building["property_id_nma"]].append({"$ref": "buildings", "$id": building["_id"]})

    property_owners = {}
    for owner in owner_data:
        if owner["property_id_nma"] not in property_owners:
            property_owners[owner["property_id_nma"]] = []
        property_owners[owner["property_id_nma"]].append({"$ref": "owners", "$id": owner["_id"]})

    property_units = {}
    for unit in unit_data:
        if unit["property_id_nma_main"] not in property_units:
            property_units[unit["property_id_nma_main"]] = []
        property_units[unit["property_id_nma_main"]].append({"$ref": "units", "$id": unit["_id"]})

        if unit["property_id_nma"] != unit["property_id_nma_main"]:
            if unit["property_id_nma"] not in property_units:
                property_units[unit["property_id_nma"]] = []
            property_units[unit["property_id_nma"]].append({"$ref": "units", "$id": unit["_id"]})

    with open("static/processed/property_information_box.json", "r", encoding="utf-8") as reader:
        properties = json.loads(reader.read())

    for property in properties:
        property["buildings"] = property_buildings.get(property["property_id_nma"], [])
        property["owners"] = property_owners.get(property["property_id_nma"], [])
        property["units"] = property_units.get(property["property_id_nma"], [])

    data = []
    for property in properties:
        data.append(Property(**property).model_dump())

    collection = db["properties"]
    collection.insert_many(data)


def prepare_unit_valuations(unit, index):
    fields = ["rental_valuation", "rental_model_valuation", "index_valuation", "comparables_valuation", "listing_valuation", "transaction_valuation"]

    for i in index:
        if i["date"].split("-")[1] in {"01", "04", "07", "10"} and i["date"].split("-")[0] != "2003":
            val = {**unit, "date": i["date"], "index": i["index"]}
            for field in fields:
                if unit[field]:
                    val[field] = unit[field] / index[-1]["index"] * i["index"]
                else:
                    val[field] = None

            with jsonlines.open(f"static/timeseries/{val['date']}.jsonl", "a") as writer:
                writer.write(val)


def prepare_valuation_data():
    with open("static/processed/unit-update.json", encoding="utf-8") as reader:
        units = json.loads(reader.read())

    with open("static/processed/index-data.json") as reader:
        indexes = json.loads(reader.read())

    index_data = {}
    for index in indexes:
        if index["index_id"]:
            index_data[index["index_id"]] = index["index_data"]

    for unit in units:
        if unit["index_id"]:
            index_id = unit["index_id"]
            index = index_data[index_id]
            prepare_unit_valuations(unit, index)
