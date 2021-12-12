from django.db import models
from students.models import Institute

"""class Branch(models.Model):
    Branch_name = models.CharField(max_length=10, default="")

class companies_stats(models.Model):
    companies_visited = models.IntegerField(default=0)
    companies_yet_to_visit = models.IntegerField(default=0)
    results_pending = models.IntegerField(default=0)

class UnderGraduates(companies_stats):
    under_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)

class PostGraduates(companies_stats):
    under_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
# --------------------------------------------------------------------------------------------------"""



class Courses(models.Model):
    course_name = models.CharField(max_length=30, default="", unique=True)
    institue = models.ForeignKey(Institute, null=True, on_delete=models.CASCADE)
    is_ug = models.BooleanField(default=True)

    def __str__(self):
        grad = "UG"
        if(not self.is_ug):
            grad = "PG"
        return self.course_name + " " + self.institue.name +" " + grad

class Company(models.Model):
    name_of_the_company = models.CharField(max_length=50, default="")
    profile_offered = models.CharField(max_length=50, default="")
    package = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name_of_the_company


class CompanyCousesPlaced(models.Model):
    company_id = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    courses_id = models.ForeignKey(Courses, null=True, on_delete=models.CASCADE)
    placed_count = models.IntegerField(default=-1)

    def __str__(self):
        return self.company_id.name_of_the_company+" - "+self.courses_id.course_name

    class Meta:
        ordering = ['company_id']


# ------------------------------------------------------------------------------------------------------

class Git_ug(Company):
    CSE = models.IntegerField(default=-1)
    IT = models.IntegerField(default=-1)
    ECE = models.IntegerField(default=-1)
    EEE = models.IntegerField(default=-1)
    Mech = models.IntegerField(default=-1)
    Civil = models.IntegerField(default=-1)
    Bio = models.IntegerField(default=-1)

    @property
    def total_no_of_seats(self):
        return self.CSE + self.IT + self.ECE + self.EEE + self.Mech + self.Civil + self.Bio

class Git_pg(Company):
    CST = models.IntegerField(default=-1)
    CFIS = models.IntegerField(default=-1)
    DS = models.IntegerField(default=-1)
    VSLI = models.IntegerField(default=-1)
    PSA = models.IntegerField(default=-1)
    MD = models.IntegerField(default=-1)
    MTA = models.IntegerField(default=-1)

    @property
    def total_no_of_seats(self):
        return self.CST + self.CFIS + self.DS + self.VSLI + self.PSA + self.MD + self.MTA


class Gis_ug(Company):
    BSc_Chemistry_Honors = models.IntegerField(default=-1)
    Computer_Science_BCA = models.IntegerField(default=-1)
    Food_Science_Technology_BSc_Hons = models.IntegerField(default=-1)
    Math_BSc = models.IntegerField(default=-1)
    Enviromental_BEM = models.IntegerField(default=-1)
    BioTechnology_BSc = models.IntegerField(default=-1)

    @property
    def total(self):
        return (self.BSc_Chemistry_Honors +
                self.Computer_Science_BCA +
                self.Food_Science_Technology_BSc_Hons +
                self.Math_BSc +
                self.Enviromental_BEM +
                self.BioTechnology_BSc)

class Gis_pg(Company):
    MSc_chemistry_analytics = models.IntegerField(default=-1)
    MSc_chemistry_organic = models.IntegerField(default=-1)
    Computer_Science_MCA_3years = models.IntegerField(default=-1)
    Computer_Science_MCA_2years = models.IntegerField(default=-1)
    Biotechnology_MSc = models.IntegerField(default=-1)
    Microbiology_MSc = models.IntegerField(default=-1)
    Food_Science_Technology_MSc = models.IntegerField(default=-1)
    Math_MSc = models.IntegerField(default=-1)
    Math_MSc_Statistics = models.IntegerField(default=-1)
    BioChemisty_Msc = models.IntegerField(default=-1)
    Enviromental_MSc = models.IntegerField(default=-1)
    Physics_and_Electronics_MSc = models.IntegerField(default=-1)
    Physics_and_Electronics_MPC = models.IntegerField(default=-1)
    Physics_and_Electronics_MPCS = models.IntegerField(default=-1)
    Physics_and_Electronics_MECS = models.IntegerField(default=-1)
    Interg_Biotecchnology_MSc = models.IntegerField(default=-1)

    @property
    def total(self):
        return (self.MSc_chemistry_analytics +
                self.MSc_chemistry_organic +
                self.Computer_Science_MCA_3years +
                self.Computer_Science_MCA_2years +
                self.Biotechnology_MSc +
                self.Microbiology_MSc +
                self.Food_Science_Technology_MSc +
                self.Math_MSc +
                self.Math_MSc_Statistics +
                self.BioChemisty_Msc +
                self.Enviromental_MSc +
                self.Physics_and_Electronics_MSc +
                self.Physics_and_Electronics_MPC +
                self.Physics_and_Electronics_MPCS +
                self.Physics_and_Electronics_MECS +
                self.Interg_Biotecchnology_MSc)


class Pharmacy(Company):
    B_Pharmacy = models.IntegerField(default=-1)
    M_Pharmacy_Pharmaceutical_Analysis = models.IntegerField(default=-1)
    M_Pharmacy_Pharmacology = models.IntegerField(default=-1)
    M_Pharmacy_Quality_Assurance = models.IntegerField(default=-1)
    M_Pharmacy_Pharmaceutical_Chemistry = models.IntegerField(default=-1)
    M_Pharmacy_Pharmaceutics = models.IntegerField(default=-1)

    @property
    def total(self):
        return (self.B_Pharmacy +
                self.M_Pharmacy_Pharmaceutical_Analysis +
                self.M_Pharmacy_Pharmacology +
                self.M_Pharmacy_Quality_Assurance +
                self.M_Pharmacy_Pharmaceutical_Chemistry +
                self.M_Pharmacy_Pharmaceutics)

class Gim_BBA_BCOM(Company):
    BBA = models.IntegerField(default=-1)
    BCOM = models.IntegerField(default=-1)
    BBA_Logistics = models.IntegerField(default=-1)
    BBA_Business_Analytics = models.IntegerField(default=-1)

    @property
    def total(self):
        return (self.BBA +
                self.BCOM +
                self.BBA_Logistics +
                self.BBA_Business_Analytics)

class Gim_MBA(Company):
    MBA_Finance = models.IntegerField(default=-1)
    MBA_HR = models.IntegerField(default=-1)
    MBA_Marketing = models.IntegerField(default=-1)
    MBA_IB = models.IntegerField(default=-1)
    MBA = models.IntegerField(default=-1)

    @property
    def total(self):
        return (self.MBA_Finance +
                self.MBA_HR +
                self.MBA_Marketing +
                self.MBA_IB +
                self.MBA)

