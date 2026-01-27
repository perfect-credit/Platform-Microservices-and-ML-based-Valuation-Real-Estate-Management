from collection import download_data, process_data
from push import client, push_building_data, push_floor_data, push_property_data, push_owner_data, push_unit_data, prepare_valuation_data


def run():
    download_data()
    process_data()
    push_owner_data()
    push_floor_data()
    push_building_data()
    push_unit_data()
    push_property_data()
    prepare_valuation_data()
    client.close()


if __name__ == "__main__":
    run()
