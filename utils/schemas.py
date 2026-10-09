EMPLOYEE_SCHEMA = {
    "type": "object",
    "required": ["id", "first_name", "last_name",
                 "email", "department", "title"],
    "properties": {
        "id": {"type": "integer"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "title": {"type": "string"},
        "department": {"enum": [
            "engineering", "qa", "project_management", "hr",
            "devops", "business_analysis", "design", "executive",
        ]},
    },
}
