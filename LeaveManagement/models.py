from django.db import models,transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta, time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from UserManagement.models import CustomUser
from EmpManagement.models import EmailConfiguration
from django.core.mail import EmailMultiAlternatives,get_connection, send_mail
from django.template import Context, Template
from django.utils.html import strip_tags
from calendars.models import assign_weekend,assign_holiday
from django.db.models import F
from django.utils import timezone
import pytz
# Create your models here.

class leave_type(models.Model):
    type_choice =   [
        ('paid','paid'),
        ('unpaid','unpaid'),
    ]
    unit_choice = [
        ('days','days'),
        ('hours','hours'),
    ]

    balance_choice = [
        ('fixed','fixed'),
        ('leave_grant','leave_grant')
    ]
    
    name                          = models.CharField(max_length=50,unique=True)
    image                         = models.ImageField(upload_to='leave_images/')
    code                          = models.CharField(max_length=30,unique=True)
    type                          = models.CharField(max_length=20,choices=type_choice)
    unit                          = models.CharField(max_length=10,choices=unit_choice)
    negative                      = models.BooleanField(default=False)
    description                   = models.CharField(max_length=200)  
    allow_half_day                = models.BooleanField(default=False)  # Allows half-day leave if set to True
    valid_from                    = models.DateField()
    valid_to                      = models.DateField(null=True,blank=True)
    include_weekend_and_holiday   = models.BooleanField(default=False)
    use_common_workflow           = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name}"
    def get_email_template(self, template_type):
        # Try fetching a specific template for the request type
        email_templates = self.email_templates.filter(template_type=template_type)

        # Check if there are multiple templates and handle appropriately
        if email_templates.count() > 1:
            raise ValueError(f"Multiple email templates found for template type '{template_type}' and request type '{self.name}'")
        elif email_templates.exists():
            return email_templates.first()


class leave_entitlement(models.Model):  
    EFFECTIVE_AFTER_CHOICES = [
        ('date_of_joining', 'Date of Joining'),
        ('date_of_confirmation', 'Date of Confirmation'),
    ]
    TIME_UNIT_CHOICES = [
        ('years', 'Years'),
        ('months', 'Months'),
        ('days','days')

    ]
    ROUND_OF_TYPE = [ 
        ('nearest_lowest','nearest_lowest'),
        ('nearest_highest','nearest_highest')
    ]
    DAY_CHOICES = [
        ('1st', '1st Day of the Month'),
        ('last', 'Last Day of the Month'),
    ]
    UNIT_CHOICES =[
        ('percentage','percentage'),
        ('unit','unit')
    ]
    MONTH_CHOICES = [
        ('Jan', 'January'),
        ('Feb', 'February'),
        ('Mar', 'March'),
        ('Apr', 'April'),
        ('May', 'May'),
        ('Jun', 'June'),
        ('Jul', 'July'),
        ('Aug', 'August'),
        ('Sep', 'September'),
        ('Oct', 'October'),
        ('Nov', 'November'),
        ('Dec', 'December')
    ]
    CARRY_CHOICE = [
        ('carry_forward','carry forward'),
        ('carry_forward_with_expiry','carry forward with expiry')
    ]
    PRORATE_CHOICES = [
        ('start_of_policy', 'Start of Policy'),
        ('start_and_end_of_policy', 'Start and End of Policy'),
        ('do_not_prorate', 'Do not Prorate')
    ]
    leave_type                    = models.ForeignKey(leave_type, on_delete=models.CASCADE)
    effective_after               = models.PositiveIntegerField(default=0)
    effective_after_unit          = models.CharField(max_length=10, choices=TIME_UNIT_CHOICES, default='months')
    effective_after_from          = models.CharField(max_length=20, choices=EFFECTIVE_AFTER_CHOICES)


    accrual                       = models.BooleanField(default=False)
    accrual_rate                  = models.FloatField(default=0, help_text="Accrual rate per period (e.g., days/months/yearly)")
    accrual_frequency             = models.CharField(max_length=20, choices=TIME_UNIT_CHOICES)
    accrual_month                 = models.CharField(max_length=3, choices=MONTH_CHOICES, default='Jan',null=True,blank=True)
    accrual_day                   = models.CharField(max_length=10, choices=DAY_CHOICES, default='1st')
    round_of                      = models.CharField(choices=ROUND_OF_TYPE,max_length=20)


    reset                         = models.BooleanField(default=False)
    frequency                     = models.CharField(max_length=20, choices=TIME_UNIT_CHOICES)
    month                         = models.CharField(max_length=30, choices=MONTH_CHOICES, default='Dec')
    day                           = models.CharField(max_length=20, choices=DAY_CHOICES)


    carry_forward_choice          = models.CharField(max_length=100,choices=CARRY_CHOICE)
    cf_value                      = models.PositiveIntegerField()
    cf_unit_or_percentage         = models.CharField(max_length=50,choices=UNIT_CHOICES)
    cf_max_limit                  = models.PositiveIntegerField()
    cf_expires_in_value           = models.PositiveIntegerField()
    cf_time_choice                = models.CharField(max_length=20,choices=TIME_UNIT_CHOICES)


    encashment_value               = models.PositiveIntegerField(default=50)
    encashment_unit_or_percentage  = models.CharField(max_length=50,choices=UNIT_CHOICES)
    encashment_max_limit           = models.PositiveIntegerField()


    prorate_accrual                 = models.BooleanField(default=False, help_text="Enable prorate accrual for this leave type.")
    prorate_type                    = models.CharField(max_length=30, choices=PRORATE_CHOICES, null=True, blank=True, help_text="Prorate accrual type.")
    def __str__(self):
        return f"{self.leave_type.name} Entitlement"


# from django.db.models import Q

