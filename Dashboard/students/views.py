from rest_framework import generics, status, views, response
from organization.models import Institute, Campus, Stream
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from organization.serializers import CampusSerialize, InstituteSerialize
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
from .models import *
from rest_framework.status import *
from account.models import *
from dateutil.tz import gettz
from datetime import datetime
import calendar
import traceback
import logging

map = {
    'git': 'GIT',
    'gim': 'GIM',
    'gis': 'GIS',
    'gsoa': 'GSoA',
    'gin': 'GIN',
    'gip': 'GIP',
    'gsol': 'GSoL',
    'gsgs': 'GSGS',
    'soth': 'SoTH',
    'hbs': 'HBS',
    'soph': 'SoPH',
    'sosh': 'SoSH',
    'sotb': 'SoTB',
    'sosp': 'SoSP',
    'gsbb': 'GSBB',
    'sosb':'SoSB',
}


class GraduateList(generics.ListAPIView):
    serializer_class = GraduatesSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        db_logger = logging.getLogger('db')
        try:
            send_data = {}
            cmps = Campus.objects.all()
            for cmp in cmps:
                send_data[cmp.name] = {}
                ints = Campus.objects.get(
                    name=cmp.name).institute_set.all()
                for int in ints:
                    send_data[cmp.name][int.name] = []
                    ug = Graduates.objects.filter(
                        Q(under_campus=cmp) & Q(under_institute=int)
                        & Q(is_ug=True))
                    ug_data = GraduatesSerializer(ug, many=True).data
                    pg = Graduates.objects.filter(
                        Q(under_campus=cmp) & Q(under_institute=int)
                        & Q(is_ug=False))
                    pg_data = GraduatesSerializer(pg, many=True).data
                    send_data[cmp.name][int.name].append(ug_data)
                    send_data[cmp.name][int.name].append(pg_data)
        except Exception as e:
            db_logger.exception(str(e))
            return response.Response({
                    'status': 'error',
                    'result': str(e)
            },
            status=HTTP_500_INTERNAL_SERVER_ERROR)
        return response.Response({'status': 'OK', 'result': send_data})

# --
#
# {  }
#
# --


class InstituteGradList(generics.ListAPIView):
    serializer_class = InstituteGradListSeralizer
    permission_classes = (IsAuthenticated, )

    def get(self, request, institute):
        db_logger = logging.getLogger('db')
        try:
            try:
                inst = Institute.objects.get(name=institute)
            except Exception as e:
                return response.Response({
                    'status': 'error',
                    'result': str(e)
                },
                                         status=HTTP_400_BAD_REQUEST)
            send_data = []

            ug = Graduates.objects.filter(under_institute=inst, is_ug=True)
            ug = InstituteGradListSeralizer(ug, many=True).data
            send_data.append(ug[0])

            pg = Graduates.objects.filter(under_institute=inst, is_ug=False)
            pg = InstituteGradListSeralizer(pg, many=True).data
            send_data.append(pg[0])

            # [
            #     # students detalis[student_details,placement_details,salary] ,
            #     #
            #     # ug details[student_details,placement_details,salary] ,
            #     #
            #     # pg details[student_details,placement_details,salary]
            # ]
            return response.Response({'status': 'OK', 'result': send_data})
        except Exception as e:
            db_logger.exception(e)


class Overall(generics.ListAPIView):
    serializer_class = InstituteGradListSeralizer
    permission_classes = (IsAuthenticated, )

    def get(self, request, stream):
        db_logger = logging.getLogger('db')
        try:
            send_data = {}
            stream_data = Stream.objects.filter(name=stream)

            if len(stream_data) == 0:
                db_logger.warning('Stream Does not Exists with'+str(stream))
                return response.Response(
                    {
                        'status': 'error',
                        'result': 'Stream Does not Exists'
                    },
                    status=HTTP_400_BAD_REQUEST)

            inst_data = Institute.objects.filter(stream=stream_data[0].id)
            for inst in inst_data:
                send_data[map[inst.name]] = []
                graduates = Graduates.objects.filter(under_institute=inst.id,
                                                     is_ug=True)
                data = InstituteGradListSeralizer(graduates, many=True).data
                send_data[map[inst.name]].append(data)

                graduates = Graduates.objects.filter(under_institute=inst.id,
                                                     is_ug=False)
                data = InstituteGradListSeralizer(graduates, many=True).data
                send_data[map[inst.name]].append(data)

            return response.Response({'status': 'OK', 'result': send_data})
        except Exception as e:
            db_logger.exception(e)


