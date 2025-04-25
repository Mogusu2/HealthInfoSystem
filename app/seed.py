from sqlmodel import Session
from app.database import engine
from app.models.models import Client, HealthProgram, Enrollment

def seed_data():
    with Session(engine) as session:
        # Sample programs
        tb = HealthProgram(name="Tuberculosis")
        malaria = HealthProgram(name="Malaria")
        hiv = HealthProgram(name="HIV/AIDS")

        # Sample clients
        alice = Client(name="Alice Njeri", age=29, gender="Female", contact="alice@gmail.com")
        bob = Client(name="Bob Otieno", age=35, gender="Male", contact="bob@gmail.com")

        # Add to DB
        session.add_all([tb, malaria, hiv, alice, bob])
        session.commit()

        # Sample enrollments
        enroll1 = Enrollment(client_id=alice.id, program_id=tb.id)
        enroll2 = Enrollment(client_id=bob.id, program_id=hiv.id)
        enroll3 = Enrollment(client_id=alice.id, program_id=malaria.id)

        session.add_all([enroll1, enroll2, enroll3])
        session.commit()

        print("Sample data seeded successfully.")

if __name__ == "__main__":
    seed_data()
