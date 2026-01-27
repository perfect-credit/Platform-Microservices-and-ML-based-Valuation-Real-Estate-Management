from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class PointGeometry(BaseModel):
    type: str = "Point"
    coordinates: list[float] = Field(default_factory=list)


class Owner(BaseModel):
    property_id: int
    property_id_nma: str
    name: str
    full_address: str
    phone_number: str | None
    geometry: PointGeometry


class Floor(BaseModel):
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


class Building(BaseModel):
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
    floor_data: list[Floor] = Field(default_factory=list)

    @model_validator(mode="after")
    def process(self):
        if not self.floor_data:
            self.floor_data = None
        return self


class Unit(BaseModel):
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


class Property(BaseModel):
    property_id: int
    property_id_nma: str
    established_date: datetime | str | None
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

    @model_validator(mode="after")
    def process(self):
        if isinstance(self.established_date, datetime):
            self.established_date = self.established_date.isoformat()
        return self


class PropertyDetail(Property):
    buildings: list[Building] | None = Field(default_factory=list)
    owners: list[Owner] | None = Field(default_factory=list)
    units: list[Unit] | None = Field(default_factory=list)

    @model_validator(mode="after")
    def process(self):
        if not self.buildings:
            self.buildings = None
        if not self.owners:
            self.owners = None
        if not self.units:
            self.units = None
        return self


class Ad(BaseModel):
    id: str
    title: str
    description: str
    address: str
    property_id_nma: str
    price: float
    type: str
    status: str
    phone_number: str
    listed_by: str

    @model_validator(mode="before")
    @classmethod
    def fix_id(cls, values):
        values["id"] = str(values["id"])
        return values


class Valuation(BaseModel):
    unit_id: int
    date: str
    rental_valuation: float | None
    rental_model_valuation: float | None
    index_valuation: float | None
    comparables_valuation: float | None
    listing_valuation: float | None
    transaction_valuation: float | None
