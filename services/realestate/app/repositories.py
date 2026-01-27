from beanie.operators import In

import schemas
from models import Ad, Owner, Property, Unit, Valuation
from pb.properties_pb2 import RangeQuery


async def read_single_property(property_id_nma: str) -> schemas.PropertyDetail:
    property = await Property.find(Property.property_id_nma == property_id_nma, fetch_links=True).project(schemas.PropertyDetail).first_or_none()
    return property


async def search_properties(area: RangeQuery, page: int) -> list[schemas.Property]:
    match_query = {"geometry.coordinates.0": {"$gte": 10.65, "$lte": 10.85}, "geometry.coordinates.1": {"$gte": 59.95, "$lte": 59.97}}

    if area.min or area.max:
        match_query["area"] = {}
        if area.min:
            match_query["area"]["$gte"] = area.min
        if area.max:
            match_query["area"]["$lte"] = area.max

    properties = await Property.find(match_query).project(schemas.Property).skip((page - 1) * 20).limit(20).to_list()
    return properties


async def count_properties(area: RangeQuery, page: int) -> int:
    match_query = {"geometry.coordinates.0": {"$gte": 10.65, "$lte": 10.85}, "geometry.coordinates.1": {"$gte": 59.95, "$lte": 59.97}}

    if area.min or area.max:
        match_query["area"] = {}
        if area.min:
            match_query["area"]["$gte"] = area.min
        if area.max:
            match_query["area"]["$lte"] = area.max

    properties = await Property.find(match_query).count()
    return properties


async def read_single_unit(unit_id: int) -> schemas.Unit:
    unit = await Unit.find(Unit.unit_id == unit_id).project(schemas.Unit).first_or_none()
    return unit


async def read_property_units(property_id_nma: str, page: int | None = None) -> list[schemas.Unit]:
    query = {
        "geometry.coordinates.0": {"$gte": 10.65, "$lte": 10.85},
        "geometry.coordinates.1": {"$gte": 59.95, "$lte": 59.97},
    }

    if page:
        query["property_id_nma"] = property_id_nma
        return await Unit.find(query).project(schemas.Unit).skip((page - 1) * 20).limit(20).to_list()
    else:
        query["property_id_nma_main"] = property_id_nma
        return await Unit.find(query).project(schemas.Unit).to_list()


async def count_property_units(property_id_nma: str, page: int | None = None) -> int:
    query = {
        "geometry.coordinates.0": {"$gte": 10.65, "$lte": 10.85},
        "geometry.coordinates.1": {"$gte": 59.95, "$lte": 59.97},
    }

    if page:
        query["property_id_nma"] = property_id_nma
        return await Unit.find(query).count()
    else:
        query["property_id_nma_main"] = property_id_nma
        return await Unit.find(query).count()


async def get_owned_properties(owner_id: str, page: int) -> list[schemas.Property]:
    query = {
        "phone_number": owner_id,
        "geometry.coordinates.0": {"$gte": 10.65, "$lte": 10.85},
        "geometry.coordinates.1": {"$gte": 59.95, "$lte": 59.97},
    }

    owned_properties = await Owner.find(query).skip((page - 1) * 20).limit(20).to_list()
    properties = [item.property_id_nma for item in owned_properties]

    if properties:
        return await Property.find(In(Property.property_id_nma, properties)).project(schemas.Property).to_list()
    else:
        return []


async def count_owned_properties(owner_id: str) -> int:
    query = {
        "phone_number": owner_id,
        "geometry.coordinates.0": {"$gte": 10.65, "$lte": 10.85},
        "geometry.coordinates.1": {"$gte": 59.95, "$lte": 59.97},
    }
    owned_properties = await Owner.find(query).count()
    return owned_properties


async def check_permission(owner_id: str, property_id_nma: str) -> bool:
    query = {
        "phone_number": owner_id,
        "property_id_nma": property_id_nma,
    }
    return await Owner.find(query).count() > 0


async def read_property_owner(owner_id: str, property_id_nma: str) -> schemas.Owner:
    query = {
        "phone_number": owner_id,
        "property_id_nma": property_id_nma,
    }
    owner = await Owner.find(query).project(schemas.Owner).first_or_none()
    return owner


async def create_ad(
    title: str,
    description: str,
    address: str,
    price: float,
    property_id_nma: str,
    type: str,
    phone_number: str,
    listed_by: str,
) -> schemas.Ad:
    ad = Ad(
        title=title,
        description=description,
        address=address,
        price=price,
        property_id_nma=property_id_nma,
        type=type,
        phone_number=phone_number,
        listed_by=listed_by,
        status="live",
    )
    await ad.insert()
    return schemas.Ad(**ad.model_dump())


async def read_single_ad(ad_id: str) -> schemas.Ad:
    ad = await Ad.get(ad_id)
    return schemas.Ad(**ad.model_dump())


async def get_ads(
    property_id_nma: str | None = None,
    phone_number: str | None = None,
    type: str | None = None,
    status: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    page: int = 1,
) -> list[schemas.Ad]:
    query = {}

    if property_id_nma:
        query["property_id_nma"] = property_id_nma
    if phone_number:
        query["phone_number"] = phone_number
    if type:
        query["type"] = type
    if status:
        query["status"] = status

    if min_price or max_price:
        query["price"] = {}
        if min_price:
            query["price"]["$gte"] = min_price
        if max_price:
            query["price"]["$lte"] = max_price

    print(f"{query = }")
    ads = await Ad.find(query).skip((page - 1) * 20).limit(20).to_list()
    return [schemas.Ad(**ad.model_dump()) for ad in ads]


async def count_ads(
    property_id_nma: str | None = None,
    phone_number: str | None = None,
    type: str | None = None,
    status: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> list[schemas.Ad]:
    query = {}

    if property_id_nma:
        query["property_id_nma"] = property_id_nma
    if phone_number:
        query["phone_number"] = phone_number
    if type:
        query["type"] = type
    if status:
        query["status"] = status

    if min_price or max_price:
        query["price"] = {}
        if min_price:
            query["price"]["$gte"] = min_price
        if max_price:
            query["price"]["$lte"] = max_price

    print(f"{query = }")
    ads = await Ad.find(query).count()
    return ads


async def update_ad(
    ad_id: str,
    title: str | None = None,
    description: str | None = None,
    address: str | None = None,
    price: float | None = None,
    type: str | None = None,
    status: str | None = None,
) -> schemas.Ad:
    ad = await Ad.get(ad_id)

    if title:
        ad.title = title
    if description:
        ad.description = description
    if address:
        ad.address = address
    if price:
        ad.price = price
    if type:
        ad.type = type
    if status:
        ad.status = status

    await ad.save()
    return schemas.Ad(**ad.model_dump())


async def delete_ad(ad_id: str) -> bool:
    ad = await Ad.get(ad_id)
    await ad.delete()
    return True


async def get_historic_valuations(unit_id: int) -> list[schemas.Valuation]:
    valuations = await Valuation.find(Valuation.unit_id == unit_id).project(schemas.Valuation).to_list()
    return valuations
