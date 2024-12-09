from django.db import models
# from UserManagement.models import company
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from datetime import timedelta,timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save
from datetime import datetime
import re
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from .utils import send_dynamic_email
from email.utils import formataddr
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.contrib.sites.models import Site
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template import Context, Template
import uuid
import random
import string
import json
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives,get_connection, send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.apps import apps

#EmpManagement
class emp_master(models.Model):    
    GENDER_CHOICES = [ ("M", "Male"), ("F", "Female"),("O", "Other"),]
    MARITAL_STATUS_CHOICES = [("M", "Married"),("S", "Single"),('divorced','divorced'),('widow','widow')]
    
    emp_code                 = models.CharField(max_length=50,unique=True,null=True,blank =True)
    emp_first_name           = models.CharField(max_length=50,null=True,blank =True)
    emp_last_name            = models.CharField(max_length=50,null=True,blank =True)
    emp_gender               = models.CharField(max_length=20,choices=GENDER_CHOICES,null=True,blank =True)
    emp_date_of_birth        = models.DateField(null=True,blank =True)
    emp_personal_email       = models.EmailField(unique=True,null=True,blank =True)
    emp_company_email        = models.EmailField(unique=True,null=True,blank =True)
    emp_mobile_number_1      = models.CharField(null=True,blank =True)
    emp_mobile_number_2      = models.CharField(null=True,blank =True)
    emp_reporting_manager    = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    emp_country_id           = models.ForeignKey("Core.cntry_mstr",on_delete = models.CASCADE,null=True,blank =True)
    emp_state_id             = models.ForeignKey("Core.state_mstr",on_delete=models.CASCADE,null=True,blank =True)
    emp_city                 = models.CharField(max_length=50,null=True,blank =True)
    emp_permenent_address    = models.CharField(max_length=200,null=True,blank =True)
    emp_present_address      = models.CharField(max_length=200,blank=True,null=True)
    emp_status               = models.BooleanField(default=True,null=True,blank =True)
    emp_joined_date          = models.DateField(null=True,blank =True)
    emp_date_of_confirmation = models.DateField(null=True,blank=True)
    emp_relegion             = models.CharField(max_length=50,null=True,blank =True)
    emp_profile_pic          = models.ImageField(null=True,blank =True )
    emp_blood_group          = models.CharField(max_length=50,blank=True)
    emp_nationality          = models.CharField(null=True,blank =True)
    emp_marital_status       = models.CharField(max_length=10,choices=MARITAL_STATUS_CHOICES,null=True,blank =True)
    emp_father_name          = models.CharField(max_length=50,null=True,blank =True)
    emp_mother_name          = models.CharField(max_length=50,null=True,blank =True)
    created_at               = models.DateTimeField(auto_now_add=True,null=True,blank =True)
    created_by               = models.ForeignKey('UserManagement.CustomUser', on_delete=models.CASCADE, null=True,  related_name='emp_created_by1')
    updated_at               = models.DateTimeField(auto_now=True,null=True,blank =True)
    updated_by               = models.ForeignKey('UserManagement.CustomUser', on_delete=models.CASCADE, null=True, related_name='emp_updated_by1')
    is_active                = models.BooleanField(default=True,null=True,blank =True)
    epm_ot_applicable        = models.BooleanField(default=False,null=True,blank =True)
    is_ess                   = models.BooleanField(default=False)
    emp_branch_id            = models.ForeignKey("OrganisationManager.brnch_mstr",on_delete = models.CASCADE,null=True,blank =True)
    emp_dept_id              = models.ForeignKey("OrganisationManager.dept_master",on_delete = models.CASCADE,null=True,blank =True)
    emp_desgntn_id           = models.ForeignKey("OrganisationManager.desgntn_master",on_delete = models.CASCADE,null=True,blank =True)
    emp_ctgry_id             = models.ForeignKey("OrganisationManager.ctgry_master",on_delete = models.CASCADE,null=True,blank =True)
    emp_weekend_calendar     = models.ForeignKey("calendars.weekend_calendar",on_delete = models.CASCADE,null=True,blank =True)
    holiday_calendar         = models.ForeignKey("calendars.holiday_calendar",on_delete = models.CASCADE,null=True,blank =True)
    users                    = models.ForeignKey('UserManagement.CustomUser', on_delete=models.CASCADE, related_name='employees',null=True,blank =True)
    
    def save(self, *args, **kwargs):
        from UserManagement.models import company
        created = not self.pk  # Check if the instance is being created for the first time
        super().save(*args, **kwargs)

        if created and self.is_ess:  # Check if is_ess is True before creating the user
            # Create a new user with default password
            user_model = get_user_model()
            username = self.emp_code
            password = 'admin'  # You can set a default password here
            email = self.emp_personal_email
            # Get the tenant_id from the request or context
            schema_name = connection.schema_name
            # Fetch the company instance based on the schema name
            try:
                company_instance = company.objects.get(name=schema_name)
            except company.DoesNotExist:
            # Handle the case where company instance does not exist for the schema
                company_instance = None
            # Create the user
            user = user_model.objects.create_user(username=username, email=email, password=password)
            # Link the user to the employee
            self.created_by = user
            if company_instance:
            # Set the tenant_id to the user using the set() method
                user.tenants.set([company_instance])
            else:
            # Handle the case where company instance is not found
                pass  # You can handle this according to your requirement
            # Set is_ess to True
            user.is_ess = True
            user.save()
            
    def __str__(self):
        return self.emp_code
    
    def get_custom_fields(self):
        return self.custom_fields.all()
    
    def get_attendance(self):
        from LeaveManagement.models import Attendance
        # Fetch approvals assigned to this user
        return Attendance.objects.filter(employee=self)

