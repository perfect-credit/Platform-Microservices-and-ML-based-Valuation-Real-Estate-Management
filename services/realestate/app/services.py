import json

import grpc

from pb.ads_pb2 import CountResponse, MultipleAdsResponse, RealEstateAd, StatusResponse
from pb.ads_pb2_grpc import AdServiceServicer
from pb.properties_pb2 import Response
from pb.properties_pb2_grpc import PropertyServiceServicer
from repositories import (
    check_permission,
    count_properties,
    count_property_units,
    count_ads,
    create_ad,
    delete_ad,
    get_ads,
    get_historic_valuations,
    get_owned_properties,
    count_owned_properties,
    read_property_owner,
    read_property_units,
    read_single_ad,
    read_single_property,
    read_single_unit,
    search_properties,
    update_ad,
)


class PropertyService(PropertyServiceServicer):
    async def SearchProperties(self, request, context) -> Response:
        properties = await search_properties(area=request.area, page=request.page)

        data = []
        for property in properties:
            data.append(property.model_dump())

        return Response(data=json.dumps(data))

    async def CountProperties(self, request, context):
        data = await count_properties(area=request.area, page=request.page)
        return Response(data=json.dumps({"count": data}))

    async def GetProperty(self, request, context) -> Response:
        property_id_nma = request.property_id_nma
        property = await read_single_property(property_id_nma)

        if not property:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Property not found")
            return Response()

        property_data = property.model_dump_json()
        return Response(data=property_data)

    async def GetPropertyUnits(self, request, context) -> Response:
        property_id_nma = request.property_id_nma
        units = await read_property_units(property_id_nma, request.page)

        data = []
        for unit in units:
            data.append(unit.model_dump())

        return Response(data=json.dumps(data))

    async def CountPropertyUnits(self, request, context):
        data = await count_property_units(property_id_nma=request.property_id_nma, page=request.page)
        return Response(data=json.dumps({"count": data}))

    async def GetUnit(self, request, context) -> Response:
        unit_id = request.unit_id
        unit = await read_single_unit(unit_id)

        if not unit:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Unit not found")
            return Response()

        unit_data = unit.model_dump_json()
        return Response(data=unit_data)

    async def GetOwnedProperties(self, request, context) -> Response:
        owner_id = request.owner_id
        properties = await get_owned_properties(owner_id, request.page)

        data = []
        for property in properties:
            data.append(property.model_dump())

        return Response(data=json.dumps(data))

    async def CountOwnedProperties(self, request, context):
        data = await count_owned_properties(owner_id=request.owner_id)
        return Response(data=json.dumps({"count": data}))

    async def GetHistoricValuations(self, request, context) -> Response:
        unit_id = request.unit_id
        valuations = await get_historic_valuations(unit_id)

        data = []
        for valuation in valuations:
            data.append(valuation.model_dump())

        return Response(data=json.dumps(data))


class AdService(AdServiceServicer):
    async def CreateAd(self, request, context) -> RealEstateAd:
        owner = await read_property_owner(owner_id=request.phone_number, property_id_nma=request.property_id_nma)
        if not owner:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Owner does not have permission to create ad for this property")
            return RealEstateAd()

        ad = await create_ad(
            title=request.title,
            description=request.description,
            address=request.address,
            property_id_nma=request.property_id_nma,
            price=request.price,
            type=request.type,
            phone_number=owner.phone_number,
            listed_by=owner.name,
        )
        return RealEstateAd(**ad.model_dump())

    async def GetAd(self, request, context) -> RealEstateAd:
        ad_id = request.id
        ad = await read_single_ad(ad_id)

        if not ad:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Ad not found")
            return RealEstateAd()

        return RealEstateAd(**ad.model_dump())

    async def GetAds(self, request, context) -> MultipleAdsResponse:
        ads = await get_ads(
            property_id_nma=request.property_id_nma,
            type=request.type,
            status=request.status,
            min_price=request.min_price,
            max_price=request.max_price,
            page=request.page,
        )

        data = []
        for ad in ads:
            data.append(RealEstateAd(**ad.model_dump()))

        return MultipleAdsResponse(ads=data)

    async def CountAds(self, request, context) -> CountResponse:
        data = await count_ads(
            property_id_nma=request.property_id_nma,
            type=request.type,
            status=request.status,
            min_price=request.min_price,
            max_price=request.max_price,
        )
        return CountResponse(count=data)

    async def GetOwnedAds(self, request, context) -> MultipleAdsResponse:
        ads = await get_ads(phone_number=request.phone_number, page=request.page)

        data = []
        for ad in ads:
            data.append(RealEstateAd(**ad.model_dump()))

        return MultipleAdsResponse(ads=data)

    async def CountOwnedAds(self, request, context) -> CountResponse:
        data = await count_ads(phone_number=request.phone_number)
        return CountResponse(count=data)

    async def UpdateAd(self, request, context) -> RealEstateAd:
        has_permission = await check_permission(owner_id=request.phone_number, property_id_nma=request.property_id_nma)
        if not has_permission:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Owner does not have permission to update ad for this property")
            return RealEstateAd()

        updated_ad = await update_ad(
            ad_id=request.id,
            title=request.title,
            description=request.description,
            address=request.address,
            price=request.price,
            type=request.type,
            status=request.status,
        )
        return RealEstateAd(**updated_ad.model_dump())

    async def DeleteAd(self, request, context) -> StatusResponse:
        has_permission = await check_permission(owner_id=request.phone_number, property_id_nma=request.property_id_nma)
        if not has_permission:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Owner does not have permission to delete ad for this property")
            return StatusResponse(success=False)

        response = await delete_ad(ad_id=request.id)
        return StatusResponse(success=response)

    async def HasWriteAccess(self, request, context) -> StatusResponse:
        has_permission = await check_permission(owner_id=request.phone_number, property_id_nma=request.property_id_nma)
        return StatusResponse(success=has_permission)
