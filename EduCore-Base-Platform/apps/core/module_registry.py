MODULE_REGISTRY = {
    "accounts": {
        "name": "Accounts",
        "app": "apps.accounts",
        "icon": "users",
        "url": "accounts:index",
    },
    "organizations": {
        "name": "Organizations",
        "app": "apps.organizations",
        "icon": "office-building",
        "url": "organizations:index",
    },
    "people": {
        "name": "People",
        "app": "apps.people",
        "icon": "user-group",
        "url": "people:index",
    },
    "academics": {
        "name": "Academics",
        "app": "apps.academics",
        "icon": "academic-cap",
        "url": "academics:index",
    },
    "enrollment": {
        "name": "Enrollment",
        "app": "apps.enrollment",
        "icon": "document-check",
        "url": "enrollment:index",
    },
    "operations": {
        "name": "Operations",
        "app": "apps.operations",
        "icon": "clock",
        "url": "operations:index",
    },
    "assessment": {
        "name": "Assessment",
        "app": "apps.assessment",
        "icon": "clipboard-document-check",
        "url": "assessment:index",
    },
    "finance": {
        "name": "Finance",
        "app": "apps.finance",
        "icon": "currency-dollar",
        "url": "finance:index",
    },
    "communication": {
        "name": "Communication",
        "app": "apps.communication",
        "icon": "chat-bubble-left-right",
        "url": "communication:index",
    },
    "configuration": {
        "name": "Settings",
        "app": "apps.configuration",
        "icon": "cog-6-tooth",
        "url": "configuration:index",
    }
}

ENABLED_MODULES = [
    "accounts",
    "organizations",
    "people",
    "academics",
    "enrollment",
    "operations",
    "assessment",
    "finance",
    "communication",
    "configuration",
]

def get_enabled_modules():
    return {k: v for k, v in MODULE_REGISTRY.items() if k in ENABLED_MODULES}
