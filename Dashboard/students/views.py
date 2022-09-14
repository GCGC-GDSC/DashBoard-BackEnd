from socket import INADDR_ALLHOSTS_GROUP
from tokenize import Name
from unicodedata import name
from rest_framework import generics, status, views, response
from organization.models import Institute, Campus, Stream, Programs, Courses
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from organization.serializers import CampusSerialize, InstituteSerialize
from rest_framework.response import Response
from django.db.models import Q, Sum
from .serializers import *
from .models import *
from rest_framework.status import *
from account.models import *
from dateutil.tz import gettz
from datetime import datetime
import calendar
import traceback
import logging
import json
from collections import defaultdict

from django.http import HttpResponse


class GraduateList(generics.ListAPIView):
    serializer_class = GraduatesSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, year):
        db_logger = logging.getLogger('db')
        try:
            send_data = {}
            cmps = Campus.objects.all()
            for cmp_ in cmps:
                send_data[cmp_.name] = {}
                ints = Campus.objects.get(name=cmp_.name).institute_set.all()
                for int_ in ints:
                    send_data[cmp_.name][int_.name] = []
                    ug = Graduates.objects.filter(
                        Q(under_campus=cmp_) & Q(under_institute=int_)
                        & Q(is_ug=True) & Q(passing_year=year))
                    ug_data = GraduatesSerializer(ug, many=True).data
                    pg = Graduates.objects.filter(
                        Q(under_campus=cmp_) & Q(under_institute=int_)
                        & Q(is_ug=False) & Q(passing_year=year))
                    pg_data = GraduatesSerializer(pg, many=True).data
                    send_data[cmp_.name][int_.name].append(ug_data)
                    send_data[cmp_.name][int_.name].append(pg_data)
        except Exception as e:
            db_logger.exception(str(e))
            return response.Response({
                'status': 'error',
                'result': str(e)
            },
                                     status=HTTP_500_INTERNAL_SERVER_ERROR)
        return response.Response({'status': 'OK', 'result': send_data})


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
            send_data = defaultdict(list)
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
                name = inst.name + "-" + inst.under_campus.name
                graduates = Graduates.objects.filter(under_institute=inst.id,
                                                     is_ug=True,
                                                     passing_year=year)
                data = InstituteGradListSeralizer(graduates, many=True).data
                send_data[name].append(data)

                graduates = Graduates.objects.filter(under_institute=inst.id,
                                                     is_ug=False,
                                                     passing_year=year)
                data = InstituteGradListSeralizer(graduates, many=True).data
                send_data[name].append(data)

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

            

            # print(ug_grad.aggregate(total_students__sum=Sum('total_students'))['total_students__sum'])
            # print(ug_grad.aggregate(total_final_years__sum=Sum('total_final_years'))['total_final_years__sum'])
            # print(ug_grad.aggregate(total_higher_study_and_pay_crt__sum=Sum('total_higher_study_and_pay_crt'))['total_higher_study_and_pay_crt__sum'])
            # print(ug_grad.aggregate(total_backlogs__sum=Sum('total_backlogs'))['total_backlogs__sum'])
            # print(ug_grad.aggregate(total_students_eligible__sum=Sum('total_students_eligible'))['total_students_eligible__sum'])
            # print(ug_grad.aggregate(total_not_intrested_in_placments__sum=Sum('total_not_intrested_in_placments'))['total_not_intrested_in_placments__sum'])
            # print(ug_grad.aggregate(total_opted_for_higher_studies_only__sum=Sum('total_opted_for_higher_studies_only'))['total_opted_for_higher_studies_only__sum'])



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
    serializer_class = GraduatesSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, year, institute, coursename, grad, campus):
        db_logger = logging.getLogger('db')
        try:
            campus = Campus.objects.get(name=campus)
            inst = Institute.objects.get(name=institute, under_campus=campus)
            if coursename == "null":
                grads = Graduates.objects.get(
                    under_institute=inst,
                    is_ug=(True if grad == "ug" else False),
                    passing_year=year,
                    under_campus=campus)
                send_data = GraduatesSerializer(grads).data
                return response.Response({
                    'status': 'OK',
                    'result': [send_data]
                })
            else:
                program = Programs.objects.get(
                    name=coursename,
                    is_ug=(True if grad == "ug" else False),
                    under_institute=inst,
                    under_campus=campus)
                queryset = GraduatesWithPrograms.objects.filter(
                    program=program, under_campus=campus).all()
                grads = queryset.filter(
                    is_ug=(True if grad == "ug" else False), passing_year=year)
                send_data = ProgramGraduatesSerializer(grads, many=True).data
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

            f = open('./logs/dblog.txt', 'a')

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
                # print("==>", qs)
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

            f = open('./logs/dblog.txt', 'a')

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
            # print(e)
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
            # print(e)
            return response.Response({
                'status': 'Error',
                'result': str(e)
            },
                                     status=HTTP_400_BAD_REQUEST)

