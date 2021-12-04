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

    def get_queryset(self,cmp,int,is_ug):
        qs = Graduates.objects.filter(
                    Q(under_campus=cmp) & Q(under_institute=int)
                    & Q(is_ug=is_ug))
        return qs
    def get(self, request):
        send_data = {}
        cmps = Campus.objects.all()
        for cmp in cmps:
            send_data[cmp.name] = {}
            ints = Campus.objects.get(name=cmp.name).institute_set.all()
            for int in ints:
                send_data[cmp.name][int.name] = []
                ug = self.get_queryset(cmp,int,True)
                ug_data = GraduatesSerialize(ug, many=True).data
                pg = self.get_queryset(cmp,int,False)
                pg_data = GraduatesSerialize(pg, many=True).data
                send_data[cmp.name][int.name].extend([ug_data, pg_data])
        return response.Response({'status': 'OK', 'result': send_data})
