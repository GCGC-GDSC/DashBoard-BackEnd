from django.db import models

# Create your models here.
class Branch(models.Model):
    Branch_name = models.CharField(max_length=10, default="")

class companies_stats(models.Model):
    companies_visited = models.IntegerField(default=0)
    companies_yet_to_visit = models.IntegerField(default=0)
    results_pending = models.IntegerField(default=0)

class UnderGraduates(companies_stats):
    under_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)

class PostGraduates(companies_stats):
    under_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
# --------------------------------------------------------------------------------------------------
class Company(models.Model):
    name_of_the_company = models.CharField(max_length=50, default="")
    profile_offered = models.CharField(max_length=50, default="")
    package = models.DecimalField(max_digits=5, decimal_places=2)

class Git(Company):
    CSE = models.IntegerField(default=0)
    IT = models.IntegerField(default=0)
    ECE = models.IntegerField(default=0)
    EEE = models.IntegerField(default=0)
    Mech = models.IntegerField(default=0)
    Civil = models.IntegerField(default=0)
    Bio = models.IntegerField(default=0)

    @property
    def total_no_of_seats(self):
        return self.CSE + self.IT + self.ECE + self.EEE + self.Mech + self.Civil + self.Bio

class Gis(Company):
    MSc_chemistry_analytics = models.IntegerField(default=0)
    MSc_chemistry_organic = models.IntegerField(default=0)
    BSc_Chemistry_Honors = models.IntegerField(default=0)
    Computer_Science_BCA = models.IntegerField(default=0)
    Computer_Science_MCA_3years = models.IntegerField(default=0)
    Computer_Science_MCA_2years = models.IntegerField(default=0)
    Biotechnology_MSc = models.IntegerField(default=0)
    Microbiology_MSc = models.IntegerField(default=0)
    Food_Science_Technology_MSc = models.IntegerField(default=0)
    Food_Science_Technology_BSc_Hons = models.IntegerField(default=0)
    Math_MSc = models.IntegerField(default=0)
    Math_MSc_Statistics = models.IntegerField(default=0)
    Math_BSc = models.IntegerField(default=0)
    BioChemisty_Msc = models.IntegerField(default=0)
    Enviromental_MSc = models.IntegerField(default=0)
    Enviromental_BEM = models.IntegerField(default=0)
    Physics_and_Electronics_MSc = models.IntegerField(default=0)
    Physics_and_Electronics_MPC = models.IntegerField(default=0)
    Physics_and_Electronics_MPCS = models.IntegerField(default=0)
    Physics_and_Electronics_MECS = models.IntegerField(default=0)
    BioTechnology_BSc = models.IntegerField(default=0)
    Interg_Biotecchnology_MSc = models.IntegerField(default=0)

    @property
    def total(self):
        return (self.MSc_chemistry_analytics +
                self.MSc_chemistry_organic +
                self.BSc_Chemistry_Honors +
                self.Computer_Science_BCA +
                self.Computer_Science_MCA_3years +
                self.Computer_Science_MCA_2years +
                self.Biotechnology_MSc +
                self.Microbiology_MSc +
                self.Food_Science_Technology_MSc +
                self.Food_Science_Technology_BSc_Hons +
                self.Math_MSc +
                self.Math_MSc_Statistics +
                self.Math_BSc +
                self.BioChemisty_Msc +
                self.Enviromental_MSc +
                self.Enviromental_BEM +
                self.Physics_and_Electronics_MSc +
                self.Physics_and_Electronics_MPC +
                self.Physics_and_Electronics_MPCS +
                self.Physics_and_Electronics_MECS +
                self.BioTechnology_BSc +
                self.Interg_Biotecchnology_MSc )

class Pharmacy(Company):
    B_Pharmacy = models.IntegerField(default=0)
    M_Pharmacy_Pharmaceutical_Analysis = models.IntegerField(default=0)
    M_Pharmacy_Pharmacology = models.IntegerField(default=0)
    M_Pharmacy_Quality_Assurance = models.IntegerField(default=0)
    M_Pharmacy_Pharmaceutical_Chemistry = models.IntegerField(default=0)
    M_Pharmacy_Pharmaceutics = models.IntegerField(default=0)

    @property
    def total(self):
        return (self.B_Pharmacy +
                self.M_Pharmacy_Pharmaceutical_Analysis +
                self.M_Pharmacy_Pharmacology +
                self.M_Pharmacy_Quality_Assurance +
                self.M_Pharmacy_Pharmaceutical_Chemistry +
                self.M_Pharmacy_Pharmaceutics)

class Gim_BBA_BCOM(Company):
    BBA = models.IntegerField(default=0)
    BCOM = models.IntegerField(default=0)
    BBA_Logistics = models.IntegerField(default=0)
    BBA_Business_Analytics = models.IntegerField(default=0)

    @property
    def total(self):
        return (self.BBA +
                self.BCOM +
                self.BBA_Logistics +
                self.BBA_Business_Analytics)

class Gim_MBA(Company):
    MBA_Finance = models.IntegerField(default=0)
    MBA_HR = models.IntegerField(default=0)
    MBA_Marketing = models.IntegerField(default=0)
    MBA_IB = models.IntegerField(default=0)
    MBA = models.IntegerField(default=0)

    @property
    def total(self):
        return (self.MBA_Finance +
                self.MBA_HR +
                self.MBA_Marketing +
                self.MBA_IB +
                self.MBA)