class Report(models.Model):
    file_name   = models.CharField(max_length=100,null=True,unique=True)
    report_data = models.FileField(upload_to='employee_report/', null=True, blank=True) 
    # created_at = models.DateTimeField(auto_now_add=True,null=True,blank =True)
    class Meta:
        permissions = (
            ('export_report', 'Can export report'),
            # Add more custom permissions here
        )
    
    
    def __str__(self):
        return self.file_name

class Doc_Report(models.Model):
    file_name   = models.CharField(max_length=100,null=True,unique=True)
    report_data = models.FileField(upload_to='document_report/', null=True, blank=True)
    class Meta:
        permissions = (
            ('export_document_report', 'Can export doc report'),
            # Add more custom permissions here
        )

    def __str__(self):
        return self.file_name

class GeneralRequestReport(models.Model):
    file_name   = models.CharField(max_length=100,null=True,unique=True)
    report_data = models.FileField(upload_to='general_report/', null=True, blank=True)
    class Meta:
        permissions = (
            ('export_general_request_report', 'Can export general request report'),
            # Add more custom permissions here
        )
    
    def __str__(self):
        return self.file_name

class Emp_CustomField(models.Model):
    FIELD_TYPES = (   
        ('dropdown', 'DropdownField'),
        ('radio', 'RadioButtonField'),
        ('date', 'DateField'),
        ('text', 'TextField'),
        ('checkbox', 'CheckboxField'),
    )
    # emp_master = models.ForeignKey(emp_master, on_delete=models.CASCADE, related_name='custom_fields',null=True)
    emp_custom_field = models.CharField(unique=True,max_length=100)  # Field name provided by end user
    data_type        = models.CharField(max_length=20, choices=FIELD_TYPES, null=True, blank=True)
    dropdown_values  = models.JSONField(null=True, blank=True)
    radio_values     = models.JSONField(null=True, blank=True)
    checkbox_values  = models.JSONField(null=True,blank=True)
    def __str__(self):
        return self.emp_custom_field    
    
    def clean(self):
        # Validate dropdown field values
        if self.data_type == 'dropdown':
            if self.dropdown_values:
                options = self.dropdown_values
                if  not  options:
                    raise ValidationError({'field_value': 'Select a value from the dropdown options.'})
            else:
                raise ValidationError({'field_value': 'provide value to the dropdown options.'})
        # Validate radio field values
        elif self.data_type == 'radio':
            if self.radio_values:
                options = self.radio_values
                if not  options:
                    raise ValidationError({'field_value': 'Select a value from the radio options.'})
            else:
                raise ValidationError({'field_value': 'provide value to the radio options.'})
        # Validate checkbox field values
        elif self.data_type == 'checkbox':
            if self.checkbox_values:
                options = self.checkbox_values
                if not  options:
                    raise ValidationError({'field_value': 'Select a value from the checkbox options.'})
            else:
                raise ValidationError({'field_value': 'provide value to the checkbox options.'})
    def save(self, *args, **kwargs):
        self.clean()  # Call clean to perform validation
        super().save(*args, **kwargs)
    

class Emp_CustomFieldValue(models.Model):
    emp_custom_field = models.CharField(max_length=100,null=True)
    field_value      = models.TextField(null=True, blank=True)  # Field value provided by end user
    emp_master       = models.ForeignKey('emp_master', on_delete=models.CASCADE, related_name='custom_field_values',null=True)

    def __str__(self):
        return f'{self.emp_custom_field.emp_custom_field}: {self.field_value}'

    def save(self, *args, **kwargs):
        if not self.emp_custom_field:
            raise ValueError("Field name cannot be None or empty.")
        if not Emp_CustomField.objects.filter(emp_custom_field=self.emp_custom_field).exists():
            raise ValueError(f"Field name '{self.emp_custom_field}' does not exist in Emp_CustomField.")

        # Check if a custom field value already exists for the same emp_master and emp_custom_field
        existing_value = Emp_CustomFieldValue.objects.filter(
            emp_custom_field=self.emp_custom_field,
            emp_master=self.emp_master
        ).first()

        if existing_value:
            # If it exists, update the existing record instead of creating a new one
            existing_value.field_value = self.field_value
            # Use update() to avoid calling save() and prevent recursion
            Emp_CustomFieldValue.objects.filter(
                id=existing_value.id
            ).update(field_value=self.field_value)
        else:
            # Call full_clean to ensure that the clean method is called
            self.full_clean()
            super().save(*args, **kwargs)

    def clean(self):
        # Retrieve the custom field object
        custom_field = Emp_CustomField.objects.filter(emp_custom_field=self.emp_custom_field).first()

        if not custom_field:
            raise ValidationError(f"Field name '{self.emp_custom_field}' does not exist in Emp_CustomField.")
        
        field_value = self.field_value

        if custom_field.data_type == 'dropdown':
            if custom_field.dropdown_values:
                options = custom_field.dropdown_values
                if not field_value or field_value not in options:
                    raise ValidationError({'field_value': 'Select a value from the dropdown options.'})
        
        elif custom_field.data_type == 'radio':
            if custom_field.radio_values:
                options = custom_field.radio_values
                if not field_value or field_value not in options:
                    raise ValidationError({'field_value': 'Select a value from the radio options.'})
       
        elif custom_field.data_type == 'checkbox':
            if custom_field.checkbox_values:
                options = custom_field.checkbox_values
                if not field_value or field_value not in options:
                    raise ValidationError({'field_value': 'Select a value from the checkbox options.'})


        elif custom_field.data_type == 'date':
            if field_value:
                try:
                    parts = field_value.split('-')
                    if len(parts) != 3:
                        raise ValueError
                    day, month, year = parts
                    formatted_date = f"{day.zfill(2)}-{month.zfill(2)}-{year}"
                    datetime.strptime(formatted_date, '%d-%m-%Y')
                except ValueError:
                    raise ValidationError({'field_value': 'Invalid date format. Date should be in DD-MM-YYYY format.'})
            else:
                raise ValidationError({'field_value': 'Date value is required.'})


