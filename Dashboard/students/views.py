from rest_framework import generics, status, views, response
from organization.models import Institute, Campus, Stream
from django.db.models import Q, Count, Max
from organization.serializers import CampusSerialize, InstituteSerialize
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response

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
    serializer_class = DataUpdateSerializer

    def get(self, request, institute, grad):
        send_data = {}
        inst = Institute.objects.filter(name=institute)
        if grad == 'ug':
            grads = Graduates.objects.filter(under_institute=inst[0].id,
                                             is_ug=True)
            print("grads id : ", grads[0].id)
            data = DataUpdateSerializer(grads, many=True).data
        elif grad == 'pg':
            grads = Graduates.objects.filter(under_institute=inst[0].id,
                                             is_ug=False)
            print("grads id : ", grads[0].id)
            data = DataUpdateSerializer(grads, many=True).data
        return response.Response({'status': 'OK', 'result': data})


class UpdateGraduates(generics.RetrieveUpdateDestroyAPIView):
    queryset = Graduates.objects.all()
    serializer_class = DataUpdateSerializer


# v0.2
# class GraduateRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Graduates.objects.all()
#     serializer_class = GraduatesSerialize

# class GraduateRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Graduates.objects.all()
#     serializer_class = GraduatesSerialize

# class InstituteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Institute.objects.all()
#     serializer_class = InstituteSerialize

# class CampusRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Campus.objects.all()
#     serializer_class = CampusSerialize
"""@api_view(['GET', 'PUT'])
def inventory_list(request, institute, grad):

    if request.method == 'GET':
        inst = Institute.objects.filter(name=institute)
        if grad == 'ug':
            grads = Graduates.objects.filter(under_institute=inst[0].id, is_ug=True)
            data = DataUpdateSerializer(grads, many=True).data
        elif grad == 'pg':
            grads = Graduates.objects.filter(under_institute=inst[0].id, is_ug=False)
            data = DataUpdateSerializer(grads, many=True).data
        return response.Response({'status': 'OK', 'result': data})

    elif request.method == 'PUT':
        serializer = DataUpdateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
"""
