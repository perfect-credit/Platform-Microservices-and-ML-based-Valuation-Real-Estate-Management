from datetime import datetime, timezone

from beanie import Document, Link
from pydantic import BaseModel, Field


class Base(Document):
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
    phone_number: str | None
    geometry: PointGeometry

    class Settings:
        name = "owners"


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
    floor_code_name: str | None
    floor_code_value: str

    class Settings:
        name = "floors"


class Building(Base):
    property_id: int
    property_id_nma: str
    building_id: int
    building_number: str
    address: str | None
    has_sefrak_artifact: bool
    has_cultural_artifact: bool
    has_elevator: bool
    units_home: int
    built_area: float
    gba_total: float
    ufs_total: float
    building_status_code_name: str
    industry_group_code_name: str | None
    industry_group_code_value: str | None
    building_type_code_name: str | None
    building_type_code_value: float | None
    building_change_code_name: str | None
    energy_grade: str | None
    heating_grade: str | None
    floors: int | None
    serial_number: int
    city_name: str
    cultural_artifact_id: int | None
    locality_number: int | None
    cultural_monument_number: str | None
    geometry: PointGeometry
    floor_data: list[Link[Floor]] = Field(default_factory=list)

    class Settings:
        name = "buildings"


class Unit(Base):
    unit_id: int
    property_id_nma: str
    property_id_nma_main: str | None
    address: str | None
    full_address: str | None
    postal_code: int | None
    index_id: int | None
    unit_type: str | None
    building_type_name_aggregated: str | None
    floor_number: int | None
    floors: int | None
    land_area: float
    bta: float | None
    bra: float
    prom: float | None
    rooms: int
    bedrooms: int | None
    bathrooms: int
    built_year: int | None
    energy_label: str | None
    rental_valuation: float | None
    rental_model_valuation: float | None
    bar: float | None
    index_valuation: float | None
    comparables_valuation: float | None
    listing_valuation: float | None
    transaction_valuation: float | None
    building_id: int
    property_id: int
    apartment_number: str | None
    floor_code_value: str
    wcs: int
    building_enr: float | None
    city_name: str
    building_number: int | None
    ownership_form: str
    bra_i: float | None
    bra_e: float | None
    bra_b: float | None
    tba_area: float | None
    comparable_price_per_sqm: float | None
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

    class Settings:
        name = "units"


class Property(Base):
    property_id: int
    property_id_nma: str
    established_date: datetime | None
    number_of_buildings: int
    number_of_addresses: int
    number_of_sections: int
    number_of_leases: int
    number_of_owners: int
    number_of_plots: int
    parking_garage: bool
    area: float
    postal_number: int | None
    postal_location: str | None
    city_name: str
    city_district_id: int | None
    city_district_name: str | None
    geometry: PointGeometry
    buildings: list[Link[Building]] = Field(default_factory=list)
    owners: list[Link[Owner]] = Field(default_factory=list)
    units: list[Link[Unit]] = Field(default_factory=list)

    class Settings:
        name = "properties"


class Ad(Base):
    title: str
    description: str
    address: str
    property_id_nma: str
    price: float
    type: str
    status: str
    phone_number: str
    listed_by: str

    class Settings:
        name = "ads"


class Valuation(Base):
    unit_id: int
    date: str
    rental_valuation: float | None
    rental_model_valuation: float | None
    index_valuation: float | None
    comparables_valuation: float | None
    listing_valuation: float | None
    transaction_valuation: float | None

    class Settings:
        name = "valuations"
