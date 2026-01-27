import json
from datetime import date

import grpc
from fastapi import HTTPException, status
from google.protobuf.json_format import MessageToDict

from server.config import settings
from server.pb import ads_pb2, ads_pb2_grpc, auth_pb2, auth_pb2_grpc, properties_pb2, properties_pb2_grpc, valuation_pb2, valuation_pb2_grpc
from server.schemas.requests.auth import LoginRequest, RegisterRequest
from server.schemas.requests.ads import CreateAdRequest
from server.schemas.responses.ads import Ad


class AuthClient:
    def __init__(self):
        self.channel = grpc.insecure_channel(f"{settings.AUTH_SERVICE_HOST}:{settings.AUTH_SERVICE_PORT}")
        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

    def send_otp(self, phone_number: str) -> dict:
        try:
            response = self.stub.SendOtp(auth_pb2.SendOtpRequest(phone_number=phone_number))
            return MessageToDict(response)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def register(self, payload: RegisterRequest) -> dict:
        try:
            response = self.stub.Register(auth_pb2.RegisterRequest(**payload.model_dump()))
            res = MessageToDict(response)
            if "success" in res and res["success"]:
                return res
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res["message"])
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def login(self, payload: LoginRequest) -> dict:
        try:
            response = self.stub.Login(auth_pb2.LoginRequest(**payload.model_dump()))
            res = MessageToDict(response)
            if "success" in res and res["success"]:
                return res
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res["message"])
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def validate(self, token: str) -> dict:
        try:
            response = self.stub.Validate(auth_pb2.ValidateRequest(token=token))
            return MessageToDict(response)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())


