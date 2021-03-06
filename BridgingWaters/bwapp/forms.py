import datetime

from django import forms
# Use FormWizard to split form across multiple pages
# https://docs.djangoproject.com/en/1.3/ref/contrib/formtools/form-wizard/
from django.forms.extras.widgets import SelectDateWidget
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard import FormWizard
from django_countries import countries
from django.core.exceptions import ValidationError

import bwapp.models as models

now = datetime.datetime.now()
YEARS = [str(i) for i in range(1980,now.year+1)]
YEARS.reverse()

EMPTY_CHOICE = (None,'- - - -') #REMOVE
EMPTY_LABEL = "- - - -"

PROJ_TYPES = [(obj.code, obj.value) for obj in models.CodeProjType.objects.all()]

YES_NO = [('False','No'),('True','Yes')]

EXISTING_KEYWORDS = [(obj.id, obj.value) for obj in models.Keyword.objects.all()]

MONTHS = ((1,'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),
    (6,'June'),(7,'July'),(8,'August'),(9,'September'),(10,'October'),
    (11,'November'),(12,'December'),)
    
class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(widget=SelectDateWidget(years=YEARS),
        label="Start Date")
    end_date = forms.DateField(widget=SelectDateWidget(years=YEARS),
        label="End Date")
    goal = forms.CharField(max_length=768, label='Project Goal', 
        widget=forms.TextInput(attrs={'size':'70'}))
    proj_mgmt = forms.CharField(widget=forms.Textarea,
                                label='Project Management Description',
                                help_text='Describe how your project was managed.')
    proj_types = forms.MultipleChoiceField (
        widget=forms.CheckboxSelectMultiple,
        label='Project Type',
        help_text='Select all that apply. At least one is required.',
        choices=PROJ_TYPES)
    
    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        if end_date < start_date:
            raise forms.ValidationError(u"End date must be after start date.")
        return end_date
    
    class Meta:
        model = models.Project
        exclude = ('reviewed', 'keywords',) #TODO: Add keywords
        widgets = {
            'title' : forms.TextInput(attrs={'class':'title'}),
            'goal' : forms.TextInput(attrs={'size':'70'}),
        }
    
class LocationForm(forms.ModelForm):
    
    name = forms.CharField(max_length=60, label='Location Name',
        help_text="Name of community/village/area/etc.",
        widget=forms.TextInput(attrs={'class':'title'}))
    country = forms.ChoiceField(widget=forms.Select,
        choices=countries.COUNTRIES) #TODO: Maybe restrict to countries in the selected region
    region = forms.ModelChoiceField(queryset=models.CodeRegion.objects.all(), 
        empty_label=EMPTY_LABEL)
    latitude = forms.FloatField() #TODO: Some kind of google map interface to find location?
    longitude = forms.FloatField()
    #TODO: have region automatically populate in the db, based on country?
    elevation = forms.ModelChoiceField(queryset=models.CodeElevation.objects.all(), 
        empty_label=EMPTY_LABEL)
    topography = forms.ModelChoiceField(queryset=models.CodeTopography.objects.all(), 
        empty_label=EMPTY_LABEL)
    description = forms.CharField(widget=forms.Textarea, required=False,
                                  help_text='Describe the location.')
    
    class Meta:
        model = models.Location
        exclude = ('project',) 

class ClimateForm(forms.ModelForm):
    climate_zone = forms.ModelChoiceField(queryset=models.CodeClimateZone.objects.all(), 
        empty_label=EMPTY_LABEL,
        label="Climate Zone")
    precipitation = forms.ModelChoiceField(queryset=models.CodePrecipLevel.objects.all(), 
        empty_label=EMPTY_LABEL)
    has_rainy_season = forms.ChoiceField(widget=forms.Select, choices=YES_NO,
        label="Has Rainy Season?",
        help_text="Is there a wet season in your project location?")
    rainy_months = forms.ModelMultipleChoiceField(
        queryset=models.CodeMonth.objects.all().order_by('code'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Rainy Months",
        help_text="Select the months during which the wet season occurs.")
        
    #def clean_rainy_months(self):
    #    if not self.cleaned_data['has_rainy_season']:
    #        return None #return empty list if No was selected 
        
    class Meta:
        model = models.Climate
        exclude = ('project',)

class CommunityInfoForm(forms.ModelForm):
    num_ppl_served = forms.ModelChoiceField(
        queryset=models.CodePplServed.objects.all(), 
        empty_label=EMPTY_LABEL,
        label="Number of People Served",
        help_text="Number of people directly served by the project.")
    community_size = forms.IntegerField(label="Community Size",
        help_text="Total population of community.")
    urban_rural = forms.ModelChoiceField(
        queryset=models.CodeUrbanRural.objects.all(), 
        empty_label=EMPTY_LABEL,
        label="Urban/Rural")
    water_mgmt_level = forms.ModelChoiceField(
        queryset=models.CodeWaterMgmtLevel.objects.all(), 
        empty_label=EMPTY_LABEL,
        label="Water Management Level",
        help_text="Level of government at which water is managed.")
    description = forms.CharField(widget=forms.Textarea,
        help_text="Describe the community.") #TODO: Add more direction for what is wanted here
    
    class Meta:
        fields = ('num_ppl_served','community_size','urban_rural','water_mgmt_level','description')
        model = models.CommunityInfo
        exclude = ('project',)
        
class GeoConditionsForm(forms.ModelForm):
    soil_type = forms.ModelChoiceField(
        queryset=models.CodeSoilType.objects.all(), 
        empty_label=EMPTY_LABEL,
        label="Primary Soil Type",
        help_text="Select the soil type most prevalent in your project area.")
    description = forms.CharField(widget=forms.Textarea, required=False,
        help_text="Describe the geological and soil conditions of your project area.")
    hit_bedrock = forms.ChoiceField(widget=forms.Select, choices=YES_NO,
        label="Hit Bedrock?",
        help_text="Did you encounter bedrock while implementing your project?")
    hit_water_table = forms.ChoiceField(widget=forms.Select, choices=YES_NO,
        label="Hit Water Table?",
        help_text="Did you encounter the water table while implementing your project?")
    geo_impact = forms.CharField(widget=forms.Textarea, required=False,
        label="Impact of Geological Conditions",
        help_text="Describe how the geological and soil conditions impacted your project.")
    
    class Meta:
        model = models.GeoConditions
        exclude = ('project',)
        
class OrganizationForm(forms.ModelForm):
    name = forms.CharField(max_length=40, label='Organization Name', 
        widget=forms.TextInput(attrs={'class':'title'}))
    add_street1 = forms.CharField(max_length=80, label="Street Address")
    add_street2 = forms.CharField(max_length=80, label="Street Address 2",
                                  required=False)
    add_city = forms.CharField(max_length=80, label="City")
    add_state_prov = forms.CharField(max_length=30, label="State/Province")
    add_code = forms.CharField(max_length=20, label="Postal Code")
    add_country = forms.ChoiceField(widget=forms.Select, label="Country",
                                    choices=countries.COUNTRIES,
                                    initial="US")
    notes = forms.CharField(widget=forms.Textarea, required=False)
    
    #TODO: Validation that at least one contact method is required.
    
    class Meta:
        model = models.Organization
        fields = ('name', 'phone', 'email', 'website', 'add_street1',
                    'add_street2', 'add_city', 'add_state_prov', 'add_code',
                    'add_country', 'notes')
        exclude = ('project',)

class ProjectContactForm(forms.ModelForm):
    given_name = forms.CharField(max_length=30, label="Given Name")
    middle_name = forms.CharField(max_length=30, required=False, 
        label="Middle Name/Initial")
    add_street1 = forms.CharField(max_length=80, label="Street Address")
    add_street2 = forms.CharField(max_length=80, label="Street Address 2",
                                  required=False)
    add_city = forms.CharField(max_length=80, label="City")
    add_state_prov = forms.CharField(max_length=30, label="State/Province")
    add_code = forms.CharField(max_length=20, label="Postal Code")
    add_country = forms.ChoiceField(widget=forms.Select, label="Country",
                                    choices=countries.COUNTRIES)
    
    class Meta:
        model = models.ProjectContact
        fields = ('given_name', 'middle_name', 'surname', 'phone', 'email', 
                    'add_street1', 'add_street2', 'add_city', 'add_state_prov', 
                    'add_code','add_country')
        exclude = ('project', 'website')

class HumanResourceContactForm(forms.ModelForm):
    given_name = forms.CharField(max_length=30, label="Given Name")
    middle_name = forms.CharField(max_length=30, required=False, 
        label="Middle Name/Initial")
    
    type = forms.ModelChoiceField(
        queryset=models.CodeProfession.objects.all(), 
        empty_label=EMPTY_LABEL)
    
    #TODO: Hide the label and help_text also
    other_type = forms.CharField(max_length=30, required=False, 
        label="Profession (other)",
        help_text="Please input a profession if you selected 'Other'",
        widget=forms.TextInput(attrs={'class':''})) #TODO: class jsHide
    
    add_street1 = forms.CharField(max_length=80, label="Street Address",
                                   required=False)
    add_street2 = forms.CharField(max_length=80, label="Street Address 2",
                                  required=False)
    add_city = forms.CharField(max_length=80, label="City", required=False)
    add_state_prov = forms.CharField(max_length=30, label="State/Province",
                                   required=False)
    add_code = forms.CharField(max_length=20, label="Postal Code", required=False)
    add_country = forms.ChoiceField(widget=forms.Select, label="Country",
                                    choices=countries.COUNTRIES,
                                    required=False)
    notes = forms.CharField(widget=forms.Textarea, required=False)
    
    def clean_other_type(self):
        if self.cleaned_data['type'] == 10: #Code for other
            if self.cleaned_data['other_type'].length == 0:
                raise forms.ValidationError(u"If 'other' is selected, a profession must be entered.")
        return self.cleaned_data['other_type']
    
    class Meta:
        model = models.ProjectContact
        fields = ('given_name', 'middle_name', 'surname', 'phone', 'email',
                    'type', 'other_type', 'add_street1', 'add_street2', 
                    'add_city', 'add_state_prov', 'add_code','add_country',
                    'notes')
        exclude = ('project', 'website',)
