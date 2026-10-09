from datetime import date
import time

import pytest
import requests
from jsonschema import validate, ValidationError
from utils.schemas import EMPLOYEE_SCHEMA

def test_employees_need_sign_in(api_url):
    response = requests.get(f"{api_url}/employees")
    assert response.status_code == 401

def test_employees_list(api):
    response = api.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_employee(api):
    payload = {
        "first_name": "Ada",
        "last_name": "Lovelace",
        "email": f"ada.{time.time_ns()}@example.com",
        "department": "engineering",
        "title": "Test Analyst",
        "hire_date": date.today().isoformat(),
    }
    response = api.post("/employees", json=payload)
    assert response.status_code == 201
    assert response.json()["first_name"] == "Ada"

def test_employee_lifecycle(api, api_employee):
    path = f"/employees/{api_employee['id']}"
    assert api.get(path).json()["last_name"] == api_employee["last_name"]
    api.put(path, json={"title": "Senior Test Analyst"})
    assert api.get(path).json()["title"] == "Senior Test Analyst"
    assert api.delete(path).status_code == 204
    assert api.get(path).status_code == 404

def valid_employee():
    return {
        "first_name": "Alan",
        "last_name": "Turing",
        "email": f"alan.{time.time_ns()}@example.com",
        "department": "engineering",
        "title": "Test Analyst",
        "hire_date": date.today().isoformat(),
        "postcode": "2000",
    }

MISSING = object()

@pytest.mark.parametrize("field, bad_value", [
    ("title", MISSING),
    ("hire_date", "2023-01-01"),
    ("postcode", "123"),
    ("department", "Marketing"),
])
def test_server_refuses_bad_data(api, field, bad_value):
    payload = valid_employee()
    if bad_value is MISSING:
        del payload[field]
    else:
        payload[field] = bad_value
    response = api.post("/employees", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", field]

def test_duplicate_email_is_refused(api, api_employee):
    payload = {
        "first_name": "Grace",
        "last_name": "Hopper",
        "email": api_employee["email"],
        "department": "engineering",
        "title": "Test Analyst",
        "hire_date": date.today().isoformat(),
    }
    response = api.post("/employees", json=payload)
    assert response.status_code == 409

def test_employees_match_schema(api):
    employees = api.get("/employees").json()
    for employee in employees:
        validate(employee, EMPLOYEE_SCHEMA)

def test_schema_catches_a_changed_value(api):
    employee = api.get("/employees").json()[0]
    changed = {**employee, "department": "Engineering"}
    with pytest.raises(ValidationError):
        validate(changed, EMPLOYEE_SCHEMA)
