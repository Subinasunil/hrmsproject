
from django.db import models
from OrganisationManager.models import brnch_mstr
# Create your models here.
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,BaseUserManager,PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from .manager import CustomUserManager
from django.contrib.auth import get_user_model
import uuid
from tenant_users.tenants.models import TenantBase,UserProfile
from tenant_users.tenants.tasks import provision_tenant
from django_tenants.models import TenantMixin, DomainMixin
from tenant_users.tenants.models import UserTenantPermissions
from django_tenants.utils import schema_context
from tenant_users.permissions.functional import tenant_cached_property

class company(TenantBase):
    name       = models.CharField(max_length=100)
    paid_until =  models.DateField(auto_now_add=True)
    created_on = models.DateField(auto_now_add=True)
    country    = models.ForeignKey('Core.cntry_mstr',on_delete=models.CASCADE,null=True)
    logo       = models.ImageField(null=True,blank =True )

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def get_timezone(self):
        return self.country.timezone if self.country else 'UTC'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the company and create the schema

        # Ensure a domain exists for the tenant
        if not Domain.objects.filter(domain=f"{self.schema_name}.localhost").exists():
            Domain.objects.create(domain=f"{self.schema_name}.localhost", tenant=self)

        # Switch to the newly created schema
        with schema_context(self.schema_name):
            # Set up the timezone for the tenant's schema
            from django.conf import settings
            settings.TIME_ZONE = self.get_timezone()

            # Create the default branch
            brnch_mstr.objects.create(
                branch_name=self.name,
                branc_logo=self.logo,
                branch_code='BR001',
                notification_period_days=30,
                br_country_id=self.country.id,
                br_city='Sample City',
                br_pincode='123456',
                br_branch_nmbr_1='BR-0001',
                br_branch_mail='branch@example.com',
            )

    def __str__(self):
        return self.schema_name
    
class Domain(DomainMixin):
    pass


class CustomUser(UserProfile):
    username     = models.CharField(max_length=150,unique=True)
    is_ess       = models.BooleanField(default=False,null=True,blank =True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'  # Change USERNAME_FIELD to 'username'
    REQUIRED_FIELDS = ['email']  # Remove 'username' from REQUIRED_FIELDS

    objects = CustomUserManager()
    # def save(self, *args, **kwargs):
    #     # Set is_active to True before saving
    #     self.is_active = True
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        # Hash the password if it is not already hashed
        if self.pk is None or not self.password.startswith("pbkdf2_"):
            self.set_password(self.password)
        super().save(*args, **kwargs)
    # Add any additional fields if needed
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    
    
    