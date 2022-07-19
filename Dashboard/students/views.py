from rest_framework import generics, status, views, response
from organization.models import Institute, Campus, Stream, Programs, Courses
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


class GraduateList(generics.ListAPIView):
    serializer_class = GraduatesSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, year):
        db_logger = logging.getLogger('db')
        try:
            send_data = {}
            cmps = Campus.objects.all()
            for cmp in cmps:
                send_data[cmp.name] = {}
                ints = Campus.objects.get(name=cmp.name).institute_set.all()
                for int in ints:
                    send_data[cmp.name][int.name] = []
                    ug = Graduates.objects.filter(
                        Q(under_campus=cmp) & Q(under_institute=int)
                        & Q(is_ug=True) & Q(passing_year=year))
                    ug_data = GraduatesSerializer(ug, many=True).data
                    pg = Graduates.objects.filter(
                        Q(under_campus=cmp) & Q(under_institute=int)
                        & Q(is_ug=False) & Q(passing_year=year))
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

    def get(self, request, year, institute, campus):
        campus = Campus.objects.get(name=campus)
        print("Campus==>", campus)
        db_logger = logging.getLogger('db')
        try:
            try:
                insts = Institute.objects.filter(name=institute)
            except Exception as e:
                return response.Response({
                    'status': 'error',
                    'result': str(e)
                },
                                         status=HTTP_400_BAD_REQUEST)
            send_data = []
            for inst in insts:
                ug = Graduates.objects.filter(under_institute=inst,
                                              is_ug=True,
                                              passing_year=year,
                                              under_campus=campus)
                if ug.exists():
                    ug = InstituteGradListSeralizer(ug, many=True).data
                    print("UG ser: ", ug)
                    send_data.append(ug[0])

                pg = Graduates.objects.filter(under_institute=inst,
                                              is_ug=False,
                                              passing_year=year,
                                              under_campus=campus)
                if pg.exists():
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

    def get(self, request, year, stream):
        db_logger = logging.getLogger('db')
        try:
            send_data = {}
            stream_data = Stream.objects.filter(name=stream)

            if len(stream_data) == 0:
                db_logger.warning('Stream Does not Exists with' + str(stream))
                return response.Response(
                    {
                        'status': 'error',
                        'result': 'Stream Does not Exists'
                    },
                    status=HTTP_400_BAD_REQUEST)

            inst_data = Institute.objects.filter(stream=stream_data[0].id)
            for inst in inst_data:
                send_data[inst.name] = []
                graduates = Graduates.objects.filter(under_institute=inst.id,
                                                     is_ug=True,
                                                     passing_year=year)
                data = InstituteGradListSeralizer(graduates, many=True).data
                send_data[inst.name].append(data)

                graduates = Graduates.objects.filter(under_institute=inst.id,
                                                     is_ug=False,
                                                     passing_year=year)
                data = InstituteGradListSeralizer(graduates, many=True).data
                send_data[inst.name].append(data)

            return response.Response({'status': 'OK', 'result': send_data})
        except Exception as e:
            db_logger.exception(e)


class Gbstats(generics.ListAPIView):
    serializer_class = GBstatsSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, year):
        db_logger = logging.getLogger('db')
        try:
            send_data = {'UG': {}, 'PG': {}}
            ug_grad = Graduates.objects.filter(is_ug=True, passing_year=year)
            pg_grad = Graduates.objects.filter(is_ug=False, passing_year=year)

            send_data['UG'] = GBstatsSerializer(ug_grad).data
            send_data['PG'] = GBstatsSerializer(pg_grad).data
            return response.Response({'status': 'OK', 'result': send_data})
        except Exception as e:
            db_logger.exception(e)
            return response.Response({
                'status': 'Error',
                'result': str(e)
            },
                                     status=HTTP_400_BAD_REQUEST)


