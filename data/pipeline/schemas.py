import random
from datetime import datetime, timezone
from typing import Union

from pydantic import BaseModel, Field, model_validator


class Base(BaseModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The date and time of the document creation",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The date and time of the document update",
    )


class PointGeometry(BaseModel):
    type: str = "Point"
    coordinates: list[float] = Field(default_factory=list)


class Owner(Base):
    property_id: int
    property_id_nma: str
    name: str
    full_address: str
    phone_number: Union[str, None]
    geometry: PointGeometry

    @model_validator(mode='before')
    @classmethod
    def validate_phone_number(cls, values):
        if "phone_number" not in values:
            values["phone_number"] = str(int(values["phone"])) if values["phone"] else None
        return values


class Floor(Base):
    building_id: int
    floor_id: int
    floor_code_id: int
    floor_number: int
    units_home: int
    ufs_home: float
    ufs_other: float
    ufs_total: float
    alternative_area: int
    alternative_area_2: int
    gba_home: float
    gba_other: float
    gba_total: float
    floor_code_name: Union[str, None]
    floor_code_value: str


class Building(Base):
    property_id: int
    property_id_nma: str
    building_id: int
    building_number: str
    address: Union[str, None]
    has_sefrak_artifact: bool
    has_cultural_artifact: bool
    has_elevator: bool
    units_home: int
    built_area: float
    gba_total: float
    ufs_total: float
    building_status_code_name: str
    industry_group_code_name: Union[str, None]
    industry_group_code_value: Union[str, None]
    building_type_code_name: Union[str, None]
    building_type_code_value: Union[float, None]
    building_change_code_name: Union[str, None]
    energy_grade: Union[str, None]
    heating_grade: Union[str, None]
    floors: Union[int, None]
    serial_number: int
    city_name: str
    cultural_artifact_id: Union[int, None]
    locality_number: Union[int, None]
    cultural_monument_number: Union[str, None]
    geometry: PointGeometry
    floor_data: list = Field(default_factory=list)


class Property(Base):
    property_id: int
    property_id_nma: str
    established_date: Union[datetime, None]
    number_of_buildings: int
    number_of_addresses: int
    number_of_sections: int
    number_of_leases: int
    number_of_owners: int
    number_of_plots: int
    parking_garage: bool
    area: float
    postal_number: Union[int, None]
    postal_location: Union[str, None]
    city_name: str
    city_district_id: Union[int, None]
    city_district_name: Union[str, None]
    geometry: PointGeometry
    buildings: list = Field(default_factory=list)
    owners: list = Field(default_factory=list)
    units: list = Field(default_factory=list)


class Unit(Base):
    unit_id: int
    property_id_nma: str
    property_id_nma_main: Union[str, None]
    address: Union[str, None]
    full_address: Union[str, None]
    postal_code: Union[int, None]
    index_id: Union[int, None]
    unit_type: Union[str, None]
    building_type_name_aggregated: Union[str, None]
    floor_number: Union[int, None]
    floors: Union[int, None]
    land_area: float
    bta: Union[float, None]
    bra: float
    prom: Union[float, None]
    rooms: int
    bedrooms: Union[int, None]
    bathrooms: int
    built_year: Union[int, None]
    energy_label: Union[str, None]
    rental_valuation: Union[float, None]
    rental_model_valuation: Union[float, None]
    bar: Union[float, None]
    index_valuation: Union[float, None]
    comparables_valuation: Union[float, None]
    listing_valuation: Union[float, None]
    transaction_valuation: Union[float, None]
    building_id: int
    property_id: int
    apartment_number: Union[str, None]
    floor_code_value: str
    wcs: int
    building_enr: Union[float, None]
    city_name: str
    building_number: Union[int, None]
    ownership_form: str
    bra_i: Union[float, None]
    bra_e: Union[float, None]
    bra_b: Union[float, None]
    tba_area: Union[float, None]
    comparable_price_per_sqm: Union[float, None]
    nearest_train_station_distance: float
    nearest_bus_station_distance: float
    nearest_ferry_terminal_distance: float
    nearest_tram_station_distance: float
    nearest_underground_station_distance: float
    nearest_gondola_lift_station_distance: float
    nearest_airport_distance: float
    nearest_kindergartens_distance: float
    nearest_elementary_middle_school_distance: float
    nearest_high_school_distance: float
    nearest_fire_station_distance: float
    in_beach_zone: bool
    distance: float
    geometry: PointGeometry

    @model_validator(mode='before')
    @classmethod
    def validate_property_id_nma_short(cls, values):
        if "property_id_nma_short" not in values:
            values["property_id_nma_main"] = "-".join(values["property_id_nma"].split("-")[:3]) + "-0-0"
        else:
            values["property_id_nma_main"] = values["property_id_nma_short"] + "-0-0"
        return values