class CompareYearsData(generics.ListAPIView):
    serializer_class = CompareSerializer
    permission_classes = (IsAuthenticated, )

    def grads_helper(self, grads_array):
            total_students_eligible = 0
            total_placed = 0
            total_multiple_offers = 0
            highest_salary = 0
            average_salary = 0
            n = 0
            m = 0
            for i in grads_array:
                n+=1
                total_students_eligible+=i.total_students_eligible
                total_placed+=i.total_placed
                total_multiple_offers+=i.total_multiple_offers
                highest_salary = max(highest_salary, i.highest_salary)
                average_salary += i.average_salary
                if i.average_salary>0: m += 1 
            
            if m>0: average_salary /= m

            return {
                                "total_students_eligible"   :total_students_eligible,
                                "total_placed"              :total_placed,
                                "total_multiple_offers"     :total_multiple_offers,
                                "highest_salary"            :highest_salary,
                                "average_salary"            :average_salary,}

    def get(self, request, year1, year2, campus, institute):


        if institute=="gst":
            try:
                inst = Institute.objects.get(name=institute,under_campus__name=campus)
                graduates_with_programs = GraduatesWithPrograms.objects.filter(under_institute=inst)
                graduates_with_programs_yearwise = {}
                graduates_with_programs_yearwise[year1] = graduates_with_programs.filter(passing_year=year1)
                graduates_with_programs_yearwise[year2] = graduates_with_programs.filter(passing_year=year2)
                
                send_data = {year1:{},year2:{}}

                keys = ["total_students_eligible", "total_placed", "total_multiple_offers", "highest_salary", "average_salary"]

                # year1
                
                programs = Programs.objects.filter(under_institute=inst)

                for year in [year1,year2]:
                    for program in programs:
                        course_ = program.under_course
                        if course_.course not in send_data[year]:
                            
                            grads_array = graduates_with_programs_yearwise[year].filter(program__under_course=course_)
                            send_data[year][course_.course] =  self.grads_helper(grads_array)

                return response.Response({"status": "OK", "result": send_data})

            except Exception as e:
                print(traceback.print_exc())
                return response.Response({"status": "Error", "result": send_data}, status=HTTP_404_NOT_FOUND)
            pass
        else:
            try:
                inst = Institute.objects.get(name=institute,under_campus__name=campus)
                send_data = {year1:{"UG":{},"PG":{}},year2:{"UG":{},"PG":{}}}
                graduates_objects = Graduates.objects.filter(under_institute=inst)
                graduates_y1 = graduates_objects.filter(passing_year=year1)
                graduates_y2 = graduates_objects.filter(passing_year=year2)
                
                res_y1 = CompareSerializer(graduates_y1, many=True).data
                res_y2 = CompareSerializer(graduates_y2, many=True).data
                send_data[year1]["UG"] = res_y1[0]
                send_data[year1]["PG"] = res_y1[1]


                send_data[year2]["UG"] = res_y2[0]
                send_data[year2]["PG"] = res_y2[1]
                return response.Response({"status": "OK", "result": send_data}, status=HTTP_200_OK)
            except Exception as e:
                return response.Response({"status": "Error", "result": str(e)}, status=HTTP_404_NOT_FOUND)

        return response.Response({"status": "Error", "result": "something went wrong."}, status=HTTP_400_BAD_REQUEST)


        # Prev's code:--
#         compare_years = [year1, year2]
#         if grad == 'ug':
#             grad = True
#         elif grad == 'pg':
#             grad = False
#         else:
#             grad = None

#         send_data = {}
#         try:
#             campus = Campus.objects.get(name=campus)
#             institute = Institute.objects.get(name=institute,
#                                               under_campus=campus)
#         except Exception as e:
#             # print(e)
#             return response.Response({
#                 'status': 'Error',
#                 'result': str(e)
#             },
#                                      status=HTTP_400_BAD_REQUEST)
# # 
        
#         if coursename != "null":
#             course = Courses.objects.get(course=coursename)
#             prog = Programs.objects.filter(under_campus=campus,
#                                         under_institute=institute,
#                                         under_course=course,
#                                         is_ug=grad)
#             print("Programs ===> ", prog)

#             # prog = Programs.objects.get(under_campus=campus,
#             #                             under_institute=institute,
#             #                             name=program,
#             #                             is_ug=grad)
#             # print("programs: ", program)

