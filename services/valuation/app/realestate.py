import json

import grpc

from config import settings
from pb import properties_pb2, properties_pb2_grpc


class RealestateClient:
    def __init__(self):
        self.channel = grpc.insecure_channel(f"{settings.REALESTATE_SERVICE_HOST}:{settings.REALESTATE_SERVICE_PORT}")
        self.stub = properties_pb2_grpc.PropertyServiceStub(self.channel)

    def get_property_units(self, property_id_nma: int) -> list:
        response = self.stub.GetPropertyUnits(properties_pb2.PropertyUnitsRequest(property_id_nma=property_id_nma))
        return json.loads(response.data)

    def get_unit(self, unit_id: int) -> dict:
        response = self.stub.GetUnit(properties_pb2.SingleUnitRequest(unit_id=unit_id))
        return json.loads(response.data)
