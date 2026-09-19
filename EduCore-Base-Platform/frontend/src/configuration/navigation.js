import { 
  LayoutDashboard, 
  Users, 
  Building2, 
  GraduationCap, 
  CalendarCheck, 
  FileEdit,
  BookOpen,
  CreditCard,
  Settings,
  Grid
} from 'lucide-react';

export const navigationItems = [
  {
    label: "Dashboard",
    route: "/",
    icon: LayoutDashboard,
    alwaysVisible: true
  },
  {
    label: "People",
    route: "/people",
    icon: Users,
    module: "people"
  },
  {
    label: "Organization",
    route: "/organization",
    icon: Building2,
    module: "organization"
  },
  {
    label: "Academics",
    route: "/academics",
    icon: GraduationCap,
    module: "academics"
  },
  {
    label: "Attendance",
    route: "/attendance",
    icon: CalendarCheck,
    module: "attendance"
  },
  {
    label: "Assessments",
    route: "/assessments",
    icon: FileEdit,
    module: "assessments"
  },
  {
    label: "LMS",
    route: "/lms",
    icon: BookOpen,
    module: "lms"
  },
  {
    label: "Finance",
    route: "/finance",
    icon: CreditCard,
    module: "finance"
  },
  {
    label: "Modules",
    route: "/modules",
    icon: Grid,
    alwaysVisible: true
  },
  {
    label: "Settings",
    route: "/settings",
    icon: Settings,
    alwaysVisible: true
  }
];

export const getEnabledNavigation = (modules = []) => {
  return navigationItems.filter(item => {
    if (item.alwaysVisible) return true;
    if (item.module && modules.some(m => m.key === item.module)) return true;
    return false;
  });
};