#             for j in compare_years:
#                 send_data[j] = dict()
#                 total_offers_aggri = 0
#                 total_multiple_offers_aggri = 0
#                 highest_salary_max = 0
#                 average_salary_avg = 0
#                 for pro in prog:
#                     data = GraduatesWithPrograms.objects.filter(program=pro,
#                                                                 passing_year=j)
#                     print("data: ", data)
#                     if data.exists():
#                         serializedData = CompareSerializer(data, many=True).data
#                         for i in serializedData:
#                             # print("data i ========> ", i)
#                             total_offers_aggri += i['total_offers']
#                             total_multiple_offers_aggri += i[
#                                 'total_multiple_offers']
#                             highest_salary_max = max(
#                                 highest_salary_max,
#                                 int(float(i['highest_salary'])))
#                             average_salary_avg += int(
#                                 float(i['average_salary']))
#                         # send_data[year1].append(serializedData)
#                     try:
#                         send_data[j] = dict({
#                             'total_offers':
#                             total_offers_aggri,
#                             'total_multiple_offers':
#                             total_multiple_offers_aggri,
#                             'highest_salary':
#                             highest_salary_max,
#                             'average_salary':
#                             average_salary_avg
#                         })
#                     except:
#                         send_data[j] = dict({
#                             'total_offers': 0,
#                             'total_multiple_offers': 0,
#                             'highest_salary': 0,
#                             'average_salary': 0
#                         })
#             return response.Response({'status': 'OK', 'result': send_data})

#                 # if data.exists():
#                 #     # print("==>>", data)
#                 #     try:
#                 #         send_data[j] = dict({
#                 #             'total_offers':
#                 #             data[0].total_offers,
#                 #             'total_multiple_offers':
#                 #             data[0].total_multiple_offers,
#                 #             'highest_salary':
#                 #             data[0].highest_salary,
#                 #             'average_salary':
#                 #             data[0].average_salary
#                 #         })
#                 #     except:
#                 #         send_data[j] = dict({
#                 #             'total_offers': 0,
#                 #             'total_multiple_offers': 0,
#                 #             'highest_salary': 0,
#                 #             'average_salary': 0
#                 #         })
#         # else:
#         #     for j in compare_years:
#         #         send_data[j] = dict()
#         #         data = Graduates.objects.filter(under_institute=institute, under_campus=campus, is_ug=grad, passing_year=j)
#         #         print("data: ", data)
#         #         total_offers_aggri = 0
#         #         total_multiple_offers_aggri = 0
#         #         highest_salary_max = 0
#         #         average_salary_avg = 0
#         #         if data.exists():
#         #             serializedData = CompareSerializer(data, many=True).data
#         #             for i in serializedData:
#         #                 print("data i ========> ", i)
#         #                 total_offers_aggri += i['total_offers']
#         #                 total_multiple_offers_aggri += i[
#         #                     'total_multiple_offers']
#         #                 highest_salary_max = max(
#         #                     highest_salary_max,
#         #                     int(float(i['highest_salary'])))
#         #                 average_salary_avg += int(
#         #                     float(i['average_salary']))
#         #             # send_data[year1].append(serializedData)
#         #         try:
#         #             send_data[j] = dict({
#         #                 'total_offers':
#         #                 total_offers_aggri,
#         #                 'total_multiple_offers':
#         #                 total_multiple_offers_aggri,
#         #                 'highest_salary':
#         #                 highest_salary_max,
#         #                 'average_salary':
#         #                 average_salary_avg
#         #             })
#         #         except:
#         #             send_data[j] = dict({
#         #                 'total_offers': 0,
#         #                 'total_multiple_offers': 0,
#         #                 'highest_salary': 0,
#         #                 'average_salary': 0
#         #             })

#         # # send_data[year2] = dict()

#         # # total_offers_aggri = 0
#         # # total_multiple_offers_aggri = 0
#         # # highest_salary_max = 0
#         # # average_salary_avg = 0
#         # # count = 0

#         # # for i in programs:
#         # #     data = GraduatesWithPrograms.objects.filter(program=i,
#         # #                                                 passing_year=year2,
#         # #                                                 is_ug=grad)
#         # #     if data.exists():
#         # #         count += 1
#         # #         serializedData = CompareSerializer(data, many=True).data
#         # #         serializedData = serializedData[0]
#         # #         total_offers_aggri += serializedData['total_offers']
#         # #         total_multiple_offers_aggri += serializedData[
#         # #             'total_multiple_offers']
#         # #         highest_salary_max = max(
#         # #             highest_salary_max,
#         # #             int(float(serializedData['highest_salary'])))
#         # #         average_salary_avg += int(
#         # #             float(serializedData['average_salary']))
#         # #         # send_data[year2].append(serializedData)
#         # # try:
#         # #     send_data[year2] = dict({
#         # #         'total_offers':
#         # #         total_offers_aggri,
#         # #         'total_multiple_offers':
#         # #         total_multiple_offers_aggri,
#         # #         'highest_salary':
#         # #         highest_salary_max,
#         # #         'average_salary':
#         # #         average_salary_avg / count
#         # #     })
#         # # except:
#         # #     send_data[year2] = dict({
#         # #         'total_offers': 0,
#         # #         'total_multiple_offers': 0,
#         # #         'highest_salary': 0,
#         # #         'average_salary': 0,
#         # #     })
#         # return response.Response({'status': 'OK', 'result': send_data})


