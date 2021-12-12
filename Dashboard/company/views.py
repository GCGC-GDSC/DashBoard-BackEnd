from rest_framework import generics, status, views, response
from django.db.models import Q, Count, Max
from .serializers import *
from .models import *
from students.models import Institute

class InstitueCompanyList(generics.ListAPIView):
    serializer_class = InstitueLevelSerializer

    def get(self, request, institute):
        institute_id = Institute.objects.get(name=institute)
        institue_courses = Courses.objects.filter(institue=institute_id)
        institute_placed = CompanyCousesPlaced.objects.filter(courses_id__in = institue_courses)

        companies = institute_placed.values('company_id').distinct()

        send_data = {institute:[[],[]]}
        
        for comp in companies:
            company = institute_placed.filter(company_id=comp['company_id'])
            ug_list = company.filter(courses_id__is_ug=True)
            pg_list = company.filter(courses_id__is_ug=False)
            
            dt1 = {}
            dt2 = {}

            dt1["name_of_the_company"] = company[0].company_id.name_of_the_company
            dt1["profile_offered"] = company[0].company_id.profile_offered
            dt1['package'] = company[0].company_id.package
            dt2 = dt1.copy()
            
            for i in ug_list:
                dt1[i.courses_id.course_name] = i.placed_count

            for i in pg_list:
                dt2[i.courses_id.course_name] = i.placed_count

            send_data[institute][0].append(dt1)
            send_data[institute][1].append(dt2)

        return response.Response({'status': 'OK', 'result': send_data})


# --------------------------------------------------------------------------------------
class GitPgList(generics.ListAPIView):
    serializer_class = GitPgSerializer

    def get(self, request):
        send_data = {}

        return response.Response({'status': 'OK', 'result': send_data})

class GisUgList(generics.ListAPIView):
    serializer_class = GisUgSerializer

    def get(self, request):
        send_data = {}

        return response.Response({'status': 'OK', 'result': send_data})

class GisPgList(generics.ListAPIView):
    serializer_class = GisPgSerializer

    def get(self, request):
        send_data = {}

        return response.Response({'status': 'OK', 'result': send_data})

class PharmacyList(generics.ListAPIView):
    serializer_class = PharmacySerializer

    def get(self, request):
        send_data = {}

        return response.Response({'status': 'OK', 'result': send_data})


class Gim_BBA_BCOMList(generics.ListAPIView):
    serializer_class = Gim_MBASerializer

    def get(self, request):
        send_data = {}

        return response.Response({'status': 'OK', 'result': send_data})


class Gim_MBAList(generics.ListAPIView):
    serializer_class = Gim_MBASerializer

    def get(self, request):
        send_data = {}

        return response.Response({'status': 'OK', 'result': send_data})