class Gbstats(generics.ListAPIView):
    serializer_class = GBstatsSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        db_logger = logging.getLogger('db')
        try:
            send_data = {'UG': {}, 'PG': {}}
            ug_grad = Graduates.objects.filter(is_ug=True)
            pg_grad = Graduates.objects.filter(is_ug=False)

            send_data['UG'] = GBstatsSerializer(ug_grad).data
            send_data['PG'] = GBstatsSerializer(pg_grad).data
            return response.Response({'status': 'OK', 'result': send_data})
        except Exception as e:
            db_logger.exception(e)
            return response.Response({'status': 'Error', 'result': str(e)},status=HTTP_400_BAD_REQUEST)



class SelectGraduates(generics.ListAPIView):
    queryset = Graduates.objects.all()
    serializer_class = GraduatesSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, institute, grad):
        db_logger = logging.getLogger('db')
        try:
            inst = Institute.objects.filter(name=institute)
            if len(inst) == 0:
                return response.Response({
                    'status': 'OK',
                    'result': 'No such institute'
                })
            if grad == 'ug':
                grads = Graduates.objects.filter(under_institute=inst[0].id,
                                                 is_ug=True)
                send_data = GraduatesSerializer(grads, many=True).data
            elif grad == 'pg':

                grads = Graduates.objects.filter(under_institute=inst[0].id,
                                                 is_ug=False)
                send_data = GraduatesSerializer(grads, many=True).data
            else:
                send_data = []
            return response.Response({'status': 'OK', 'result': send_data})
        except Exception as e:
            db_logger.exception(e)
            return response.Response({'status': 'Error', 'result': str(e)},status=HTTP_400_BAD_REQUEST)



