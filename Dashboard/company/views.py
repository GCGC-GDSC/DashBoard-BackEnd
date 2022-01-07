from rest_framework import generics, status, views, response
from django.db.models import Q, Count, Max
from .serializers import (CompanySeralizer, CoursesSeralizer,
                          CompanyCousesPlacedSeralizer,
                          InstituteLevelSeralizer)
from .models import (Company, Courses, CompanyCousesPlaced)
from students.models import (Institute, Campus)
from django.db.models import Q


class CompanyList(generics.ListAPIView):
    serializer_class = CompanySeralizer

    def get(self, request):
        send_data = []
        qs = Company.objects.all()
        send_data = CompanySeralizer(qs, many=True).data
        return response.Response({'status': 'OK', 'result': send_data})


class InstituteLevel(generics.ListAPIView):
    serializer_class = InstituteLevelSeralizer

    def get(self, request):
        send_data = {}
        cmps = Campus.objects.all()

        for cmp in cmps:
            send_data[cmp.name] = {}
            insts = Institute.objects.filter(under_campus=cmp)
            for inst in insts:
                send_data[cmp.name][inst.name] = []
                q = CompanyCousesPlaced.objects.filter(
                    course__in=Courses.objects.filter(
                        Q(campus=cmp) & Q(institute=inst)))
                qs = Company.objects.filter(id__in=q)
                send_data[cmp.name][inst.name].append(
                    CompanySeralizer(qs, many=True).data)

        return response.Response({'status': 'OK', 'result': send_data})


# class CoursesList(generics.ListAPIView):
#     serializer_class = CompanySeralizer

#     def get(self,request):
#         send_data = []
#         qs = Courses.objects.all()
#         send_data = CoursesSeralizer(qs,many=True).data
#         return response.Response({'status': 'OK', 'result': send_data})

# class CompanyCoursesPlasedList(generics.ListAPIView):
#     serializer_class = CompanyCousesPlacedSeralizer

#     def get(self,request):
#         send_data = []
#         qs = CompanyCousesPlaced.objects.all()
#         send_data = CompanySeralizer(qs,many=True).data
#         return response.Response({'status': 'OK', 'result': send_data})
