# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)

    fname = models.CharField(max_length=50, null=True, blank=True)
    lname = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.email} - {self.fname} - {self.lname} - {self.gender} - {self.phone} - {self.registration_id} - {self.registered_time}"



import uuid
from django.db import models
class Feedback(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    message = models.CharField(max_length=255, null=True, blank=True)  # Increased length for messages

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='feedback_set',  # Unique related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='feedback_permissions_set',  # Unique related name
        blank=True
    )
    def __str__(self):
        return f"{self.name} - {self.email} - {self.phone} - {self.message} - {self.registration_id} - {self.registered_time}"




import uuid
from django.db import models
class Bus(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    plate_no = models.CharField(max_length=50, null=True, blank=True)
    sideno = models.CharField(max_length=50, null=True, blank=True)
    no_seats = models.CharField(max_length=50, null=True, blank=False)
    level = models.CharField(max_length=50, null=False, blank=False, default='unknown')  # Replace 'unknown' with your desired default
    groups = models.ManyToManyField('auth.Group', related_name='bus_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='bus_permissions_set', blank=True)
    def __str__(self):
        return f"{self.plate_no} - {self.sideno} - {self.lastname} {self.firstname} - {self.name} {self.level} - {self.registration_id} - {self.registered_time}"



import uuid
from django.db import models
class City(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='city_set',  # Unique related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='city_permissions_set',  # Unique related name
        blank=True
    )
    def __str__(self):
        return f"{self.depcity} - {self.registration_id} - {self.registered_time}"

import uuid
from django.db import models
class Service_fee(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)

    service_fee = models.CharField(max_length=50, null=True, blank=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='service_fee_set',  # Unique related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='service_fee_permissions_set',  # Unique related name
        blank=True
    )
    def __str__(self):
        return f"{self.service_fee} - {self.registration_id} - {self.registered_time}"


import uuid
from django.db import models
class Route(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    kilometer = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    plate_no = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)  # Add this line
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='route_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='route_permissions_set',
        blank=True
    )
    def __str__(self):
        return f"{self.depcity} - {self.descity}, {self.plate_no} - {self.side_no} - {self.kilometer} - {self.price} - {self.date} - {self.registration_id} - {self.registered_time} - {self.is_active}"


import uuid
from django.db import models
from django.contrib.auth.hashers import make_password
class Sc(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    side = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    level = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=128)  # Store hashed password
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='sc_set',
        blank=True
    )
    sc_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='sc_permissions_set',
        blank=True
    )
    def set_password(self, raw_password):
        self.password = make_password(raw_password)  # Hash the password
    def __str__(self):
        return f"{self.username} - {self.firstname} - {self.lastname} - {self.gender} - {self.name} - {self.side} - {self.email} - {self.level} - {self.phone} - {self.registration_id} - {self.registered_time}"





import uuid
from django.db import models
class Worker(models.Model):
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    fname = models.CharField(max_length=50, null=True, blank=True)
    lname = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)  # Store hashed password
    #side_no = models.CharField(max_length=50, null=True, blank=True)
    #plate_no = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='worker_set',
        blank=True
    )
    worker_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='worker_permissions_set',
        blank=True
    )
    def __str__(self):
        return f"{self.username} - {self.fname} - {self.lname} - {self.gender} - {self.phone} - {self.city}  - {self.registration_id} - {self.registered_time}"


from django.contrib.auth.models import AbstractUser
from django.db import models
class Admin(models.Model):
    #id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)

    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    registered_time = models.DateTimeField(auto_now_add=True)


    fname = models.CharField(max_length=50, null=True, blank=True)
    lname = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)  # Store hashed password
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='admin_set',
        blank=True
    )
    admin_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='admin_permissions_set',
        blank=True
    )

    def formatted_registered_time(self):
        # Convert registered_time to the current timezone
        local_registered_time = self.registered_time.astimezone(timezone.get_current_timezone())
        return local_registered_time.strftime('%m,%d,%Y %I:%M %p')

    def save(self, *args, **kwargs):
        # Populate date and time components before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.fname} - {self.lname} - {self.gender} - {self.password} - {self.phone} - {self.registration_id} - {self.registered_time}"



import uuid
import random
import string
from django.db import models
from django.utils import timezone
import qrcode
from io import BytesIO
import base64
class Ticket(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pnr = models.CharField(max_length=6, unique=True, editable=False)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    no_seat = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=20, null=True, blank=True)
    plate_no = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    booked_time = models.DateTimeField(default=timezone.now)
    qr_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - PNR: {self.pnr} - username: {self.username}"
    def generate_pnr(self):
        return ''.join(random.choices(string.ascii_uppercase, k=6))

    def generate_qr_data(self):
        return (
            f"Ticket ID: {self.ticket_id}\n"
            f"PNR: {self.pnr}\n"
            f"Name: {self.firstname} {self.lastname}\n"
            f"Phone: {self.phone}\n"
            f"Departure City: {self.depcity}\n"
            f"Destination City: {self.descity}\n"
            f"Date: {self.date}\n"
            f"No. of Seats: {self.no_seat}\n"
            f"Price: {self.price}\n"
            f"Side No: {self.side_no}\n"
            f"Plate No: {self.plate_no}\n"
            f"Booked Time: {self.booked_time}"
        )

    def generate_qr_code(self):
        data = self.generate_qr_data()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        qr_code = 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()
        
        return qr_code

    def save(self, *args, **kwargs):
        if not self.pnr:
            self.pnr = self.generate_pnr()

        super().save(*args, **kwargs)
        self.qr_code = self.generate_qr_code()
        self.__class__.objects.filter(ticket_id=self.ticket_id).update(qr_code=self.qr_code)


"""
class Buschange(models.Model):
    new_side_no = models.CharField(max_length=50, null=True, blank=True)
    new_plate_no = models.CharField(max_length=50, null=True, blank=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=20, null=True, blank=True)
    plate_no = models.CharField(max_length=20, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='buschange_set',
        blank=True
    )
    buschange_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='buschange_permissions_set',
        blank=True
    )
    def __str__(self):
        return f"{self.depcity} - {self.descity}, {self.new_side_no} - {self.new_plate_no}, - {self.plate_no} - {self.side_no} - {self.date}"
"""
from django.db import models

class Buschange(models.Model):
    new_side_no = models.CharField(max_length=50, null=True, blank=True)
    new_plate_no = models.CharField(max_length=50, null=True, blank=True)
    depcity = models.CharField(max_length=50, null=True, blank=True)
    descity = models.CharField(max_length=50, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    side_no = models.CharField(max_length=20, null=True, blank=True)
    plate_no = models.CharField(max_length=20, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='buschange_set',
        blank=True
    )
    buschange_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='buschange_permissions_set',
        blank=True
    )

    def __str__(self):
        return f"{self.depcity} - {self.descity}, {self.new_side_no} - {self.new_plate_no}, - {self.plate_no} - {self.side_no} - {self.date}"