class emp_leave_balance(models.Model):
    employee       = models.ForeignKey('EmpManagement.emp_master',on_delete=models.CASCADE)
    leave_type     = models.ForeignKey('leave_type',on_delete=models.CASCADE)
    balance        = models.FloatField(null=True,blank=True)
    openings       = models.IntegerField(null=True,blank=True)
    updated_at     = models.DateTimeField(auto_now=True)  # Track last update
    def is_weekend(self, date):
        """ Check if the given date is a weekend based on the employee's weekend calendar """
        if self.employee.emp_weekend_calendar:
            # Assuming emp_weekend_calendar has a method is_weekend
            return self.employee.emp_weekend_calendar.is_weekend(date)
        return False

    def is_holiday(self, date):
        """ Check if the given date is a holiday based on the employee's holiday calendar """
        if self.employee.holiday_calendar:
            # Assuming holiday_calendar has a method is_holiday
            return self.employee.holiday_calendar.is_holiday(date)
        return False

    def get_leave_days(self, start_date, end_date):
        """ Calculate total leave days between start and end date, excluding weekends and holidays if applicable """
        total_days = 0
        current_date = start_date
        while current_date <= end_date:
            is_weekend = self.is_weekend(current_date)
            is_holiday = self.is_holiday(current_date)

            if self.leave_type.include_weekend_and_holiday:
                # Include both weekends and holidays
                total_days += 1
            else:
                # Exclude weekends and holidays
                if not is_weekend and not is_holiday:
                    total_days += 1

            current_date += timedelta(days=1)

        return total_days

    def deduct_leave(self, start_date, end_date, is_half_day=False):
        """ Deduct leave from balance, considering half-day and whether weekends/holidays are included """
        if is_half_day:
            leave_days = 0.5
        else:
            leave_days = self.get_leave_days(start_date, end_date)

        self.balance -= leave_days
        self.save()
    
    def __str__(self):
        return f"{self.employee} - {self.balance}"

class leave_accrual_transaction(models.Model):
    employee     = models.ForeignKey('EmpManagement.emp_master', on_delete=models.CASCADE)
    leave_type   = models.ForeignKey(leave_type, on_delete=models.CASCADE)
    accrual_date = models.DateField()
    amount       = models.DecimalField(max_digits=5, decimal_places=2)
    year         = models.PositiveIntegerField(default=datetime.now().year)

class leave_reset_transaction(models.Model):
    employee               = models.ForeignKey('EmpManagement.emp_master', on_delete=models.CASCADE)
    leave_type             = models.ForeignKey('leave_type',on_delete=models.CASCADE)
    reset_date             = models.DateField()
    carry_forward_amount   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    encashment_amount      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reset_balance          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    year                   = models.PositiveIntegerField(default=datetime.now().year) 
    def __str__(self):
        return f"{self.employee} - {self.leave_type} Reset on {self.reset_date}"
    