#EMPLOYEE FAMILY(ef) data
class emp_family(models.Model):
    emp_id             = models.ForeignKey('emp_master',on_delete = models.CASCADE,null=True,blank=True, related_name='emp_family')
    ef_member_name     = models.CharField(max_length=50)
    emp_relation       = models.CharField(max_length=50)
    ef_company_expence = models.FloatField()
    ef_date_of_birth   = models.DateField()
    created_at         = models.DateTimeField(auto_now_add=True)
    created_by         = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    updated_at         = models.DateTimeField(auto_now=True)
    updated_by         = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')
    is_active          = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.ef_member_name

#EMPLOYEE FAMILY UDF
class EmpFamily_CustomField(models.Model):
    FIELD_TYPES = (
        ('dropdown', 'DropdownField'),
        ('radio', 'RadioButtonField'),)
    emp_family      = models.ForeignKey('emp_family', on_delete=models.CASCADE, related_name='fam_custom_fields')
    field_name      = models.CharField(max_length=100)  # Field name provided by end user
    field_value     = models.TextField(null=True, blank=True)  # Field value provided by end user
    data_type       = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values = models.JSONField(null=True, blank=True)
    radio_values    = models.JSONField(null=True, blank=True)
    

#EMPLOPYEE JOB HISTORY
class EmpJobHistory(models.Model):
    emp_id                          = models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_job_history')
    emp_jh_from_date                = models.DateField()
    emp_jh_end_date                 = models.DateField()
    emp_jh_company_name             = models.CharField(max_length=50)
    emp_jh_designation              = models.CharField(max_length=50)
    emp_jh_leaving_salary_permonth  = models.FloatField()
    emp_jh_reason                   = models.CharField(max_length=100)
    emp_jh_years_experiance         = models.FloatField()
    created_at                      = models.DateTimeField(auto_now_add=True)
    created_by                      = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    updated_at                      = models.DateTimeField(auto_now=True)
    updated_by                      = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')

#EMPLOPYEE JOB HISTORY UDF
class EmpJobHistory_CustomField(models.Model):
    FIELD_TYPES = (
        ('dropdown', 'DropdownField'),
        ('radio', 'RadioButtonField'),)
    emp_job_history    = models.ForeignKey(EmpJobHistory, on_delete=models.CASCADE,related_name='jobhistory_customfields')
    field_name         = models.CharField(max_length=100)  # Field name provided by end user
    field_value        = models.TextField(null=True, blank=True)  # Field value provided by end user
    data_type          = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values    = models.JSONField(null=True, blank=True)
    radio_values       = models.JSONField(null=True, blank=True)
    
    

#EMPLOYEE QUALIFICATION
class EmpQualification(models.Model):
    emp_id                = models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_qualification')
    emp_qualification     = models.CharField(max_length=50)
    emp_qf_instituition   = models.CharField(max_length=50)
    emp_qf_year           = models.DateField()
    emp_qf_subject        = models.CharField(max_length=50)
    created_at            = models.DateTimeField(auto_now_add=True)
    created_by            = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    updated_at            = models.DateTimeField(auto_now=True)
    updated_by            = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')
#EMPLOYEE QUALIFICATION UDF
class EmpQualification_CustomField(models.Model):
    FIELD_TYPES = (
        ('dropdown', 'DropdownField'),
        ('radio', 'RadioButtonField'),
        )
    emp_qualification    = models.ForeignKey(EmpQualification, on_delete=models.CASCADE,related_name='custom_fields')
    field_name           = models.CharField(max_length=100)  # Field name provided by end user
    field_value          = models.TextField(null=True, blank=True)  # Field value provided by end user
    data_type            = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values      = models.JSONField(null=True, blank=True)
    radio_values         = models.JSONField(null=True, blank=True)
    
    


#EMPLOYEE DOCUMENTS
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
#EMPLOYEE DOCUMENTS
class Emp_Documents(models.Model):
    emp_id               =models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_documents')
    emp_sl_no            = models.CharField(max_length=50, unique=True, null=True,blank =True,default=None)
    document_type        = models.ForeignKey('Core.document_type',on_delete = models.CASCADE,null=True,blank =True)
    emp_doc_number       = models.IntegerField()#unique number
    emp_doc_issued_date  = models.DateField()
    emp_doc_expiry_date  = models.DateField()
    emp_doc_document     = models.FileField()
    is_active            = models.BooleanField(default=True)
    created_at           = models.DateTimeField(auto_now_add=True)
    created_by           = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    updated_at           = models.DateTimeField(auto_now=True)
    updated_by           = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')
    
   
    def __str__(self):
        return f"{self.document_type} - {self.emp_id}" 
