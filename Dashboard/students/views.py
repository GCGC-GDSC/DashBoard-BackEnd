from rest_framework import generics, status, views, response
from django.db.models import Q, Count, Max
from .serializers import *
from .models import *

# class CampusesList(generics.ListAPIView):
# 	serializer_class = CampusSerialize
# 	def get(self,request):
# 		qs = Campus.objects.all()
# 		send_data = CampusSerialize(qs,many=True).data
# 		return response.Response({'status':'OK','result':send_data})

# class InstituteList(generics.ListAPIView):
# 	serializer_class = InstituteSerialize
# 	def get(self,request,campus):
# 		campus = self.kwargs['campus'].strip()
# 		qs = Campus.objects.get(name=campus).institute_set.all()
# 		send_data = InstituteSerialize(qs,many=True).data
# 		return response.Response({'status':'OK','result':send_data})


class GraduateList(generics.ListAPIView):
    serializer_class = GraduatesSerialize

    def get(self, request):
        send_data = {}
        cmps = Campus.objects.all()
        for cmp in cmps:
            send_data[cmp.name] = {}
            ints = Campus.objects.get(name=cmp.name).institute_set.all()
            for int in ints:
                send_data[cmp.name][int.name] = []
                ug = Graduates.objects.filter(
                    Q(under_campus=cmp) & Q(under_institute=int)
                    & Q(is_ug=True))
                ug_data = GraduatesSerialize(ug, many=True).data
                pg = Graduates.objects.filter(
                    Q(under_campus=cmp) & Q(under_institute=int)
                    & Q(is_ug=False))
                pg_data = GraduatesSerialize(pg, many=True).data
                send_data[cmp.name][int.name].append(ug_data)
                send_data[cmp.name][int.name].append(pg_data)

        return response.Response({'status': 'OK', 'result': send_data})


class GraduateRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Graduates.objects.all()
    serializer_class = GraduatesSerialize

class InstituteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Institute.objects.all()
    serializer_class = InstituteSerialize

class CampusRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campus.objects.all()
    serializer_class = CampusSerialize