class applicablity_critirea(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    
    leave_type         = models.ForeignKey(leave_type,on_delete=models.CASCADE)
    gender             = models.CharField(choices=GENDER_CHOICES,null=True,blank=True)
    branch             = models.ManyToManyField('OrganisationManager.brnch_mstr',blank=True)
    department         = models.ManyToManyField('OrganisationManager.dept_master',blank=True)
    designation        = models.ManyToManyField('OrganisationManager.desgntn_master',blank=True)
    role               = models.ManyToManyField('OrganisationManager.ctgry_master',blank=True)

class LvEmailTemplate(models.Model):
    request_type = models.ForeignKey('leave_type', related_name='email_templates', on_delete=models.CASCADE,null=True)
    template_type = models.CharField(max_length=50, choices=[
        ('request_created', 'Request Created'),
        ('request_approved', 'Request Approved'),
        ('request_rejected', 'Request Rejected')
    ])
    subject = models.CharField(max_length=255)
    body    = models.TextField()
    
class LvApprovalNotify(models.Model):
    recipient_user       = models.ForeignKey('UserManagement.CustomUser', null=True, blank=True,on_delete=models.CASCADE)
    recipient_employee   = models.ForeignKey('EmpManagement.emp_master', null=True, blank=True, on_delete=models.CASCADE)
    message              = models.CharField(max_length=255)
    created_at           = models.DateTimeField(auto_now_add=True)
    is_read              = models.BooleanField(default=False)

    def __str__(self):
        if self.recipient_user:
            return f"Notification for {self.recipient_user.username}: {self.message}"
        else:
            return f"Notification for employee: {self.message}"    
    def send_email_notification(self, template_type, context):
        try:
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

                # Fetch the email template
                try:
                    email_template = LvEmailTemplate.objects.get(template_type=template_type)
                    subject = email_template.subject
                    template = Template(email_template.body)
                    html_message = template.render(Context(context))
                    plain_message = strip_tags(html_message)
                except LvEmailTemplate.DoesNotExist:
                    raise ValidationError("Email template not found. Please set an email template for this notification type.")

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

        except ValidationError as e:
            print(f"Validation Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    # def send_email_notification(self, template_type, context):
    #      # Try to retrieve the active email configuration
    #     try:
    #         email_config = EmailConfiguration.objects.get(is_active=True)
    #         use_custom_config = True
    #     except EmailConfiguration.DoesNotExist:
    #         use_custom_config = False
    #         default_email = settings.EMAIL_HOST_USER

    #     # Use custom or default email configuration
    #     if use_custom_config:
    #         default_email = email_config.email_host_user
    #         connection = get_connection(
    #             host=email_config.email_host,
    #             port=email_config.email_port,
    #             username=email_config.email_host_user,
    #             password=email_config.email_host_password,
    #             use_tls=email_config.email_use_tls,
    #         )
    #     else:
    #         connection = get_connection(
    #             host=settings.EMAIL_HOST,
    #             port=settings.EMAIL_PORT,
    #             username=settings.EMAIL_HOST_USER,
    #             password=settings.EMAIL_HOST_PASSWORD,
    #             use_tls=settings.EMAIL_USE_TLS,
    #         )

    #     # Determine recipient email and name
    #     to_email = None
    #     recipient_name = None
    #     if self.recipient_user and self.recipient_user.email:
    #         to_email = self.recipient_user.email
    #         recipient_name = self.recipient_user.username
    #     elif self.recipient_employee and self.recipient_employee.emp_personal_email:
    #         to_email = self.recipient_employee.emp_personal_email
    #         recipient_name = self.recipient_employee.emp_first_name

    #     if to_email:
    #         context.update({'recipient_name': recipient_name})

    #         # Fetch the email template
    #         try:
    #             email_template = LvEmailTemplate.objects.get(template_type=template_type)
    #             subject = email_template.subject
    #             template = Template(email_template.body)
    #             html_message = template.render(Context(context))
    #         except LvEmailTemplate.DoesNotExist:
    #             subject = "Request Notification"
    #         plain_message = strip_tags(html_message)

    #         # Send the email
    #         email = EmailMultiAlternatives(
    #             subject=subject,
    #             body=plain_message,
    #             from_email=default_email,  # From email
    #             to=[to_email],  # Recipient list
    #             connection=connection,
    #             headers={'From': 'zeosoftware@abc.com'}  # Custom header
    #         )
    #         email.attach_alternative(html_message, "text/html")
    #         email.send(fail_silently=False)
class LvCommonWorkflow(models.Model):
    level    = models.IntegerField()
    role     = models.CharField(max_length=50, null=True, blank=True)
    approver = models.ForeignKey('UserManagement.CustomUser', null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['level'], name='Lv_common_workflow_level')
        ]
    def __str__(self):
        return f"Level {self.level} - {self.role or self.approver}"
#compensatory leave
class CompensatoryLeaveTransaction(models.Model):
    """Logs the addition and deduction of compensatory leave days."""
    TRANSACTION_TYPE_CHOICES = [
        ('addition', 'Addition'),
        ('deduction', 'Deduction'),
    ]
    
    employee         = models.ForeignKey('EmpManagement.emp_master', on_delete=models.CASCADE)
    transaction_date = models.DateField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    days             = models.FloatField()
    reason           = models.TextField()

    def __str__(self):
        return f"{self.employee} - {self.transaction_type} of {self.days} days on {self.transaction_date}"
     
class CompensatoryLeaveBalance(models.Model):
    """Tracks the total compensatory leave balance for each employee."""
    employee = models.OneToOneField('EmpManagement.emp_master', on_delete=models.CASCADE)
    balance  = models.FloatField(default=0)

    def __str__(self):
        return f"{self.employee} - Compensatory Balance: {self.balance} days"

class CompensatoryLeaveRequest(models.Model):
    LEAVE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    REQUEST_TYPE_CHOICES = [
        ('work_request', 'Work Request'),
        ('leave_request', 'Compensatory Leave Request'),
    ]
    request_type    = models.CharField(max_length=15, choices=REQUEST_TYPE_CHOICES, default='work_request')
    employee        = models.ForeignKey('EmpManagement.emp_master', on_delete=models.CASCADE)
    request_date    = models.DateField(auto_now_add=True)
    work_date       = models.DateField()  # Date employee worked on weekend/holiday
    reason          = models.TextField()
    status          = models.CharField(max_length=10, choices=LEAVE_STATUS_CHOICES, default='pending')
    created_by=models.ForeignKey('UserManagement.CustomUser',on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return f"Compensatory Request for {self.employee} on {self.work_date} - {self.status}"
    def save(self, *args, **kwargs):
        # Fetch the existing status before saving
        old_status = None
        if self.pk:
            old_status = CompensatoryLeaveRequest.objects.get(pk=self.pk).status

        # Call the original save method
        super().save(*args, **kwargs)

        # Proceed only if the request is approved and status has changed to approved
        if self.status == 'Approved' and old_status != 'Approved':
            # Wrap balance updates and transaction creation in an atomic transaction
            with transaction.atomic():
                # Fetch or create a compensatory leave balance record for the employee
                leave_balance, created = CompensatoryLeaveBalance.objects.get_or_create(employee=self.employee)

                if self.request_type == 'work_request':
                    # Add 1 day to balance for approved work requests
                    leave_balance.balance += 1
                    # Log the addition transaction
                    CompensatoryLeaveTransaction.objects.create(
                        employee=self.employee,
                        transaction_type='addition',
                        days=1,
                        reason=f"Approved work request on {self.work_date}"
                    )
                elif self.request_type == 'leave_request':
                    # Deduct 1 day from balance for approved leave requests
                    if leave_balance.balance >= 1:
                        leave_balance.balance -= 1
                        # Log the deduction transaction
                        CompensatoryLeaveTransaction.objects.create(
                            employee=self.employee,
                            transaction_type='deduction',
                            days=1,
                            reason=f"Approved compensatory leave on {self.work_date}"
                        )
                    else:
                        raise ValueError("Insufficient compensatory leave balance for this request.")

                # Save the updated leave balance
                leave_balance.save()


    def move_to_next_level(self):
        if self.approvals.filter(status=LeaveApproval.REJECTED).exists():
            self.status = 'Rejected'
            self.save()

            # Notify creator about rejection
            notification = LvApprovalNotify.objects.create(
                recipient_user=self.created_by,
                message=f"Your compensatory leave request for {self.work_date} has been rejected."
            )
            notification.send_email_notification('request_rejected', {
                'request_type': 'Compensatory Leave',
                'rejection_reason': 'Reason for rejection...',
                'work_date': self.work_date,
                'employee_name': self.employee.emp_first_name,
                'emp_gender': self.employee.emp_gender,
                'emp_date_of_birth': self.employee.emp_date_of_birth,
                'emp_personal_email': self.employee.emp_personal_email,
                'emp_company_email': self.employee.emp_company_email,
                'emp_branch_name': self.employee.emp_branch_id,
                'emp_department_name': self.employee.emp_dept_id,
                'emp_designation_name': self.employee.emp_desgntn_id,
            })
            return

        # Check current approval level and set up the next level
        current_approved_levels = self.approvals.filter(status=LeaveApproval.APPROVED).count()
        next_level = LeaveApprovalLevels.objects.filter(is_compensatory=True, level=current_approved_levels + 1).first()

        if next_level:
            last_approval = self.approvals.order_by('-level').first()
            LeaveApproval.objects.create(
                compensatory_request=self,
                approver=next_level.approver,
                role=next_level.role,
                level=next_level.level,
                status=LeaveApproval.PENDING,
                note=last_approval.note if last_approval else None
            )

            # Notify next approver
            notification = LvApprovalNotify.objects.create(
                recipient_user=next_level.approver,
                message=f"New compensatory leave request for approval: work date {self.work_date}, employee: {self.employee}"
            )
            notification.send_email_notification('request_created', {
                'request_type': 'Compensatory Leave',
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
            # Final approval reached, mark as approved and notify creator
            self.status = 'Approved'
            self.save()

            notification = LvApprovalNotify.objects.create(
                recipient_user=self.created_by,
                message=f"Your compensatory leave request for {self.work_date} has been approved."
            )
            notification.send_email_notification('request_approved', {
                'request_type': 'Compensatory Leave',
                'emp_gender': self.employee.emp_gender,
                'emp_date_of_birth': self.employee.emp_date_of_birth,
                'emp_personal_email': self.employee.emp_personal_email,
                'emp_company_email': self.employee.emp_company_email,
                'emp_branch_name': self.employee.emp_branch_id,
                'emp_department_name': self.employee.emp_dept_id,
                'emp_designation_name': self.employee.emp_desgntn_id,
            })
            if self.employee:
                notification = LvApprovalNotify.objects.create(
                    recipient_employee=self.employee,
                    message=f"Your compensatory leave request for {self.work_date} has been approved."
                )
                notification.send_email_notification('request_approved', {
                    'request_type': 'Compensatory Leave',
                    'emp_gender': self.employee.emp_gender,
                    'emp_date_of_birth': self.employee.emp_date_of_birth,
                    'emp_personal_email': self.employee.emp_personal_email,
                    'emp_company_email': self.employee.emp_company_email,
                    'emp_branch_name': self.employee.emp_branch_id,
                    'emp_department_name': self.employee.emp_dept_id,
                    'emp_designation_name': self.employee.emp_desgntn_id,
                })
        # if self.approvals.filter(status=LeaveApproval.REJECTED).exists():
        #     self.status = 'Rejected'
        #     self.save()
        #     return

        # current_approved_levels = self.approvals.filter(status=LeaveApproval.APPROVED).count()

        # next_level = LeaveApprovalLevels.objects.filter(is_compensatory=True, level=current_approved_levels + 1).first()
        
        # if next_level:
        #     last_approval = self.approvals.order_by('-level').first()
        #     LeaveApproval.objects.create(
        #         compensatory_request=self,
        #         approver=next_level.approver,
        #         role=next_level.role,
        #         level=next_level.level,
        #         status=LeaveApproval.PENDING,
        #         note=last_approval.note if last_approval else None
        #     )
        # else:
        #     self.status = 'Approved'
        #     self.save()
    
@receiver(post_save, sender=CompensatoryLeaveRequest)
def create_initial_approval_for_compensatory_leave(sender, instance, created, **kwargs):
    if created:
        # Fetch the first level for compensatory leave
        first_level = LeaveApprovalLevels.objects.filter(is_compensatory=True).order_by('level').first()

        if first_level:
            LeaveApproval.objects.create(
                compensatory_request=instance,
                approver=first_level.approver,
                role=first_level.role,
                level=first_level.level,
                status=LeaveApproval.PENDING
            )
        # Notify first approver
            notification = LvApprovalNotify.objects.create(
                recipient_user=first_level.approver,
                message=f"New request for approval: Compensatory Leave, employee: {instance.employee}"
            )
            notification.send_email_notification('request_created', {
                'request_type': 'Compensatory Leave',
                'employee_name': instance.employee.emp_first_name,
                'reason': instance.reason,
                'emp_gender':instance.employee.emp_gender,
                'emp_date_of_birth':instance.employee.emp_date_of_birth,
                'emp_personal_email':instance.employee.emp_personal_email,
                'emp_company_email':instance.employee.emp_company_email,
                'emp_branch_name':instance.employee.emp_branch_id,
                'emp_department_name':instance.employee.emp_dept_id,
                'emp_designation_name':instance.employee.emp_desgntn_id,
            }) 
    # def clean(self):
    #     """Validate that work_date is a weekend or holiday."""
    #     if not self.employee.emp_weekend_calendar.is_weekend(self.work_date) and \
    #        not self.employee.holiday_calendar.is_holiday(self.work_date):
    #         raise ValidationError("The selected work date is neither a weekend nor a holiday.")
        
    # def save(self, *args, **kwargs):
    #     # If approved, add a compensatory day to balance
    #     if self.status == 'approved' and not self.approved_on:
    #         self.approved_on = datetime.now().date()
    #         compensatory_balance, created = CompensatoryLeaveBalance.objects.get_or_create(employee=self.employee)
    #         compensatory_balance.add_leave(1)  # Add 1 day for approved request
    #     super().save(*args, **kwargs)
    
    # def __str__(self):
    #     return f"Compensatory Request for {self.employee} on {self.work_date} - {self.status}"


    


class employee_leave_request(models.Model):
    LEAVE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    HALF_DAY_CHOICES = [
        ('first_half', 'First Half'),
        ('second_half', 'Second Half'),
    ]
    
    employee          = models.ForeignKey('EmpManagement.emp_master', on_delete=models.CASCADE)
    leave_type        = models.ForeignKey(leave_type, on_delete=models.CASCADE)    
    start_date        = models.DateField()
    end_date          = models.DateField()
    reason            = models.TextField()
    status            = models.CharField(max_length=10, choices=LEAVE_STATUS_CHOICES, default='pending')
    applied_on        = models.DateField(auto_now_add=True)
    dis_half_day      = models.BooleanField(default=False)  # True if it's a half-day leave
    half_day_period   = models.CharField(max_length=20, choices=HALF_DAY_CHOICES, null=True, blank=True)  # First Half / Second Half
    created_by        = models.ForeignKey('UserManagement.CustomUser',on_delete=models.CASCADE,null=True,blank=True)
    number_of_days    = models.FloatField(default=1)
    def clean(self):
        super().clean()
        # Validate if half-day leave is allowed for this leave type
        if self.dis_half_day and not self.leave_type.allow_half_day:
            raise ValidationError(f"{self.leave_type} does not allow half-day leaves.")

        # If half-day leave is chosen, ensure the date range is correct
        if self.dis_half_day and self.start_date != self.end_date:
            raise ValidationError("Half-day leave should be on the same day.")

    def save(self, *args, **kwargs):
        # Calculate leave days based on start and end date
        self.number_of_days = self.calculate_leave_days()
        # Check if the status changed to "approved"
        previous_instance = type(self).objects.filter(pk=self.pk).first()
        status_changed_to_approved = (
            previous_instance is None or previous_instance.status != 'Approved'
        ) and self.status == 'Approved'
        print("s",status_changed_to_approved)
        with transaction.atomic():
            super().save(*args, **kwargs)
            if status_changed_to_approved:
                self.deduct_leave_balance()
            # Handle rejoining logic if leave is approved
            if self.status == 'Approved':
                rejoining_date = self.fetch_rejoining_date()
                if rejoining_date:
                    self.handle_rejoining(rejoining_date)
   
    def calculate_leave_days(self):
        leave_days = 0
        current_date = self.start_date

        # Determine if weekends and holidays should be included
        include_weekend_and_holiday = self.leave_type.include_weekend_and_holiday

        # Fetch assigned weekend and holiday calendars for the employee
        assigned_weekend = assign_weekend.objects.filter(employee=self.employee).first()
        assigned_holiday = assign_holiday.objects.filter(employee=self.employee).first()

        weekend_days = []
        if assigned_weekend and not include_weekend_and_holiday:
            calendar = assigned_weekend.weekend_model
            weekend_days = [
                day for day, value in {
                    'monday': calendar.monday,
                    'tuesday': calendar.tuesday,
                    'wednesday': calendar.wednesday,
                    'thursday': calendar.thursday,
                    'friday': calendar.friday,
                    'saturday': calendar.saturday,
                    'sunday': calendar.sunday
                }.items() if value == 'leave'
            ]

        holiday_dates = set()
        if assigned_holiday and not include_weekend_and_holiday:
            holiday_dates = set(assigned_holiday.holiday_model.holiday.all().values_list('date', flat=True))

        # Iterate over the date range
        while current_date <= self.end_date:
            # Check if the day should be counted
            if include_weekend_and_holiday or (
                current_date.strftime('%A').lower() not in weekend_days and current_date not in holiday_dates
            ):
                if self.dis_half_day and current_date == self.start_date == self.end_date:
                    leave_days += 0.5
                else:
                    leave_days += 1
            current_date += timedelta(days=1)

        return leave_days
    def deduct_leave_balance(self):
        # Fetch or create the employee's leave balance for this leave type
        leave_balance, created = emp_leave_balance.objects.get_or_create(
            employee=self.employee,
            leave_type=self.leave_type
        )
        print(leave_balance)
        # Deduct the number_of_days from balance, allow negative if leave_type.negative is True
        # if not self.leave_type.negative and leave_balance.balance < self.number_of_days:
        #     raise ValueError("Insufficient leave balance for this leave type.")

        leave_balance.balance -= self.number_of_days
        leave_balance.save()
    
    
    def fetch_rejoining_date(self):
        # Fetch the earliest attendance record after the leave period
        attendance_record = Attendance.objects.filter(
            employee=self.employee,
            date__gt=self.end_date
        ).order_by('date').first()

        return attendance_record.date if attendance_record else None
    def handle_rejoining(self, rejoining_date):
        # Calculate the number of unpaid days (extra leave days)
        unpaid_days = 0
        if rejoining_date > self.end_date:
            unpaid_days = max(0, (rejoining_date - self.end_date).days - 1)
            print("unpaid_days",unpaid_days)

        # Deduct extra leave days from leave balance
        if unpaid_days > 0:
            leave_balance, created = emp_leave_balance.objects.get_or_create(
            employee=self.employee,
            leave_type=self.leave_type
        )
            # Allow negative balance only if leave_type allows it
            # if not self.leave_type.negative and leave_balance.balance < unpaid_days:
            #     raise ValueError("Insufficient leave balance to cover the extra leave days.")
            
            # Deduct extra days
            leave_balance.balance -= unpaid_days
            s=leave_balance.save()
            print("s",s)


        # Create or update the EmployeeRejoining record
        rejoining_record, created = EmployeeRejoining.objects.update_or_create(
            employee=self.employee,
            leave_request=self,
            defaults={
                'rejoining_date': rejoining_date,
                'unpaid_leave_days': unpaid_days
            }
        )

        if created:
            print(f"EmployeeRejoining record created for {self.employee}. Rejoining date: {rejoining_date}, Unpaid days: {unpaid_days}.")
        else:
            print(f"EmployeeRejoining ss record updated for {self.employee}. Rejoining date: {rejoining_date}, Unpaid days: {unpaid_days}.")
    
    def __str__(self):
        return f"{self.employee} - {self.leave_type} from {self.start_date} to {self.end_date}"
    
    # def get_employee_requests(employee_id):
    #     return employee_leave_request.objects.filter(employee_id=employee_id).order_by('-applied_on')
     
    def move_to_next_level(self):
        if self.approvals.filter(status=LeaveApproval.REJECTED).exists():
            self.status = 'Rejected'
            self.save()

            # Notify rejection
            notification = LvApprovalNotify.objects.create(
                recipient_user=self.created_by,
                message=f"Your request for  {self.leave_type} has been rejected."
            )
            notification.send_email_notification('request_rejected', {
                'request_type': self.leave_type,
                'rejection_reason': 'Reason for rejection...',
                'emp_gender': self.employee.emp_gender,
                'emp_date_of_birth': self.employee.emp_date_of_birth,
                'emp_personal_email': self.employee.emp_personal_email,
                'emp_branch_name': self.employee.emp_branch_id,
                'emp_department_name': self.employee.emp_dept_id,
                'emp_designation_name': self.employee.emp_desgntn_id,
            })

            if self.employee:
                notification = LvApprovalNotify.objects.create(
                    recipient_employee=self.employee,
                    message=f"Request {self.leave_type} has been rejected."
                )
                notification.send_email_notification('request_rejected', {
                    'request_type': self.leave_type,
                    'rejection_reason': 'Reason for rejection...',
                    'emp_gender': self.employee.emp_gender,
                    'emp_date_of_birth': self.employee.emp_date_of_birth,
                    'emp_personal_email': self.employee.emp_personal_email,
                    'emp_branch_name': self.employee.emp_branch_id,
                    'emp_department_name': self.employee.emp_dept_id,
                    'emp_designation_name': self.employee.emp_desgntn_id,
                })
            return

        current_approved_levels = self.approvals.filter(status=LeaveApproval.APPROVED).count()

        if self.leave_type.use_common_workflow:
            next_level = LvCommonWorkflow.objects.filter(level=current_approved_levels + 1).first()
        else:
            next_level = LeaveApprovalLevels.objects.filter(request_type=self.leave_type, level=current_approved_levels + 1).first()

        if next_level:
            last_approval = self.approvals.order_by('-level').first()
            LeaveApproval.objects.create(
                leave_request=self,
                approver=next_level.approver,
                role=next_level.role,
                level=next_level.level,
                status=LeaveApproval.PENDING,
                note=last_approval.note if last_approval else None,
                employee_id=self.employee_id
            )

            # Notify next approver
            notification = LvApprovalNotify.objects.create(
                recipient_user=next_level.approver,
                message=f"New request for approval: {self.leave_type}, employee: {self.employee}"
            )
            notification.send_email_notification('request_created', {
                'request_type': self.leave_type,
                'employee_name': self.employee.emp_first_name,
                'reason': self.reason,
                'note': last_approval.note if last_approval else None,
                'emp_gender': self.employee.emp_gender,
                'emp_date_of_birth': self.employee.emp_date_of_birth,
                'emp_personal_email': self.employee.emp_personal_email,
                'emp_branch_name': self.employee.emp_branch_id,
                'emp_department_name': self.employee.emp_dept_id,
                'emp_designation_name': self.employee.emp_desgntn_id,
            })
        else:
            self.status = 'Approved'
            self.save()

            # Notify the creator about approval
            notification = LvApprovalNotify.objects.create(
                recipient_user=self.created_by,
                message=f"Your request {self.leave_type} has been approved."
            )
            notification.send_email_notification('request_approved', {
                'request_type': self.leave_type,
                'emp_gender': self.employee.emp_gender,
                'emp_date_of_birth': self.employee.emp_date_of_birth,
                'emp_personal_email': self.employee.emp_personal_email,
                'emp_branch_name': self.employee.emp_branch_id,
                'emp_department_name': self.employee.emp_dept_id,
                'emp_designation_name': self.employee.emp_desgntn_id,
            })

            if self.employee:
                notification = LvApprovalNotify.objects.create(
                    recipient_employee=self.employee,
                    message=f"Request {self.leave_type} has been approved."
                )
                notification.send_email_notification('request_approved', {
                    'request_type': self.leave_type,
                    'emp_gender': self.employee.emp_gender,
                    'emp_date_of_birth': self.employee.emp_date_of_birth,
                    'emp_personal_email': self.employee.emp_personal_email,
                    'emp_branch_name': self.employee.emp_branch_id,
                    'emp_department_name': self.employee.emp_dept_id,
                    'emp_designation_name': self.employee.emp_desgntn_id,
                })

class EmployeeRejoining(models.Model):
    employee = models.ForeignKey('EmpManagement.emp_master', on_delete=models.CASCADE)
    leave_request = models.OneToOneField('employee_leave_request', on_delete=models.CASCADE)
    rejoining_date = models.DateField()
    unpaid_leave_days = models.FloatField(default=0)
    # paid_leave_days = models.IntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Rejoining for {self.employee.emp_first_name} on {self.rejoining_date}"
class LvRejectionReason(models.Model):
    reason_text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.reason_text

class LeaveApprovalLevels(models.Model):
    level            = models.IntegerField()
    role             = models.CharField(max_length=50, null=True, blank=True)  # Use this for role-based approval like 'CEO' or 'Manager'
    approver         = models.ForeignKey('UserManagement.CustomUser', null=True, blank=True, on_delete=models.SET_NULL)  # Use this for user-based approval
    request_type     = models.ForeignKey('leave_type', related_name='leave_approval_levels', on_delete=models.CASCADE, null=True, blank=True)  # Nullable for common workflow
    is_compensatory  = models.BooleanField(default=False)
    class Meta:
        unique_together = ('level', 'request_type')

class LeaveApproval(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    leave_request = models.ForeignKey(employee_leave_request, related_name='approvals', on_delete=models.CASCADE,null=True, blank=True)
    compensatory_request = models.ForeignKey(CompensatoryLeaveRequest, related_name='approvals', on_delete=models.CASCADE, null=True, blank=True)
    approver = models.ForeignKey('UserManagement.CustomUser', on_delete=models.CASCADE)
    role = models.CharField(max_length=50, null=True, blank=True)
    level = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default=PENDING)
    note = models.TextField(null=True, blank=True)
    rejection_reason = models.ForeignKey(LvRejectionReason,null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    employee_id = models.IntegerField(null=True, blank=True)

    def approve(self, note=None):
        self.status = self.APPROVED
        if note:
            self.note = note
        self.save()
        if self.leave_request:
            self.leave_request.move_to_next_level()
        elif self.compensatory_request:
            self.compensatory_request.move_to_next_level()

    def reject(self, rejection_reason, note=None):
        if rejection_reason:
            self.rejection_reason = rejection_reason
        self.status = self.REJECTED
        if note:
            self.note = note
        self.save()
        if self.leave_request:
            self.leave_request.status = 'Rejected'
            self.leave_request.save()
        elif self.compensatory_request:
            self.compensatory_request.status = 'Rejected'
            self.compensatory_request.save()

        if self.leave_request:
            self.leave_request.status = 'Rejected'
            self.leave_request.save()

            notification = LvApprovalNotify.objects.create(
                recipient_user=self.leave_request.created_by,
                message=f"Your leave request has been rejected."
            )
            notification.send_email_notification('request_rejected', {
                'request_type': self.leave_request.leave_type,
                'rejection_reason': self.rejection_reason.reason_text if self.rejection_reason else "No reason provided",
                'emp_gender': self.leave_request.employee.emp_gender,
                'emp_date_of_birth': self.leave_request.employee.emp_date_of_birth,
                'emp_personal_email': self.leave_request.employee.emp_personal_email,
                'emp_branch_name': self.leave_request.employee.emp_branch_id,
                'emp_department_name': self.leave_request.employee.emp_dept_id,
                'emp_designation_name': self.leave_request.employee.emp_desgntn_id,
                'emp_hired_date': self.leave_request.employee.emp_hired_date,
            })

            if self.leave_request.employee:
                notification = LvApprovalNotify.objects.create(
                    recipient_employee=self.leave_request.employee,
                    message=f"Your leave request has been rejected."
                )
                notification.send_email_notification('request_rejected', {
                    'request_type': self.leave_request.leave_type,
                    'rejection_reason': self.rejection_reason.reason_text if self.rejection_reason else "No reason provided",
                    'emp_gender': self.leave_request.employee.emp_gender,
                    'emp_date_of_birth': self.leave_request.employee.emp_date_of_birth,
                    'emp_personal_email': self.leave_request.employee.emp_personal_email,
                    'emp_branch_name': self.leave_request.employee.emp_branch_id,
                    'emp_department_name': self.leave_request.employee.emp_dept_id,
                    'emp_designation_name': self.leave_request.employee.emp_desgntn_id,
                    'emp_hired_date': self.leave_request.employee.emp_hired_date,
                })

        # Handle notifications for compensatory requests
        elif self.compensatory_request:
            self.compensatory_request.status = 'Rejected'
            self.compensatory_request.save()

            notification = LvApprovalNotify.objects.create(
                recipient_user=self.compensatory_request.created_by,
                message=f"Your compensatory leave request has been rejected."
            )
            notification.send_email_notification('request_rejected', {
                'request_type': 'Compensatory Leave',
                'rejection_reason': self.rejection_reason.reason_text if self.rejection_reason else "No reason provided",
                'emp_gender': self.compensatory_request.employee.emp_gender,
                'emp_date_of_birth': self.compensatory_request.employee.emp_date_of_birth,
                'emp_personal_email': self.compensatory_request.employee.emp_personal_email,
                'emp_branch_name': self.compensatory_request.employee.emp_branch_id,
                'emp_department_name': self.compensatory_request.employee.emp_dept_id,
                'emp_designation_name': self.compensatory_request.employee.emp_desgntn_id,
                'emp_hired_date': self.compensatory_request.employee.emp_hired_date,
            })

            if self.compensatory_request.employee:
                notification = LvApprovalNotify.objects.create(
                    recipient_employee=self.compensatory_request.employee,
                    message=f"Your compensatory leave request has been rejected."
                )
                notification.send_email_notification('request_rejected', {
                    'request_type': 'Compensatory Leave',
                    'rejection_reason': self.rejection_reason.reason_text if self.rejection_reason else "No reason provided",
                    'emp_gender': self.compensatory_request.employee.emp_gender,
                    'emp_date_of_birth': self.compensatory_request.employee.emp_date_of_birth,
                    'emp_personal_email': self.compensatory_request.employee.emp_personal_email,
                    'emp_branch_name': self.compensatory_request.employee.emp_branch_id,
                    'emp_department_name': self.compensatory_request.employee.emp_dept_id,
                    'emp_designation_name': self.compensatory_request.employee.emp_desgntn_id,
                    'emp_hired_date': self.compensatory_request.employee.emp_hired_date,
                })
    
@receiver(post_save, sender=employee_leave_request)
def create_initial_approval(sender, instance, created, **kwargs):
    if created:
        if instance.leave_type.use_common_workflow:
            first_level = LvCommonWorkflow.objects.order_by('level').first()
        else:
        # Select the first approval level
            first_level = LeaveApprovalLevels.objects.filter(request_type=instance.leave_type).order_by('level').first()

        if first_level:
            # Prevent duplicate creation of approvals at the same level
            if not instance.approvals.filter(level=first_level.level).exists():
                LeaveApproval.objects.create(
                    leave_request=instance,
                    approver=first_level.approver,
                    role=first_level.role,
                    level=first_level.level,
                    status=LeaveApproval.PENDING,
                    employee_id=instance.employee_id
                )
            # Notify first approver
            notification = LvApprovalNotify.objects.create(
                recipient_user=first_level.approver,
                message=f"New request for approval: {instance.leave_type}, employee: {instance.employee}"
            )
            notification.send_email_notification('request_created', {
                'request_type': instance.leave_type,
                'employee_name': instance.employee.emp_first_name,
                'reason': instance.reason,
                'emp_gender':instance.employee.emp_gender,
                'emp_date_of_birth':instance.employee.emp_date_of_birth,
                'emp_personal_email':instance.employee.emp_personal_email,
                'emp_branch_name':instance.employee.emp_branch_id,
                'emp_department_name':instance.employee.emp_dept_id,
                'emp_designation_name':instance.employee.emp_desgntn_id,
            }) 


class EmployeeMachineMapping(models.Model):
    employee = models.ForeignKey("EmpManagement.emp_master", on_delete=models.CASCADE)
    machine_code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.employee.emp_code} - {self.machine_code}'

class Shift(models.Model):
    name            = models.CharField(max_length=50)
    start_time      = models.TimeField(null=True, blank=True)  # Optional for off days
    end_time        = models.TimeField(null=True, blank=True)    # Optional for off days
    break_duration  = models.DurationField(default=timedelta(minutes=0))  # Break time in minutes

    def __str__(self):
        return f"{self.name}"
    
class ShiftPattern(models.Model):
    """Defines a shift pattern for a rotating schedule, managing shifts by week and weekday."""
    name             = models.CharField(max_length=100)  # Name for the pattern (e.g., 'Morning Rotation')
    # rotation_cycle_weeks = models.IntegerField(default=4)  # Length of the rotation cycle
    monday_shift     = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='pattern_monday')
    tuesday_shift    = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='pattern_tuesday')
    wednesday_shift  = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='pattern_wednesday')
    thursday_shift   = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='pattern_thursday')
    friday_shift     = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='pattern_friday')
    saturday_shift   = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='pattern_saturday')
    sunday_shift     = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, related_name='pattern_sunday')

    def get_shift_for_day(self, weekday):
        """Return the shift for the given weekday (0=Monday, ..., 6=Sunday)."""
        shifts = {
            0: self.monday_shift,
            1: self.tuesday_shift,
            2: self.wednesday_shift,
            3: self.thursday_shift,
            4: self.friday_shift,
            5: self.saturday_shift,
            6: self.sunday_shift,
        }
        return shifts.get(weekday)

    def __str__(self):
        return f"Shift Pattern: {self.name}"

