import requests




def test_get_employees_list(api, api_employee, api_url):
    response = api.get(f"{api_url}/employees/{api_employee['id']}")
    print(f"The employee with id {response.json()['id']} is found")                   
    assert response.status_code == 200