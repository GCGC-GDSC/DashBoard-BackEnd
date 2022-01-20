from rest_framework import generics, status, views, response
from organization.models import Institute, Campus, Stream
from django.db.models import Q, Count, Max
from organization.serializers import CampusSerialize, InstituteSerialize
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from django.contrib import messages
from django.http import HttpResponse
from .serializers import *
from .models import *


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


# --
#
# {  }
#
# --


class InstituteGradList(generics.ListAPIView):
    serializer_class = InstituteGradListSeralizer

    def get(self, request, institute):
        inst = Institute.objects.get(name=institute)
        grds = Graduates.objects.filter(under_institute=inst)
        send_data = InstituteGradListSeralizer(grds, many=True).data

        # [
        #     # students detalis[student_details,placement_details,salary] ,
        #     #
        #     # ug details[student_details,placement_details,salary] ,
        #     #
        #     # pg details[student_details,placement_details,salary]
        # ]
        return response.Response({'status': 'OK', 'result': send_data})


class Overall(generics.ListAPIView):
    serializer_class = GraduatesSerialize

    def get(self, request, stream):
        send_data = {}
        stream_data = Stream.objects.filter(name=stream)
        inst_data = Institute.objects.filter(stream=stream_data[0].id)
        for inst in inst_data:
            send_data[inst.name] = []
            graduates = Graduates.objects.filter(under_institute=inst.id)
            #data = GraduatesSerialize(graduates, many=True).data
            data = InstituteGradListSeralizer(graduates, many=True).data
            send_data[inst.name].append(data)

        return response.Response({'status': 'OK', 'result': send_data})


class SelectGraduates(generics.ListAPIView):
    queryset = Graduates.objects.all()
    serializer_class = GraduatesSerialize

    def get(self, request, institute, grad):
        inst = Institute.objects.filter(name=institute)
        if grad == 'ug':
            grads = Graduates.objects.filter(under_institute=inst[0].id,
                                             is_ug=True)
            send_data = GraduatesSerialize(grads, many=True).data
        elif grad == 'pg':
            grads = Graduates.objects.filter(under_institute=inst[0].id,
                                             is_ug=False)
            send_data = GraduatesSerialize(grads, many=True).data
        else:
            send_data = []
        return response.Response({'status': 'OK', 'result': send_data})


class UpdateGraduates(generics.UpdateAPIView):
    queryset = Graduates.objects.all()
    serializer_class = GraduatesSerialize

    def patch(self, request, *args, **kwargs):
        data = request.data
        qs.total_students = data['total_students']
        qs.total_final_years = data.get('total_final_years',
                                        qs.total_final_years)
        qs.total_higher_study_and_pay_crt = data.get(
            'total_higher_study_and_pay_crt',
            qs.total_higher_study_and_pay_crt)
        qs.total_not_intrested_in_placments = data.get(
            'total_not_intrested_in_placments',
            qs.total_not_intrested_in_placments)
        qs.total_offers = data.get('total_offers', qs.total_offers)
        qs.total_multiple_offers = data.get('total_multiple_offers',
                                            qs.total_multiple_offers)
        qs.highest_salary = data.get('highest_salary', qs.highest_salary)
        qs.lowest_salary = data.get('lowest_salary', qs.lowest_salary)
        qs.average_salary = data.get('average_salary', qs.average_salary)
        qs.save()

        return response.Response({
            'status': 'OK',
            'message': "send data succefully"
        })

    def put(self, request, pk, *args, **kwargs):
        qs = Graduates.objects.get(id=pk)

        data = request.data
        qs.total_students = data['total_students']
        qs.total_final_years = data['total_final_years']
        qs.total_higher_study_and_pay_crt = data[
            'total_higher_study_and_pay_crt']
        qs.total_not_intrested_in_placments = data[
            'total_not_intrested_in_placments']
        qs.total_offers = data['total_offers']
        qs.total_multiple_offers = data['total_multiple_offers']
        qs.highest_salary = data['highest_salary']
        qs.lowest_salary = data['lowest_salary']
        qs.average_salary = data['average_salary']
        qs.save()

        return response.Response({
            'status': 'OK',
            'message': "send data succefully"
        })

