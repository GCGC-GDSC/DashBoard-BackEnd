from django.db import models

# Create your models here.

class Campus(models.Model):
	camp = models.CharField(max_length=30)
	inst_cnt = models.IntegerField(default=0)

	def __str__(self):
		return self.camp 

class Institue(models.Model):
	inst = models.CharField(max_length=30)
	under_camp = models.ForeignKey(Campus, on_delete=models.CASCADE)

	def __str__(self):
		return self.inst

		# META 
		# Model intneritance

# Model intneritance
# class Graduates(models.Model):
# 	total_no_of_students = models.IntegerField(default=0)
# 	total_no_of_final_year_students = models.IntegerField(default=0)
# 	total_no_of_students_opt_higher_study_and_pay_crt = models.IntegerField(default=0)

class UnderGraduates(models.Model):
	total_no_of_students = models.IntegerField(default=0)
	total_no_of_final_year_students = models.IntegerField(default=0)
	total_no_of_students_opt_higher_study_and_pay_crt = models.IntegerField(default=0)
	under_inst = models.ForeignKey(Institue, on_delete=models.CASCADE)

class PostGraduates(models.Model):
	total_no_of_students = models.IntegerField(default=0)
	total_no_of_final_year_students = models.IntegerField(default=0)
	total_no_of_students_opt_higher_study_and_pay_crt = models.IntegerField(default=0)
	under_inst = models.ForeignKey(Institue, on_delete=models.CASCADE)