#             # return response.Response({'status': 'OK', 'result': send_data})
#         elif coursename == "null" and grad != None:
#             send_data = dict({
#                 "total_offers": 0,
#                 "total_multiple_offers": 0,
#                 "highest_salary": 0,
#                 "average_salary": 0
#             })
#             try:
#                 for j in compare_years:
#                     res = Graduates.objects.get(under_institute=institute,
#                                                 passing_year=j,
#                                                 is_ug=grad)
#                     send_data[j]["total_offers"] = res.total_offers
#                     send_data[j][
#                         "total_multiple_offers"] = res.total_multiple_offers
#                     send_data[j]["highest_salary"] = res.highest_salary
#                     send_data[j]["average_salary"] = res.average_salary
#                 return response.Response({"status": "ok", "result": send_data})
#             except Exception as e:
#                 return response.Response(
#                     {
#                         "status": "Error",
#                         "result": send_data,
#                         "message": str(e)
#                     },
#                     status=HTTP_400_BAD_REQUEST)
#         else:
#             return response.Response(
#                 {
#                     "status":
#                     "Error",
#                     "result":
#                     None,
#                     "message":
#                     "request is not allowed with the params" + str(
#                         (year1, year2, campus, institute, coursename, grad))
#                 },
#                 status=HTTP_400_BAD_REQUEST)


class LogsDataListAPIView(generics.ListAPIView):
    serializer_class = GraduatesSerializer

    def get(self, request):
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
            return Response({'status': 'ok', 'result': send_data[::-1]})
        except Exception as e:
            db_logger.exception(e)


class UpdateGraduatesWithPrograms(generics.UpdateAPIView):
    queryset = GraduatesWithPrograms.objects.all()
    serializer_class = UpdateGraduatesWithProgramsSerializer
    permission_classes = (IsAuthenticated, )

    def put(self, request, year, pk, *args, **kwargs):
        db_logger = logging.getLogger('db')
        try:
            user = request.user
            try:
                qs = GraduatesWithPrograms.objects.get(id=pk,
                                                       passing_year=year)
                # print("===>>>", qs)
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

            serializer = UpdateGraduatesWithProgramsSerializer(qs, data=data)
            # print("==>", serializer)

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

            f = open('./logs/dblog.txt', 'a')

            filecontent = f'''<p>Data <span style="font-family: monospace;font-family: monospace;text-transform: capitalize;"><em>{qs.under_campus.name.upper()}>{qs.program.name.upper()}>{qs.under_campus.name.upper()}>{ug_pg}</em></span> was <span style="">Updated</span> by <span style="color: #2c7dff;text-transform: capitalize;"><b>{user.name}({user.designation})</b></span> at <span style="color:#555;">{data_time}</span></p>\n'''

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
            db_logger.exception(e)
            return response.Response({
                'status': 'Error',
                'result': str(e)
            },
                                     status=HTTP_400_BAD_REQUEST)

        def patch(self, request, year, pk, *args, **kwargs):
            return response.Response(
                {
                    "status": "Error",
                    "result": "This method is not Allowed."
                },
                status=HTTP_400_BAD_REQUEST)


def CreateInstances(request, year):
    try:
        val = Graduates.objects.filter(passing_year='2022')
        for i in val:
            Graduates.objects.create(under_campus=i.under_campus,
                                     under_institute=i.under_institute,
                                     is_ug=i.is_ug,
                                     passing_year=year)

        val = GraduatesWithPrograms.objects.filter(passing_year='2022')
        for i in val:
            GraduatesWithPrograms.objects.create(
                under_campus=i.under_campus,
                under_institute=i.under_institute,
                is_ug=i.is_ug,
                program=i.program,
                passing_year=year)
        response_data = {}
        response_data['result'] = 'success'
        response_data['message'] = 'worked well'

        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")
    except Exception as e:
        response_data = {}
        response_data['result'] = 'error'
        response_data['message'] = 'Some error message'

        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")

# class HighlightsView(generics.ListAPIView):
#     serializer_class = HighlightsSerializer
#     permission_classes = (IsAuthenticated, )
    
#     def get(self, request, year):
#         try:
#             data = Highlights.objects.filter(passing_year=year)
#             responce_data = HighlightsSerializer(data, many=True).data
#             return response.Response({'status': 'OK', 'result': responce_data})
#         except Exception as e:
#             return response.Response({
#                 'status': 'Error',
#                 'result': str(e)
#             },
#                                      status=HTTP_400_BAD_REQUEST)