import os
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd


def convert_to_int(x):
    if isinstance(x, dict):
        if '$numberLong' in x:
            return int(x['$numberLong'])
        if '$numberDouble' in x:
            return float(x['$numberDouble']) if x['$numberDouble'] != 'NaN' else None
    return x


def download_data():
    static = Path('static')
    if len(list(static.iterdir())) > 0:
        return

    base_url = os.getenv("BASE_URL")
    files = [
        "PropertyDetails.BUILDING_BOX.json",
        "PropertyDetails.BUILDING_FLOORS.json",
        "PropertyDetails.PERSON_PROPERTY_BOX.json",
        "PropertyDetails.PREDICTION_DATA.json",
        "PropertyDetails.PRICE_INDEXES.json",
        "PropertyDetails.PROPERTY_INFORMATION_BOX.json",
        "PropertyDetails.UNITS.json",
    ]

    for file in files:
        # use urllib to download the file
        urlretrieve(f"{base_url}/{file}", f"static/{file}")


def process_data():
    static = Path('static')
    for file in static.iterdir():
        if not file.is_file() or not file.suffix == ".json":
            continue

        with open(file, encoding="utf-8") as f:
            data = pd.read_json(f, encoding="utf-8")

        data = data.drop(columns=['_id'])
        data.columns = data.columns.str.lower()
        collection_name = file.stem.replace("PropertyDetails.", "").lower()

        if collection_name == "building_floors":
            data = data.drop_duplicates(subset=["floor_id"])

        # for any column, if there is any row that have a dict having {'$numberLong': 'string'} as value, convert it to int
        for col in data.columns:
            if col != "geometry":
                print(col, collection_name)
                data[col] = data[col].apply(convert_to_int)

        with open(f"static/processed/{collection_name}.json", "w", encoding="utf-8") as f:
            f.write(data.to_json(orient='records', indent=4))
