from django.db import models


class User(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile_no = models.BigIntegerField(unique=True,null=True, blank=True)
    password = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    pincode = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'User Info'

    def __int__(self):
        return self.mobile_no
    


class UserToken(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    token = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "User_token"

    def __str__(self):
        return self.token


class Resources(models.Model):

    objects = None
    id = models.AutoField(primary_key=True)
    resource = models.CharField(max_length=100)
    quantity_available = models.FloatField()
    quantity_sold = models.FloatField()
    quantity_unit = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resources'
        unique_together = ('resource', 'quantity_unit')

    def __str__(self):
        return self.resource


class BookedResources(models.Model):

    objects = None
    id = models.AutoField(primary_key=True)
    quantity = models.FloatField(default=0.0)
    resources = models.ForeignKey(Resources, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "booked_resource"






