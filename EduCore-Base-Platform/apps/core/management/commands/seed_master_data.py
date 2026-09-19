import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from decimal import Decimal

# Import all models
from apps.accounts.models import User, Role
from apps.organizations.models import Organization, OrganizationType, Campus, Department
from apps.people.models import Person, StudentProfile, InstructorProfile, GuardianProfile, StaffProfile
from apps.academics.models import AcademicSession, Program, AcademicTerm, Subject, SubjectOffering
from apps.enrollment.models import Enrollment
from apps.operations.models import Timetable, ClassSchedule, AttendanceRecord
from apps.finance.models import FeeStructure, Invoice, Payment
from apps.assessment.models import AssessmentType, Assessment, Result

class Command(BaseCommand):
    help = 'Seeds the database with a complete, realistic Indian education dataset'

    def handle(self, *args, **options):
        self.stdout.write("Starting Master Seed Process...")

        # 1. Clear existing data safely
        self.stdout.write("Clearing existing data...")
        Payment.objects.all().delete()
        Invoice.objects.all().delete()
        FeeStructure.objects.all().delete()
        Result.objects.all().delete()
        Assessment.objects.all().delete()
        AssessmentType.objects.all().delete()
        AttendanceRecord.objects.all().delete()
        ClassSchedule.objects.all().delete()
        Timetable.objects.all().delete()
        Enrollment.objects.all().delete()
        SubjectOffering.objects.all().delete()
        Subject.objects.all().delete()
        AcademicTerm.objects.all().delete()
        Program.objects.all().delete()
        AcademicSession.objects.all().delete()
        StudentProfile.objects.all().delete()
        InstructorProfile.objects.all().delete()
        GuardianProfile.objects.all().delete()
        StaffProfile.objects.all().delete()
        Person.objects.all().delete()
        Department.objects.all().delete()
        Campus.objects.all().delete()
        Organization.objects.all().delete()
        OrganizationType.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # 2. Roles & Users
        self.stdout.write("Creating Roles...")
        roles = {
            'Admin': Role.objects.get_or_create(name='Admin', defaults={'description': 'System Administrator'})[0],
            'Instructor': Role.objects.get_or_create(name='Instructor', defaults={'description': 'Faculty Member'})[0],
            'Student': Role.objects.get_or_create(name='Student', defaults={'description': 'Learner'})[0],
            'Parent': Role.objects.get_or_create(name='Parent', defaults={'description': 'Guardian'})[0],
            'Accountant': Role.objects.get_or_create(name='Accountant', defaults={'description': 'Finance Staff'})[0],
        }

        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@educore.com',
                'first_name': 'Super',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
                'password': make_password('admin')
            }
        )
        if not created:
            admin_user.set_password('admin')
        admin_user.role = roles['Admin']
        admin_user.save()

        # 3. Organization Structure
        self.stdout.write("Creating Organization Structure...")
        org_type = OrganizationType.objects.create(name='University', description='Higher Education')
        org = Organization.objects.create(
            name='EduCore Institute of Technology',
            organization_type=org_type,
            email='contact@educore.edu.in',
            phone='+91 9876543210',
            currency='INR'
        )
        
        main_campus = Campus.objects.create(organization=org, name='Main Campus', address='Bangalore, Karnataka')
        city_campus = Campus.objects.create(organization=org, name='City Campus', address='Pune, Maharashtra')

        dept_cs = Department.objects.create(organization=org, name='Computer Science')
        dept_it = Department.objects.create(organization=org, name='Information Technology')
        dept_mgmt = Department.objects.create(organization=org, name='Management')

        # 4. Academics
        self.stdout.write("Creating Academics...")
        session_25 = AcademicSession.objects.create(organization=org, name='2025-2026', start_date='2025-06-01', end_date='2026-05-31')
        session_26 = AcademicSession.objects.create(organization=org, name='2026-2027', start_date='2026-06-01', end_date='2027-05-31', is_current=True)

        prog_btech_cs = Program.objects.create(organization=org, name='B.Tech Computer Science', program_type='Undergraduate')
        prog_btech_it = Program.objects.create(organization=org, name='B.Tech Information Technology', program_type='Undergraduate')
        prog_bca = Program.objects.create(organization=org, name='BCA', program_type='Undergraduate')
        
        term_fall = AcademicTerm.objects.create(program=prog_btech_cs, name='Fall Semester 2026', start_date='2026-08-01', end_date='2026-12-15')
        term_fall_it = AcademicTerm.objects.create(program=prog_btech_it, name='Fall Semester 2026', start_date='2026-08-01', end_date='2026-12-15')
        term_fall_bca = AcademicTerm.objects.create(program=prog_bca, name='Fall Semester 2026', start_date='2026-08-01', end_date='2026-12-15')

        subjects_data = [
            ('Data Structures', 'CS201', 4.0),
            ('Machine Learning', 'CS401', 3.0),
            ('Database Management', 'IT201', 4.0),
            ('Web Development', 'IT301', 3.0),
            ('Programming in C++', 'BCA102', 3.0),
        ]
        
        subjects = []
        for name, code, credits in subjects_data:
            subjects.append(Subject.objects.create(name=name, code=code, credits=Decimal(str(credits))))

        # 5. People
        self.stdout.write("Creating People...")
        instructor_names = ['Rahul Sharma', 'Priya Desai', 'Vikram Singh', 'Anjali Gupta']
        instructors = []
        for i, name in enumerate(instructor_names):
            first, last = name.split()
            user = User.objects.create_user(username=f'inst{i}', email=f'inst{i}@educore.com', password='password123', first_name=first, last_name=last)
            user.role = roles['Instructor']
            user.save()
            person = Person.objects.create(user=user, first_name=first, last_name=last, email=user.email, phone=f'+91 99000000{i:02d}')
            profile = InstructorProfile.objects.create(person=person, organization=org, department=dept_cs, employee_id=f'EMP100{i}')
            instructors.append(profile)

        offerings = []
        for i, subj in enumerate(subjects):
            prog = prog_btech_cs if i < 2 else (prog_btech_it if i < 4 else prog_bca)
            offering = SubjectOffering.objects.create(subject=subj, program=prog, academic_session=session_26, instructor=instructors[i % len(instructors)])
            offerings.append(offering)

        parent_names = ['Amit Patel', 'Sunita Kumar', 'Rajesh Verma']
        parents = []
        for i, name in enumerate(parent_names):
            first, last = name.split()
            user = User.objects.create_user(username=f'parent{i}', email=f'parent{i}@educore.com', password='password123', first_name=first, last_name=last)
            user.role = roles['Parent']
            user.save()
            person = Person.objects.create(user=user, first_name=first, last_name=last, email=user.email, phone=f'+91 98000000{i:02d}')
            profile = GuardianProfile.objects.create(person=person, relationship='Parent')
            parents.append(profile)

        # Accountant / Finance Staff
        accountant_user = User.objects.create_user(
            username='accountant',
            email='accountant@educore.com',
            password='password123',
            first_name='Ramesh',
            last_name='Gupta'
        )
        accountant_user.role = roles['Accountant']
        accountant_user.save()
        accountant_person = Person.objects.create(
            user=accountant_user,
            first_name='Ramesh',
            last_name='Gupta',
            email=accountant_user.email,
            phone='+91 9600000001'
        )
        StaffProfile.objects.create(
            person=accountant_person,
            organization=org,
            employee_id='STAFF-FIN-01',
            designation='Chief Accountant',
            department=dept_mgmt
        )

        student_names = [
            'Aarav Sharma', 'Neha Singh', 'Karan Gupta', 'Rohan Mehta', 'Sneha Patel', 
            'Aditya Verma', 'Isha Kumar', 'Arjun Reddy', 'Kavya Nair', 'Siddharth Iyer',
            'Riya Joshi', 'Kabir Das', 'Meera Rao', 'Aryan Menon', 'Ananya Pillai',
            'Dev Chauhan', 'Tara Bhatia', 'Yash Ahuja', 'Diya Saxena', 'Rishi Mathur'
        ]
        
        students = []
        for i, name in enumerate(student_names):
            first, last = name.split()
            user = User.objects.create_user(username=f'stu{i}', email=f'stu{i}@educore.com', password='password123', first_name=first, last_name=last)
            user.role = roles['Student']
            user.save()
            person = Person.objects.create(user=user, first_name=first, last_name=last, email=user.email, phone=f'+91 97000000{i:02d}')
            profile = StudentProfile.objects.create(person=person, organization=org, student_id=f'STU-2026-10{i:02d}')
            
            # Assign parent (link GuardianProfile to StudentProfile via M2M)
            parent_profile = parents[i % len(parents)]
            parent_profile.students.add(profile)
            
            students.append(profile)

        # 6. Enrollments
        self.stdout.write("Creating Enrollments & Fees...")
        fee_btech = FeeStructure.objects.create(name='B.Tech Annual Tuition', amount=Decimal('150000.00'))
        fee_bca = FeeStructure.objects.create(name='BCA Annual Tuition', amount=Decimal('85000.00'))

        for i, student_profile in enumerate(students):
            prog = prog_btech_cs if i < 8 else (prog_btech_it if i < 15 else prog_bca)
            fee = fee_btech if prog in [prog_btech_cs, prog_btech_it] else fee_bca
            term = term_fall if prog == prog_btech_cs else (term_fall_it if prog == prog_btech_it else term_fall_bca)
            
            enrollment = Enrollment.objects.create(
                person=student_profile.person,
                organization=org,
                program=prog,
                academic_session=session_26,
                status='Active'
            )

            inv = Invoice.objects.create(
                person=student_profile.person,
                enrollment=enrollment,
                fee_structure=fee,
                amount_due=fee.amount,
                amount_paid=fee.amount if i % 3 == 0 else (fee.amount / 2 if i % 2 == 0 else Decimal('0.00')),
                due_date=(timezone.now() + timedelta(days=30)).date(),
                status='Paid' if i % 3 == 0 else ('Partial' if i % 2 == 0 else 'Pending')
            )
            
            if inv.amount_paid > 0:
                Payment.objects.create(
                    invoice=inv,
                    amount=inv.amount_paid,
                    method='Online',
                    reference_number=f'TXN{i}987654'
                )

        # 7. Timetable & Schedule
        self.stdout.write("Creating Timetables & Schedules...")
        tt = Timetable.objects.create(name='Fall 2026 CS Timetable', organization=org, program=prog_btech_cs, term=term_fall)
        schedules = []
        for i, offering in enumerate([o for o in offerings if o.program == prog_btech_cs]):
            schedules.append(ClassSchedule.objects.create(
                timetable=tt,
                subject_offering=offering,
                day_of_week=i,
                start_time='09:00:00',
                end_time='10:30:00',
                room=f'Lab {i+1}'
            ))

        # 8. Attendance (last 10 days)
        self.stdout.write("Generating Attendance...")
        cs_students = [s.person for s in students if s.person.enrollments.first().program == prog_btech_cs]
        today = timezone.now().date()
        
        for schedule in schedules:
            for day_offset in range(10):
                date = today - timedelta(days=day_offset)
                if date.weekday() == schedule.day_of_week:
                    for student in cs_students:
                        status = random.choices(['Present', 'Absent', 'Late'], weights=[85, 10, 5])[0]
                        AttendanceRecord.objects.create(
                            class_schedule=schedule,
                            date=date,
                            person=student,
                            status=status
                        )

        # 9. Assessments & Results
        self.stdout.write("Generating Assessments & Results...")
        atype = AssessmentType.objects.create(name='Mid Term Exam')
        
        for offering in [o for o in offerings if o.program == prog_btech_cs]:
            assessment = Assessment.objects.create(
                subject_offering=offering,
                assessment_type=atype,
                name=f'{offering.subject.name} Mid Term',
                date=today - timedelta(days=5),
                max_marks=100.00,
                passing_marks=40.00
            )
            
            for student in cs_students:
                marks = Decimal(random.uniform(45.0, 98.0)).quantize(Decimal('0.00'))
                Result.objects.create(
                    assessment=assessment,
                    person=student,
                    marks_obtained=marks,
                    remarks='Good performance' if marks > 75 else 'Needs improvement'
                )

        self.stdout.write(self.style.SUCCESS("Master Seed Process Complete!"))
