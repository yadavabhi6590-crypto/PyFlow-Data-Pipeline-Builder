

from pyflow.utils import flatten_json,flatten_json_records


if __name__=="__main__":
    print("___JSON Flattening Test")

    #one Sample nested JSON object

    sample_trip_json={
        "trip_id":101,
        "vendor":{
            "id":1,
            "name":"Creative Mobile Test"
        },
        "Location":{
            "pickup":{
                "latitude":40.7128,
                "longitude":-74.0060
            },
            "dropoff":{
                "latitude":40.7589,
                "longitude":-73.9851
            }
        },
        "fare":{
            "amount":15.50,
            "currency":"USD"
        }
    }

    flat_result=flatten_json(sample_trip_json)

    print("\n[Success] Flattened JSON output:")
    for key, value in flat_result.items():
        print(f"->{key}:{value}")