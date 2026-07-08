import requests

TOKEN = "f22be4422dd84d4fad61a9a37dfb9f96"

HEADERS = {
    "X-Token": TOKEN
}

URL = "https://fiberdigital.smartolt.com/api/onu/get_onus_statuses"


def obtener_onus():

    try:

        response = requests.get(
            URL,
            headers=HEADERS,
            timeout=30
        )

        print("STATUS:", response.status_code)

        if response.status_code == 200:

            data = response.json()

            return data.get("response", [])

    except Exception as e:

        print("ERROR:", e)

    return []