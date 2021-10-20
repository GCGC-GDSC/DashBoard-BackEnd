from .serializers import GitSerializer, GisSerializer
from .models import Git, Gis
from rest_framework import viewsets

# Create your views here.
class GitViewSet(viewsets.ModelViewSet):
    queryset = Git.objects.all().order_by('id')
    serializer_class = GitSerializer

class GisViewset(viewsets.ModelViewSet):
    queryset = Gis.objects.all().order_by('id')
    serializer_class = GisSerializer