class SelectGraduates(generics.ListAPIView):
    queryset = Graduates.objects.all()
    serializer_class = GraduatesSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, year, institute, grad, campus):
        db_logger = logging.getLogger('db')
        try:
            campus = Campus.objects.get(name=campus)
            inst = Institute.objects.filter(name=institute)
            if len(inst) == 0:
                return response.Response({
                    'status': 'OK',
                    'result': 'No such institute'
                })
            if grad == 'ug':
                grads = Graduates.objects.filter(under_institute=inst[0].id,
                                                 is_ug=True,
                                                 passing_year=year,
                                                 under_campus=campus)

                send_data = GraduatesSerializer(grads, many=True).data
            elif grad == 'pg':

                grads = Graduates.objects.filter(under_institute=inst[0].id,
                                                 is_ug=False,
                                                 passing_year=year)
                send_data = GraduatesSerializer(grads, many=True).data
            else:
                send_data = []
            return response.Response({'status': 'OK', 'result': send_data})
        except Exception as e:
            db_logger.exception(e)
            return response.Response({
                'status': 'Error',
                'result': str(e)
            },
            status=HTTP_400_BAD_REQUEST)


class UpdateGraduates(generics.UpdateAPIView):
    queryset = Graduates.objects.all()
    serializer_class = UpdateGraduatesSerializer
    permission_classes = (IsAuthenticated, )

    def patch(self, request, year, pk, *args, **kwargs):
        db_logger = logging.getLogger('db')
        try:
            user = request.user
            try:
                qs = Graduates.objects.get(id=pk, passing_year=year)
                print("======>", qs)
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

            filecontent = f'''<p>Data <span style="font-family: monospace;font-family: monospace;text-transform: capitalize;"><em>{qs.under_campus.name.upper()}>{qs.under_institute.name.upper()}>{ug_pg}</em></span> was <span style="">Updated</span> by <span style="color: #2c7dff;text-transform: capitalize;"><b>{user.name}({user.designation})</b></span> at <span style="color:#555;">{data_time}</span></p>\n'''

            f.write(filecontent)

            f.close()

            db_logger.info("Data Instance Updated Succefully by " + str(user))
            return response.Response(
                {
                    'status': 'OK',
                    'message': "send data succefully",
                    'result': serializer.data
                },
                status=HTTP_201_CREATED)

        except Exception as e:
            db_logger.exception(e)
            return response.Response({
                'status': 'Error',
                'result': str(e)
            },
                                     status=HTTP_400_BAD_REQUEST)

    def put(self, request, year, pk, *args, **kwargs):
        db_logger = logging.getLogger('db')
        try:
            user = request.user
            try:
                qs = Graduates.objects.get(id=pk, passing_year=year)
                print("==>", qs)
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

            filecontent = f'''<p>Data <span style="font-family: monospace;font-family: monospace;text-transform: capitalize;"><em>{qs.under_campus.name.upper()}>{qs.under_institute.name.upper()}>{ug_pg}</em></span> was <span style="">Updated</span> by <span style="color: #2c7dff;text-transform: capitalize;"><b>{user.name}({user.designation})</b></span> at <span style="color:#555;">{data_time}</span></p>\n'''

            f.write(filecontent)
            f.close()
            db_logger.info("Data Instance Created Succefully by" + str(user))
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
            return response.Response({
                'status': 'Error',
                'result': str(e)
            },
                                     status=HTTP_400_BAD_REQUEST)


class ProgramsGraduates(generics.ListAPIView):
    serializer_class = ProgramGraduatesSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, year):
        try:
            qs_wp = GraduatesWithPrograms.objects.filter(passing_year=year)
            qs_g = Graduates.objects.filter(passing_year=year)

            send_data = dict()

            campuses = Campus.objects.all()
            institutes = Institute.objects.filter().all()

            for campus in campuses:
                send_data[campus.name] = dict()
                for institute in institutes.filter(under_campus=campus):
                    send_data[campus.name][institute.name] = dict()
                    if institute.name == "gst":
                        queryset = qs_wp.filter(under_campus=campus,
                                                under_institute=institute)
                        send_data[campus.name][
                            institute.name] = ProgramGraduatesSerializer(
                                queryset, many=True).data
                    else:
                        queryset = qs_g.filter(under_campus=campus,
                                               under_institute=institute)
                        send_data[campus.name][
                            institute.name] = GraduatesSerializer(
                                queryset, many=True).data

            return response.Response({'status': 'OK', 'result': send_data})
        except Exception as e:
            print(e)
            return response.Response({
                'status': 'Error',
                'result': str(e)
            },
                                     status=HTTP_400_BAD_REQUEST)


