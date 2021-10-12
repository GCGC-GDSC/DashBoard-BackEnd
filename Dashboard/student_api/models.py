from django.db import models
# Create your models here.

class Campus(models.Model):
	campus_name = models.CharField(max_length=30,default="")
	institue_count = models.IntegerField(default=0)

	def __str__(self):
		return self.campus_name+" 'Campus"

class Institue(models.Model):
	institute_name = models.CharField(max_length=10,default="")
	under_campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

	def __str__(self):
		return self.institute_name + f" ({str(self.under_campus)}) "

class Graduates(models.Model):
	total_students = models.IntegerField(default=0)
	total_final_years = models.IntegerField(default=0)
	total_higher_study_and_pay_crt = models.IntegerField(default=0)
	total_not_intrested_in_placments = models.IntegerField(default=0)
	total_backlogs = models.IntegerField(default=0)

	@property
	def total_students_eligible(self):
		return self.total_final_years-(self.total_backlogs+self.total_not_intrested_in_placments)

	total_offers = models.IntegerField(default=0)
	total_multiple_offers = models.IntegerField(default=0)

	@property
	def total_placed(self):
		return self.total_offers-self.total_multiple_offers

	@property
	def total_yet_to_place(self):
		return self.total_students_eligible-self.total_placed

	highest_salary = models.DecimalField(max_digits = 5, decimal_places = 2, default=0.0)
	average_salary = models.DecimalField(max_digits = 5, decimal_places = 2, default=0.0)
	lowest_salary = models.DecimalField(max_digits = 5, decimal_places = 2, default=0.0)

	def __str__(self):
		return 'Grad'

class UnderGraduates(Graduates):
	under_institute = models.ForeignKey(Institue, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return 'UG: '+str(self.under_institute)


class PostGraduates(Graduates):
	under_institute = models.ForeignKey(Institue, on_delete=models.CASCADE, null=True)
	
	def __str__(self):
		return 'PG '+str(self.under_institute)