# @receiver(post_save, sender=Emp_Documents)
# def create_expiry_notification(sender, instance, created, **kwargs):
#     if created:
#         today = timezone.now().date()
#         print("today",today)
#         expiry_date = instance.emp_doc_expiry_date
#         print("exipiry",expiry_date)
        
#         # Check if emp_master exists and has a valid branch
#         if instance.emp_id and instance.emp_id.emp_branch_id:
#             branch_notification_days = instance.emp_id.emp_branch_id.notification_period_days
#             if branch_notification_days is not None:
#                 notification_delta = timedelta(days=branch_notification_days)  # Notify based on branch's notification period
#                 print(notification_delta )
#                 if expiry_date - today <= notification_delta:
#                     notification_message = f"The document '{instance.document_type}' of '{instance.emp_id}' is expiring on {expiry_date}."
#                     # Create notification for the newly created document
#                     notification.objects.create(
#                         message=notification_message,
#                         document_id=instance
#                     )
#         else:
#             # Handle cases where emp_id or emp_branch_id is not valid
#             print("Warning: Invalid emp_id or emp_branch_id detected. Cannot create notification.")      


#Document UDF
class EmpDocuments_CustomField(models.Model):
    FIELD_TYPES = (
        ('dropdown', 'DropdownField'),
        ('radio', 'RadioButtonField'),
        )
    emp_documents    = models.ForeignKey(Emp_Documents, on_delete=models.CASCADE,related_name='custom_fields')
    field_name       = models.CharField(max_length=100)  # Field name provided by end user
    field_value      = models.TextField(null=True, blank=True)  # Field value provided by end user
    data_type        = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values  = models.JSONField(null=True, blank=True)
    radio_values     = models.JSONField(null=True, blank=True)
    
    
    
# Display document type name and employee ID  
class EmpLeaveRequest(models.Model):
    employee    = models.ForeignKey('emp_master', on_delete=models.CASCADE,related_name='emp_leaverequest')
    start_date  = models.DateField()
    end_date    = models.DateField()
    status      = models.CharField(max_length=20, default='Pending')
    reason      = models.CharField(max_length=150,default='its ook')




class notification(models.Model):
    # notified_emp =models.ForeignKey('EmpManagement.emp_master',on_delete=models.CASCADE)
    message      = models.CharField(max_length=200)
    created_at   = models.DateTimeField(auto_now_add=True)
    document_id  = models.ForeignKey('Emp_Documents',on_delete = models.CASCADE,null=True)
    


class LanguageSkill(models.Model):
    language = models.CharField(max_length=100,null=True,blank =True,default=None)
    
    def __str__(self):
        return f"{self.language }"

class MarketingSkill(models.Model):
    marketing = models.CharField(max_length=100,null=True,blank =True,default=None)

    def __str__(self):
        return f"{self.marketing }"

class ProgrammingLanguageSkill(models.Model):
    programming_language = models.CharField(max_length=100,null=True,blank =True,default=None)

    def __str__(self):
        return f"{self.programming_language }"

class EmployeeSkill(models.Model):

    emp_id =models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_skills')
    language_skill               = models.ForeignKey(LanguageSkill, on_delete=models.SET_NULL, null=True, blank=True)
    marketing_skill              = models.ForeignKey(MarketingSkill, on_delete=models.SET_NULL, null=True, blank=True)
    programming_language_skill   = models.ForeignKey(ProgrammingLanguageSkill, on_delete=models.SET_NULL, null=True, blank=True)
    percentage                   = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    value_choices = (
        ('Language Skill', 'Language Skill'),
        ('Marketing Skill', 'Marketing Skill'),
        ('Programming Language Skill', 'Programming Language Skill'),
    )
    value = models.CharField(max_length=100, choices=value_choices , null=True, blank=True)
    

    def __str__(self):
        return f"{self.emp_id} - {self.value}"

@receiver(pre_save, sender=EmployeeSkill)
def update_value_field(sender, instance, **kwargs):
    if instance.language_skill:
        instance.value = instance.language_skill.language
    elif instance.marketing_skill:
        instance.value = instance.marketing_skill.marketing
    elif instance.programming_language_skill:
        instance.value = instance.programming_language_skill.programming_language
    
class EmployeeMarketingSkill(models.Model):
    emp_id           = models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_market_skills')
    marketing_skill  = models.ForeignKey(MarketingSkill, on_delete=models.SET_NULL, null=True, blank=True)
    percentage       = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    value            = models.CharField(max_length=100,null=True,blank =True,default=None)

    def __str__(self):
        return f"{self.emp_id} - {self.value}"
@receiver(pre_save, sender=EmployeeMarketingSkill)
def update_value_field(sender, instance, **kwargs):
    if instance.marketing_skill:
        instance.value = instance.marketing_skill.marketing
class EmployeeProgramSkill(models.Model):
    emp_id        =models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_prgrm_skills')
    program_skill = models.ForeignKey(ProgrammingLanguageSkill, on_delete=models.SET_NULL, null=True, blank=True)
    percentage    = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    value         = models.CharField(max_length=100,null=True,blank =True,default=None)

    def __str__(self):
        return f"{self.emp_id} - {self.value}"