class EmployeeShiftSchedule(models.Model):
    """Handles shift assignments for employees and departments over a rotating schedule."""
    employee             = models.ManyToManyField('EmpManagement.emp_master', blank=True)
    departments          = models.ManyToManyField('OrganisationManager.dept_master', blank=True)
    week_patterns        = models.ManyToManyField(ShiftPattern, through='WeekPatternAssignment', blank=True,related_name='week_pattern_schedules')
    rotation_cycle_weeks = models.IntegerField(default=4)  # Total weeks in the rotation cycle
    start_date           = models.DateField(default=timezone.now, blank=True)
    is_rotating          = models.BooleanField(default=True)  # Flag for rotating schedule or not
    single_shift_pattern = models.ForeignKey(ShiftPattern, null=True, blank=True, on_delete=models.SET_NULL,related_name='single_shift_schedules')
    def get_shift_for_date(self, employee, date):
        """Determine the shift for a given date."""
        if not self.is_rotating:  # If not rotating, use a single shift pattern
            if self.single_shift_pattern:
                weekday = date.weekday()
                return self.single_shift_pattern.get_shift_for_day(weekday)
            return None

        # Check if there's an override shift for the specific date
        override = ShiftOverride.objects.filter(employee=employee, date=date).first()
        if override:
            return override.override_shift

        # Ensure date is in date format
        if isinstance(date, datetime):
            date = date.date()

        # Get the schedule start date for the employee
        start_date = self.get_schedule_start_date(employee)

        # Calculate the week number within the month
        month_start_date = date.replace(day=1)
        days_since_month_start = (date - month_start_date).days
        week_number_in_month = (days_since_month_start // 7) + 1

        # Calculate week number in the rotation cycle based on month-based calculation
        week_number = ((week_number_in_month - 1) % self.rotation_cycle_weeks) + 1

        print(f"Start Date: {start_date}")
        print(f"Month Start Date: {month_start_date}")
        print(f"Days Since Month Start: {days_since_month_start}")
        print(f"Week Number in Month: {week_number_in_month}")
        print(f"Week Number in Rotation Cycle: {week_number}")

        # Retrieve the shift pattern template for the calculated week
        assignment = WeekPatternAssignment.objects.filter(schedule=self, week_number=week_number).first()
        if assignment and assignment.template:
            weekday = date.weekday()
            return assignment.template.get_shift_for_day(weekday)
        return None
    
    
    def get_schedule_start_date(self, employee):
        # Get the current year for calculation
        current_year = timezone.now().year
        # Set January 1st of the current year as the start date for schedule
        return timezone.datetime(current_year, 1, 1).date()
    

    def __str__(self):
        return f"Rotating Shift Schedule for {self.departments} "
class WeekPatternAssignment(models.Model):
    """Assigns a shift pattern template to a specific week in the rotation."""
    schedule = models.ForeignKey(EmployeeShiftSchedule, on_delete=models.CASCADE)
    week_number = models.IntegerField()  # Week number in the cycle
    template = models.ForeignKey(ShiftPattern, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('schedule', 'week_number')  # Ensure unique assignment per week in a schedule

    def __str__(self):
        return f"Week {self.week_number} using {self.template.name} in {self.schedule}"

class ShiftOverride(models.Model):
    employee = models.ForeignKey('EmpManagement.emp_master', on_delete=models.CASCADE)
    date = models.DateField()
    override_shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('employee', 'date')  # Ensure only one override per employee per date

    def __str__(self):
        return f"Shift Override for {self.employee} on {self.date}"
    
class Attendance(models.Model):
    employee       = models.ForeignKey("EmpManagement.emp_master", on_delete=models.CASCADE)
    shift          = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    date           = models.DateField()
    check_in_time  = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    total_hours    = models.DurationField(null=True, blank=True)
    class Meta:
        unique_together = ('employee', 'date')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if this attendance marks rejoining after approved leave
        approved_leave = employee_leave_request.objects.filter(
            employee=self.employee,
            status='Approved',
            end_date__lt=self.date
        ).order_by('-end_date').first()

        if approved_leave:
            # Trigger rejoining logic
            approved_leave.handle_rejoining(self.date)
    def calculate_total_hours(self):
        if self.check_in_time and self.check_out_time:
            # Ensure that check_in_time and check_out_time are time objects
            check_in_time = self.check_in_time if isinstance(self.check_in_time, time) else self.check_in_time.time()
            check_out_time = self.check_out_time if isinstance(self.check_out_time, time) else self.check_out_time.time()

            # Combine the date with the check-in and check-out times to get datetime objects
            check_in_datetime = datetime.combine(self.date, check_in_time)
            check_out_datetime = datetime.combine(self.date, check_out_time)

            # Handle check-out after midnight
            if check_out_datetime < check_in_datetime:
                check_out_datetime += timedelta(days=1)

            # Calculate total time worked as a timedelta
            total_duration = check_out_datetime - check_in_datetime
            self.total_hours = total_duration  # Store as timedelta (if using DurationField)
            self.save()
    
    def __str__(self):
        return f"attendance of {self.employee} on {self.date}"
class LeaveReport(models.Model):
    file_name   = models.CharField(max_length=100,null=True,unique=True)
    report_data = models.FileField(upload_to='leave_report/', null=True, blank=True)
    class Meta:
        permissions = (
            ('export_report', 'Can export report'),
            # Add more custom permissions here
        )
    
    
    def __str__(self):
        return self.file_name 
    
class LeaveApprovalReport(models.Model):
    file_name   = models.CharField(max_length=100,null=True,unique=True)
    report_data = models.FileField(upload_to='leave_approval_report/', null=True, blank=True)
    class Meta:
        permissions = (
            ('export_report', 'Can export report'),
            # Add more custom permissions here
        )
       
    def __str__(self):
        return self.file_name 

class AttendanceReport(models.Model):
    file_name   = models.CharField(max_length=100,null=True,unique=True)
    report_data = models.FileField(upload_to='attendance_report/', null=True, blank=True)
    class Meta:
        permissions = (
            ('export_report', 'Can export report'),
            # Add more custom permissions here
        )
       
    def __str__(self):
        return self.file_name 

class lvBalanceReport(models.Model):
    file_name   = models.CharField(max_length=100,null=True,unique=True)
    report_data = models.FileField(upload_to='lvbalance_report/', null=True, blank=True)
    class Meta:
        permissions = (
            ('export_report', 'Can export report'),
            # Add more custom permissions here
        )
       
    def __str__(self):
        return self.file_name


    
    
    
    

    
    
    