import pandas as pd


def convert_data(units: list[dict], last_date: str | None = None) -> pd.DataFrame:
    # get first dates of each quarter up to last_date
    if not last_date:
        last_date = pd.Timestamp.now().strftime("%Y-%m-%d")

    dates = pd.date_range(start="2024-07-01", end=last_date, freq="QS", inclusive="both")
    data = []

    for unit in units:
        records = []
        for date in dates:
            record = {**unit}
            record["lat"] = unit["geometry"]["coordinates"][1]
            record["lon"] = unit["geometry"]["coordinates"][0]
            record["year"] = date.year
            record["month"] = date.month
            records.append(record)
            record = {}
        data.extend(records)

    df = pd.DataFrame(data)
    return df