@receiver(pre_save, sender=EmployeeProgramSkill)
def update_value_field(sender, instance, **kwargs):
    if instance.program_skill:
        instance.value = instance.program_skill.programming_language
class EmployeeLangSkill(models.Model):
    emp_id          = models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_lang_skills')
    language_skill  = models.ForeignKey(LanguageSkill, on_delete=models.SET_NULL, null=True, blank=True)
    percentage      = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)
    value           = models.CharField(max_length=100,null=True,blank =True,default=None)

    def __str__(self):
        return f"{self.emp_id} - {self.value}"
@receiver(pre_save, sender=EmployeeLangSkill)
def update_value_field(sender, instance, **kwargs):
    if instance.language_skill:
        instance.value = instance.language_skill.language


### EmailTemplate Model ###
class EmailTemplate(models.Model):
    request_type  = models.ForeignKey('RequestType', related_name='email_templates', on_delete=models.CASCADE,null=True)
    template_type = models.CharField(max_length=50, choices=[
        ('request_created', 'Request Created'),
        ('request_approved', 'Request Approved'),
        ('request_rejected', 'Request Rejected')
    ])
    subject             = models.CharField(max_length=255)
    body                = models.TextField()
    use_common_template = models.BooleanField(default=False)
    def __str__(self):
        if self.use_common_template:
            return f"Common {self.template_type} template"
        return f"{self.template_type} for {self.request_type.name if self.request_type else 'None'}"


class EmailConfiguration(models.Model):
    email_host            = models.CharField(max_length=255, default='smtp.gmail.com')
    email_port            = models.IntegerField(default=587)
    email_use_tls         = models.BooleanField(default=True)
    email_host_user       = models.CharField(max_length=255, blank=True, null=True)
    email_host_password   = models.CharField(max_length=255, blank=True, null=True)
    is_active             = models.BooleanField(default=False)

    def __str__(self):
        return f"Email Configuration ({'Active' if self.is_active else 'Inactive'})"
    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate other configurations
            EmailConfiguration.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

class RequestNotification(models.Model):
    recipient_user     = models.ForeignKey('UserManagement.CustomUser', null=True, blank=True,on_delete=models.CASCADE)
    recipient_employee = models.ForeignKey('emp_master', null=True, blank=True, on_delete=models.CASCADE)
    message            = models.CharField(max_length=255)
    created_at         = models.DateTimeField(auto_now_add=True)
    is_read            = models.BooleanField(default=False)

    def __str__(self):
        if self.recipient_user:
            return f"Notification for {self.recipient_user.username}: {self.message}"
        else:
            return f"Notification for employee: {self.message}"    
    
    def send_email_notification(self, template_type, context):
        # # Generate unique approval and rejection URLs
        # approval_url_approve = f"{settings.SITE_URL}/approve/{self.id}/"
        # approval_url_reject = f"{settings.SITE_URL}/reject/{self.id}/"
        
        # # Update the context with these URLs
        # context.update({
        #     'approval_url_approve': approval_url_approve,
        #     'approval_url_reject': approval_url_reject,
        # })
        # Ensure that request_type in the context is an instance of RequestType
        request_type = context.get('request_type')
        
        if isinstance(request_type, str):
            # If request_type is passed as a string, retrieve the actual RequestType object
            request_type = RequestType.objects.get(name=request_type)

        # Try to fetch the specific email template for the request type and template type
        email_templates = request_type.email_templates.filter(template_type=template_type)

        if email_templates.exists():
            # Use the specific email template for this request type
            email_template = email_templates.first()
        else:
            # No specific template, fall back to the common email template if it exists
            common_templates = EmailTemplate.objects.filter(template_type=template_type, use_common_template=True)
            if common_templates.exists():
                email_template = common_templates.first()  # Use the common template
            else:
                # Handle the case where no template is found
                raise ValueError(f"No email template found for template type '{template_type}' and request type '{request_type.name}', and no common template found.")

        # Proceed with sending the email using the selected template
        subject = email_template.subject
        template = Template(email_template.body)
        html_message = template.render(Context(context))
        plain_message = strip_tags(html_message)

        # Try to retrieve the active email configuration
        try:
            email_config = EmailConfiguration.objects.get(is_active=True)
            use_custom_config = True
        except EmailConfiguration.DoesNotExist:
            use_custom_config = False
            default_email = settings.EMAIL_HOST_USER

        # Use custom or default email configuration
        if use_custom_config:
            default_email = email_config.email_host_user
            connection = get_connection(
                host=email_config.email_host,
                port=email_config.email_port,
                username=email_config.email_host_user,
                password=email_config.email_host_password,
                use_tls=email_config.email_use_tls,
            )
        else:
            connection = get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS,
            )

        # Determine recipient email and name
        to_email = None
        recipient_name = None
        if self.recipient_user and self.recipient_user.email:
            to_email = self.recipient_user.email
            recipient_name = self.recipient_user.username
        elif self.recipient_employee and self.recipient_employee.emp_personal_email:
            to_email = self.recipient_employee.emp_personal_email
            recipient_name = self.recipient_employee.emp_first_name

        if to_email:
            context.update({'recipient_name': recipient_name})

            plain_message = strip_tags(html_message)

            # Send the email
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=default_email,  # From email
                to=[to_email],  # Recipient list
                connection=connection,
                headers={'From': 'zeosoftware@abc.com'}  # Custom header
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)

