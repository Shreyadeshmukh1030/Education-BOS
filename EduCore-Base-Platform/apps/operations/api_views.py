from rest_framework import viewsets
from apps.core.api_views import BaseViewSet
from .models import Timetable, ClassSchedule, AttendanceRecord
from .serializers import TimetableSerializer, ClassScheduleSerializer, AttendanceRecordSerializer

class TimetableViewSet(BaseViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer


class ClassScheduleViewSet(BaseViewSet):
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer


class AttendanceRecordViewSet(BaseViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
