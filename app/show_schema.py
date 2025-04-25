import json
from sqlmodel import SQLModel
from app.models.models import Client, HealthProgram, Enrollment

def print_model_schemas():
    print(" Client Table Schema:")
    print(json.dumps(Client.model_json_schema(), indent=2))

    print("\n Program Table Schema:")
    print(json.dumps(HealthProgram.model_json_schema(), indent=2))

    print("\n Enrollment Table Schema:")
    print(json.dumps(Enrollment.model_json_schema(), indent=2))

if __name__ == "__main__":
    print_model_schemas()