class CompareYearsData(generics.ListAPIView):
    serializer_class = CompareSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, year1, year2, coursename, grad):
        if grad == 'ug':
            grad = True
        else:
            grad = False

        send_data = {}
        try:
            course = Courses.objects.get(course=coursename)
        except Exception as e:
            print(e)
            return response.Response({
                'status': 'Error',
                'result': str(e)
            },
                                     status=HTTP_400_BAD_REQUEST)

        programs = Programs.objects.filter(under_course=course)

        send_data[year1] = dict()

        total_offers_aggri = 0
        total_multiple_offers_aggri = 0
        highest_salary_max = 0
        average_salary_avg = 0
        count = 0

        for i in programs:
            data = GraduatesWithPrograms.objects.filter(program=i,
                                                        passing_year=year1,
                                                        is_ug=grad)
            if data.exists():
                count += 1
                serializedData = CompareSerializer(data, many=True).data
                serializedData = serializedData[0]
                total_offers_aggri += serializedData['total_offers']
                total_multiple_offers_aggri += serializedData[
                    'total_multiple_offers']
                highest_salary_max = max(
                    highest_salary_max,
                    int(float(serializedData['highest_salary'])))
                average_salary_avg += int(
                    float(serializedData['average_salary']))
                # send_data[year1].append(serializedData)

        try:
            send_data[year1] = dict({
                'total_offers':
                total_offers_aggri,
                'total_multiple_offers':
                total_multiple_offers_aggri,
                'highest_salary':
                highest_salary_max,
                'average_salary':
                average_salary_avg / count
            })
        except:
            send_data[year1] = dict({
                'total_offers': 0,
                'total_multiple_offers': 0,
                'highest_salary': 0,
                'average_salary': 0
            })

        send_data[year2] = dict()

        total_offers_aggri = 0
        total_multiple_offers_aggri = 0
        highest_salary_max = 0
        average_salary_avg = 0
        count = 0

        for i in programs:
            data = GraduatesWithPrograms.objects.filter(program=i,
                                                        passing_year=year2,
                                                        is_ug=grad)
            if data.exists():
                count += 1
                serializedData = CompareSerializer(data, many=True).data
                serializedData = serializedData[0]
                total_offers_aggri += serializedData['total_offers']
                total_multiple_offers_aggri += serializedData[
                    'total_multiple_offers']
                highest_salary_max = max(
                    highest_salary_max,
                    int(float(serializedData['highest_salary'])))
                average_salary_avg += int(
                    float(serializedData['average_salary']))
                # send_data[year2].append(serializedData)
        try:
            send_data[year2] = dict({
                'total_offers':
                total_offers_aggri,
                'total_multiple_offers':
                total_multiple_offers_aggri,
                'highest_salary':
                highest_salary_max,
                'average_salary':
                average_salary_avg / count
            })
        except:
            send_data[year2] = dict({
                'total_offers': 0,
                'total_multiple_offers': 0,
                'highest_salary': 0,
                'average_salary': 0,
            })
        return response.Response({'status': 'OK', 'result': send_data})


class LogsDataListAPIView(generics.ListAPIView):

    def get(self, request):
        print("Hello")
        db_logger = logging.getLogger('db')
        try:
            with open("DBLog.txt", "r") as file:
                i = 0
                lines_size = 10
                last_lines = []
                for line in file:
                    if i < lines_size:
                        last_lines.append(line)
                    else:
                        last_lines[i % lines_size] = line
                    i = i + 1

            last_lines = last_lines[
                (i % lines_size):] + last_lines[:(i % lines_size)]

            send_data = []
            for line in last_lines:
                send_data.append(line)
            print("HI")
            return Response({'status': 'ok', 'result': send_data[::-1]})
        except Exception as e:
            db_logger.exception(e)
