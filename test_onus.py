import requests

TOKEN = "f22be4422dd84d4fad61a9a37dfb9f96"

headers = {
    "X-Token": TOKEN
}

url = "https://fiberdigital.smartolt.com/api/onu/get_all_onus_details"

response = requests.get(url, headers=headers)

print("STATUS:", response.status_code)
print(response.text[:5000])