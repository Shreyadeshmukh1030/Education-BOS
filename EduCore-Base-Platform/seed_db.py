import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.organizations.models import Organization
from apps.people.models import Person, StudentProfile

def run():
    print("Seeding database...")
    
    # 1. Ensure an Organization exists
    org, created = Organization.objects.get_or_create(
        name="EduCore Demo Institute",
        defaults={
            "type": "School",
            "code": "EDI-001"
        }
    )
    
    # 2. Seed 25 Learners
    first_names = ["Aarav", "Priya", "Rahul", "Neha", "Vikram", "Anjali", "Rohan", "Meera", "Karan", "Sita"]
    last_names = ["Sharma", "Patel", "Desai", "Gupta", "Singh", "Reddy", "Verma", "Kumar", "Iyer", "Nair"]
    
    existing_students = StudentProfile.objects.count()
    if existing_students < 25:
        print(f"Creating {25 - existing_students} mock learners...")
        for i in range(existing_students, 25):
            fname = random.choice(first_names)
            lname = random.choice(last_names)
            
            person = Person.objects.create(
                first_name=fname,
                last_name=lname,
                email=f"{fname.lower()}.{lname.lower()}{i}@example.com",
                gender=random.choice(['M', 'F']),
            )
            
            StudentProfile.objects.create(
                person=person,
                organization=org,
                student_id=f"LRN26-{1000 + i}",
                status=random.choice(['active', 'active', 'active', 'inactive', 'pending']),
                admission_date=datetime.now() - timedelta(days=random.randint(10, 365))
            )
            
    print("Database seeded successfully!")

if __name__ == '__main__':
    run()
