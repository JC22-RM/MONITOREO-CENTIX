import requests

TOKEN = "f22be4422dd84d4fad61a9a37dfb9f96"

headers = {
    "X-Token": TOKEN
}

urls = [

    "https://fiberdigital.smartolt.com/api/onu/get_all_onus",

    "https://fiberdigital.smartolt.com/api/onu/get_onus",

    "https://fiberdigital.smartolt.com/api/onu/get_all_onus_details",

    "https://fiberdigital.smartolt.com/api/onu/list",

    "https://fiberdigital.smartolt.com/api/onu/get",

    "https://fiberdigital.smartolt.com/api/system/get_olts"

]

for url in urls:

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        print("\n--------------------------------")
        print(url)
        print("STATUS:", response.status_code)

    except Exception as e:

        print(url)
        print(e)