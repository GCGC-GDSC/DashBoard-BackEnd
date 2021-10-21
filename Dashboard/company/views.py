from .serializers import GitSerializer, GisSerializer, PharmacySerializer, Gim_MBASerializer, Gim_BBA_BCOMSerializer
from .models import Git, Gis, Pharmacy, Gim_BBA_BCOM, Gim_MBA
from rest_framework import viewsets

# Create your views here.
class GitViewSet(viewsets.ModelViewSet):
    queryset = Git.objects.all().order_by('id')
    serializer_class = GitSerializer

class GisViewset(viewsets.ModelViewSet):
    queryset = Gis.objects.all().order_by('id')
    serializer_class = GisSerializer

class PharmacyViewset(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all().order_by('id')
    serializer_class = PharmacySerializer

class Gim_BBA_BCOMViewset(viewsets.ModelViewSet):
    queryset =  Gim_BBA_BCOM.objects.all().order_by('id')
    serializer_class = Gim_BBA_BCOMSerializer

class Gim_MBAViewset(viewsets.ModelViewSet):
    queryset = Gim_MBA.objects.all().order_by('id')
    serializer_class = Gim_MBASerializer