class RequestType(models.Model):
    name                =  models.CharField(max_length=50)
    description         = models.CharField(max_length=150)
    created_at          = models.DateField(auto_now_add=True)
    updated_at          = models.DateField(auto_now_add=True)
    created_by          = models.ForeignKey('UserManagement.CustomUser',on_delete=models.CASCADE)
    use_common_workflow = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    # # Fetch email template for this request type based on template type
    # def get_email_template(self, template_type):
    #     return self.email_templates.filter(template_type=template_type).first()
    
    def get_email_template(self, template_type):
        # Try fetching a specific template for the request type
        email_templates = self.email_templates.filter(template_type=template_type)

        # Check if there are multiple templates and handle appropriately
        if email_templates.count() > 1:
            raise ValueError(f"Multiple email templates found for template type '{template_type}' and request type '{self.name}'")
        elif email_templates.exists():
            return email_templates.first()

        # If no specific template, try fetching a common template
        common_templates = EmailTemplate.objects.filter(template_type=template_type, use_common_template=True)
        
        if common_templates.count() > 1:
            raise ValueError(f"Multiple common email templates found for template type '{template_type}'")
        elif common_templates.exists():
            return common_templates.first()

        # If no templates found
        return None
class CommonWorkflow(models.Model):
    level = models.IntegerField()
    role = models.CharField(max_length=50, null=True, blank=True)
    approver = models.ForeignKey('UserManagement.CustomUser', null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['level'], name='unique_common_workflow_level')
        ]
    def __str__(self):
        return f"Level {self.level} - {self.role or self.approver}"


class GeneralRequest(models.Model):
    doc_number       =  models.CharField(max_length=120,unique=True,null=True,blank=True)
    reason           =  models. CharField(max_length=200)
    branch           =  models.ForeignKey('OrganisationManager.brnch_mstr',on_delete = models.CASCADE)
    request_type     =  models.ForeignKey('RequestType',on_delete = models.CASCADE)
    employee         =  models.ForeignKey('emp_master',on_delete = models.CASCADE)
    total            =  models.IntegerField(null=True)
    status           =  models.CharField(max_length=20, default='Pending')
    created_by       =  models.ForeignKey('UserManagement.CustomUser',on_delete=models.CASCADE,null=True,blank=True)
    created_at_date  =  models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.doc_number}-{self.request_type.name}"
    
    def get_employee_requests(employee_id):
        return GeneralRequest.objects.filter(employee_id=employee_id).order_by('-created_at_date')

    def move_to_next_level(self):
        if self.approvals.filter(status=Approval.REJECTED).exists():
            self.status = 'Rejected'
            self.save()

            # Notify rejection
            notification = RequestNotification.objects.create(
                recipient_user=self.created_by,
                message=f"Your request {self.doc_number} has been rejected."
            )
            notification.send_email_notification('request_rejected', {
                'doc_number': self.doc_number,
                'request_type': self.request_type.name,
                'rejection_reason': 'Reason for rejection...',
                'emp_gender': self.employee.emp_gender,
                'emp_date_of_birth': self.employee.emp_date_of_birth,
                'emp_personal_email': self.employee.emp_personal_email,
                'emp_company_email': self.employee.emp_company_email,
                'emp_branch_name': self.employee.emp_branch_id,
                'emp_department_name': self.employee.emp_dept_id,
                'emp_designation_name': self.employee.emp_desgntn_id,
            })

            if self.employee:
                notification = RequestNotification.objects.create(
                    recipient_employee=self.employee,
                    message=f"Request {self.doc_number} has been rejected."
                )
                notification.send_email_notification('request_rejected', {
                    'doc_number': self.doc_number,
                    'request_type': self.request_type.name,
                    'rejection_reason': 'Reason for rejection...',
                    'emp_gender': self.employee.emp_gender,
                    'emp_date_of_birth': self.employee.emp_date_of_birth,
                    'emp_personal_email': self.employee.emp_personal_email,
                    'emp_company_email': self.employee.emp_company_email,
                    'emp_branch_name': self.employee.emp_branch_id,
                    'emp_department_name': self.employee.emp_dept_id,
                    'emp_designation_name': self.employee.emp_desgntn_id,
                })
            return

        current_approved_levels = self.approvals.filter(status=Approval.APPROVED).count()

        if self.request_type.use_common_workflow:
            next_level = CommonWorkflow.objects.filter(level=current_approved_levels + 1).first()
        else:
            next_level = ApprovalLevel.objects.filter(request_type=self.request_type, level=current_approved_levels + 1).first()

        if next_level:
            last_approval = self.approvals.order_by('-level').first()
            Approval.objects.create(
                general_request=self,
                approver=next_level.approver,
                role=next_level.role,
                level=next_level.level,
                status=Approval.PENDING,
                note=last_approval.note if last_approval else None
            )

            # Notify next approver
            notification = RequestNotification.objects.create(
                recipient_user=next_level.approver,
                message=f"New request for approval: {self.doc_number}, employee: {self.employee}"
            )
            notification.send_email_notification('request_created', {
                'doc_number': self.doc_number,
                'request_type': self.request_type.name,
                'employee_name': self.employee.emp_first_name,
                'reason': self.reason,
                'note': last_approval.note if last_approval else None,
                'emp_gender': self.employee.emp_gender,
                'emp_date_of_birth': self.employee.emp_date_of_birth,
                'emp_personal_email': self.employee.emp_personal_email,
                'emp_company_email': self.employee.emp_company_email,
                'emp_branch_name': self.employee.emp_branch_id,
                'emp_department_name': self.employee.emp_dept_id,
                'emp_designation_name': self.employee.emp_desgntn_id,
            })
        else:
            self.status = 'Approved'
            self.save()

            # Notify the creator about approval
            notification = RequestNotification.objects.create(
                recipient_user=self.created_by,
                message=f"Your request {self.doc_number} has been approved."
            )
            notification.send_email_notification('request_approved', {
                'doc_number': self.doc_number,
                'request_type': self.request_type.name,
                'emp_gender': self.employee.emp_gender,
                'emp_date_of_birth': self.employee.emp_date_of_birth,
                'emp_personal_email': self.employee.emp_personal_email,
                'emp_company_email': self.employee.emp_company_email,
                'emp_branch_name': self.employee.emp_branch_id,
                'emp_department_name': self.employee.emp_dept_id,
                'emp_designation_name': self.employee.emp_desgntn_id,
            })

            if self.employee:
                notification = RequestNotification.objects.create(
                    recipient_employee=self.employee,
                    message=f"Request {self.doc_number} has been approved."
                )
                notification.send_email_notification('request_approved', {
                    'doc_number': self.doc_number,
                    'request_type': self.request_type.name,
                    'emp_gender': self.employee.emp_gender,
                    'emp_date_of_birth': self.employee.emp_date_of_birth,
                    'emp_personal_email': self.employee.emp_personal_email,
                    'emp_company_email': self.employee.emp_company_email,
                    'emp_branch_name': self.employee.emp_branch_id,
                    'emp_department_name': self.employee.emp_dept_id,
                    'emp_designation_name': self.employee.emp_desgntn_id,
                })

