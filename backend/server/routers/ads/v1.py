from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query

from server.dependencies.auth import authenticate_user
from server.dependencies.grpc import RealestateClient
from server.dependencies.requests import page_number
from server.schemas.requests.ads import CreateAdRequest, UpdateAdRequest
from server.schemas.responses import CountResponse, StatusResponse
from server.schemas.responses.ads import Ad
from server.utils import get_listing_description


def router_factory() -> APIRouter:
    router = APIRouter(prefix="/v1/ads", tags=["Realestate Advertisements Management System"])

    @router.post("", response_model=Ad)
    async def create_ad(
        payload: Annotated[CreateAdRequest, Body()],
        phone_number: Annotated[str, Depends(authenticate_user)],
        client: Annotated[RealestateClient, Depends(RealestateClient)],
    ):
        res = client.create_ad(payload, phone_number)
        return res

    @router.get("", response_model=list[Ad])
    async def get_ads(
        client: Annotated[RealestateClient, Depends(RealestateClient)],
        property_id_nma: Annotated[str | None, Query()] = None,
        type: Annotated[str | None, Query()] = None,
        status: Annotated[str | None, Query()] = None,
        min_price: Annotated[float | None, Query()] = None,
        max_price: Annotated[float | None, Query()] = None,
        page: Annotated[int, Depends(page_number)] = 1,
    ):
        return client.get_ads(property_id_nma, type, status, min_price, max_price, page)

    @router.get("/has-access", response_model=StatusResponse)
    async def has_access(
        phone_number: Annotated[str, Depends(authenticate_user)],
        property_id_nma: Annotated[str, Query(...)],
        client: Annotated[RealestateClient, Depends(RealestateClient)],
    ):
        return client.has_write_access(phone_number, property_id_nma)

    @router.get("/me", response_model=list[Ad])
    async def get_my_ads(
        phone_number: Annotated[str, Depends(authenticate_user)],
        client: Annotated[RealestateClient, Depends(RealestateClient)],
        page: Annotated[int, Depends(page_number)] = 1,
    ):
        return client.get_owned_ads(phone_number, page)

    @router.get("/me/count", response_model=CountResponse)
    async def count_my_ads(
        phone_number: Annotated[str, Depends(authenticate_user)],
        client: Annotated[RealestateClient, Depends(RealestateClient)],
    ):
        return client.count_owned_ads(phone_number)

    @router.get("/count", response_model=CountResponse)
    async def count_ads(
        client: Annotated[RealestateClient, Depends(RealestateClient)],
        property_id_nma: Annotated[str | None, Query()] = None,
        type: Annotated[str | None, Query()] = None,
        status: Annotated[str | None, Query()] = None,
        min_price: Annotated[float | None, Query()] = None,
        max_price: Annotated[float | None, Query()] = None,
    ):
        return client.count_ads(property_id_nma, type, status, min_price, max_price)

    @router.get("/{ad_id}", response_model=Ad)
    async def get_ad(
        ad_id: str,
        client: Annotated[RealestateClient, Depends(RealestateClient)],
    ):
        return client.get_ad(ad_id)

    @router.patch("/{ad_id}", response_model=Ad)
    async def update_ad(
        ad_id: str,
        payload: Annotated[UpdateAdRequest, Body()],
        property_id_nma: Annotated[str, Query(...)],
        phone_number: Annotated[str, Depends(authenticate_user)],
        client: Annotated[RealestateClient, Depends(RealestateClient)],
    ):
        return client.update_ad(ad_id, payload, phone_number, property_id_nma)

    @router.delete("/{ad_id}", response_model=StatusResponse)
    async def delete_ad(
        ad_id: str,
        property_id_nma: Annotated[str, Query(...)],
        phone_number: Annotated[str, Depends(authenticate_user)],
        client: Annotated[RealestateClient, Depends(RealestateClient)],
    ):
        return client.delete_ad(ad_id, phone_number, property_id_nma)

    @router.get("/description/{property_id_nma}", dependencies=[Depends(authenticate_user)], response_model=StatusResponse)
    async def get_description(
        property_id_nma: str,
        client: Annotated[RealestateClient, Depends(RealestateClient)],
    ):
        property = client.get_property(property_id_nma)
        return get_listing_description(property)

    return router
