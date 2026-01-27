import json
import random
from datetime import date

import joblib

from etl import convert_data
from pb.valuation_pb2_grpc import ValuationServiceServicer
from pb.valuation_pb2 import ValuationResponse
from realestate import RealestateClient


class ValuationService(ValuationServiceServicer):
    def __init__(self):
        super().__init__()
        self.model = joblib.load("models/valuation.pkl")
        self.features = ["floor_number", "floors", "bta", "bra", "prom", "rooms", "bedrooms", "bathrooms", "wcs", "nearest_train_station_distance", "nearest_bus_station_distance", "nearest_ferry_terminal_distance", "nearest_tram_station_distance", "nearest_underground_station_distance", "nearest_airport_distance", "nearest_kindergartens_distance", "nearest_elementary_middle_school_distance", "nearest_high_school_distance", "nearest_fire_station_distance", "in_beach_zone", "lat", "lon", "year", "month"]
        self.valuation_types = ["rental_valuation", "rental_model_valuation", "index_valuation", "comparables_valuation", "listing_valuation", "transaction_valuation"]

        with open("models/valuation-rates.json") as reader:
            rates = json.loads(reader.read())

        self.valuation_rates = {}
        for rate in rates:
            self.valuation_rates[rate["index_id"]] = {key: rate[f"{key}_rate"] for key in self.valuation_types}

    def calculate_valuations(self, index_data: list[dict]) -> list[dict]:
        today = date.today()
        year = today.year
        inflation_rate = 0.3
        valuations = []

        for index in index_data:
            difference = index["year"] - year
            if difference < 2:
                inflation_parameter = (index["year"] - year + 3 - difference) * inflation_rate
            elif difference < 4:
                inflation_parameter = (index["year"] - year + 1.5) * inflation_rate
            else:
                inflation_parameter = (index["year"] - year + 0.5) * inflation_rate
            index["index"] = index["index"] * (1 + inflation_parameter)

            valuation = {**index}
            for key in self.valuation_types:
                disturbance = random.uniform(0.05, 0.07)
                valuation[key] = index["index"] * self.valuation_rates[index["index_id"]][key] * (1 + disturbance)
            valuations.append(valuation)
        return valuations

    async def GetPropertyValuation(self, request, context) -> ValuationResponse:
        client = RealestateClient()
        units = client.get_property_units(request.property_id_nma)
        X = convert_data(units, request.date)
        y = self.model.predict(X[self.features])
        X["index"] = y
        valuations = self.calculate_valuations(X[["unit_id", "year", "month", "index", "index_id"]].to_dict(orient="records"))
        return ValuationResponse(valuations=json.dumps(valuations))

    async def GetUnitValuation(self, request, context) -> ValuationResponse:
        client = RealestateClient()
        unit = client.get_unit(request.unit_id)
        X = convert_data([unit], request.date)
        y = self.model.predict(X[self.features])
        X["index"] = y
        valuations = self.calculate_valuations(X[["unit_id", "year", "month", "index", "index_id"]].to_dict(orient="records"))
        return ValuationResponse(valuations=json.dumps(valuations))