class UpdateGraduates(generics.UpdateAPIView):
    queryset = Graduates.objects.all()
    serializer_class = UpdateGraduatesSerializer
    permission_classes = (IsAuthenticated, )

    def patch(self, request, pk, *args, **kwargs):
        db_logger = logging.getLogger('db')
        try:
            user = request.user
            try:
                qs = Graduates.objects.get(id=pk)
            except:
                return response.Response(
                    {
                        'status': 'error',
                        'result': 'institute does not exist'
                    },
                    status=HTTP_400_BAD_REQUEST)

            if user.access == 'view':
                return response.Response(
                    {
                        'status': 'error',
                        'result': 'permission denied'
                    },
                    status=HTTP_423_LOCKED)

            if user.access == "edit_all" and user.university != "univ" and qs.under_campus != user.university:
                return response.Response(
                    {
                        'status': 'error',
                        'result': 'permission denied'
                    },
                    status=HTTP_423_LOCKED)

            check_editor_list = EditorInstitutes.objects.filter(
                Q(account=user) & Q(institute=qs.under_institute)).exists()
            if user.access == "edit_some" and not check_editor_list:
                return response.Response(
                    {
                        'status': 'error',
                        'result': 'PermissionDenied'
                    },
                    status=HTTP_423_LOCKED)

            data = request.data
            serializer = UpdateGraduatesSerializer(qs, data=data, partial=True)

            if not serializer.is_valid():
                return response.Response(
                    {
                        'status': 'error',
                        'result': 'Invalid data'
                    },
                    status=HTTP_205_RESET_CONTENT)

            

            dtobj = datetime.now(tz=gettz('Asia/Kolkata'))
            timer = dtobj.strftime("%I:%M %p")

            ug_pg = 'UG' if qs.is_ug == True else 'PG'
            month = datetime.now().month
            year = str(datetime.now().year)
            day = str(datetime.now().day)
            data_time = timer + ", " + day + " " + calendar.month_name[
                month] + " " + year

            f = open('DBLog.txt', 'a')
            # f.write(
            #     f"Data `{qs.under_campus}>{qs.under_institute}>{ug_pg}` was Updated by {user.name}({user.designation}) at {data_time}\n"
            # )




            filecontent = f'''<p>Data <span style="font-family: monospace;font-family: monospace;text-transform: capitalize;"><em>{qs.under_campus.name.upper()}>{qs.under_institute.name.upper()}>{ug_pg}</em></span> was <span style="">Updated</span> by <span style="color: #2c7dff;text-transform: capitalize;"><b>{user.name}({user.designation})</b></span> at <span style="color:#555;">{data_time}</span></p>\n'''

            # filecontent = f"""<p> Data <span className="campus_path">`{grad.under_campus.name.upper()}>{grad.under_institute.name.upper()}>{ug_pg}`</span> was <span className="action_name updated"> Updated</span> by <span className="author_name">{user.name}({user.designation})</span> at <span className="time">{data_time}</span></p>\n"""

            f.write(filecontent)

            f.close()

            db_logger.info("Data Instance Updated Succefully by "+str(user))
            return response.Response(
                {
                    'status': 'OK',
                    'message': "send data succefully",
                    'result': serializer.data
                },
                status=HTTP_201_CREATED)

        except Exception as e:
            db_logger.exception(e)
            return response.Response({'status': 'Error', 'result': str(e)},status=HTTP_400_BAD_REQUEST)
    


    def put(self, request, pk, *args, **kwargs):
        db_logger = logging.getLogger('db')
        try:
            user = request.user
            try:
                qs = Graduates.objects.get(id=pk)
            except:
                return response.Response(
                    {
                        'status': 'error',
                        'result': 'institute does not exist'
                    },
                    status=HTTP_400_BAD_REQUEST)

            if user.access == 'view':
                return response.Response(
                    {
                        'status': 'error',
                        'result': 'permission denied'
                    },
                    status=HTTP_423_LOCKED)

            if user.access == "edit_all" and user.university != "univ" and qs.under_campus != user.university:
                return response.Response(
                    {
                        'status': 'error',
                        'result': 'permission denied'
                    },
                    status=HTTP_423_LOCKED)

            check_editor_list = EditorInstitutes.objects.filter(
                Q(account=user) & Q(institute=qs.under_institute)).exists()
            if user.access == "edit_some" and not check_editor_list:
                return response.Response(
                    {
                        'status': 'error',
                        'result': 'PermissionDenied'
                    },
                    status=HTTP_423_LOCKED)

            data = request.data
            data = request.data

            serializer = UpdateGraduatesSerializer(qs, data=data)

            if not serializer.is_valid():
                return response.Response(
                    {
                        'status': 'error',
                        'result': 'Invalid data'
                    },
                    status=HTTP_205_RESET_CONTENT)

            serializer.save()
            ug_pg = 'UG' if qs.is_ug == True else 'PG'

            dtobj = datetime.now(tz=gettz('Asia/Kolkata'))
            timer = dtobj.strftime("%I:%M %p")


            month = datetime.now().month
            year = str(datetime.now().year)
            day = str(datetime.now().day)
            data_time = timer + ", " + day + " " + calendar.month_name[
                month] + " " + year


            f = open('DBLog.txt', 'a')

            # f.write(
            #     f"Data `{qs.under_campus}>{qs.under_institute}>{ug_pg}` was Added by {user.name}({user.designation}) at {data_time}\n"
            # )

            # filecontent = f"""<p className="log_line"> Data <span className="campus_path">`{grad.under_campus.name.upper()}>{grad.under_institute.name.upper()}>{ug_pg}`</span> was <span className="action_name updated"> Updated</span> by <span className="author_name">{user.name}({user.designation})</span> at <span className="time">{data_time}</span></p>\n"""

            filecontent = f'''<p>Data <span style="font-family: monospace;font-family: monospace;text-transform: capitalize;"><em>{qs.under_campus.name.upper()}>{qs.under_institute.name.upper()}>{ug_pg}</em></span> was <span style="">Updated</span> by <span style="color: #2c7dff;text-transform: capitalize;"><b>{user.name}({user.designation})</b></span> at <span style="color:#555;">{data_time}</span></p>\n'''

            f.write(filecontent)
            f.close()
            db_logger.info("Data Instance Created Succefully by"+str(user))
            return response.Response(
                {
                    'status': 'OK',
                    'message': "send data succefully",
                    'result': serializer.data
                },
                status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            db_logger.exception(e)
            return response.Response({'status': 'Error', 'result': str(e)},status=HTTP_400_BAD_REQUEST)