class ApprovalLevel(models.Model):
    level = models.IntegerField()
    role = models.CharField(max_length=50, null=True, blank=True)  # Use this for role-based approval like 'CEO' or 'Manager'
    approver = models.ForeignKey('UserManagement.CustomUser', null=True, blank=True, on_delete=models.SET_NULL)  # Use this for user-based approval
    # request_type = models.ForeignKey('RequestType', related_name='approval_levels', on_delete=models.CASCADE)
    request_type = models.ForeignKey('RequestType', related_name='approval_levels', on_delete=models.CASCADE, null=True, blank=True)  # Nullable for common workflow
    # is_common_workflow = models.BooleanField(default=False)  # Mark as part of the common workflow
    class Meta:
        unique_together = ('level', 'request_type')
    
class Approval(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    general_request = models.ForeignKey(GeneralRequest, related_name='approvals', on_delete=models.CASCADE)
    approver = models.ForeignKey('UserManagement.CustomUser', on_delete=models.CASCADE)
    role = models.CharField(max_length=50, null=True, blank=True)
    level = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default=PENDING)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
   
    def approve(self,note=None):
        self.status = self.APPROVED
        if note:
            self.note = note
        self.save()
        self.general_request.move_to_next_level()
    def reject(self,note=None):
        self.status = self.REJECTED
        if note:
            self.note = note
        self.save()
        self.general_request.status = 'Rejected'
        self.general_request.save()

        branch_email = self.general_request.branch.branch_name

        notification = RequestNotification.objects.create(
            recipient_user=self.general_request.created_by,
            message=f"Your request {self.general_request.doc_number} has been rejected."
        )
        notification.send_email_notification('request_rejected', {
            'doc_number': self.general_request.doc_number,
            'request_type': self.general_request.request_type.name,
            'rejection_reason': 'Reason for rejection...',  # Add actual reason if available
            'emp_gender': self.general_request.employee.emp_gender,
            'emp_date_of_birth': self.general_request.employee.emp_date_of_birth,
            'emp_personal_email': self.general_request.employee.emp_personal_email,
            'emp_company_email': self.general_request.employee.emp_company_email,
            'emp_branch_name': self.general_request.employee.emp_branch_id,
            'emp_department_name': self.general_request.employee.emp_dept_id,
            'emp_designation_name': self.general_request.employee.emp_desgntn_id,
            'emp_hired_date':self.general_request.employee.emp_hired_date,

        })

        if self.general_request.employee:
            notification = RequestNotification.objects.create(
                recipient_employee=self.general_request.employee,
                message=f"Request {self.general_request.doc_number} has been rejected."
            )
            notification.send_email_notification('request_rejected', {
                'doc_number': self.general_request.doc_number,
                'request_type': self.general_request.request_type.name,
                'rejection_reason': 'Reason for rejection...', # Add actual reason if available
                'emp_gender': self.general_request.employee.emp_gender,
                'emp_date_of_birth': self.general_request.employee.emp_date_of_birth,
                'emp_personal_email': self.general_request.employee.emp_personal_email,
                'emp_company_email': self.general_request.employee.emp_company_email,
                'emp_branch_name': self.general_request.employee.emp_branch_id,
                'emp_department_name': self.general_request.employee.emp_dept_id,
                'emp_designation_name': self.general_request.employee.emp_desgntn_id,
        })

