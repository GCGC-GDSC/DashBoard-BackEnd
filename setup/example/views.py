from .serializers import CampusSerializer, InstitueSerializer, UnderGraduatesSerializer, PostGraduatesSerializer
from .models import Campus, Institue, UnderGraduates, PostGraduates
from rest_framework import viewsets

class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects.all().order_by('id')
    serializer_class = CampusSerializer

class InstitueViewSet(viewsets.ModelViewSet):
    queryset = Institue.objects.all().order_by('id')
    serializer_class = InstitueSerializer

class UnderGraduatesViewSet(viewsets.ModelViewSet):
    queryset = UnderGraduates.objects.all().order_by('id')
    serializer_class = UnderGraduatesSerializer

class PostGraduatesViewSet(viewsets.ModelViewSet):
    queryset = PostGraduates.objects.all().order_by('id')
    serializer_class = PostGraduatesSerializer