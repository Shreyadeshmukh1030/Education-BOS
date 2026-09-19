import os
import django
from django.core.management.base import BaseCommand
from apps.core.models import ModuleDefinition, OrganizationModule
from apps.organizations.models import Organization

class Command(BaseCommand):
    help = 'Seeds initial module definitions and enables them for the default organization'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding Modules...")
        
        # Ensure we have at least one organization
        org, _ = Organization.objects.get_or_create(
            name="Default EduCore Institute"
        )
        
        modules_data = [
            {
                "key": "people",
                "name": "People Management",
                "icon": "Users",
                "category": "core",
                "is_core": True,
                "sort_order": 1,
                "enabled": True
            },
            {
                "key": "organization",
                "name": "Organization Management",
                "icon": "Building2",
                "category": "core",
                "is_core": True,
                "sort_order": 2,
                "enabled": True
            },
            {
                "key": "academics",
                "name": "Academic Structure",
                "icon": "GraduationCap",
                "category": "academic",
                "is_core": True,
                "sort_order": 3,
                "enabled": True
            },
            {
                "key": "attendance",
                "name": "Attendance Tracker",
                "icon": "CalendarCheck",
                "category": "operations",
                "is_core": False,
                "sort_order": 4,
                "enabled": True
            },
            {
                "key": "assessments",
                "name": "Assessments & Exams",
                "icon": "FileEdit",
                "category": "academic",
                "is_core": False,
                "sort_order": 5,
                "enabled": True
            },
            {
                "key": "lms",
                "name": "Learning Management System",
                "icon": "BookOpen",
                "category": "addon",
                "is_core": False,
                "sort_order": 6,
                "enabled": True
            },
            {
                "key": "finance",
                "name": "Finance & Fees",
                "icon": "CreditCard",
                "category": "commercial",
                "is_core": False,
                "sort_order": 7,
                "enabled": False # Deliberately disabled for testing as agreed
            }
        ]
        
        for data in modules_data:
            mod, created = ModuleDefinition.objects.update_or_create(
                key=data["key"],
                defaults={
                    "name": data["name"],
                    "icon": data["icon"],
                    "category": data["category"],
                    "is_core": data["is_core"],
                    "sort_order": data["sort_order"]
                }
            )
            
            # Enable for organization
            OrganizationModule.objects.update_or_create(
                organization=org,
                module=mod,
                defaults={
                    "enabled": data["enabled"]
                }
            )
            
        self.stdout.write(self.style.SUCCESS("Successfully seeded modules."))
