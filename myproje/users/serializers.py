# myapp/serializers.py
from rest_framework import serializers
from .models import Ticket, Bus, Feedback, City, Worker, CustomUser

from rest_framework import serializers
from .models import Route, Bus
class RSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'  # Or specify a list of fields you want to serialize

class BSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'  # Adjust fields as necessary
from rest_framework import serializers
from .models import Ticket, Route, Sc # Adjust the import if your models are in a different location

from rest_framework import serializers
from .models import Ticket
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['firstname', 'lastname', 'phone', 'depcity', 'descity', 'date', 'no_seat', 'price', 'side_no', 'plate_no' 'gender' 'email']

from rest_framework import serializers
from .models import Ticket, Sc
class ScSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sc
        fields = '__all__'  # Adjust fields as necessary


from rest_framework import serializers
from .models import Ticket, Route  # Adjust the import if your models are in a different location
class TickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket  # Ensure this is the correct model for tickets
        fields = ['firstname', 'lastname', 'phone', 'plate_no', 'date', 'depcity', 'descity', 'no_seat', 'price', 'side_no']

class TSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket  # Ensure this is the correct model for routes
        fields = '__all__'


from rest_framework import serializers
from .models import Route
class RoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'date', 'depcity', 'descity', 'plate_no', 'side_no']  # Include side_no

"""
from rest_framework import serializers
from .models import Activate
class ActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activate
        fields = ['date', 'depcity', 'descity', 'plate_no', 'kilometer',  'price']  # Include side_no
"""


from rest_framework import serializers
from .models import Route, City  # Import your models
class RouSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['depcity', 'descity', 'date', 'plate_no']  # Include necessary



from rest_framework import serializers
from .models import Route
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


from rest_framework import serializers
from .models import CustomUser
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password', 'fname', 'lname', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


from rest_framework import serializers
class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker  # Replace with your actual model
        fields = '__all__'  # or a list of fields  BusesSerializer


from rest_framework import serializers
class BusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus  # Replace with your actual model
        fields = '__all__'  # or a list of fields  BusesSerializer


from rest_framework import serializers
class CommentteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Replace with your actual model
        fields = '__all__'  # or a list of fields


from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Bus, Sc
class BusSerializer(serializers.ModelSerializer):
    name = serializers.CharField()  # Ensure name is included
    class Meta:
        model = Bus
        fields = ['plate_no', 'sideno', 'no_seats', 'level', 'name', 'firstname', 'lastname', 'phone']

    def create(self, validated_data):
        # Retrieve the name from validated data
        name = validated_data.get('name')
        # Get the corresponding Sc instance
        try:
            sc_instance = Sc.objects.get(name=name)
            validated_data['level'] = sc_instance.level  # Set the level from Sc
        except Sc.DoesNotExist:
            raise serializers.ValidationError({"name": "The selected name does not exist."})
        # Create the Bus instance with the updated validated_data
        bus = Bus.objects.create(**validated_data)
        return bus

from rest_framework import serializers
from .models import Bus, Route, Ticket, Buschange
class BusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buschange
        fields = ['plate_no', 'side_no', 'new_plate_no', 'new_side_no', 'date', 'depcity', 'descity']

class CSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['depcity']  # Adjust fields as needed

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Worker, Service_fee
class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['username', 'phone', 'password', 'fname', 'lname', 'city', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['depcity']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_fee
        fields = ['service_fee']



from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Worker, Sc
class scSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sc
        fields = ['username', 'phone', 'password', 'name', 'side', 'firstname', 'email', 'level', 'lastname', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)



from rest_framework import serializers
from .models import Bus
class BusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['plate_no', 'sideno', 'no_seats']

from rest_framework import serializers
from .models import Feedback
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'phone', 'message']


from rest_framework import serializers
from .models import Route
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

