from django.core.management.base import BaseCommand
import random
from datetime import datetime, timedelta
from apps.organizations.models import Organization
from apps.people.models import Person, StudentProfile

class Command(BaseCommand):
    help = 'Seeds the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")
        
        org, created = Organization.objects.get_or_create(
            name="EduCore Demo Institute",
            defaults={"email": "info@educoredemo.com", "currency": "USD"}
        )
        
        first_names = ["Aarav", "Priya", "Rahul", "Neha", "Vikram", "Anjali", "Rohan", "Meera", "Karan", "Sita"]
        last_names = ["Sharma", "Patel", "Desai", "Gupta", "Singh", "Reddy", "Verma", "Kumar", "Iyer", "Nair"]
        
        existing = StudentProfile.objects.count()
        count_to_create = 50 - existing
        
        if count_to_create > 0:
            self.stdout.write(f"Creating {count_to_create} mock learners...")
            for i in range(count_to_create):
                fname = random.choice(first_names)
                lname = random.choice(last_names)
                
                person = Person.objects.create(
                    first_name=fname,
                    last_name=lname,
                    email=f"{fname.lower()}.{lname.lower()}{i+existing}@example.com",
                    gender=random.choice(['M', 'F']),
                )
                
                StudentProfile.objects.create(
                    person=person,
                    organization=org,
                    student_id=f"LRN26-{1000 + i + existing}",
                    status=random.choice(['active', 'active', 'active', 'inactive', 'pending']),
                    admission_date=datetime.now() - timedelta(days=random.randint(10, 365))
                )
                
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