class RealestateClient:
    def __init__(self):
        self.properties_channel = grpc.insecure_channel(f"{settings.REALESTATE_SERVICE_HOST}:{settings.REALESTATE_SERVICE_PORT}")
        self.properties_stub = properties_pb2_grpc.PropertyServiceStub(self.properties_channel)

        self.ads_channel = grpc.insecure_channel(f"{settings.REALESTATE_SERVICE_HOST}:{settings.REALESTATE_SERVICE_PORT}")
        self.ads_stub = ads_pb2_grpc.AdServiceStub(self.ads_channel)

    def search_properties(self, min_area: float | None, max_area: float | None, page: int = 1) -> dict:
        try:
            payload = {"area": {"min": min_area, "max": max_area}, "page": page}
            response = self.properties_stub.SearchProperties(properties_pb2.FilterPropertyRequest(**payload))
            return json.loads(response.data)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def count_properties(self, min_area: float | None, max_area: float | None) -> dict:
        try:
            payload = {"area": {"min": min_area, "max": max_area}}
            response = self.properties_stub.CountProperties(properties_pb2.FilterPropertyRequest(**payload))
            return json.loads(response.data)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def get_property(self, property_id_nma: str) -> dict:
        try:
            payload = {"property_id_nma": property_id_nma}
            response = self.properties_stub.GetProperty(properties_pb2.SinglePropertyRequest(**payload))
            return json.loads(response.data)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def get_property_units(self, property_id_nma: str, page: int = 1) -> dict:
        try:
            payload = {"property_id_nma": property_id_nma, "page": page}
            response = self.properties_stub.GetPropertyUnits(properties_pb2.PropertyUnitsRequest(**payload))
            return json.loads(response.data)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def count_property_units(self, property_id_nma: str) -> dict:
        try:
            payload = {"property_id_nma": property_id_nma}
            response = self.properties_stub.CountPropertyUnits(properties_pb2.PropertyUnitsRequest(**payload))
            return json.loads(response.data)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def get_unit(self, unit_id: str) -> dict:
        try:
            payload = {"unit_id": unit_id}
            response = self.properties_stub.GetUnit(properties_pb2.SingleUnitRequest(**payload))
            return json.loads(response.data)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def get_owned_properties(self, owner_id: str, page: int = 1) -> dict:
        try:
            payload = {"owner_id": owner_id, "page": page}
            response = self.properties_stub.GetOwnedProperties(properties_pb2.OwnedItemsRequest(**payload))
            return json.loads(response.data)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def count_owned_properties(self, owner_id: str) -> dict:
        try:
            payload = {"owner_id": owner_id}
            response = self.properties_stub.CountOwnedProperties(properties_pb2.OwnedItemsRequest(**payload))
            return json.loads(response.data)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def get_historic_valuations(self, unit_id: int) -> dict:
        try:
            response = self.properties_stub.GetHistoricValuations(properties_pb2.SingleUnitRequest(unit_id=unit_id))
            return json.loads(response.data)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def has_write_access(self, owner_id: str, property_id_nma: str) -> bool:
        try:
            payload = {"phone_number": owner_id, "property_id_nma": property_id_nma}
            response = self.ads_stub.HasWriteAccess(ads_pb2.SingleAdRequest(**payload))
            return response
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def create_ad(self, payload: CreateAdRequest, owner_id: str) -> dict:
        try:
            response = self.ads_stub.CreateAd(ads_pb2.RealEstateAd(**payload.model_dump(), phone_number=owner_id))
            print(response)
            print(MessageToDict(response))
            return Ad.model_validate(response)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def get_ads(
        self,
        property_id_nma: str | None = None,
        type: str | None = None,
        status: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        page: int = 1,
    ) -> list[dict]:
        try:
            payload = {
                "property_id_nma": property_id_nma,
                "type": type,
                "status": status,
                "min_price": min_price,
                "max_price": max_price,
                "page": page,
            }

            response = self.ads_stub.GetAds(ads_pb2.FilterAdsRequest(**payload))
            data = []
            for ad in response.ads:
                data.append(Ad.model_validate(ad))
            return data
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def count_ads(
        self,
        property_id_nma: str | None = None,
        type: str | None = None,
        status: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> dict:
        try:
            payload = {
                "property_id_nma": property_id_nma,
                "type": type,
                "status": status,
                "min_price": min_price,
                "max_price": max_price,
            }

            response = self.ads_stub.CountAds(ads_pb2.FilterAdsRequest(**payload))
            return MessageToDict(response)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def get_ad(self, ad_id: str) -> dict:
        try:
            response = self.ads_stub.GetAd(ads_pb2.SingleAdRequest(id=ad_id))
            return Ad.model_validate(response)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def get_owned_ads(self, owner_id: str, page: int = 1) -> list[dict]:
        try:
            response = self.ads_stub.GetOwnedAds(ads_pb2.OwnedAdsRequest(phone_number=owner_id, page=page))
            data = []
            for ad in response.ads:
                data.append(Ad.model_validate(ad))
            return data
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def count_owned_ads(self, owner_id: str) -> dict:
        try:
            response = self.ads_stub.CountOwnedAds(ads_pb2.OwnedAdsRequest(phone_number=owner_id))
            return MessageToDict(response)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def update_ad(self, ad_id: str, payload: CreateAdRequest, owner_id: str, property_id_nma: str) -> dict:
        try:
            grpc_payload = {"id": ad_id, **payload.model_dump(exclude_unset=True), "phone_number": owner_id, "property_id_nma": property_id_nma}
            response = self.ads_stub.UpdateAd(ads_pb2.RealEstateAd(**grpc_payload))
            return Ad.model_validate(response)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def delete_ad(self, ad_id: str, owner_id: str, property_id_nma: str) -> dict:
        try:
            response = self.ads_stub.DeleteAd(ads_pb2.SingleAdRequest(id=ad_id, phone_number=owner_id, property_id_nma=property_id_nma))
            return MessageToDict(response)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())


class ValuationClient:
    def __init__(self):
        self.channel = grpc.insecure_channel(f"{settings.VALUATION_SERVICE_HOST}:{settings.VALUATION_SERVICE_PORT}")
        self.stub = valuation_pb2_grpc.ValuationServiceStub(self.channel)

    def get_property_valuation(self, property_id_nma: str) -> dict:
        try:
            response = self.stub.GetPropertyValuation(valuation_pb2.PropertyValuationRequest(property_id_nma=property_id_nma))
            return json.loads(response.valuations)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())

    def get_unit_valuation(self, unit_id: int, date: date | None = None) -> dict:
        try:
            date = date or date.today()
            response = self.stub.GetUnitValuation(valuation_pb2.UnitValuationRequest(unit_id=unit_id, date=date.isoformat()))
            return json.loads(response.valuations)
        except grpc.RpcError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.details())
