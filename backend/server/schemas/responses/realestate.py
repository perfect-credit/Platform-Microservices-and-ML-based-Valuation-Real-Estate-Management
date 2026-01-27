from datetime import datetime

from pydantic import Field, model_validator

from server.schemas import BaseResponseSchema


class PointGeometry(BaseResponseSchema):
    type: str = Field("Point", description="The type of the geometry")
    coordinates: list[float] = Field(default_factory=list, description="The coordinates of the location")


class Owner(BaseResponseSchema):
    name: str = Field(..., description="The name of the owner")
    phone_number: str | None = Field(None, description="The phone number of the owner")


class Floor(BaseResponseSchema):
    building_id: int = Field(..., description="The identification number of the building")
    floor_id: int = Field(..., description="The identification number of the floor")
    floor_code_id: int = Field(..., description="The identification number of the floor code")
    floor_number: int = Field(..., description="The number of the floor")
    units_home: int = Field(..., description="The number of home units in the floor")
    ufs_home: float = Field(..., description="The total area of the home units in the floor")
    ufs_other: float = Field(..., description="The total area of the other units in the floor")
    ufs_total: float = Field(..., description="The total area of the units in the floor")
    alternative_area: int = Field(..., description="The alternative area of the floor")
    alternative_area_2: int = Field(..., description="The secondary alternative area of the floor")
    gba_home: float = Field(..., description="The total area of the home units in the floor")
    gba_other: float = Field(..., description="The total area of the other units in the floor")
    gba_total: float = Field(..., description="The total area of the units in the floor")
    floor_code_name: str | None = Field(None, description="The name of the floor code")
    floor_code_value: str = Field(..., description="The value of the floor code")


class Building(BaseResponseSchema):
    property_id: int = Field(..., description="The identification number of the property")
    property_id_nma: str = Field(..., description="The identification number of the property in the NMA system")
    building_id: int = Field(..., description="The identification number of the building")
    building_number: str | None = Field(None, description="The number of the building")
    address: str | None = Field(None, description="The address of the building")
    has_sefrak_artifact: bool = Field(..., description="Whether the building has a SEFRAK artifact")
    has_cultural_artifact: bool = Field(..., description="Whether the building has a cultural artifact")
    has_elevator: bool = Field(..., description="Whether the building has an elevator")
    units_home: int = Field(..., description="The number of home units in the building")
    built_area: float = Field(..., description="The total area of the building")
    gba_total: float = Field(..., description="The total area of the building")
    ufs_total: float = Field(..., description="The total area of the units in the building")
    building_status_code_name: str = Field(..., description="The name of the building status code")
    industry_group_code_name: str | None = Field(None, description="The name of the industry group code")
    industry_group_code_value: str | None = Field(None, description="The value of the industry group code")
    building_type_code_name: str | None = Field(None, description="The name of the building type code")
    building_type_code_value: float | None = Field(None, description="The value of the building type code")
    building_change_code_name: str | None = Field(None, description="The name of the building change code")
    energy_grade: str | None = Field(None, description="The energy grade of the building")
    heating_grade: str | None = Field(None, description="The heating grade of the building")
    floors: int | None = Field(None, description="The number of floors in the building")
    serial_number: int | None = Field(None, description="The serial number of the building")
    city_name: str = Field(..., description="The name of the city where the building is located")
    cultural_artifact_id: int | None = Field(None, description="The identification number of the cultural artifact")
    locality_number: int | None = Field(None, description="The number of the locality")
    cultural_monument_number: str | None = Field(None, description="The number of the cultural monument")
    geometry: PointGeometry = Field(default_factory=dict, description="The geographical location of the building")
    floor_data: list[Floor] | None = Field(default=None, description="The details of the floors in the building")


