from rest_framework import generics, status, views, response
from organization.models import Institute, Campus, Stream
from django.db.models import Q, Count, Max, Sum, Min, Avg
from organization.serializers import CampusSerialize, InstituteSerialize
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from django.contrib import messages
from django.http import HttpResponse
from .serializers import *
from .models import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from tablib import Dataset


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


class Gbstats(generics.ListAPIView):
    serializer_class = GBstatsSerializer

    def get(self, request):
        send_data = {'UG': {}, 'PG': {}}
        ug_grad = Graduates.objects.filter(is_ug=True)
        pg_grad = Graduates.objects.filter(is_ug=False)

        send_data['UG'] = GBstatsSerializer(ug_grad).data
        send_data['PG'] = GBstatsSerializer(pg_grad).data


        return response.Response({'status': 'OK', 'result': send_data})

        '''ug_total_final_years = ug_grad.aggregate(
            sum=Sum('total_final_years')).get('sum')

        ug_total_not_intrested_in_placments = ug_grad.aggregate(
            sum=Sum('total_not_intrested_in_placments')).get('sum')

        ug_total_backlogs_opted_for_higherstudies = ug_grad.aggregate(
            sum=Sum('total_backlogs_opted_for_higherstudies')).get('sum')
        ug_total_backlogs_opted_for_placements = ug_grad.aggregate(
            sum=Sum('total_backlogs_opted_for_placements')).get('sum')
        ug_total_backlogs_opted_for_other_career_options = ug_grad.aggregate(
            sum=Sum('total_backlogs_opted_for_other_career_options')).get(
                'sum')

        ug_total_backlogs = ug_total_backlogs_opted_for_higherstudies + ug_total_backlogs_opted_for_placements + ug_total_backlogs_opted_for_other_career_options

        ug_total_students_eligible = (ug_total_final_years -
                                      ug_total_backlogs +
                                      ug_total_not_intrested_in_placments)

        ug_placed = (
            ug_grad.aggregate(sum=Sum('total_offers')).get('sum') -
            ug_grad.aggregate(sum=Sum('total_multiple_offers')).get('sum'))

        ug_yet_to_place = (ug_total_students_eligible - ug_placed)

        pg_total_final_years = pg_grad.aggregate(
            sum=Sum('total_final_years')).get('sum')
        pg_total_not_intrested_in_placments = pg_grad.aggregate(
            sum=Sum('total_not_intrested_in_placments')).get('sum')
        pg_total_backlogs_opted_for_higherstudies = pg_grad.aggregate(
            sum=Sum('total_backlogs_opted_for_higherstudies')).get('sum')
        pg_total_backlogs_opted_for_placements = pg_grad.aggregate(
            sum=Sum('total_backlogs_opted_for_placements')).get('sum')
        pg_total_backlogs_opted_for_other_career_options = pg_grad.aggregate(
            sum=Sum('total_backlogs_opted_for_other_career_options')).get(
                'sum')

        pg_total_backlogs = pg_total_not_intrested_in_placments + pg_total_backlogs_opted_for_placements + pg_total_backlogs_opted_for_other_career_options
        pg_total_students_eligible = (pg_total_final_years -
                                      pg_total_backlogs +
                                      pg_total_not_intrested_in_placments)

        pg_placed = (
            pg_grad.aggregate(sum=Sum('total_offers')).get('sum') -
            pg_grad.aggregate(sum=Sum('total_multiple_offers')).get('sum'))

        pg_yet_to_place = (pg_total_students_eligible - pg_placed)

        send_data['UG']['student_details'] = {
            'total_students':
            ug_grad.aggregate(sum=Sum('total_students')).get('sum'),

            'total_final_years':
            ug_grad.aggregate(sum=Sum('total_final_years')).get('sum'),

            'total_backlogs':
            (ug_grad.aggregate(
                sum=Sum('total_backlogs_opted_for_higherstudies')).get('sum') +
             ug_grad.aggregate(
                 sum=Sum('total_backlogs_opted_for_placements')).get('sum') +
             ug_grad.aggregate(sum=Sum(
                 'total_backlogs_opted_for_other_career_options')).get('sum')),

            'total_higher_study_and_pay_crt':
            ug_grad.aggregate(
                sum=Sum('total_higher_study_and_pay_crt')).get('sum')
        }

        send_data['UG']['placement_details'] = {
            
            "total_students_eligible":
            (ug_total_final_years - ug_total_backlogs +
             ug_total_not_intrested_in_placments),
            
            "total_not_intrested_in_placments": (ug_grad.aggregate(
                sum=Sum('total_not_intrested_in_placments')).get('sum')),
            
            "total_offers":
            (ug_grad.aggregate(sum=Sum('total_offers')).get('sum')),
            
            "placed":
            (ug_grad.aggregate(sum=Sum('total_offers')).get('sum') -
             ug_grad.aggregate(sum=Sum('total_multiple_offers')).get('sum')),
            
            "yet_to_place":
            ug_yet_to_place,
            
            "total_multiple_offers":
            ug_grad.aggregate(sum=Sum('total_multiple_offers')).get('sum')
        }

        send_data['UG']['salary'] = {
            "highest": ug_grad.aggregate(max=Max('highest_salary')).get('max'),
            "average": ug_grad.aggregate(avg=Avg('average_salary')).get('avg'),
            "lowest": ug_grad.aggregate(min=Min('lowest_salary')).get('min')
        }

        send_data['PG']['student_details'] = {
            'total_students':
            pg_grad.aggregate(sum=Sum('total_students')).get('sum'),
            'total_final_years':
            pg_grad.aggregate(sum=Sum('total_final_years')).get('sum'),
            'total_backlogs':
            (pg_grad.aggregate(
                sum=Sum('total_backlogs_opted_for_higherstudies')).get('sum') +
             pg_grad.aggregate(
                 sum=Sum('total_backlogs_opted_for_placements')).get('sum') +
             pg_grad.aggregate(sum=Sum(
                 'total_backlogs_opted_for_other_career_options')).get('sum')),
            'total_higher_study_and_pay_crt':
            pg_grad.aggregate(
                sum=Sum('total_higher_study_and_pay_crt')).get('sum')
        }

        send_data['PG']['placement_details'] = {
            "total_students_eligible":
            (pg_total_final_years - pg_total_backlogs +
             pg_total_not_intrested_in_placments),
            "total_not_intrested_in_placments": (pg_grad.aggregate(
                sum=Sum('total_not_intrested_in_placments')).get('sum')),
            "total_offers":
            pg_grad.aggregate(sum=Sum('total_offers')).get('sum'),
            "placed":
            (pg_grad.aggregate(sum=Sum('total_offers')).get('sum') -
             pg_grad.aggregate(sum=Sum('total_multiple_offers')).get('sum')),
            "yet_to_place":
            pg_yet_to_place,
            "total_multiple_offers":
            pg_grad.aggregate(sum=Sum('total_multiple_offers')).get('sum')
        }

        send_data['PG']['salary'] = {
            "highest": pg_grad.aggregate(max=Max('highest_salary')).get('max'),
            "average": pg_grad.aggregate(avg=Avg('average_salary')).get('avg'),
            "lowest": pg_grad.aggregate(min=Min('lowest_salary')).get('min')
        }

        return response.Response({'status': 'OK', 'result': send_data})'''


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


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, format=None):
        excel_file = request.data['file']
        print(excel_file)
        dataset = Dataset()
        if not excel_file.name.endswith('.xlsx'):
            return Response("File should be excel only", status=404)
        imported_data = dataset.load(excel_file.read(),
                                     headers=False,
                                     format='xlsx')
        print("imported_data: \n", imported_data)

        data = {}
        try:
            under_campus = Campus.objects.get(name=imported_data[0][1])
            under_institute = Institute.objects.get(name=imported_data[1][1])
            is_ug = imported_data[-1][1]
        except Campus.DoesNotExist:
            return Response("Campus Invalid: " + str(imported_data))
        except Institute.DoesNotExist:
            return Response("Institute Invalid" + str(imported_data[1]))

        for key_val in imported_data[2:-1]:
            data[key_val[0]] = key_val[1]
        qs, create = Graduates.objects.get_or_create(
            under_campus=under_campus,
            under_institute=under_institute,
            is_ug=is_ug)
        qs.total_students = data['total_students']
        qs.total_final_years = data['total_final_years']
        qs.total_higher_study_and_pay_crt = data[
            'total_higher_study_and_pay_crt']
        qs.total_not_intrested_in_placments = data[
            'total_not_intrested_in_placments']
        qs.total_backlogs_opted_for_placements = data[
            'total_backlogs_opted_for_placements']
        qs.total_backlogs_opted_for_higherstudies = data[
            'total_backlogs_opted_for_higherstudies']
        qs.total_backlogs_opted_for_other_career_options = data[
            'total_backlogs_opted_for_other_career_options']
        qs.total_offers = data['total_offers']
        qs.total_multiple_offers = data['total_multiple_offers']
        qs.highest_salary = data['highest_salary']
        qs.lowest_salary = data['lowest_salary']
        qs.average_salary = data['average_salary']
        qs.save()

        return Response("Data sent", status=204)

    def post(self, request, format=None):
        excel_file = request.data['file']
        dataset = Dataset()
        if not excel_file.name.endswith('.xlsx'):
            return Response("File should be excel only", status=404)
        imported_data = dataset.load(excel_file.read(),
                                     headers=False,
                                     format='xlsx')

        data = {}

        try:
            under_campus = Campus.objects.get(name=imported_data[0][1])
            under_institute = Institute.objects.get(name=imported_data[1][1])
        except Campus.DoesNotExist:
            return Response("Campus Invalid: " + str(imported_data))
        except Institute.DoesNotExist:
            return Response("Institute Invalid" + str(imported_data[1]))

        for key_val in imported_data[2:]:
            data[key_val[0]] = key_val[1]

        qs = Graduates(under_campus=under_campus,
                       under_institute=under_institute,
                       **data)
        qs.save()
        return Response("Data sent", status=204)
