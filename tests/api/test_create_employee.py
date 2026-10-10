from datetime import date
from uuid import uuid4


def test_create_employee(api):
    unique_id = uuid4().hex
    employee_data = {
        "first_name": "API",
        "last_name": unique_id,
        "email": f"api.employee.{unique_id}@example.com",
        "department": "qa",
        "title": "QA Engineer",
        "hire_date": date.today().isoformat(),
    }

    create_response = api.post("/employees", json=employee_data)
    assert create_response.status_code == 201, create_response.text

    created_employee = create_response.json()
    assert created_employee["first_name"] == employee_data["first_name"]
    assert created_employee["last_name"] == employee_data["last_name"]
    assert created_employee["email"] == employee_data["email"]
    assert created_employee["department"] == employee_data["department"]
    assert created_employee["title"] == employee_data["title"]

    get_response = api.get(f"/employees/{created_employee['id']}")
    assert get_response.status_code == 200, get_response.text
    assert get_response.json()["email"] == employee_data["email"]