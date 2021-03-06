from django.db import models
from django_countries import CountryField
from django.contrib.auth.models import User

class NewsUpdate(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=30) #TODO: Link to admin/editor users
    
    def __unicode__(self):
        return self.title
    
#--------------------------------------

class CodeInfoResource(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.value
    
class InfoResource(models.Model):
    name = models.CharField(max_length=40)
    website = models.URLField()
    type = models.ForeignKey(CodeInfoResource)
    
    def __unicode__(self):
        return self.name

#--------------------------------------

class CodeFundingSourceType(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=40)
    is_grant = models.BooleanField()
    
    def __unicode__(self):
        return self.value

class CodeMonth(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.value

class CodeProximity(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.value

class CodeRegion(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.value

class CodeElevation(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.value

class CodeTopography(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.value

class CodeProjType(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.value

class CodeProfession(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.value
    
class CodeClimateZone(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=30)
    description = models.CharField(max_length=256, null=True, blank=True) #TODO: Add desc to initial_data 
    
    def __unicode__(self):
        return self.value
    
class CodePrecipLevel(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.value

class CodeUrbanRural(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.value
    
class CodePplServed(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.value

class CodeWaterMgmtLevel(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.value

class CodeSoilType(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.value

class Keyword(models.Model):
    value = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.value
    
    class Meta:
        verbose_name="Keyword"
        verbose_name_plural="Keywords"

class Resource(models.Model):
    proximity = models.ForeignKey(CodeProximity)   

    class Meta:
        abstract = True

class ContactInfo(models.Model):
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    add_street1 = models.CharField(max_length=80, verbose_name="Street",
                                   null=True, blank=True)
    add_street2 = models.CharField(max_length=80, verbose_name="Street 2",
                                   null=True, blank=True)
    add_city = models.CharField(max_length=80, verbose_name="City",
                                null=True, blank=True)
    add_state_prov = models.CharField(max_length=30,
                                      verbose_name="State/Province",
                                      null=True, blank=True)
    add_code = models.CharField(max_length=20, verbose_name="Postal Code",
                                null=True, blank=True)
    add_country = CountryField(verbose_name="Country",
                               null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    
    class Meta:
        abstract = True
     
class Project(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    goal = models.CharField(max_length=768)
    proj_mgmt = models.TextField(verbose_name="Project Management")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    keywords = models.ManyToManyField(Keyword, null=True, blank=True)
    owner = models.ForeignKey(User, null=True) #TODO: How to do initial data?
    proj_types = models.ManyToManyField(CodeProjType,
                            verbose_name="Project Type", null=True, blank=True)
    
    reviewed = models.BooleanField()
    #TODO: material_res with near/close/far/very far checkboxes
    #TODO: infra_res
    #TODO: natural_res
    #TODO: retail_res
    #TODO: transpo_res
    
    #TODO: funding_sources
    #TODO: images/gallery
    #TODO: documents  class Document: title, blob, summary, type fk, project fk
    
    def __unicode__(self):
        return self.title

class Organization(ContactInfo):
    name = models.CharField(max_length=40)
    notes = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project)
    
    def __unicode__(self):
        return self.name        
        
class FundingSource(models.Model):
    #TODO: Initial data
    
    type = models.ForeignKey(CodeFundingSourceType)
    name = models.CharField(max_length=40, null=True, blank=True) #Only necessary if CodeFundingSource.is_grant=True
    percent = models.IntegerField() #Between 0-100  
    amount = models.IntegerField(null=True, blank=True)
    project = models.ForeignKey(Project)
    
    def __unicode__(self):
        return "%s - %s\%" % (self.source_type, self.percent)      
        
class GeoConditions(models.Model):
    soil_type = models.ForeignKey(CodeSoilType)
    description = models.TextField(null=True, blank=True)
    hit_bedrock = models.BooleanField()
    hit_water_table = models.BooleanField()
    geo_impact = models.TextField(
        verbose_name="Impact of Geological Conditions", null=True, blank=True)
    project = models.ForeignKey(Project, unique=True)
    
    def __unicode__(self):
        return "%s - %s" % (self.id, self.soil_type)
    
    class Meta:
        verbose_name="Geological Conditions"
        verbose_name_plural="Geological Conditions"
        

class Location(models.Model):
    name = models.CharField(max_length=60)
    state_prov = models.CharField(max_length=24, verbose_name="Province/State")
    country = CountryField()
    region = models.ForeignKey(CodeRegion)
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.ForeignKey(CodeElevation)
    topography = models.ForeignKey(CodeTopography)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, unique=True)
    
    def __unicode__(self):
        return "%s - %s (%s)" % (self.id, self.name, self.country.name)

class CommunityInfo(models.Model):
    urban_rural = models.ForeignKey(CodeUrbanRural, verbose_name="Urban/Rural")
    description = models.TextField()
    num_ppl_served = models.ForeignKey(CodePplServed,
                                       verbose_name="Number of People Served")
    community_size = models.PositiveIntegerField()
    water_mgmt_level = models.ForeignKey('CodeWaterMgmtLevel',
                                         verbose_name="Water Management Level")
    project = models.ForeignKey(Project, unique=True)
    
    def __unicode__(self):
        return "%s - Served: %s | Size: %s" % (self.id,
                                               self.num_ppl_served.value,
                                               self.community_size)

    class Meta:
        verbose_name = "Community Information"
        verbose_name_plural = "Community Information"

class Climate(models.Model):
    climate_zone = models.ForeignKey(CodeClimateZone)
    precipitation = models.ForeignKey(CodePrecipLevel)
    has_rainy_season = models.BooleanField()
    rainy_months = models.ManyToManyField(CodeMonth, null=True, blank=True)
    project = models.ForeignKey(Project, unique=True)
    
    def __unicode__(self):
        return "%s - %s | %s Precipitation" % (self.id,
                                               self.climate_zone.value,
                                               self.precipitation.value)
        
class HumanResContact(ContactInfo):
    given_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    surname = models.CharField(max_length=30)
    type = models.ForeignKey(CodeProfession, verbose_name="Profession")
    other_type = models.CharField(max_length='30',
                                  verbose_name="Profession (if other)",
                                  null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project)
    
    def __unicode__(self):
        return "%s %s - %s" % (self.given_name, self.surname, self.type.value)
        
    class Meta:
        verbose_name = "Human Resources Contact"
        verbose_name_plural = "Human Resources Contacts"
    
class ProjectContact(ContactInfo): 
    given_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    surname = models.CharField(max_length=30)
    project = models.ForeignKey(Project)
    
    def __unicode__(self):
        return "%s %s" % (self.given_name, self.surname)
    
class FeaturedProject(models.Model):
    project = models.ForeignKey(Project)
    created = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=280)
    
    def __unicode__(self):
        return self.project.title

