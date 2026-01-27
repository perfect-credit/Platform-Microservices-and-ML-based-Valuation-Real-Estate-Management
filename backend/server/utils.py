import cohere

from server.config import settings


def get_listing_description(property: dict) -> str:
    property_keys = {
        "area": "total area of placeholder m²",
        "number_of_buildings": "placeholder building?plural",
        "parking_garage": "has garage",
    }

    building_keys = {
        "has_elevator": "has elevator",
        "floors": "placeholder floor?plural",
        "energy_grade": "at energy grid 'placeholder'",
        "heating_grade": "at heating grid 'placeholder'",
        "has_sefrak_artifact": "has sefrak artifact",
        "has_cultural_artifact": "has cultural artifact",
    }

    unit_keys = {
        "address": "located at placeholder",
        "building_type_name_aggregated": "placeholder type",
        "bra": "built residential area placeholder m²",
        "rooms": "placeholder room?plural",
        "bedrooms": "placeholder bedroom?plural",
        "bathrooms": "placeholder bathroom?plural",
        "wcs": "placeholder wcs",
        "nearest_train_station_distance": "nearest - train station at placeholder km",
        "nearest_bus_station_distance": "bus station at placeholder km",
        "nearest_ferry_terminal_distance": "ferry terminal at placeholder km",
        "nearest_tram_station_distance": "tram station at placeholder km",
        "nearest_underground_station_distance": "underground station at placeholder km",
        "nearest_gondola_lift_station_distance": "gondola lift station at placeholder km",
        "nearest_airport_distance": "airport at placeholder km",
        "nearest_kindergarten_distance": "kindergartens at placeholder km",
        "nearest_elementary_middle_school_distance": "elementary/middle school at placeholder km",
        "nearest_high_school_distance": "high school at placeholder km",
        "nearest_fire_station_distance": "fire station at placeholder km",
        "in_beach_zone": "in beach zone",
    }

    data = {}

    for key, value in property_keys.items():
        if property.get(key):
            data[key] = value.replace("placeholder", str(property[key]))
            if "?plural" in value and property[key] > 1:
                data[key] = data[key].replace("?plural", "s")
            else:
                data[key] = data[key].replace("?plural", "")

    if property.get("buildings"):
        for key, value in building_keys.items():
            for building in property["buildings"]:
                if building.get(key):
                    data[key] = value.replace("placeholder", str(building[key]))
                    if "?plural" in value and building[key] > 1:
                        data[key] = data[key].replace("?plural", "s")
                    else:
                        data[key] = data[key].replace("?plural", "")
                    break

    if property.get("units"):
        for key, value in unit_keys.items():
            for unit in property["units"]:
                if unit.get(key):
                    data[key] = value.replace("placeholder", str(unit[key]))
                    if "?plural" in value and unit[key] > 1:
                        data[key] = data[key].replace("?plural", "s")
                    else:
                        data[key] = data[key].replace("?plural", "")
                    break

    prompts = ["Make an ad for this unit:"]
    key_sequence = [
        "address",
        "area",
        "number_of_buildings",
        "building_type_name_aggregated",
        "parking_garage",
        "floors",
        "has_elevator",
        "energy_grade",
        "heating_grade",
        "has_sefrak_artifact",
        "has_cultural_artifact",
        "bra",
        "rooms",
        "bedrooms",
        "bathrooms",
        "wcs",
        "nearest_train_station_distance",
        "nearest_bus_station_distance",
        "nearest_ferry_terminal_distance",
        "nearest_tram_station_distance",
        "nearest_underground_station_distance",
        "nearest_gondola_lift_station_distance",
        "nearest_airport_distance",
        "nearest_kindergarten_distance",
        "nearest_elementary_middle_school_distance",
        "nearest_high_school_distance",
        "nearest_fire_station_distance",
        "in_beach_zone",
    ]

    for key in key_sequence:
        if key in data:
            prompts.append(f"{data.get(key)},")

    prompt = " ".join(prompts)[:-1]

    client = cohere.Client(settings.GAN_API_KEY)
    response = client.generate(model="command", prompt=prompt, max_tokens=300, temperature=0.9, k=0, stop_sequences=[], return_likelihoods='NONE')
    return {"message": response.generations[0].text, "success": True}