class Unit(BaseResponseSchema):
    unit_id: int = Field(..., description="The identification number of the unit")
    property_id_nma: str = Field(..., description="The identification number of the property in the NMA system")
    property_id_nma_main: str | None = Field(None, description="The identification number of the main property in the NMA system")
    address: str | None = Field(None, description="The address of the unit")
    full_address: str | None = Field(None, description="The full address of the unit")
    postal_code: int | None = Field(None, description="The postal code of the unit")
    index_id: int | None = Field(None, description="The identification number of the index")
    unit_type: str | None = Field(None, description="The type of the unit")
    building_type_name_aggregated: str | None = Field(None, description="The aggregated name of the building type")
    floor_number: int | None = Field(None, description="The number of the floor where the unit is located")
    floors: int | None = Field(None, description="The number of floors in the building where the unit is located")
    land_area: float | None = Field(None, description="The area of the land where the unit is located")
    bta: float | None = Field(None, description="The total area of the unit")
    bra: float | None = Field(None, description="The total area of the unit")
    prom: float | None = Field(None, description="The total area of the unit")
    rooms: int | None = Field(None, description="The number of rooms in the unit")
    bedrooms: int | None = Field(None, description="The number of bedrooms in the unit")
    bathrooms: int | None = Field(None, description="The number of bathrooms in the unit")
    built_year: int | None = Field(None, description="The year when the unit was built")
    energy_label: str | None = Field(None, description="The energy label of the unit")
    rental_valuation: float | None = Field(None, description="The rental valuation of the unit")
    rental_model_valuation: float | None = Field(None, description="The rental model valuation of the unit")
    bar: float | None = Field(None, description="The bar of the unit")
    index_valuation: float | None = Field(None, description="The index valuation of the unit")
    comparables_valuation: float | None = Field(None, description="The comparables valuation of the unit")
    listing_valuation: float | None = Field(None, description="The listing valuation of the unit")
    transaction_valuation: float | None = Field(None, description="The transaction valuation of the unit")
    building_id: int | None = Field(None, description="The identification number of the building where the unit is located")
    property_id: int | None = Field(None, description="The identification number of the property where the unit is located")
    apartment_number: str | None = Field(None, description="The number of the apartment")
    floor_code_value: str | None = Field(None, description="The value of the floor code")
    wcs: int | None = Field(None, description="The number of water closets in the unit")
    building_enr: float | None = Field(None, description="The building enr of the unit")
    city_name: str | None = Field(None, description="The name of the city where the unit is located")
    building_number: int | None = Field(None, description="The number of the building where the unit is located")
    ownership_form: str | None = Field(None, description="The ownership form of the unit")
    bra_i: float | None = Field(None, description="The bra_i of the unit")
    bra_e: float | None = Field(None, description="The bra_e of the unit")
    bra_b: float | None = Field(None, description="The bra_b of the unit")
    tba_area: float | None = Field(None, description="The tba area of the unit")
    comparable_price_per_sqm: float | None = Field(None, description="The comparable price per square meter of the unit")
    nearest_train_station_distance: float = Field(..., description="The distance to the nearest train station")
    nearest_bus_station_distance: float = Field(..., description="The distance to the nearest bus station")
    nearest_ferry_terminal_distance: float = Field(..., description="The distance to the nearest ferry terminal")
    nearest_tram_station_distance: float = Field(..., description="The distance to the nearest tram station")
    nearest_underground_station_distance: float = Field(..., description="The distance to the nearest underground station")
    nearest_gondola_lift_station_distance: float = Field(..., description="The distance to the nearest gondola lift station")
    nearest_airport_distance: float = Field(..., description="The distance to the nearest airport")
    nearest_kindergartens_distance: float = Field(..., description="The distance to the nearest kindergartens")
    nearest_elementary_middle_school_distance: float = Field(..., description="The distance to the nearest elementary middle school")
    nearest_high_school_distance: float = Field(..., description="The distance to the nearest high school")
    nearest_fire_station_distance: float = Field(..., description="The distance to the nearest fire station")
    in_beach_zone: bool = Field(..., description="Whether the unit is in the beach zone")
    distance: float = Field(..., description="The distance to the unit")
    geometry: PointGeometry = Field(default_factory=dict, description="The geographical location of the unit")


class Property(BaseResponseSchema):
    property_id: int = Field(..., description="Registry identification number of the property")
    property_id_nma: str = Field(..., description="Registry identification number of the property in the NMA system")
    established_date: datetime | None = Field(None, description="The date when the property was established")
    number_of_buildings: int = Field(..., description="The number of buildings in the property")
    number_of_addresses: int = Field(..., description="The number of addresses in the property")
    number_of_sections: int = Field(..., description="The number of sections in the property")
    number_of_leases: int = Field(..., description="The number of leases in the property")
    number_of_owners: int = Field(..., description="The number of owners in the property")
    number_of_plots: int = Field(..., description="The number of plots in the property")
    parking_garage: bool = Field(..., description="Whether the property has a parking garage")
    area: float = Field(..., description="The area of the property in square meters")
    postal_number: int | None = Field(None, description="The postal number of the property")
    postal_location: str | None = Field(None, description="The postal location of the property")
    city_name: str = Field(..., description="The name of the city where the property is located")
    city_district_id: int | None = Field(None, description="The identification number of the city district where the property is located")
    city_district_name: str | None = Field(None, description="The name of the city district where the property is located")
    geometry: PointGeometry = Field(..., description="The geographical location of the property")
    buildings: list[Building] | None = Field(default=None, description="The details of the buildings in the property")
    owners: list[Owner] | None = Field(default=None, description="The details of the owners of the property")
    units: list[Unit] | None = Field(default=None, description="The details of the units in the property")


class Valuation(BaseResponseSchema):
    unit_id: int = Field(..., description="The identification number of the unit")
    date: str = Field(..., description="The date of the valuation")
    rental_valuation: float | None = Field(None, description="The rental valuation of the unit")
    rental_model_valuation: float | None = Field(None, description="The rental model valuation of the unit")
    index_valuation: float | None = Field(None, description="The index valuation of the unit")
    comparables_valuation: float | None = Field(None, description="The comparables valuation of the unit")
    listing_valuation: float | None = Field(None, description="The listing valuation of the unit")
    transaction_valuation: float | None = Field(None, description="The transaction valuation of the unit")

    @model_validator(mode="before")
    @classmethod
    def construct_date(cls, values):
        if "date" not in values:
            values["date"] = f"{values['year']}-{str(values['month']).zfill(2)}-01"
        return values