@receiver(post_save, sender=GeneralRequest)
def create_initial_approval(sender, instance, created, **kwargs):
    if created:
        if instance.request_type.use_common_workflow:
            first_level = CommonWorkflow.objects.order_by('level').first()
        else:
            first_level = ApprovalLevel.objects.filter(request_type=instance.request_type).order_by('level').first()

        if first_level:
            Approval.objects.create(
                general_request=instance,
                approver=first_level.approver,
                role=first_level.role,
                level=first_level.level,
                status=Approval.PENDING
            )

            # Notify first approver
            notification = RequestNotification.objects.create(
                recipient_user=first_level.approver,
                message=f"New request for approval: {instance.doc_number}, employee: {instance.employee}"
            )
            notification.send_email_notification('request_created', {
                'doc_number': instance.doc_number,
                'request_type': instance.request_type.name,
                'employee_name': instance.employee.emp_first_name,
                'reason': instance.reason,
                'emp_gender':instance.employee.emp_gender,
                'emp_date_of_birth':instance.employee.emp_date_of_birth,
                'emp_personal_email':instance.employee.emp_personal_email,
                'emp_company_email':instance.employee.emp_company_email,
                'emp_branch_name':instance.employee.emp_branch_id,
                'emp_department_name':instance.employee.emp_dept_id,
                'emp_designation_name':instance.employee.emp_desgntn_id,
                'emp_first_name':instance.employee.emp_first_name
            })         

class SelectedEmpNotify(models.Model):
    # selected_ess_user = models.ForeignKey(emp_master, on_delete=models.SET_NULL, null=True, blank=True)
    # selected_ess_users=models.ManyToManyField(emp_master, blank=True)
    selected_employees = models.ManyToManyField(emp_master, blank=True)  # Allows multiple employee selections

class NotificationSettings(models.Model):
    branch              = models.ForeignKey("OrganisationManager.brnch_mstr", on_delete=models.CASCADE)
    days_before_expiry  = models.IntegerField(default=7)  # Default reminder 7 days before expiry
    days_after_expiry   = models.IntegerField(default=0)  # Default reminder 0 days after expiry (on expiry day)

    def __str__(self):
        return f"Reminder Settings for {self.branch.name}"

class DocExpEmailTemplate(models.Model):
    Name_Choices=[("Employee Notification","Employee Notification"),
                  ("ESS User Notification","ESS User Notification")
                  ]
    template_name   = models.CharField(max_length=100,choices=Name_Choices)
    subject         = models.CharField(max_length=255)
    body            = models.TextField()
        
    def __str__(self):
        return self.template_name















# class DocumentReminderSettings(models.Model):
#     user = models.OneToOneField(emp_master, on_delete=models.CASCADE)
#     first_reminder_days_before_expiry = models.IntegerField(default=7)  # Default to 7 days before expiry
#     second_reminder_days_before_expiry = models.IntegerField(default=5)  # Default to 5 days before expiry
#     final_reminder_days_after_expiry = models.IntegerField(default=0)  # Default to no days after expiry

# @receiver(post_save, sender=GeneralRequest)
# def create_initial_approval(sender, instance, created, **kwargs):
#     if created:
#         first_level = ApprovalLevel.objects.filter(request_type=instance.request_type).order_by('level').first()
#         branch_email = instance.branch.br_branch_mail

#         if first_level:
#             Approval.objects.create(
#                 general_request=instance,
#                 approver=first_level.approver,
#                 role=first_level.role,
#                 level=first_level.level,
#                 status=Approval.PENDING
#             )
           
#             notification = RequestNotification.objects.create(
#                 recipient_user=first_level.approver,
#                 message=f"New request for approval: {instance.doc_number} employee: {instance.employee}"
#             )
#             notification.send_email_notification('request_created.html', {
#                 'doc_number': instance.doc_number,
#                 'request_type': instance.request_type.name,
#                 'employee_name': instance.employee.emp_first_name,
#                 'reason': instance.reason,
                
#             }, branch_email)

#         notification = RequestNotification.objects.create(
#             recipient_user=instance.created_by,
#             message=f"Your request {instance.doc_number} has been created for employee: {instance.employee} and is pending approval."
#         )
#         notification.send_email_notification('request_created.html', {
#             'doc_number': instance.doc_number,
#             'request_type': instance.request_type.name,
#             'employee_name': instance.employee.emp_first_name,
#             'reason': instance.reason
#         }, branch_email)

#         if instance.employee:
#             notification = RequestNotification.objects.create(
#                 recipient_employee=instance.employee,
#                 message=f"Request {instance.doc_number} has been created for you and is pending approval."
#             )
#             notification.send_email_notification('request_created.html', {
#                 'doc_number': instance.doc_number,
#                 'request_type': instance.request_type.name,
#                 'employee_name': instance.employee.emp_first_name,
#                 'reason': instance.reason
#             },branch_email)


# class FilteredReportData(models.Model):
#     report = models.ForeignKey(Doc_Report, on_delete=models.CASCADE)
#     filtered_data = models.TextField()  # Store JSON data
#     created_at = models.DateTimeField(auto_now_add=True)

# class FilteredGeneralReportData(models.Model):
#     report = models.ForeignKey(GeneralRequestReport, on_delete=models.CASCADE)
#     filtered_data = models.TextField()  # Store JSON data
#     created_at = models.DateTimeField(auto_now_add=True)