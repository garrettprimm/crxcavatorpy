import requests

BASE_URL = "https://api.crxcavator.io/v1/"


def get_all_reports(extension_id: str) -> list:
    endpoint = "report/"
    full_url = f"{BASE_URL}{endpoint}{extension_id}"
    response = requests.get(url=full_url)
    all_reports = response.json()
    return all_reports


def get_report(extension_id: str, extension_version: str) -> dict:
    endpoint = "report/"
    full_url = f"{BASE_URL}{endpoint}{extension_id}/{extension_version}"
    response = requests.get(url=full_url)
    report = response.json()
    return report


def submit_extension(extension_id: str) -> dict:
    endpoint = "submit/"
    full_url = f"{BASE_URL}{endpoint}"
    data = {"extension_id": extension_id}
    try:
        response = requests.post(url=full_url, json=data)
        submission_status = response.json()
        return submission_status
    except requests.exceptions.HTTPError as err:
        raise err
