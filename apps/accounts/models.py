from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model with role-based access control.
    Supports three user types: Admin, Kitchen Staff, and Customer.
    """
    
    class UserRole(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        KITCHEN = 'KITCHEN', 'Kitchen Staff'
        CUSTOMER = 'CUSTOMER', 'Customer'
    
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
        help_text="User role determines access level"
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin(self):
        """Check if user is an administrator"""
        return self.role == self.UserRole.ADMIN
    
    def is_kitchen_staff(self):
        """Check if user is kitchen staff"""
        return self.role == self.UserRole.KITCHEN
    
    def is_customer(self):
        """Check if user is a customer"""
        return self.role == self.UserRole.CUSTOMER
