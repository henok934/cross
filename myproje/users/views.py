from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import CustomUser
from .models import Feedback
from .models import Bus
from .models import Route
from django.db import IntegrityError
from .models import City
from .models import Buschange
from .models import Admin
from .models import Ticket
from rest_framework import generics, status
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render
from .models import Buschange, City  # Ensure you import your models
def custom_csrf_failure_view(request, reason=""):
    return render(request, 'users/csrf_failure.html', {'reason': reason})
def profile(request):
    user_id = request.session.get('user_id')  # Retrieve the user ID from the session
    user = None
    if user_id:
        user = CustomUser.objects.get(id=user_id)
    return render(request, 'users/profile.html', {'user': user})

def businsert(request):
    if request.method == 'POST':
        plate_no = request.POST['plate_no']
        sideno = request.POST['sideno']
        no_seats = request.POST['no_seats']

        if Bus.objects.filter(plate_no=plate_no).exists():
            return render(request, 'users/Businsert.html', {'error': 'plate_no already exists.'})

        if Bus.objects.filter(sideno=sideno).exists():
            return render(request, 'users/Businsert.html', {'error': 'Side_no already exists.'})
        bus = Bus.objects.create(
            plate_no=plate_no,
            sideno=sideno,
            no_seats=no_seats,
            level=level
        )
        bus.save()
        return render(request, 'users/Businsert.html', {'success': 'Bus registored'})
    return render(request, 'users/Businsert.html')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
class ProcessPaymentView(APIView):
    def post(self, request, *args, **kwargs):
        payment_method = request.POST.get('payment_method')
        price = request.POST.get('price')
        # Check what payment method was selected
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            if payment_method == 'cbe':
                return render(request, 'users/cbe.html', {'price': price})
            elif payment_method == 'boa':
                return render(request, 'users/boa.html', {'price': price})
            elif payment_method == 'telebirr':
                return render(request, 'users/tele.html', {'price': price})
            elif payment_method == 'safaricom':  # Assuming you meant to add this
                return render(request, 'users/safaricom.html', {'price': price})
            elif payment_method == 'awash':
                return render(request, 'users/awash.html', {'price': price})
            else:
                return render(request, 'users/payment.html')
        return render(request, 'users/payment.html')



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Buschange  # Adjust based on your actual model imports
class AboutViews(APIView):
    def get(self, request):
        # Retrieve all bus changes
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        
        context = {
            'buschanges_count': buschanges_count
        }
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/about.html', context)
        return Response(context, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import City, Buschange  # Adjust based on your actual model imports
class HomeViews(APIView):
    def get(self, request):
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        des = City.objects.all()

        context = {
            'des': des,
            'buschanges_count': buschanges_count if buschanges_count > 0 else None
        }
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/index.html', context)

        response_data = {
            'cities': [city.depcity for city in des],
            'buschanges_count': buschanges_count
        }
        return Response(response_data, status=status.HTTP_200_OK)

class About(APIView):
    def get(self, request):
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        des = City.objects.all()

        context = {
            'des': des,
            'buschanges_count': buschanges_count if buschanges_count > 0 else None
        }

        # Check if the request is for HTML
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/about.html', context)

        # Return JSON response for API requests
        response_data = {
            'des': [city.depcity for city in des],
            'buschanges_count': buschanges_count
        }
        return Response(response_data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RouteSerializer
from .models import Route
class RouteViews(APIView):
    def post(self, request):
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            if Route.objects.filter(plate_no=plate_no, side_no=side_no, date=date).exists():
                return Response({'error': 'This bus already has a route.'}, status=status.HTTP_400_BAD_REQUEST)
            if Route.objects.filter(depcity=depcity, descity=descity, plate_no=plate_no, side_no=side_no, date=date).exists():
                return Response({'error': 'Route already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'success': 'Route Registored Successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Worker
from django.contrib.auth.hashers import make_password
class WorkerView(APIView):
    def post(self, request):
        username = request.data.get('username')
        phone = request.data.get('phone')
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        gender = request.data.get('gender')
        plate_no = request.data.get('plate_no')
        side_no = request.data.get('side_no')
        password = request.data.get('password')
        if Worker.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if Worker.objects.filter(phone=phone).exists():
            return Response({'error': 'Phone already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        user = Worker.objects.create(
            username=username,
            password=make_password(password),  # Hash the password
            phone=phone,
            fname=fname,
            lname=lname,
            gender=gender,
            plate_no=plate_no,
            side_no=side_no
        )
        user.save()
        return Response({'success': 'Worker registered successfully.'}, status=status.HTTP_201_CREATED)
    def get(self, request):
        return Response({'error': 'Use POST to register a new user.'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        phone = request.data.get('phone')
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        gender = request.data.get('gender')
        if CustomUser.objects.filter(username=username).exists():
            #return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUST)
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(phone=phone).exists():
            return Response({'error': 'Phone already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=make_password(password1),  # Hash the password
            phone=phone,
            fname=fname,
            lname=lname,
            gender=gender
        )
        user.save()
        return Response({'success': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    def get(self, request):
        return Response({'error': 'Use POST to register a new user.'}, status=status.HTTP_400_BAD_REQUEST)

def worker(request):
    if request.method == 'POST':
        username = request.POST.get['username']
        password = request.POST.get['password']
        phone = request.POST.get['phone']
        fname = request.POST.get['fname']
        lname = request.POST.get['lname']
        gender = request.POST.get['gender']
        plate_no = request.POST.get['plate_no']
        side_no = request.POST.get['side_no']
        bus = Worker.objects.create_user(
            plate_no=plate_no,
            side_no=side_no,
            username=username,
            phone=phone,
            password=password,
            fname=fname,
            lname=lname,
            gender=gender

        )
        bus.save()
    return render(request, 'users/worker.html')


from rest_framework import generics, status
from rest_framework.response import Response
from .models import Bus
from .serializers import BusSerializer
class BusInsert(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            plate_no = serializer.validated_data['plate_no']
            sideno = serializer.validated_data['sideno']
            if Bus.objects.filter(plate_no=plate_no).exists():
                return Response({'error': 'Plate number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            if Bus.objects.filter(sideno=sideno).exists():
                return Response({'error': 'Side number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'success': 'Bus registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def businsert(request):
    if request.method == 'POST':
        plate_no = request.POST['plate_no']
        sideno = request.POST['sideno']
        no_seats = request.POST['no_seats']
        level = request.POST['level']

        if Bus.objects.filter(plate_no=plate_no).exists():
            return render(request, 'users/Businsert.html', {'error': 'plate_no already exists.'})

        if Bus.objects.filter(sideno=sideno).exists():
            return render(request, 'users/Businsert.html', {'error': 'Side_no already exists.'})
        bus = Bus.objects.create(
            plate_no=plate_no,
            sideno=sideno,
            no_seats=no_seats,
            level=level
        )
        bus.save()
        return render(request, 'users/Businsert.html', {'success': 'Bus registored'})
    return render(request, 'users/Businsert.html')


from django.shortcuts import render
from .models import City
def city(request):
    if request.method == 'POST':
        depcity = request.POST['depcity']
        City.objects.create(depcity=depcity)
        City.save()
    return render(request, 'users/city.html')


from rest_framework import generics, status
from rest_framework.response import Response
from .models import City
from .serializers import CitySerializer
class CityInsert(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            depcity = serializer.validated_data['depcity']
            if City.objects.filter(depcity=depcity).exists():
                return Response({'error': 'City already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'success': 'City registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import render
from .models import Feedback, Buschange
from .serializers import FeedbackSerializer
class CommentsView(generics.GenericAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    def get(self, request, *args, **kwargs):
        buschanges_count = Buschange.objects.count()
        return render(request, 'users/comment.html', {'buschanges_count': buschanges_count})

    def post(self, request, *args, **kwargs):
        buschanges_count = Buschange.objects.count()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            message = serializer.validated_data['message']
            phone = serializer.validated_data['phone']
            email = serializer.validated_data['email']
            if Feedback.objects.filter(name=name, message=message, phone=phone, email=email).exists():
                return Response(
                    {'error': 'This Comment already exists.', 'buschanges_count': buschanges_count},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(
                {'success': 'Comment submitted successfully.', 'buschanges_count': buschanges_count},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'error': serializer.errors, 'buschanges_count': buschanges_count},
            status=status.HTTP_400_BAD_REQUEST
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus
class BusInsertViews(APIView):

    def get(self, request, *args, **kwargs):
        return render(request, 'users/Businsert.html')
    def post(self, request, *args, **kwargs):
        # Log the request data
        print(request.data)
        # Extract data from the request
        plate_no = request.data.get('plate_no')
        sideno = request.data.get('sideno')
        no_seats = request.data.get('no_seats')
        level = request.data.get('level', 'unknown')  # Default to 'unknown' if not provided

        # Validate required fields
        if not plate_no or not sideno or not no_seats:
            error_message = 'Plate number, Side number, and Number of seats are required.'
            return self.render_response(request, error=error_message)

        # Check for existing entries
        if Bus.objects.filter(plate_no=plate_no).exists():
            return self.render_response(request, error='Plate number already exists.')

        if Bus.objects.filter(sideno=sideno).exists():
            return self.render_response(request, error='Side number already exists.')

        # Create a new Bus instance
        Bus.objects.create(
            plate_no=plate_no,
            sideno=sideno,
            no_seats=no_seats,
            level=level
        )

        # Return success response
        return self.render_response(request, success='Bus registered successfully.')

    def render_response(self, request, success=None, error=None):
        context = {}
        if success:
            context['success'] = success
        if error:
            context['error'] = error

        # Check if the request accepts HTML
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/Businsert.html', context)
        else:
            # Return JSON response for API requests
            response_data = {'success': success} if success else {'error': error}
            return Response(response_data, status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST)



from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Route, City, Bus
from .serializers import RouteSerializer
class RoutesInsertView(generics.GenericAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    def get(self, request, *args, **kwargs):
        # Pass cities and buses to template for dropdowns
        cities = City.objects.all()
        buses = Bus.objects.all()

        des = City.objects.all()
        dep = City.objects.all()
        bus = Bus.objects.all()

        return render(request, 'users/route.html', {'dep': dep, 'des': des, 'bus': bus})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            depcity = serializer.validated_data['depcity'].strip()
            descity = serializer.validated_data['descity'].strip()
            date = serializer.validated_data['date']
            plate_no = serializer.validated_data['plate_no']
            side_no = serializer.validated_data['side_no']
            price = serializer.validated_data['price']
            kilometer = serializer.validated_data['kilometer']
            if depcity == descity:
                return Response({'error': 'Departure and Destination cannot be the same!'}, status=status.HTTP_400_BAD_REQUEST)
            if Route.objects.filter(depcity=depcity, descity=descity, plate_no=plate_no, side_no=side_no, date=date).exists():
                return Response({'error': 'Route already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            if Route.objects.filter(side_no=side_no, date=date, plate_no=plate_no).exists():
                return Response({'error': 'This bus is already reserved for another route for this date.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            if depcity.lower() == "addisababa":
                next_date = timezone.datetime.strptime(str(date), '%Y-%m-%d') + timedelta(days=1)
                next_date_str = next_date.strftime('%Y-%m-%d')
                Route.objects.create(
                    depcity=descity,
                    descity=depcity,
                    kilometer=kilometer,
                    plate_no=plate_no,
                    side_no=side_no,
                    price=price,
                    date=next_date_str
                )
            return Response({'success': 'route registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import City
from .serializers import CitySerializer
class CityInsertView(generics.GenericAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    def get(self, request, *args, **kwargs):
        return render(request, 'users/city.html')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            depcity = serializer.validated_data['depcity']
            if City.objects.filter(depcity__iexact=depcity).exists():
                return Response({'error': 'City already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'success': 'City registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Ticket, Buschange, City  # Ensure you import your models
def get_ticket(request):
    return render(request, 'users/getticket.html')
class TicketGetAPI(View):
    def get(self, request):
        # For GET requests, return the list of cities and bus changes
        des = City.objects.all().values()
        buschanges_count = Buschange.objects.count()
        response_data = {
            'cities': list(des),
            'buschanges_count': buschanges_count,
        }
        return JsonResponse(response_data)
    def post(self, request):
        depcity = request.POST.get('depcity')
        descity = request.POST.get('descity')
        date = request.POST.get('date')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        print("Received data:", depcity, descity, date, firstname, lastname)  # Log all inputs for debugging
        if not all([depcity, descity, date, firstname, lastname]):
            return JsonResponse({'error': "All fields are required!"}, status=400)

        ticket = Ticket.objects.filter(
        depcity=depcity,
        descity=descity,
        date=date,
        firstname=firstname,
        lastname=lastname
    ).first()
        if ticket:
            qr_code_path = ticket.generate_qr_code()  # Ensure this method exists
            return JsonResponse({
            'success': "Your Ticket is booked.",
            'ticket': ticket.id,
            'qr_code_path': qr_code_path
        })
        return JsonResponse({'error': "No ticket information found for the entered details!"}, status=404)


from django.http import JsonResponse
from django.views import View
from .models import Buschange, City
class AboutPageAPI(View):
    def get(self, request):
        try:
            buschanges = Buschange.objects.all().values()
            buschanges_count = buschanges.count()
            cities = City.objects.all().values()
            response_data = {
                'buschanges_count': buschanges_count,
                'buschanges': list(buschanges),
                'cities': list(cities),
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    def post(self, request):
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)  # Handle POST
    def put(self, request):
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)  # Handle PUT
    def delete(self, request):
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)  # Handle DELETE

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Worker, CustomUser
from .serializers import BusesSerializer, UserSerializer
class Use(APIView):
     def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)  # Serialize the data
        # Check if the request is for HTML
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/users.html', {'users': users})  # Render HTML
        else:
            return Response(serializer.data)  # Return JSON response



from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Worker, CustomUser
from .serializers import BusesSerializer, UserSerializer, ScSerializer
class Sce(APIView):
     def get(self, request):
        users = Sc.objects.all()
        serializer = ScSerializer(users, many=True)  # Serialize the data
        # Check if the request is for HTML
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/sce.html', {'users': users})  # Render HTML
        else:
            return Response(serializer.data)  # Return JSON response


from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Worker, Bus
from .serializers import BusesSerializer
class Buse(APIView):
    def get(self, request):
        buses = Bus.objects.all()  # Fetch all Worker instances
        serializer = BusesSerializer(buses, many=True)  # Serialize the data
        # Check if the request is for HTML
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/buses.html', {'buses': buses})  # Render HTML
        else:
            return Response(serializer.data)  # Return JSON response
    


from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Worker, Feedback, Route
from .serializers import WorkSerializer, CommentteSerializer, RouteSerializer
class Drivers(APIView):
    def get(self, request):
        driver = Worker.objects.all()
        serializer = WorkSerializer(driver, many=True)

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/drivers.html', {'driver': driver})
        else:
            return Response(serializer.data)


class Com(APIView):
    def get(self, request):
        comments = Feedback.objects.all()
        serializer = CommentteSerializer(comments, many=True)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/comments.html', {'comments': comments})
        else:
            return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Route
from .serializers import RouteSerializer
class Rout(APIView):
    def get(self, request):
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/routes.html', {'routes': routes})
        else:
            return Response(serializer.data)



from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bus  # Assuming you have a Bus model
from .serializers import BusSerializer  # Assuming you have a BusSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
class BusesView(APIView):
    def get(self, request):
        buses = Bus.objects.all()  # Fetch all Bus instances
        serializer = BusSerializer(buses, many=True)  # Serialize the data
        return Response(serializer.data)  # Return JSON response


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import render  # Import render
from .models import Ticket, Route
from .serializers import RouteSerializer, TickSerializer, RoutSerializer
class SelectBusView(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    def post(self, request):
        date = request.data.get('date')
        plate_no = request.data.get('plate_no')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        route = Ticket.objects.filter(plate_no=plate_no, date=date, depcity=depcity, descity=descity)
        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)
        if route.exists():
            serialized_route = TickSerializer(route, many=True)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/ticketoch.html', {'route': serialized_route.data})
            else:
                return Response({'route': serialized_route.data})
        else:
            serialized_routes = RoutSerializer(routes, many=True)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rootee.html', {'error': 'No booked tickets for this travel', 'routes': serialized_routes.data})
            return Response({'error': 'No booked tickets for this travel', 'routes': serialized_routes.data})
        return Response({'error': 'Invalid request method'}, status=400)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Ticket, City, Bus
from .serializers import TSerializer
class GetTicketViews(APIView):
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/getticket.html', {'des': des})
        return Response({'des': [city.depcity for city in des]}, status=status.HTTP_200_OK)

    def post(self, request):
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')

        # Validate input
        if depcity == descity:
            error_message = 'Departure and Destination cannot be the same!'
        elif firstname == lastname:
            error_message = 'Firstname and Lastname cannot be the same!'
        else:
            error_message = None

        if error_message:
            des = City.objects.all()
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/getticket.html', {
                    'error': error_message,
                    'des': des
                })
            else:
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the ticket
        ticket = Ticket.objects.filter(
            firstname=firstname,
            lastname=lastname,
            depcity=depcity,
            descity=descity,
            date=date
        ).first()  # Get the first ticket instance or None

        if ticket:
            plate_no = ticket.plate_no
            level = Bus.objects.filter(plate_no=plate_no).values_list('level', flat=True).first() if plate_no else None
            qr_code_path = ticket.generate_qr_code()  # Assuming generate_qr_code is a method of Ticket

            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/tickets.html', {
                    'ticket': ticket,
                    'level': level,
                    'qr_code_path': qr_code_path
                })
            else:
                serialized_ticket = TSerializer(ticket)
                return Response(serialized_ticket.data, status=status.HTTP_200_OK)
        else:
            # No ticket found
            des = City.objects.all()
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/getticket.html', {
                    'error': 'No booked tickets for this travel',
                    'des': des
                })
            else:
                return Response({'error': 'No booked tickets found for this travel'}, status=status.HTTP_404_NOT_FOUND)






from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Route, City
from .serializers import RoutSerializer, TickSerializer
class TicketInfoView(APIView):
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cheeckrouteee.html', {'des': des})  # Render the form
        else:
            return Response({'cities': [city.name for city in des]})  # Return a JSON response with city names
    def post(self, request):
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)
        if routes.exists():
            serialized_route = RoutSerializer(routes, many=True)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rootee.html', {'routes': serialized_route.data})  # Render HTML with routes
            return Response({'routes': serialized_route.data})  # Return JSON response with routes
        else:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                des = City.objects.all()  # Fetch all cities for the form
                return render(request, 'users/cheeckrouteee.html', {'error': 'No booked tickets for this travel', 'des': des})
            return Response({'error': 'No booked tickets for this travel'}, status=404)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from .models import Buschange, Route, Worker, Sc
class LoginView(APIView):
    def get(self, request):
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/login.html', {'buschanges_count': buschanges_count})
        return Response({'buschanges_count': buschanges_count}, status=status.HTTP_200_OK)

    def post(self, request):
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')

        if role == 'worker':
            return self.handle_worker_login(username, password, buschanges_count, request)
        elif role == 'user':
            return self.handle_user_login(username, password, buschanges_count, request)
        elif role == 'sc':
            return self.handle_sc_login(username, password, buschanges_count, request)
        return Response({'error': 'Invalid role specified'}, status=status.HTTP_400_BAD_REQUEST)


    def handle_worker_login(self, username, password, buschanges_count, request):
        try:
            worker = Worker.objects.get(username=username)
            if not check_password(password, worker.password):
                raise Worker.DoesNotExist  # Raise an error if the password is incorrect

            # Set session variables for worker ID and username
            request.session['worker_id'] = worker.id
            request.session['username'] = worker.username  # Store the username in session
            print(f"Session set: worker_id={worker.id}, username={worker.username}")

            # Render the HTML page with the username after successful login
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rooteee.html', {'username': worker.username})

            # Optionally return a JSON response for other formats
            return Response({'username': worker.username}, status=status.HTTP_200_OK)

        except Worker.DoesNotExist:
            return self.handle_login_error(buschanges_count, request, 'This username for Worker not found')


    def handle_user_login(self, username, password, buschanges_count, request):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/profile.html', {'user': user})
            return Response({'message': 'Login successful', 'user': {'id': user.id, 'username': user.username}}, status=status.HTTP_200_OK)
        return self.handle_login_error(buschanges_count, request, 'Invalid username or password')


    def handle_sc_login(self, username, password, buschanges_count, request):
        try:
            sc_user = Sc.objects.get(username=username)
            if not check_password(password, sc_user.password):
                return self.handle_login_error(buschanges_count, request, 'Invalid password')

            request.session['sc_id'] = sc_user.id
            request.session['username'] = sc_user.username

            routes = []
            # Calculate the parts of the `side`
            side_parts = sc_user.side.split('/')
            # Handle both single part and two parts
            if len(side_parts) == 1:
                first_part = side_parts[0].strip()  # Single part
                second_part = None  # No second part
            elif len(side_parts) == 2:
                first_part = side_parts[0].strip()  # Part before '/'
                second_part = side_parts[1].strip()  # Part after '/'
            else:
                return self.handle_login_error(buschanges_count, request, 'Invalid side format')
            # Check if the side value is 3
            if first_part == '3' or second_part == '3':
                # Fetch routes where side_no is exactly 3 digits
                routes = Route.objects.filter(side_no__regex=r'^\d{3}$')
            else:
                filters = Q(side_no__startswith=first_part) & Q(side_no__regex=r'^\d{4}$')
                #filters = Q(sideno__startswith=first_part)
                if second_part:
                    #filters |= Q(sideno__startswith=second_part)
                    filters |= Q(side_no__startswith=second_part) & Q(side_no__regex=r'^\d{4}$')

                    routes = Route.objects.filter(filters)
            serialized_routes = self.serialize_routes(routes)
            name = sc_user.name  # Get the name field
            firstname = sc_user.firstname  # Get the name field
            lastname = sc_user.lastname  # Get the name field
            side = sc_user.side  # Get the side field
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rooteeess.html', {
                'routes': serialized_routes,
                'name': name, 'firstname': firstname,'lastname': lastname,
                'side': side
            })
            return Response({'routes': serialized_routes}, status=status.HTTP_200_OK)
        except Sc.DoesNotExist:
            return self.handle_login_error(buschanges_count, request, 'This username for SC not found')
    def serialize_routes(self, routes):
        return [
            {
                'id': route.id,
                'depcity': route.depcity,
                'date': route.date,
                'plate_no': route.plate_no,
                'side_no': route.side_no,
                'descity': route.descity
            } for route in routes
        ]
    def handle_login_error(self, buschanges_count, request, error_message):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/login.html', {
                'error': error_message,
                'buschanges_count': buschanges_count
            })
        return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from .models import City, Route, Bus, Ticket, Buschange
class Books(APIView):
    des = City.objects.all()
    def get_user_from_session(self, request):
        user_id = request.session.get('worker_id')
        print(f"Worker ID in session: {user_id}")
        if user_id:
            try:
                worker = Worker.objects.get(id=user_id)
                print(f"Worker retrieved: {worker.username}")
                return worker
            except Worker.DoesNotExist:
                print("Worker not found.")
                return None
        print("No user ID found in session.")
        return None
    def get(self, request):
        buschanges_count = Buschange.objects.count()
        worker = self.get_user_from_session(request)

        if not worker:
            print("No worker session found.")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        username = worker.username.strip()
        city = worker.city
        #print(city)
        if city in ['Kality', 'Ayertena', 'Lamberet', 'Autobustera']:
            city = 'Addisababa'  # Change city to 'Addisababa'

        print(city)


        print(f"Username for session: {username}")
        #if city = Kality || Ayertena || lamberet || Autobustera = Addisababa
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/book.html', {
                'des': City.objects.all(), 'username': username, 'city': city,
                'buschanges_count': buschanges_count
            })
        return Response({'des': [city.name for city in des], 'buschanges_count': buschanges_count}, status=status.HTTP_200_OK)

    def post(self, request):
        worker = self.get_user_from_session(request)
        username = worker.username.strip()
        city = worker.city
        #print(city)
        if city in ['Kality', 'Ayertena', 'Lamberet', 'Autobustera']:
            city = 'Addisababa'  # Change city to 'Addisababa'

        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        try:
            # This line correctly parses the date in the format YYYY-MM-DD
            incoming_date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            # Handle invalid date format
            error_message = "Invalid date format. Please use YYYY-MM-DD."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/book.html', {
                    'des': City.objects.all(), 'city': city,'username': username,
                    'buschanges_count': Buschange.objects.count(),
                    'error': error_message
                })
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        today = timezone.now().date()  # Get today's date

        # Check if the incoming date is before today
        if incoming_date.date() < today:
            error_message = f"Error Incorrect date inserted."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/book.html', {
                    'des': City.objects.all(),'username': username,
                    'buschanges_count': Buschange.objects.count(),
                    'error': error_message,'city': city
                })
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        rout = Route.objects.filter(depcity=depcity, descity=descity, date=date)
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        routes = []
        error_message = "There is no Travel for this information!"
        routes = []
        remaining_seats = 0
        if rout.exists():
            for route in rout:
                buses = Bus.objects.filter(plate_no=route.plate_no)
                levels = buses.first().level if buses.exists() else None
                total_seats = sum(int(bus.no_seats) for bus in buses) if buses.exists() else 0
                booked_tickets = Ticket.objects.filter(
                    depcity=route.depcity,
                    descity=route.descity,
                    date=route.date,
                    plate_no=route.plate_no
                ).count()
                remaining_seats = total_seats - booked_tickets
                # Check if remaining seats are negative
                if remaining_seats < 0:
                    routes = []  # Clear routes if any are found, as we can't have negative remaining seats
                    break  # Exit the loop since we found an invalid state

                # Only add the route if there are remaining seats
                if remaining_seats > 0:
                    routes.append({
                        'route': route,
                        'levels': levels,
                        'remaining_seats': remaining_seats
                    })

        # Check if there are no valid routes or if remaining seats are negative
        if remaining_seats < 0 or not routes:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/book.html', {
                    'des': City.objects.all(),'username': username,
                    'buschanges_count': buschanges_count,
                    'error': error_message, 'city': city,
                })
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'routes': routes,
            'levels': levels,
            'buschanges_count': buschanges_count
        }
        worker = self.get_user_from_session(request)
        username = worker.username
        #all_routes = Activate.objects.all()  # Fetch all records
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/roo.html', {
                'routes': routes,
                'levels': levels,
                'username': username,
                'buschanges_count': buschanges_count
            })
        return Response(response_data, status=status.HTTP_200_OK)

class SeeView(APIView):
    def get_user_from_session(self, request):
        user_id = request.session.get('worker_id')
        print(f"Worker ID in session: {user_id}")
        if user_id:
            try:
                worker = Worker.objects.get(id=user_id)
                print(f"Worker retrieved: {worker.username}")
                return worker
            except Worker.DoesNotExist:
                print("Worker not found.")
                return None
        print("No user ID found in session.")
        return None

    def get(self, request):
        buschanges_count = Buschange.objects.count()
        worker = self.get_user_from_session(request)

        if not worker:
            print("No worker session found.")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        username = worker.username.strip()
        print(f"Username for session: {username}")

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/roo.html', {
                'buschanges_count': buschanges_count,
                'username': username
            })
        return Response({'buschanges_count': buschanges_count}, status=status.HTTP_200_OK)

    def post(self, request):
        plate_no = request.data.get('plate_no')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        routes = Route.objects.filter(depcity=depcity, descity=descity, date=date, plate_no=plate_no)
        route_info = []
        unbooked_seats = []
        booked_seats = []
        bus_full = False
        buses = Bus.objects.filter(plate_no=plate_no)
        levels = buses.first().level if buses.exists() else None
        for route in routes:
            try:
                bus = Bus.objects.get(plate_no=route.plate_no)
                #buses = Bus.objects.get(plate_no=plate_no)
                #levels = buses.first().level if buses.exists() else None
                total_seats = int(bus.no_seats)
                booked_tickets = Ticket.objects.filter(
                    depcity=route.depcity,
                    descity=route.descity,
                    date=route.date,
                    plate_no=route.plate_no
                ).values_list('no_seat', flat=True)
                booked_seats = set(int(seat) for seat in booked_tickets if seat)
                booked_seat_count = len(booked_seats)
                remaining_seats = total_seats - booked_seat_count
                unbooked_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]

                if route.plate_no == plate_no and remaining_seats <= 0:
                    bus_full = True
                    route_info.append({
                        'route': route,'levels': levels,
                        'remaining_seats': remaining_seats if remaining_seats > 0 else "Full"
                    })
            except Bus.DoesNotExist:
                continue
        if bus_full:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/roo.html', {
                    'error': 'This Bus is Full!','levels': levels,
                    'buschanges_count': buschanges_count
                })
            return Response({'error': 'This Bus is Full!'}, status=status.HTTP_400_BAD_REQUEST)
            # Serialize the routes
            # Serialize the routes
        serialized_routes = RouteSerializer(routes, many=True).data
        all_seats = list(range(1, total_seats + 1) if 'total_seats' in locals() else [])
        response_data = {
                'routes': serialized_routes,'levels': levels,
            'remaining_seats': len(unbooked_seats),
            'unbooked_seats': unbooked_seats,
            'booked_seats': booked_seats,
            'all_seats': all_seats
        }
        worker = self.get_user_from_session(request)
        username = worker.username
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/booker.html', {
                'routes': serialized_routes,'levels': levels,
                'remaining_seats': len(unbooked_seats),
                'unbooked_seats': unbooked_seats,
                'booked_seats': booked_seats,
                'username': username,
                'all_seats': all_seats
            })
        return Response(response_data, status=status.HTTP_200_OK)

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/rooote.html', {
                'routes': routes,'levels': levels, 'firstname': firstname, 'lastname': lastname, 'phone': phone, 'email': email, 'price': price, 'plate_no': plate_no, 'side_no': side_no, 'depcity': depcity, 'descity': descity, 'date': date,

                    'buschanges_count': buschanges_count
                })
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            error_message = "There is no Travel for this information!"
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/tickets.html', {
                    'des': City.objects.all(),
                    'buschanges_count': buschanges_count,
                    'error': error_message
                })
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.db.models import Q
from .models import Bus, Sc
from .serializers import BusSerializer
class BusDeleteViews(APIView):
    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')  # Get SC ID from session
        if user_id:
            return Sc.objects.get(id=user_id)
        return None

    def get_side_parts(self, side):
        side_parts = side.split('/')
        if len(side_parts) == 1:
            return side_parts[0].strip(), None  # Single part
        elif len(side_parts) == 2:
            return side_parts[0].strip(), side_parts[1].strip()  # Two parts
        return None, None  # Invalid format

    def get(self, request):
        # Get the SC user from the session
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the side and validate it
        side = sc_user.side.strip()  # Get the side of buses
        print(side)
        first_part, second_part = self.get_side_parts(side)

        if first_part is None:  # Invalid side format
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch buses based on the side_no logic
        if first_part == '3' or second_part == '3':
            buses = Bus.objects.filter(sideno__regex=r'^\d{3}$')
        else:
            filters = Q(sideno__startswith=first_part) & Q(sideno__regex=r'^\d{4}$')
            #filters = Q(sideno__startswith=first_part)
            if second_part:
                #filters |= Q(sideno__startswith=second_part)
                filters |= Q(sideno__startswith=second_part) & Q(sideno__regex=r'^\d{4}$')
            buses = Bus.objects.filter(filters)
        serialized_routes = BusSerializer(buses, many=True).data
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/busdelet.html', {'buses': serialized_routes})
        return Response(serialized_routes, status=status.HTTP_200_OK)

    def post(self, request):
        # Get the SC user from the session
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the side and validate it
        side = sc_user.side.strip()  # Get the side of buses
        first_part, second_part = self.get_side_parts(side)

        if first_part is None:  # Invalid side format
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch buses based on the side_no logic
        if first_part == '3' or second_part == '3':
            buses = Bus.objects.filter(sideno__regex=r'^\d{3}$')
        else:
            filters = Q(sideno__startswith=first_part) & Q(sideno__regex=r'^\d{4}$')
            #filters = Q(sideno__startswith=first_part)
            if second_part:
                #filters |= Q(sideno__startswith=second_part)
                filters |= Q(sideno__startswith=second_part) & Q(sideno__regex=r'^\d{4}$')
            buses = Bus.objects.filter(filters)

        serialized_routes = BusSerializer(buses, many=True).data

        plate_no = request.data.get('plate_no')
        sideno = request.data.get('sideno')
        no_seats = request.data.get('no_seats')

        # Check if the bus exists
        bus_exists = Bus.objects.filter(plate_no=plate_no, sideno=sideno, no_seats=no_seats).exists()
        if bus_exists:
            Bus.objects.filter(plate_no=plate_no, sideno=sideno, no_seats=no_seats).delete()

        side = sc_user.side.strip()  # Get the side of buses
        first_part, second_part = self.get_side_parts(side)
        if first_part is None:  # Invalid side format
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)
        # Fetch buses based on the side_no logic
        if first_part == '3' or second_part == '3':
            buses = Bus.objects.filter(sideno__regex=r'^\d{3}$')
        else:
            filters = Q(sideno__startswith=first_part) & Q(sideno__regex=r'^\d{4}$')
            #filters = Q(sideno__startswith=first_part)
            if second_part:
                #filters |= Q(sideno__startswith=second_part)
                filters |= Q(sideno__startswith=second_part) & Q(sideno__regex=r'^\d{4}$')
            buses = Bus.objects.filter(filters)
        serialized_routes = BusSerializer(buses, many=True).data

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/busdelet.html', {
                    'buses': serialized_routes, 
                    'success': 'Bus Deleted Successfully'
                })
            return Response({'buses': serialized_routes, 'message': 'Bus Deleted Successfully'}, status=status.HTTP_200_OK)
        else:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/busdelet.html', {
                    'buses': serialized_routes, 
                    'error': 'There is no bus for deletion.'
                })
            return Response({'error': 'Bus not found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)


class MyRoute(generics.GenericAPIView):
    queryset = Route.objects.all()
    serializer_class = RoutSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')
        if user_id:
            return Sc.objects.get(id=user_id)
        return None

    def get_sc_names(self):
        sc_instances = Sc.objects.all()
        return [sc.name for sc in sc_instances]

    def get_side_parts(self, side):
        side_parts = side.split('/')
        if len(side_parts) == 1:
            return side_parts[0].strip(), None  # Single part
        elif len(side_parts) == 2:
            return side_parts[0].strip(), side_parts[1].strip()  # Two parts
        return None, None  # Invalid format

    def get(self, request, *args, **kwargs):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        side = sc_user.side.strip()
        first_part, second_part = self.get_side_parts(side)

        if first_part is None:
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)

        if first_part == '3' or second_part == '3':
            routes = Route.objects.filter(side_no__regex=r'^\d{3}$')
        else:
            filters = Q(side_no__startswith=first_part) & Q(side_no__regex=r'^\d{4}$')
            if second_part:
                filters |= Q(side_no__startswith=second_part) & Q(side_no__regex=r'^\d{4}$') 
            routes = Route.objects.filter(filters)
        serialized_routes = RoutSerializer(routes, many=True).data
        return render(request, 'users/rooteees.html', {'routes': serialized_routes})




from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.db.models import Q
from .models import Route, Sc
from .serializers import RoutSerializer

class Specific(generics.GenericAPIView):
    queryset = Route.objects.all()
    serializer_class = RoutSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')
        if user_id:
            return Sc.objects.get(id=user_id)
        return None

    def get_side_parts(self, side):
        side_parts = side.split('/')
        if len(side_parts) == 1:
            return side_parts[0].strip(), None  # Single part
        elif len(side_parts) == 2:
            return side_parts[0].strip(), side_parts[1].strip()  # Two parts
        return None, None  # Invalid format

    def get(self, request, *args, **kwargs):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        start_date = request.query_params.get('from')  # Start date
        end_date = request.query_params.get('to')      # End date

        if not start_date or not end_date:
            return Response({'error': 'Please provide start (from) and end (to) dates.'}, status=status.HTTP_400_BAD_REQUEST)

        side = sc_user.side.strip()
        first_part, second_part = self.get_side_parts(side)
        if first_part is None:
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter routes between the start and end dates
        filters = Q(date__gte=start_date, date__lte=end_date)
        if first_part == '3' or second_part == '3':
            filters &= Q(side_no__regex=r'^\d{3}$')
        else:
            filters = Q(side_no__startswith=first_part) & Q(side_no__regex=r'^\d{4}$')
            #filters = Q(sideno__startswith=first_part)
            if second_part:
                #filters |= Q(sideno__startswith=second_part)
                filters |= Q(side_no__startswith=second_part) & Q(side_no__regex=r'^\d{4}$')

        routes = Route.objects.filter(filters)
        serialized_routes = RoutSerializer(routes, many=True).data
        
        # Render the specific.html page with the routes
        return render(request, 'users/specific.html', {'routes': serialized_routes})

    def post(self, request, *args, **kwargs):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        start_date = request.data.get('from')  # Start date
        end_date = request.data.get('to')      # End date

        if not start_date or not end_date:
            return Response({'error': 'Please provide start (from) and end (to) dates.'}, status=status.HTTP_400_BAD_REQUEST)

        side = sc_user.side.strip()
        first_part, second_part = self.get_side_parts(side)
        if first_part is None:
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter routes between the start and end dates
        filters = Q(date__gte=start_date, date__lte=end_date)
        if first_part == '3' or second_part == '3':
            filters &= Q(side_no__regex=r'^\d{3}$')

        routes = Route.objects.filter(filters)
        serialized_routes = RoutSerializer(routes, many=True).data        
        # Render the specific.html page with the routes
        return render(request, 'users/specific.html', {'routes': serialized_routes})


from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from .models import Bus, Worker, Route, Sc
from .serializers import BusSerializer
class DriverUpdateViewss(generics.GenericAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')  # Get SC ID from session
        if user_id:
            return Sc.objects.get(id=user_id)
        return None

    def get_sc_names(self):
        # Helper method to get all SC names
        sc_instances = Sc.objects.all()
        return [sc.name for sc in sc_instances]

    def get_side_parts(self, side):
        side_parts = side.split('/')
        if len(side_parts) == 1:
            return side_parts[0].strip(), None  # Single part
        elif len(side_parts) == 2:
            return side_parts[0].strip(), side_parts[1].strip()  # Two parts
        else:
            return None, None  # Invalid format

    def get(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the side and validate it
        side = sc_user.side.strip()  # Get the side of buses
        first_part, second_part = self.get_side_parts(side)

        if first_part is None:  # Invalid side format
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch buses based on the side_no logic
        if first_part == '3' or second_part == '3':
            buses = Worker.objects.filter(side_no__regex=r'^\d{3}$')
        else:
            #filters = Q(sideno__startswith=first_part)
            filters = Q(side_no__startswith=first_part) & Q(side_no__regex=r'^\d{4}$')
            if second_part:
                #filters |= Q(sideno__startswith=second_part)
                filters |= Q(side_no__startswith=second_part) & Q(side_no__regex=r'^\d{4}$')
            buses = Worker.objects.filter(filters)
        #serialized_routes = BusSerializer(buses, many=True).data
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/driverupdate.html', {
                'name': sc_user.name,
                'side': side,
                'buses': buses
            })
        return Response(BusSerializer(buses, many=True).data)  # Return JSON response

    def post(self, request):
        # Get the SC user from the session
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the side and validate it
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the side and validate it
        side = sc_user.side.strip()  # Get the side of buses
        first_part, second_part = self.get_side_parts(side)

        if first_part is None:  # Invalid side format
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)
        # Fetch buses based on the side_no logic
        if first_part == '3' or second_part == '3':
            buses = Worker.objects.filter(side_no__regex=r'^\d{3}$')
        else:
            #filters = Q(sideno__startswith=first_part)
            filters = Q(side_no__startswith=first_part) & Q(side_no__regex=r'^\d{4}$')
            if second_part:
                #filters |= Q(sideno__startswith=second_part)
                filters |= Q(side_no__startswith=second_part) & Q(side_no__regex=r'^\d{4}$')
            buses = Worker.objects.filter(filters)
        #serialized_routes = BusSerializer(buses, many=True).data

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/driverupdate.html', {
                'name': sc_user.name,
                'side': side,
                'buses': buses
            })
        return Response(BusSerializer(buses, many=True).data)  # Return JSON response

    def post(self, request):
        # Get the SC user from the session
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the side and validate it
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

         # Get the side and validate it
        side = sc_user.side.strip()  # Get the side of buses
        first_part, second_part = self.get_side_parts(side)

        if first_part is None:  # Invalid side format
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)
        # Fetch buses based on the side_no logic
        if first_part == '3' or second_part == '3':
            buses = Worker.objects.filter(side_no__regex=r'^\d{3}$')
        else:
            filters = Q(side_no__startswith=first_part) & Q(side_no__regex=r'^\d{4}$')
            #filters = Q(sideno__startswith=first_part)
            if second_part:
                #filters |= Q(sideno__startswith=second_part)
                filters |= Q(side_no__startswith=second_part) & Q(side_no__regex=r'^\d{4}$')
            buses = Worker.objects.filter(filters)
        #serialized_routes = BusSerializer(buses, many=True).data

        plate_no = request.data.get('plate_no')
        side_no = request.data.get('side_no')
        username = request.data.get('username')
        new_username = request.data.get('new_username')
        new_phone = request.POST.get('new_phone')
        # Check if the bus exists
        bus_exists = Worker.objects.filter(plate_no=plate_no).first()
        if bus_exists:
            if Worker.objects.filter(username=new_username).exists():
                return render(request, 'users/driverupdate.html', {
                    'buses': buses,
                    'error': 'This username already exists.',
                })
            if Worker.objects.filter(phone = new_phone).exists():
                return render(request, 'users/driverupdate.html', {
                    'buses': buses,
                    'error': 'This Phone already exists.',
                })

            # Update bus attributes
            bus_exists.side_no = side_no
            bus_exists.plate_no = plate_no
            bus_exists.username = new_username
            bus_exists.phone = new_phone
            bus_exists.save()
            sc_user = self.get_user_from_session(request)
            if not sc_user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Get the side and validate it
            sc_user = self.get_user_from_session(request)
            if not sc_user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            # Fetch buses after update
            #buses = Bus.objects.filter(filters)
            sc_user = self.get_user_from_session(request)
            if not sc_user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Get the side and validate it
            sc_user = self.get_user_from_session(request)
            if not sc_user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Get the side and validate it
            side = sc_user.side.strip()  # Get the side of buses
            first_part, second_part = self.get_side_parts(side)

            if first_part is None:  # Invalid side format
                return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)
            # Fetch buses based on the side_no logic
            if first_part == '3' or second_part == '3':
                buses = Worker.objects.filter(side_no__regex=r'^\d{3}$')
            else:
                filters = Q(side_no__startswith=first_part) & Q(side_no__regex=r'^\d{4}$')
                #filters = Q(sideno__startswith=first_part)
            if second_part:
                #filters |= Q(sideno__startswith=second_part)
                filters |= Q(side_no__startswith=second_part) & Q(side_no__regex=r'^\d{4}$')
                buses = Worker.objects.filter(filters)
        #serialized_routes = BusSerializer(buses, many=True).data
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/driverupdate.html', {
                    'buses': buses,
                    'success': 'Driver updated successfully.'
                })
        else:
            # Refetch the buses even if the bus does not exist
            buses = Bus.objects.filter(filters)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/driverupdate.html', {
                    'buses': buses,
                    'error_message': 'Bus not found.'
                })
        return Response({'message': 'Request processed successfully'}, status=status.HTTP_200_OK)




"""
class BusUpdateViewss(generics.GenericAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')  # Get SC ID from session
        return Sc.objects.get(id=user_id) if user_id else None

    def get_side_parts(self, side):
        side_parts = side.split('/')
        if len(side_parts) == 1:
            return side_parts[0].strip(), None  # Single part
        elif len(side_parts) == 2:
            return side_parts[0].strip(), side_parts[1].strip()  # Two parts
        return None, None  # Invalid format

    def get_buses(self, side):
        first_part, second_part = self.get_side_parts(side)
        if first_part is None:
            return None, {'error': 'Invalid side format'}

        if first_part == '3' or second_part == '3':
            return Bus.objects.filter(sideno__regex=r'^\d{3}$'), None

        filters = Q(sideno__startswith=first_part) & Q(sideno__regex=r'^\d{4}$')
        if second_part:
            filters |= Q(sideno__startswith=second_part) & Q(sideno__regex=r'^\d{4}$')

        return Bus.objects.filter(filters), None

    def get(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        side = sc_user.side.strip()
        buses, error = self.get_buses(side)
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        serialized_routes = BusSerializer(buses, many=True).data

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/busupdate.html', {
                'name': sc_user.name,
                'side': side,
                'buses': serialized_routes
            })
        return Response(serialized_routes)

    def post(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        side = sc_user.side.strip()
        print(side)
        buses, error = self.get_buses(side)
        
        plate_no = request.data.get('plate_no')
        new_sideno = request.data.get('new_sideno')
        no_seats = request.data.get('no_seats')
        
        print("Incoming request data:", request.data)
        bus_exists = Bus.objects.filter(plate_no=plate_no).first()

        if len(side) == 4:
            if side[:2] != new_sideno[:2] or side[3:] != new_sideno[:2]:
                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                    buses, _ = self.get_buses(side)
                    return render(request, 'users/busupdate.html', {
                    'buses': BusSerializer(buses, many=True).data,
                    'error': 'This side Number is not required format.'
                })
            return Response({'error': 'This side number incorrect format.'}, status=status.HTTP_400_BAD_REQUEST)

        if Bus.objects.filter(sideno=new_sideno).exists():
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                buses, _ = self.get_buses(side)
                return render(request, 'users/busupdate.html', {
                'buses': BusSerializer(buses, many=True).data,
                'error': 'This side number already exists.'
            })
        bus_exists.sideno = new_sideno
        bus_exists.no_seats = no_seats
        bus_exists.save()
        Route.objects.filter(plate_no=plate_no).update(side_no=new_sideno)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            buses, _ = self.get_buses(side)
            return render(request, 'users/busupdate.html', {
                'buses': BusSerializer(buses, many=True).data,
                'success': 'Bus updated successfully.'
            })
        return Response({'message': 'Bus updated successfully'}, status=status.HTTP_200_OK)
""" 


from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .models import Bus, Sc, Route
from .serializers import BusSerializer

class BusUpdateViewss(generics.GenericAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')  # Get SC ID from session
        return Sc.objects.get(id=user_id) if user_id else None

    def get_side_parts(self, side):
        side_parts = side.split('/')
        if len(side_parts) == 1:
            return side_parts[0].strip(), None  # Single part
        elif len(side_parts) == 2:
            return side_parts[0].strip(), side_parts[1].strip()  # Two parts
        return None, None  # Invalid format

    def get_buses(self, side):
        first_part, second_part = self.get_side_parts(side)
        if first_part is None:
            return None, {'error': 'Invalid side format'}

        if first_part == '3' or second_part == '3':
            return Bus.objects.filter(sideno__regex=r'^\d{3}$'), None

        filters = Q(sideno__startswith=first_part) & Q(sideno__regex=r'^\d{4}$')
        if second_part:
            filters |= Q(sideno__startswith=second_part) & Q(sideno__regex=r'^\d{4}$')

        return Bus.objects.filter(filters), None

    def get(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        side = sc_user.side.strip()
        buses, error = self.get_buses(side)
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        serialized_routes = BusSerializer(buses, many=True).data

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/busupdate.html', {
                'name': sc_user.name,
                'side': side,
                'buses': serialized_routes
            })
        return Response(serialized_routes)

    def post(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        side = sc_user.side.strip()
        print(side)
        buses, error = self.get_buses(side)

        plate_no = request.data.get('plate_no')
        new_sideno = request.data.get('new_sideno')
        no_seats = request.data.get('no_seats')
        print(new_sideno)
        print("Incoming request data:", request.data)
        bus_exists = Bus.objects.filter(plate_no=plate_no).first()

        # Validate if 'side' is a 4-digit number
        if len(new_sideno) == 4:
            first_part, second_part = self.get_side_parts(side)
            if Bus.objects.filter(sideno=new_sideno).exists() or (first_part[:2] != new_sideno[:2]) or (second_part and second_part[:2] != new_sideno[:2]):
                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                    buses, _ = self.get_buses(side)
                    return render(request, 'users/busupdate.html', {
                    'buses': BusSerializer(buses, many=True).data,
                    'error': 'Incorrect side number.'
                })
                return Response({'error': 'This side number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if Bus.objects.filter(sideno=new_sideno).exists():
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                buses, _ = self.get_buses(side)
                return render(request, 'users/busupdate.html', {
                    'buses': BusSerializer(buses, many=True).data,
                    'error': 'This side number already exists.'
                })
            return Response({'error': 'This side number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        bus_exists.sideno = new_sideno
        bus_exists.no_seats = no_seats
        bus_exists.save()

        Route.objects.filter(plate_no=plate_no).update(side_no=new_sideno)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            buses, _ = self.get_buses(side)
            return render(request, 'users/busupdate.html', {
                'buses': BusSerializer(buses, many=True).data,
                'success': 'Bus updated successfully.'
            })
        return Response({'message': 'Bus updated successfully'}, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Worker, Bus, Sc
from .serializers import WorkerSerializer
from rest_framework import status
class Workers(APIView):

    def get(self, request, *args, **kwargs):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            des = City.objects.all()
            return render(request, 'users/worker.html', {'des': des})  # Pass user name to the template


    def post(self, request, *args, **kwargs):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']
            fname = serializer.validated_data['fname']
            city = serializer.validated_data['city']
            lname = serializer.validated_data['lname']
            gender = serializer.validated_data['gender']
            

            if Worker.objects.filter(username=username).exists():
                return Response({'error': 'User name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            if Worker.objects.filter(phone=phone).exists():
                return Response({'error': 'Phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({'success': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.db.models import Q  # Make sure to import Q if you are using it
from .models import Worker, Sc  # Ensure Sc is imported
class WorkerDeleteViews(APIView):
    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')  # Get SC ID from session
        if user_id:
            return Sc.objects.get(id=user_id)
        return None

    def get_side_parts(self, side):
        side_parts = side.split('/')
        if len(side_parts) == 1:
            return side_parts[0].strip(), None  # Single part
        elif len(side_parts) == 2:
            return side_parts[0].strip(), side_parts[1].strip()  # Two parts
        else:
            return None, None  # Invalid format

    def get(self, request, *args, **kwargs):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        side = sc_user.side.strip()
        first_part, second_part = self.get_side_parts(side)
        if first_part is None:  # Invalid side format
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)

        if first_part == '3' or second_part == '3':
            driver = Worker.objects.filter(side_no__regex=r'^\d{3}$')
        else:
            filters = Q(side_no__startswith=first_part) & Q(side_no__regex=r'^\d{4}$')
            if second_part:
                filters |= Q(side_no__startswith=second_part) & Q(side_no__regex=r'^\d{4}$')
            driver = Worker.objects.filter(filters)

        # Pass the driver queryset directly to the template
        return render(request, 'users/driverdelete.html', {'driver': driver})

    def post(self, request):
        # Check for the _method hidden field
        if request.data.get('_method') == 'DELETE':
            plate_no = request.data.get('plate_no')
            side_no = request.data.get('side_no')
            fname = request.data.get('fname')
            lname = request.data.get('lname')
            print(f"Received data: plate_no={plate_no}, side_no={side_no}, fname={fname}, lname={lname}")

            # Check if the worker exists first
            worker_exists = Worker.objects.filter(plate_no=plate_no, side_no=side_no, fname=fname, lname=lname).exists()
            if worker_exists:
                worker = Worker.objects.get(plate_no=plate_no, side_no=side_no, fname=fname, lname=lname)
                print(worker)  # Print the worker object to the console
                worker.delete()
                context = {
                    'driver': Worker.objects.all(),
                    'success': 'Driver Deleted Successfully'
                }
                return self._render_response(request, context, status.HTTP_200_OK)

            # If worker does not exist, return a generic response
            context = {
                'driver': Worker.objects.all(),
                'error': 'Driver not found'  # Optional error message
            }
            return self._render_response(request, context, status.HTTP_200_OK)

        # If not a DELETE request
        context = {
            'driver': Worker.objects.all(),
        }
        return self._render_response(request, context, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def _render_response(self, request, context, http_status):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/driverdelete.html', context)
        return Response(context, status=http_status)





from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Worker, Bus
from .serializers import BusesSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import render
from .models import Bus, Sc
from .serializers import BusSerializer
class MyDriver(generics.GenericAPIView):
    queryset = Worker.objects.all()
    #serializer_class = BusSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')  # Get SC ID from session
        if user_id:
            return Sc.objects.get(id=user_id)
        return None
    def get_side_parts(self, side):
        side_parts = side.split('/')
        if len(side_parts) == 1:
            return side_parts[0].strip(), None  # Single part
        elif len(side_parts) == 2:
            return side_parts[0].strip(), side_parts[1].strip()  # Two parts
        else:
            return None, None  # Invalid format

    def get(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        side = sc_user.side.strip()  # Get the side of buses
        first_part, second_part = self.get_side_parts(side)
        if first_part is None:  # Invalid side format
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)
        if first_part == '3' or second_part == '3':
            buses = Worker.objects.filter(side_no__regex=r'^\d{3}$')
        else:
            filters = Q(side_no__startswith=first_part) & Q(side_no__regex=r'^\d{4}$')
            if second_part:
                filters |= Q(side_no__startswith=second_part) & Q(side_no__regex=r'^\d{4}$')
            buses = Worker.objects.filter(filters)        

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/mydriver.html', {
                'name': sc_user.name,
                'level': sc_user.level,
                'side': side,
                'buses': buses
            })
        return Response(BusSerializer(buses, many=True).data)  # Return JSON response




from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Worker, Bus
from .serializers import BusesSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import render
from .models import Bus, Sc
from .serializers import BusSerializer
class MyBus(generics.GenericAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')  # Get SC ID from session
        if user_id:
            return Sc.objects.get(id=user_id)
        return None

    def get_side_parts(self, side):
        side_parts = side.split('/')
        if len(side_parts) == 1:
            return side_parts[0].strip(), None  # Single part
        elif len(side_parts) == 2:
            return side_parts[0].strip(), side_parts[1].strip()  # Two parts
        else:
            return None, None  # Invalid format

    def get(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the side and validate it
        side = sc_user.side.strip()  # Get the side of buses
        first_part, second_part = self.get_side_parts(side)
        if first_part is None:  # Invalid side format
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch routes based on the side_no logic
        if first_part == '3' or second_part == '3':
            buses = Bus.objects.filter(sideno__regex=r'^\d{3}$')
        else:
            #filters = Q(sideno__startswith=first_part)
            filters = Q(sideno__startswith=first_part) & Q(sideno__regex=r'^\d{4}$')
            if second_part:
                #filters |= Q(sideno__startswith=second_part)
                filters |= Q(sideno__startswith=second_part) & Q(sideno__regex=r'^\d{4}$')
            buses = Bus.objects.filter(filters)
        serialized_routes = BusSerializer(buses, many=True).data

        # Check if the request is for HTML
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/mybus.html', {
                'name': sc_user.name,
                'side': side,
                'buses': serialized_routes
            })
        return Response(BusSerializer(buses, many=True).data)  # Return JSON response



from rest_framework.views import APIView
from django.shortcuts import render
from .models import Ticket, Route, Sc
from django.db.models import Q
from rest_framework.response import Response
class ShowTicketsViewss(APIView):
    def get(self, request):
        # Render the ticket page for GET requests
        return render(request, 'users/ourticketoche.html')

    def post(self, request):
        # Check if the request is expecting HTML
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            # Extract data from the POST request
            plate_no = request.POST.get('plate_no')
            side_no = request.POST.get('side_no')
            date = request.POST.get('date')
            depcity = request.POST.get('depcity')
            descity = request.POST.get('descity')
            # Filter tickets based on the provided data
            tickets = Ticket.objects.filter(
                plate_no=plate_no,
                side_no=side_no,
                date=date,
                depcity=depcity,
                descity=descity
            )
            # Render the appropriate response based on ticket existence
            if tickets.exists():
                return render(request, 'users/ourticketoche.html', {'route': tickets})
            else:
                return self.handle_no_tickets(request)
        else:
            # Handle JSON response
            return self.handle_json_request(request)

    def handle_no_tickets(self, request):
        sc_id = request.session.get('sc_id')
        if sc_id:
            try:
                sc_user = Sc.objects.get(id=sc_id)
                side_parts = sc_user.side.split('/')

                # Handle both single part and two parts
                if len(side_parts) == 1:
                    first_part = side_parts[0].strip()  # Single part
                    second_part = None  # No second part
                elif len(side_parts) == 2:
                    first_part = side_parts[0].strip()  # Part before '/'
                    second_part = side_parts[1].strip()  # Part after '/'
                else:
                    return self.handle_login_error(request, 'Invalid side format')

                # Check if the side value is '3'
                if first_part == '3' or second_part == '3':
                    # Fetch routes where side_no is exactly 3 digits
                    routes = Route.objects.filter(side_no__regex=r'^\d{3}$')
                else:
                    # Fetch routes that start with either part of the `side`
                    filters = Q(side_no__startswith=first_part)
                    if second_part:
                        filters |= Q(side_no__startswith=second_part)
                    routes = Route.objects.filter(filters)

                serialized_routes = self.serialize_routes(routes)
                return render(request, 'users/rooteees.html', {
                    'error': 'There are no booked tickets for this route',
                    'routes': serialized_routes,
                    'name': sc_user.name,
                    'side': sc_user.side
                })
            except Sc.DoesNotExist:
                return self.handle_login_error(request, 'SC user not found')
        return self.handle_login_error(request, 'User not found')
    def handle_json_request(self, request):
        plate_no = request.data.get('plate_no')
        side_no = request.data.get('side_no')
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')

        # Filter tickets based on the provided data
        tickets = Ticket.objects.filter(
            plate_no=plate_no,
            side_no=side_no,
            date=date,
            depcity=depcity,
            descity=descity
        )

        # Check if tickets exist and respond accordingly
        if tickets.exists():
            ticket_data = list(tickets.values())
            return Response(ticket_data, status=200)
        else:
            return self.handle_no_tickets_json(request)

    def handle_no_tickets_json(self, request):
        sc_id = request.session.get('sc_id')
        if sc_id:
            try:
                sc_user = Sc.objects.get(id=sc_id)
                side_parts = sc_user.side.split('/')
                if len(side_parts) != 2:
                    return Response({"error": "Invalid side format"}, status=400)

                first_part = side_parts[0]
                second_part = side_parts[1]

                # Fetch routes based on side logic
                if first_part == '3' or second_part == '3':
                    routes = Route.objects.filter(side_no__regex=r'^\d{3}$')
                else:
                    filters = Q(side_no__startswith=first_part)
                    if second_part:
                        filters |= Q(side_no__startswith=second_part)
                    routes = Route.objects.filter(filters)

                combined_routes = self.serialize_routes(routes)

                return Response({
                    "error": "There are no booked tickets for this route",
                    "routes": combined_routes
                }, status=404)
            except Sc.DoesNotExist:
                return Response({"error": "SC user not found"}, status=404)

    def serialize_routes(self, routes):
        return [
            {
                'id': route.id,
                'depcity': route.depcity,
                'date': route.date,
                'plate_no': route.plate_no,
                'side_no': route.side_no,
                'descity': route.descity
            } for route in routes
        ]

    def handle_login_error(self, request, error_message):
        # Handle error rendering and response
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/login.html', {
                'error': error_message,
            })
        return Response({'error': error_message}, status=404)



from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import render
from .models import Bus, Sc
from .serializers import BusSerializer
class BusInsertView(generics.GenericAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    def get(self, request, *args, **kwargs):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return self.handle_error(request, 'User not found.')

        name = sc_user.name
        side = sc_user.side

        # Get all names for the dropdown or any other purpose
        sc_instances = Sc.objects.all()
        names = [sc.name for sc in sc_instances]

        return render(request, 'users/Businsert.html', {
            'name': name,
            'side': side,
            'names': names
        })

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Existing checks
            plate_no = serializer.validated_data['plate_no']
            sideno = serializer.validated_data['sideno']

            if Bus.objects.filter(plate_no=plate_no).exists():
                return self.handle_error(request, 'Plate number already exists.')
            if Bus.objects.filter(sideno=sideno).exists():
                return self.handle_error(request, 'Side number already exists.')

            serializer.save()
            return self.handle_success(request, 'Bus registered successfully.')

        # Return errors if serializer is not valid
        return self.handle_error(request, serializer.errors)

    def handle_success(self, request, message):
        sc_user = self.get_user_from_session(request)

        if not sc_user:
            return self.handle_error(request, 'User not found.')

        name = sc_user.name
        side = sc_user.side
        sc_instances = Sc.objects.all()
        names = [sc.name for sc in sc_instances]

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/Businsert.html', {
                'success': message,
                'name': name,
                'side': side,
                'names': names
            })
        return Response({'success': message}, status=status.HTTP_201_CREATED)

    def handle_error(self, request, error):
        sc_user = self.get_user_from_session(request)

        if not sc_user:
            return self.handle_error(request, 'User not found.')

        name = sc_user.name
        side = sc_user.side
        sc_instances = Sc.objects.all()
        names = [sc.name for sc in sc_instances]

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            error_message = error if isinstance(error, str) else ', '.join(error.values())
            return render(request, 'users/Businsert.html', {
                'errors': error_message,
                'name': name,
                'side': side,
                'names': names
            })
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')  # Assuming the user ID is stored in the session
        if user_id:
            return Sc.objects.get(id=user_id)
        return None



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from users.models import CustomUser
from django.shortcuts import render
from django.contrib.auth import authenticate
class ForgotPasswordView(APIView):
    def get(self, request):
        return render(request, 'users/forgot_password.html')

    def post(self, request):
        # Get the username or email from the request body
        username_or_email = request.data.get('username_or_email')
        role = request.data.get('role')

        user = None
        #sc = None
        
        if role == 'user':
            # Find the user by username or email
            user = CustomUser.objects.filter(username=username_or_email).first() or \
               CustomUser.objects.filter(email=username_or_email).first()

        if user:
            # Generate a new random password
            new_password = get_random_string(length=12)
            user.set_password(new_password)  # Set the new password
            user.save()  # Save the changes

            # Authenticate with the new password to ensure it works
            authenticated_user = authenticate(username=user.username, password=new_password)

            if authenticated_user is not None:
                send_mail(
                    'Password Reset',
                    f'Your new password is: {new_password}',  # Send the new password
                    'teklemariammossie1@gmail.com',  # Replace with your sender email
                    [user.email],
                    fail_silently=False,
                )
                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                    # If the request accepts HTML, render the response
                    return render(request, 'users/forgot_password.html', {
                        'message': "Password reset successfully. Check your email for the new password."
                    })
                return Response({"message": "Password reset successfully. Check your email for the new password."},
                                status=status.HTTP_200_OK)
            else:
                error_message = "Password set but could not authenticate the user."
        elif role == 'sc':
            user = Sc.objects.filter(username=username_or_email).first() or \
               CustomUser.objects.filter(email=username_or_email).first()
    
        if user:
            # Generate a new random password
            new_password = get_random_string(length=12)
            user.set_password(new_password)  # Set the new password
            user.save()  # Save the changes
            # Authenticate with the new password to ensure it works
            #authenticated_user = authenticate(username=user.username, password=new_password)
            #if authenticated_user is not None:
            send_mail(
            'Password Reset',
            f'Your new password is: {new_password}',  # Send the new password
            'teklemariammossie1@gmail.com',  # Replace with your sender email
            [user.email],
            fail_silently=False,)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                # If the request accepts HTML, render the response
                return render(request, 'users/forgot_password.html', {
                'message': "Password reset successfully. Check your email for the new password."
                })
                return Response({"message": "Password reset successfully. Check your email for the new password."},
                                status=status.HTTP_200_OK)

            else:
                error_message = "Password set but could not authenticate the user."
        else:
            error_message = "User not found."
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            # If the request accepts HTML, render the response with the error message
            return render(request, 'users/forgot_password.html', {
                'error': error_message
            })
        return Response({"error": error_message}, status=status.HTTP_404_NOT_FOUND)


from django.http import JsonResponse
from django.views import View
from .models import Buschange, City  # Ensure you import your models
class HomePageAPI(View):
    def get(self, request):
        try:
            # Get all bus changes as dict
            buschanges = Buschange.objects.all().values()
            buschanges_count = buschanges.count()  # Count of bus changes
            # Get all cities as dict
            cities = City.objects.all().values()
            response_data = {
                'buschanges_count': buschanges_count,
                'buschanges': list(buschanges),
                'cities': list(cities),
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    def post(self, request):
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)  # Handle POST
    def put(self, request):
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)  # Handle PUT
    def delete(self, request):
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)  # Handle DELETE
def root(request):
    return render(request, 'users/checkroot.html')
def selectbus(request):
    return render(request, 'users/route.html')

from django.shortcuts import render
from django.views import View
class MainPageView(View):  # Your view class
    def get(self, request):
        print("MainPageView called")  # Debugging line
        return render(request, 'users/index.html')  # Ensure this path is correct

from django.http import JsonResponse
from django.views import View
from .models import Buschange, City
class BusChangeView(View):  # Changed class name from RootView to BusChangeView
    def get(self, request):
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        cities = City.objects.all()
        
        response_data = {
            'buschanges_count': buschanges_count,
            'cities': [city.depcity for city in cities]
        }
        return JsonResponse(response_data)
class RootView(View):
    def get(self, request):
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        cities = City.objects.all()
        response_data = {
            'buschanges_count': buschanges_count,
            'cities': [city.depcity for city in cities] 
        }
        return JsonResponse(response_data)

from rest_framework.views import APIView
from rest_framework.response import Response
class YourApiView(APIView):
    def get(self, request):
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        cities = City.objects.all()
        data = {
            'buschanges_count': buschanges_count,
            'cities': [city.depcity for city in cities]
            }
        return Response(data)

from django.http import JsonResponse
from django.views import View
from .models import Buschange, City
class ApiView(View):
    def get(self, request):
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        cities = City.objects.all()
        response_data = {
            'buschanges_count': buschanges_count if buschanges_count > 0 else None,
            'cities': [city.depcity for city in cities]
        }
        return JsonResponse(response_data)

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, Feedback, Route
class LogoutView(APIView):
    def post(self, request):
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
class UsersView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        user_data = [{'username': user.username, 'email': user.email} for user in users]
        return Response({'users': user_data}, status=status.HTTP_200_OK)


class RoutesView(APIView):
    def get(self, request):
        routes = Route.objects.all()
        route_data = [{'id': route.id, 'depcity': route.depcity, 'descity': route.descity} for route in routes]
        return Response({'routes': route_data}, status=status.HTTP_200_OK)

class SelectBusView(APIView):
    def get(self, request):
        return Response({'message': 'Select a bus for your route.'}, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ticket  # Assuming you have a Ticket model
from .serializers import TicketSerializer, BusSerializer, FeedbackSerializer
@api_view(['POST'])
def book_ticket(request):
    if request.method == 'POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_tickets(request):
    if request.method == 'GET':
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


# views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Ticket, City, Bus
from .serializers import TicketSerializer
import threading
from django.core.mail import send_mail
from django.conf import settings
class TicketBookingView(APIView):
    def post(self, request):
        des = City.objects.all()
        bus = Bus.objects.all()
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            firstname = data['firstname']
            lastname = data['lastname']
            phone = data['phone']
            depcity = data['depcity']
            descity = data['descity']
            date = data['date']
            no_seat = data['no_seat']
            price = data['price']
            side_no = data['side_no']
            plate_no = data['plate_no']
            if no_seat == "FULL":
                return Response({'error': 'Cannot book ticket: the bus is already full.'}, status=status.HTTP_400_BAD_REQUEST)
            existing_ticket = Ticket.objects.filter(
                firstname=firstname,
                lastname=lastname,
                depcity=depcity,
                descity=descity,
                date=date,
                plate_no=plate_no,
                side_no=side_no
            ).exists()
            if existing_ticket:
                return Response({'error': 'This person has already booked a ticket for this route.'}, status=status.HTTP_400_BAD_REQUEST)
            ticket_instance = Ticket(**data)
            ticket_instance.save()
            
            subject = 'Ticket Booking Confirmation'
            message = f'''
            Booking Confirmation:
            First Name: {firstname}
            Last Name: {lastname}
            Phone: {phone}
            Email: {email}
            Departure City: {depcity}
            Destination City: {descity}
            Date: {date}
            Number of Seats: {no_seat}
            Price: {price}
            Side Number: {side_no}
            Plate Number: {plate_no}
            QR Code: {ticket_instance.qr_code}
            '''
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            return Response({'success': 'Ticket booked successfully! A confirmation email has been sent.', 'qr_code': ticket_instance.qr_code}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Ticket, City
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
class TicketBookingViews(APIView):
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/ticket.html', {'des': des})
        return Response({'cities': [city.depcity for city in des]})

    def post(self, request):
        firstnames = request.data.getlist('firstname[]')
        emails = request.data.getlist('email[]')
        genders = request.data.getlist('gender[]')
        lastnames = request.data.getlist('lastname[]')
        phones = request.data.getlist('phone[]')
        prices = request.data.getlist('price[]')
        side_nos = request.data.getlist('side_no[]')
        plate_nos = request.data.getlist('plate_no[]')
        usernames = request.data.getlist('username[]')
        dates = request.data.getlist('date[]')
        no_seats = request.data.getlist('no_seat[]')
        depcitys = request.data.getlist('depcity[]')
        descitys = request.data.getlist('descity[]')
        prs = request.data.getlist('pr[]')
        das = request.data.getlist('da[]')

        # Calculate total price
        total_price = sum(float(price) for price in prices)
        if prs:  # If prs is not empty
            total_price -= sum(float(p) for p in prs)

        min_length = min(
            len(firstnames), len(lastnames), len(emails), len(genders),
            len(phones), len(prices), len(side_nos), len(plate_nos),
            len(depcitys), len(descitys), len(dates), len(no_seats)
        )

        used_seats = set()
        tickets = []  # Initialize a list to hold ticket instances

        with transaction.atomic():
            for i in range(min_length):
                current_seat = no_seats[i]

                # Check if the seat is already used
                if current_seat in used_seats:
                    des = City.objects.all()
                    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                        return render(request, 'users/ticket.html', {
                            'des': des,
                            'error': f'Seat {current_seat} has already been selected.'
                        }, status=400)
                    return Response({'error': f'Seat {current_seat} has already been selected.'}, status=400)

                used_seats.add(current_seat)
                bus_info = Bus.objects.filter(sideno=side_nos[i]).first()  # Assuming side_no is unique

                if bus_info:  # If the bus exists
                    level = bus_info.level
                    name = bus_info.name
                else:  # Otherwise, set default values
                    level = "Unknown"
                    name = "Unknown"

                validated_data = {
                    'firstname': firstnames[i],
                    'lastname': lastnames[i],
                    'phone': phones[i],
                    'price': prices[i],
                    'side_no': side_nos[i],
                    'plate_no': plate_nos[i],
                    'date': dates[i],
                    'email': emails[i],
                    'gender': genders[i],
                    'depcity': depcitys[i],
                    'descity': descitys[i],
                    'username': usernames[i],
                    'no_seat': current_seat,
                }

                existing_ticket = Ticket.objects.filter(
                    firstname=validated_data['firstname'],
                    lastname=validated_data['lastname'],
                    date=validated_data['date'],
                    plate_no=validated_data['plate_no'],
                    side_no=validated_data['side_no']
                ).exists()

                if existing_ticket:
                    des = City.objects.all()
                    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                        return render(request, 'users/ticket.html', {
                            'des': des,
                            'error': 'This person has already booked a ticket for this route.'
                        })
                    return Response({'error': 'This person has already booked a ticket for this route.'}, status=400)

                ticket_instance = Ticket(**validated_data)
                ticket_instance.save()  # Save the ticket instance
                tickets.append(ticket_instance)  # Add the instance to the tickets list

                # Email Notification
                subject = 'Ticket Booking Confirmation'
                message = f'''
                Hello {validated_data['firstname']} {validated_data['lastname']},
                Thank you for booking your ticket with us! Here are your booking details:
                - Phone: {validated_data['phone']}
                - Email: {validated_data['email']}
                - Departure City: {validated_data['depcity']}
                - Destination City: {validated_data['descity']}
                - Date: {validated_data['date']}
                - Number of Seats: {validated_data['no_seat']}
                - Price: {validated_data['price']}
                - Side Number: {validated_data['side_no']}
                - Plate Number: {validated_data['plate_no']}
                - QR Code: {ticket_instance.qr_code}
                We look forward to seeing you on your journey!
                Best regards,
                The Bus Booking Team
                '''
                recipient_list = [validated_data['email']]
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

            # Optionally delete old tickets if prs is provided
            if prs:
                for i in range(min_length):
                    Ticket.objects.filter(
                        firstname=firstnames[i],
                        lastname=lastnames[i],
                        date=das[i],
                        depcity=depcitys[i],
                        descity=descitys[i]
                    ).delete()

            # Rendering based on presence of username
            if not usernames or not usernames[0]:  # No username provided
                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                    return render(request, 'users/payment.html', {
                        'success': 'Ticket(s) booked successfully! A confirmation email has been sent.',
                        'tickets': tickets,  # Pass the list of tickets
                        'total_price': total_price
                    })
            else:  # Username is present
                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                    return render(request, 'users/myticket.html', {
                        'success': 'Ticket(s) booked successfully! A confirmation email has been sent.',
                        'tickets': tickets,  # Pass the list of tickets
                        'level': level,
                        'name': name
                    })

        return Response({
            'message': 'Booking successful.',
            'tickets': [
                {
                    'id': ticket_instance.id,
                    'firstname': ticket_instance.firstname,
                    'lastname': ticket_instance.lastname,
                    'phone': ticket_instance.phone,
                    'date': ticket_instance.date,
                    'no_seat': ticket_instance.no_seat,
                    'price': ticket_instance.price,
                    'side_no': ticket_instance.side_no,
                    'plate_no': ticket_instance.plate_no,
                } for ticket_instance in tickets  # Return list of booked tickets
            ]
        }, status=201)


from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Ticket, City, Worker
class Totalballance(APIView):
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/ballance.html', {'des': des})
        return Response({'cities': [city.depcity for city in des]})

    def post(self, request):
        dates = request.data.getlist('date[]')

        # Dictionary to hold total prices by username
        totals_by_username = {}

        # Aggregate the total prices for the given dates
        for date in dates:
            tickets = Ticket.objects.filter(booked_time__date=date)

            for ticket in tickets:
                username = ticket.username if ticket.username else "Selfbook"  # Use "selfbook" if username is empty
                
                try:
                    price = float(ticket.price)  # Convert price to float
                except ValueError:
                    continue

                # Accumulate price by username
                if username in totals_by_username:
                    totals_by_username[username] += price
                else:
                    totals_by_username[username] = price

        # Fetch cities for each username
        username_city_map = {worker.username: worker.city for worker in Worker.objects.filter(username__in=totals_by_username.keys())}

        # Prepare total data with city information
        total_data = {
            username: {
                'total_balance': total,
                'city': username_city_map.get(username, 'Unknown')  # Default to 'Unknown' if city not found
            } 
            for username, total in totals_by_username.items() if total > 0
        }

        # Render response
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/totalballance.html', {
                'totals': total_data
            })
        return Response({'totals': total_data})


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City, Buschange, Ticket
class TicketAPI(APIView):
    def get(self, request):
        des = City.objects.all()
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        cities = [city.name for city in des]
        return Response({'cities': cities, 'buschanges_count': buschanges_count}, status=status.HTTP_200_OK)

    def post(self, request):
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')

        ticket = Ticket.objects.filter(
            depcity=depcity,
            descity=descity,
            date=date,
            firstname=firstname,
            lastname=lastname
        )
        if ticket.exists():
            qr_code_path = ticket.first().generate_qr_code()  # Assuming this method exists
            return Response({
                'ticket': ticket.first().id,
                'qr_code_path': qr_code_path,
                'success': "Your Ticket is:"
            }, status=status.HTTP_200_OK)
        elif depcity == descity:
            return Response({'error': "Entered Departure and Destination are the same!"}, status=status.HTTP_400_BAD_REQUEST)
        elif firstname == lastname:
            return Response({'error': "Entered Firstname and Lastname are the same!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': "No Ticket booked info for the entered details!"}, status=status.HTTP_404_NOT_FOUND)



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City, Buschange, Ticket
class GetTicketView(APIView):
    def get(self, request):
        #des = City.objects.all()
        buschanges_count = Buschange.objects.count()
        return Response({
            #'cities': [city.name for city in des],
            'buschanges_count': buschanges_count
        }, status=status.HTTP_200_OK)
    def post(self, request):
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        ticket = Ticket.objects.filter(
            depcity=depcity,
            descity=descity,
            date=date,
            firstname=firstname,
            lastname=lastname
        )
        if ticket.exists():
            qr_code_path = ticket.first().generate_qr_code()
            return Response({
                'ticket': ticket.first().id,
                'qr_code_path': qr_code_path,
                'success': "Your Ticket is retrieved."
            }, status=status.HTTP_200_OK)
        elif depcity == descity:
            return Response({'error': "Entered Departure and Destination are the same!"}, status=status.HTTP_400_BAD_REQUEST)
        elif firstname == lastname:
            return Response({'error': "Entered Firstname and Lastname are the same!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': "No Ticket booked info for the entered details!"}, status=status.HTTP_404_NOT_FOUND)


def work(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        plate_no = request.POST.get('plate_no')
        side_no = request.POST.get('side_no')
        
        worker = Worker.objects.create(
            username=username,
            plate_no=plate_no,
            side_no=side_no,
            password=password,
            phone=phone,
            fname=fname,
            lname=lname,
            gender=gender
        )
        return render(request, 'users/worker.html')
    return render(request, 'users/worker.html')


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City, Bus
from .serializers import WorkerSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from .models import City, Bus, Route
class RouteView(APIView):
    def get(self, request):
        des = City.objects.all()
        bus = Bus.objects.all()
        return Response({
            'cities': [city.name for city in des],
            'buses': [bus.plate_no for bus in bus]
        }, status=status.HTTP_200_OK)
    def post(self, request):
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        plate_no = request.data.get('plate_no')
        side_no = request.data.get('side_no')
        price = request.data.get('price')
        kilometer = request.data.get('kilometer')
        if depcity.strip() == descity.strip():
            return Response({'error': 'Departure and Destination cannot be the same!'}, status=status.HTTP_400_BAD_REQUEST)
        if Route.objects.filter(depcity=depcity, descity=descity, plate_no=plate_no, side_no=side_no, date=date).exists():
            return Response({'error': 'Route already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if Route.objects.filter(side_no=side_no, date=date, plate_no=plate_no).exists():
            return Response({'error': 'This bus is already reserved for another route for this date'}, status=status.HTTP_400_BAD_REQUEST)
        Route.objects.create(
            depcity=depcity,
            descity=descity,
            kilometer=kilometer,
            plate_no=plate_no,
            side_no=side_no,
            price=price,
            date=date
        )
        if depcity.strip() == "Addisababa":
            date = timezone.datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
            date = date.strftime('%Y-%m-%d')
            depcity, descity = descity, depcity
            Route.objects.create(
                depcity=depcity,
                descity=descity,
                kilometer=kilometer,
                plate_no=plate_no,
                side_no=side_no,
                price=price,
                date=date
            )
        return Response({'success': 'Route registered successfully!'}, status=status.HTTP_201_CREATED)

def city_view(request):
    if request.method == 'POST':
        depcity = request.POST['depcity']
        if City.objects.filter(depcity=depcity).exists():
            return render(request, 'users/city.html', {'error': 'This city already exists.'})
        city = City.objects.create(
            depcity=depcity,
        )
        city.save()
        return render(request, 'users/city.html', {'success': 'City registored Successfully!'})
    return render(request, 'users/city.html')


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City
class CityView(APIView):
    def get(self, request):
        cities = City.objects.all()
        return Response({'cities': [city.depcity for city in cities]}, status=status.HTTP_200_OK)
    def post(self, request):
        depcity = request.data.get('depcity')
        if City.objects.filter(depcity=depcity).exists():
            return Response({'error': 'This city already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        city = City.objects.create(depcity=depcity)
        return Response({'success': 'City registered successfully!'}, status=status.HTTP_201_CREATED)


from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .models import Admin, City, Bus
def admins(request):
    des = City.objects.all()  # Fetch all cities
    bus = Bus.objects.all()    # Fetch all buses
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        if Admin.objects.filter(username=username).exists():
            return render(request, 'users/admin.html', {'bus': bus, 'des': des, 'error': 'Username Already Exists.'})
        if Admin.objects.filter(email=email).exists():
            return render(request, 'users/admin.html', {'bus': bus, 'des': des, 'error': 'This Admin already Exists.'})
        if Admin.objects.filter(phone=phone).exists():
            return render(request, 'users/admin.html', {'bus': bus, 'des': des, 'error': 'Phone already Exists.'})
        admin = Admin.objects.create(
            username=username,
            fname=fname,
            lname=lname,
            password=password,
            phone=phone,
            email=email,
            gender=gender
        )
        return render(request, 'users/admin.html', {'bus': bus, 'des': des, 'success': 'Admin Created Successfully.'})
    return render(request, 'users/admin.html', {'bus': bus, 'des': des})  # Render on GET request


def ad(request):
    return render(request, 'users/ad.html')
def get_user(request):
    return render(request, 'users/checkuser.html')
def get_route(request):
    des = City.objects.all()
    if request.method == 'POST':
        date = request.POST.get('date')
        depcity = request.POST.get('depcity')
        descity = request.POST.get('descity')
        routes = Route.objects.filter(depcity=depcity, descity=descity, date=date)         
        if routes.exists():
            return render(request, 'users/checkroot.html', {'routes': routes, 'success': "Routes info---"})
        else:
            return render(request, 'users/index.html', {'des': des, 'error': "Try Again! There is no route information!"})
    return render(request, 'users/index.html', {'des': des}) 




from django.views import View
from django.shortcuts import render, redirect
class TelebirrPaymentView(View):
    def get(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/tele.html')
    def post(self, request):
        phone_number = request.POST.get('phone[]')
        price = request.POST.get('price')
        if phone_number and len(phone_number) == 10 and phone_number.startswith('09'):
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/telepassword.html', {'phone_number': phone_number, 'price': price})
        else:
            error_message = "Invalid phone number. Please check and try again."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/tele.html', {'error': error_message})


from django.views import View
from django.shortcuts import render, redirect
class Update(View):
    def get(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/tele.html')
    def post(self, request):
        phone_number = request.POST.get('phone[]')
        price = request.POST.get('price')
        if phone_number and len(phone_number) == 10 and phone_number.startswith('09'):
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/telepassword.html', {'phone_number': phone_number, 'price': price})
        else:
            error_message = "Invalid phone number. Please check and try again."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/tele.html', {'error': error_message})


import requests
from django.views import View
from django.shortcuts import render
from users.models import Service_fee

import requests
from django.views import View
from django.shortcuts import render
from users.models import Service_fee

class Telebirrpassword(View):
    def get(self, request):
        return render(request, 'users/telepassword.html')  # Render the payment input page
    def post(self, request):
        phone_number = request.POST.get('phone')  # Retrieve the user's phone number
        password = request.POST.get('password')  # Retrieve the user's password
        price = float(request.POST.get('price', 0))  # Retrieve the price and convert to float
        print(price)

        recipient_phone = "0975143134"  # Fixed recipient phone number for normal transactions
        recipient_service_fee_phone = "0949949849"  # Recipient phone number for service fee
        service_fee_instance = Service_fee.objects.first()  # Retrieve the first service fee instance
        value = service_fee_instance.service_fee if service_fee_instance else 0  # Get the service fee

        if phone_number and len(phone_number) == 10 and phone_number.startswith('09'):
            # Validate phone number and password with the payment API
            if self.is_phone_and_password_valid(phone_number, password):
                user_balance = self.get_balance(phone_number)  # Retrieve user's balance
                recipient_balance = self.get_balance(recipient_phone)  # Retrieve recipient's balance
                recipient_balance_service_fee = self.get_balance(recipient_service_fee_phone)  # Retrieve recipient's balance for service fee

                if user_balance is not None and recipient_balance is not None:
                    if user_balance >= price:
                        transaction_response = self.create_transaction(recipient_phone, price)  # Create the transaction for the normal recipient
                        if transaction_response.get('success'):
                            user_balance -= price
                            fee = price - value  
                            value = price - fee

                            new_recipient_balance_service_fee = recipient_balance_service_fee + value
                            new_recipient_balance = recipient_balance + fee

                            add_balance_response = self.add_balance(recipient_phone, new_recipient_balance)
                            add_balance_response = self.add_balance(recipient_service_fee_phone, new_recipient_balance_service_fee)
                            if add_service_fee_response.get('success') and add_balance_response.get('success'):
                                return render(request, 'users/payment_success.html', {
                                    'success': 'Successfully paid and balances updated.',
                                    'transaction_id': transaction_response.get('transaction_id'),
                                    'recipient_balance': new_recipient_balance
                                })
                            else:
                                error_message = add_service_fee_response.get('error', 'Failed to update service fee recipient balance.')
                                return render(request, 'users/telepassword.html', {
                                    'error': error_message,
                                    'phone_number': phone_number,
                                    'price': price
                                })
                        else:
                            error_message = transaction_response.get('error', 'Transaction failed. Please try again.')
                            return render(request, 'users/telepassword.html', {
                                'error': error_message,
                                'phone_number': phone_number,
                                'price': price
                            })
                    else:
                        error_message = "Insufficient balance. Please top up your account."
                        return render(request, 'users/telepassword.html', {
                            'error': error_message,
                            'phone_number': phone_number,
                            'price': price
                        })
                else:
                    error_message = "Unable to retrieve balance. Please try again later."
                    return render(request, 'users/telepassword.html', {
                        'error': error_message,
                        'phone_number': phone_number,
                        'price': price
                    })
            else:
                error_message = "Invalid password. Please check and try again."
                return render(request, 'users/telepassword.html', {
                    'error': error_message,
                    'phone_number': phone_number,
                    'price': price
                })
        else:
            error_message = "Invalid phone number format. Please check and try again."
            return render(request, 'users/telepassword.html', {
                'error': error_message,
                'phone_number': phone_number,
                'price': price
            })

    def is_phone_and_password_valid(self, phone_number, password):
        try:
            url = "https://www.ethiotelecom.et/telebirr/validate"  # Replace with the actual validation URL
            payload = {
                'phone': phone_number,
                'password': password
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get('valid', False)  # Check if the response indicates valid credentials
            else:
                print(f"API call failed with status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error validating phone number and password: {e}")
            return False

    def get_balance(self, phone_number):
        try:
            url = "https://www.ethiotelecom.et/telebirr/balance"  # Replace with the actual balance URL
            payload = {
                'phone': phone_number
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return float(data.get('balance', 0))  # Ensure balance is returned as a float
            else:
                print(f"API call for balance failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error retrieving balance: {e}")
            return None

    def create_transaction(self, recipient_phone, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/transaction"  # Replace with the actual transaction URL
            payload = {
                'phone': recipient_phone,
                'amount': amount,
                'description': 'Payment transaction'
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()  # Return the transaction response
            else:
                print(f"Transaction API call failed with status code: {response.status_code}")
                return {'success': False, 'error': 'Transaction failed due to API error.'}
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return {'success': False, 'error': 'Transaction failed due to an error.'}

    def add_balance(self, phone_number, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/add_balance"  # Replace with the actual add balance URL
            payload = {
                'phone': phone_number,
                'amount': amount
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()  # Return the response for adding balance
            else:
                print(f"Add balance API call failed with status code: {response.status_code}")
                return {'success': False, 'error': 'Failed to add balance.'}
        except Exception as e:
            print(f"Error adding balance: {e}")
            return {'success': False, 'error': 'Failed to add balance due to an error.'}



from django.views import View
from django.shortcuts import render, redirect
class CbePaymentView(View):
    def get(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cbe.html')  # Replace with the actual template file
    def post(self, request):
        account_number = request.POST.get('account')
        price = request.POST.get('price')  # Retrieve the single password
        print(price)
        if account_number and len(account_number) == 13 and account_number.startswith('1000'):
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/cbepassword.html', {'account_number': account_number, 'price': price})  # Redirect to the correct page
        else:
            error_message = "Invalid Account number. Please check and try again."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/cbe.html', {'error': error_message})



import requests
from django.views import View
from django.shortcuts import render
class Cbepassword(View):
    def get(self, request):
        return render(request, 'users/cbepassword.html')  # Render the payment input page

    def post(self, request):
        account_number = request.POST.get('account')  # Retrieve the account number
        password = request.POST.get('password')  # Retrieve the password
        price = request.POST.get('price', '0')  # Retrieve the price as a string
        recipient_account = "1000327248549"  # Fixed recipient account number
        recipient_service_fee_account = "1000136832598"  # Recipient phone number for service fee
        service_fee_instance = Service_fee.objects.first()  # Retrieve the first service fee instance
        value = service_fee_instance.service_fee if service_fee_instance else 0  # Get the service fee
        print(value)

        if account_number and len(account_number) == 13 and account_number.startswith('1000'):
            # Validate account number and password with the payment API
            if self.is_phone_and_password_valid(account_number, password):
                user_balance = self.get_balance(account_number)  # Retrieve user's balance
                recipient_balance = self.get_balance(recipient_account)  # Retrieve recipient's balance
                recipient_balance_service_fee = self.get_balance(recipient_service_fee_account)  # Retrieve recipient's balance

                if user_balance is not None and recipient_balance is not None:
                    if user_balance >= float(price):  # Convert price to float for comparison
                        transaction_response = self.create_transaction(recipient_account, price)  # Create the transaction

                        if transaction_response.get('success'):
                            user_balance -= price
                            fee = price - value
                            value = price - fee

                            new_recipient_balance_service_fee = recipient_balance_service_fee + value
                            new_recipient_balance = recipient_balance + fee

                            add_balance_response = self.add_balance(recipient_account, new_recipient_balance)
                            add_balance_response = self.add_balance(recipient_service_fee_account, new_recipient_balance_service_fee)

                            if add_balance_response.get('success'):
                                return render(request, 'users/cbe_success.html', {
                                    'success': 'Successfully paid and balance updated.',
                                    'transaction_id': transaction_response.get('transaction_id'),
                                    'recipient_balance': new_recipient_balance
                                })
                            else:
                                error_message = add_balance_response.get('error', 'Failed to update recipient balance.')
                                return render(request, 'users/cbepassword.html', {
                                    'error': error_message,
                                    'account_number': account_number,
                                    'price': price
                                })
                        else:
                            error_message = transaction_response.get('error', 'Transaction failed. Please try again.')
                            return render(request, 'users/cbepassword.html', {
                                'error': error_message,
                                'account_number': account_number,
                                'price': price
                            })
                    else:
                        error_message = "Insufficient balance. Please top up your account."
                        return render(request, 'users/cbepassword.html', {
                            'error': error_message,
                            'account_number': account_number,
                            'price': price
                        })
                else:
                    error_message = "Unable to retrieve balance. Please try again later."
                    return render(request, 'users/cbepassword.html', {
                        'error': error_message,
                        'account_number': account_number,
                        'price': price
                    })
            else:
                error_message = "Invalid password. Please check and try again."
                return render(request, 'users/cbepassword.html', {
                    'error': error_message,
                    'account_number': account_number,
                    'price': price
                })
        else:
            error_message = "Invalid account number format. Please check and try again."
            return render(request, 'users/cbepassword.html', {
                'error': error_message,
                'account_number': account_number,
                'price': price
            })

    def is_phone_and_password_valid(self, account_number, password):
        try:
            url = "https://www.ethiotelecom.et/telebirr/validate"  # Replace with the actual validation URL
            payload = {
                'account': account_number,
                'password': password
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                return data.get('valid', False)  # Check if the response indicates valid credentials
            else:
                print(f"API call failed with status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error validating account number and password: {e}")
            return False

    def get_balance(self, account_number):
        try:
            url = "https://www.ethiotelecom.et/telebirr/balance"  # Replace with the actual balance URL
            payload = {
                'account': account_number
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                return float(data.get('balance', 0))  # Ensure balance is returned as a float
            else:
                print(f"API call for balance failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error retrieving balance: {e}")
            return None

    def create_transaction(self, recipient_account, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/transaction"  # Replace with the actual transaction URL
            payload = {
                'account': recipient_account,
                'amount': amount,
                'description': 'International payment transaction'
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                return response.json()  # Return the transaction response
            else:
                print(f"Transaction API call failed with status code: {response.status_code}")
                return {'success': False, 'error': 'Transaction failed due to API error.'}
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return {'success': False, 'error': 'Transaction failed due to an error.'}

    def add_balance(self, account_number, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/add_balance"  # Replace with the actual add balance URL
            payload = {
                'account': account_number,
                'amount': amount
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()  # Return the response for adding balance
            else:
                print(f"Add balance API call failed with status code: {response.status_code}")
                return {'success': False, 'error': 'Failed to add balance.'}
        except Exception as e:
            print(f"Error adding balance: {e}")
            return {'success': False, 'error': 'Failed to add balance due to an error.'}


import requests
from django.views import View
from django.shortcuts import render
class BoaPaymentView(View):
    def get(self, request):
        return render(request, 'users/boa.html')  # Render the initial payment page
    def post(self, request):
        account_number = request.POST.get('account')  # Corrected to retrieve single account number
        price = request.POST.get('price')  # Corrected to retrieve single account number
        # Validate the account number
        if account_number and len(account_number) == 8 and account_number.startswith('48'):
            return render(request, 'users/boapassword.html', {'account_number': account_number, 'price': price})  # Correct variable name
        else:
            # Account number is invalid
            error_message = "Invalid Account number. Please check and try again."
            return render(request, 'users/boa.html', {'error': error_message})



import requests
from django.views import View
from django.shortcuts import render
class Boapassword(View):
    def get(self, request):
        return render(request, 'users/boapassword.html')  # Render the payment input page
    def post(self, request):
        account_number = request.POST.get('account')  # Retrieve the user's phone number
        password = request.POST.get('password')  # Retrieve the user's password
        #price = float(request.POST.get('price', 0))  # Retrieve the price and convert to float
        price = request.POST.get('price', '0')  # Retrieve the price as a string
        recipient_account = "48710778"  # Fixed recipient phone number
        recipient_service_fee_account = "48710779"  # Recipient phone number for service fee
        service_fee_instance = Service_fee.objects.first()  # Retrieve the first service fee instance
        value = service_fee_instance.service_fee if service_fee_instance else 0  # Get the service fee


        # Validate phone number
        if account_number and len(account_number) == 8 and account_number.startswith('48'):
            # Validate phone number and password with the payment API
            if self.is_phone_and_password_valid(account_number, password):
                user_balance = self.get_balance(account_number)  # Retrieve user's balance
                recipient_balance = self.get_balance(recipient_phone)  # Retrieve recipient's balance

                if user_balance is not None and recipient_balance is not None:
                    if user_balance >= price:
                        transaction_response = self.create_transaction(recipient_phone, price)  # Create the transaction

                        if transaction_response.get('success'):
                            user_balance -= price
                            fee = price - value
                            value = price - fee

                            new_recipient_balance_service_fee = recipient_balance_service_fee + value
                            new_recipient_balance = recipient_balance + fee

                            add_balance_response = self.add_balance(recipient_account, new_recipient_balance)
                            add_balance_response = self.add_balance(recipient_service_fee_account, new_recipient_balance_service_fee)

                            if add_balance_response.get('success'):
                                return render(request, 'users/payment_success.html', {
                                    'success': 'Successfully paid and balance updated.',
                                    'transaction_id': transaction_response.get('transaction_id'),
                                    'recipient_balance': new_recipient_balance
                                })
                            else:
                                error_message = add_balance_response.get('error', 'Failed to update recipient balance.')
                                return render(request, 'users/boapassword.html', {
                                    'error': error_message,
                                    'phone_number': phone_number,
                                    'price': price
                                })
                        else:
                            error_message = transaction_response.get('error', 'Transaction failed. Please try again.')
                            return render(request, 'users/boapassword.html', {
                                'error': error_message,
                                'account_number': account_number,
                                'price': price
                            })
                    else:
                        error_message = "Insufficient balance. Please top up your account."
                        return render(request, 'users/boapassword.html', {
                            'error': error_message,
                            'account_number': account_number,
                            'price': price
                        })
                else:
                    error_message = "Unable to retrieve balance. Please try again later."
                    return render(request, 'users/boapassword.html', {
                        'error': error_message,
                        'account_number': account_number,
                        'price': price
                    })
            else:
                error_message = "Invalid password. Please check and try again."
                return render(request, 'users/boapassword.html', {
                    'error': error_message,
                    'account_number': account_number,
                    'price': price
                })
        else:
            error_message = "Invalid phone number format. Please check and try again."
            return render(request, 'users/boapassword.html', {
                'error': error_message,
                'account_number': account_number,
                'price': price
            })

    def is_phone_and_password_valid(self, account_number, password):
        try:
            url = "https://www.ethiotelecom.et/telebirr/validate"  # Replace with the actual validation URL
            payload = {
                'account': account_number,
                'password': password
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get('valid', False)  # Check if the response indicates valid credentials
            else:
                print(f"API call failed with status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error validating phone number and password: {e}")
            return False

    def get_balance(self, account_number):
        try:
            url = "https://www.ethiotelecom.et/telebirr/balance"  # Replace with the actual balance URL
            payload = {
                'account': account_number
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return float(data.get('balance', 0))  # Ensure balance is returned as a float
            else:
                print(f"API call for balance failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error retrieving balance: {e}")
            return None

    def create_transaction(self, recipient_account, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/transaction"  # Replace with the actual transaction URL
            payload = {
                'account': recipient_account,
                'amount': amount,
                'description': 'International payment transaction'
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()  # Return the transaction response
            else:
                print(f"Transaction API call failed with status code: {response.status_code}")
                return {'success': False, 'error': 'Transaction failed due to API error.'}
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return {'success': False, 'error': 'Transaction failed due to an error.'}

    def add_balance(self, account_number, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/add_balance"  # Replace with the actual add balance URL
            payload = {
                'account': account_number,
                'amount': amount
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()  # Return the response for adding balance
            else:
                print(f"Add balance API call failed with status code: {response.status_code}")
                return {'success': False, 'error': 'Failed to add balance.'}
        except Exception as e:
            print(f"Error adding balance: {e}")
            return {'success': False, 'error': 'Failed to add balance due to an error.'}



from django.views import View
from django.shortcuts import render
class AwashPaymentView(View):
    def get(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/awash.html')  # Render the initial payment page
    def post(self, request):
        account_number = request.POST.get('account')  # Changed to use 'account'
        price = request.POST.get('price')  # Corrected to retrieve single account number
        # Validate the account number
        if account_number and len(account_number) == 13 and account_number.startswith('1000'):
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/awashpassword.html', {'account_number': account_number,'price': price})  # Correct variable name
        else:
            error_message = "Invalid Account number. Please check and try again."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/awash.html', {'error': error_message})


import requests
from django.views import View
from django.shortcuts import render
class Awashpassword(View):
    def get(self, request):
        return render(request, 'awashpassword.html')  # Render the payment input page
    def post(self, request):
        account_number = request.POST.get('account')  # Retrieve the user's phone number
        password = request.POST.get('password')  # Retrieve the user's password
        price = float(request.POST.get('price', 0))  # Retrieve the price and convert to float
        recipient_account = "1000273165634"  # Fixed recipient phone number
        recipient_service_fee_account = "1000327248549"  # Recipient phone number for service fee
        service_fee_instance = Service_fee.objects.first()  # Retrieve the first service fee instance
        value = service_fee_instance.service_fee if service_fee_instance else 0  # Get the service fee

        # Validate phone number
        if account_number and len(account_number) == 13 and account_number.startswith('1000'):
            # Validate phone number and password with the payment API
            if self.is_phone_and_password_valid(account_number, password):
                user_balance = self.get_balance(account_number)  # Retrieve user's balance
                recipient_balance = self.get_balance(recipient_account)  # Retrieve recipient's balance

                if user_balance is not None and recipient_balance is not None:
                    if user_balance >= price:
                        transaction_response = self.create_transaction(recipient_account, price)  # Create the transaction

                        if transaction_response.get('success'):
                            user_balance -= price
                            fee = price - value
                            value = price - fee

                            new_recipient_balance_service_fee = recipient_balance_service_fee + value
                            new_recipient_balance = recipient_balance + fee

                            add_balance_response = self.add_balance(recipient_account, new_recipient_balance)
                            add_balance_response = self.add_balance(recipient_service_fee_account, new_recipient_balance_service_fee)
                            
                            if add_balance_response.get('success'):
                                return render(request, 'users/awash_success.html', {
                                    'success': 'Successfully paid and balance updated.',
                                    'transaction_id': transaction_response.get('transaction_id'),
                                    'recipient_balance': new_recipient_balance
                                })
                            else:
                                error_message = add_balance_response.get('error', 'Failed to update recipient balance.')
                                return render(request, 'users/awashpassword.html', {
                                    'error': error_message,
                                    'account_number': account_number,
                                    'price': price
                                })
                        else:
                            error_message = transaction_response.get('error', 'Transaction failed. Please try again.')
                            return render(request, 'users/awashpassword.html', {
                                'error': error_message,
                                'account_number': account_number,
                                'price': price
                            })
                    else:
                        error_message = "Insufficient balance. Please top up your account."
                        return render(request, 'users/awashpassword.html', {
                            'error': error_message,
                            'account_number': account_number,
                            'price': price
                        })
                else:
                    error_message = "Unable to retrieve balance. Please try again later."
                    return render(request, 'users/awashpassword.html', {
                        'error': error_message,
                        'account_number': account_number,
                        'price': price
                    })
            else:
                error_message = "Invalid password. Please check and try again."
                return render(request, 'users/awashpassword.html', {
                    'error': error_message,
                    'account_number': account_number,
                    'price': price
                })
        else:
            error_message = "Invalid phone number format. Please check and try again."
            return render(request, 'users/awashpassword.html', {
                'error': error_message,
                'account_number': account_number,
                'price': price
            })

    def is_phone_and_password_valid(self, account_number, password):
        try:
            url = "https://www.ethiotelecom.et/telebirr/validate"  # Replace with the actual validation URL
            payload = {
                'account': account_number,
                'password': password
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get('valid', False)  # Check if the response indicates valid credentials
            else:
                print(f"API call failed with status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error validating phone number and password: {e}")
            return False

    def get_balance(self, account_number):
        try:
            url = "https://www.ethiotelecom.et/telebirr/balance"  # Replace with the actual balance URL
            payload = {
                'account': account_number
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return float(data.get('balance', 0))  # Ensure balance is returned as a float
            else:
                print(f"API call for balance failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error retrieving balance: {e}")
            return None

    def create_transaction(self, recipient_phone, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/transaction"  # Replace with the actual transaction URL
            payload = {
                'account': recipient_account,
                'amount': amount,
                'description': 'International payment transaction'
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()  # Return the transaction response
            else:
                print(f"Transaction API call failed with status code: {response.status_code}")
                return {'success': False, 'error': 'Transaction failed due to API error.'}
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return {'success': False, 'error': 'Transaction failed due to an error.'}

    def add_balance(self, account_number, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/add_balance"  # Replace with the actual add balance URL
            payload = {
                'account': account_number,
                'amount': amount
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()  # Return the response for adding balance
            else:
                print(f"Add balance API call failed with status code: {response.status_code}")
                return {'success': False, 'error': 'Failed to add balance.'}
        except Exception as e:
            print(f"Error adding balance: {e}")
            return {'success': False, 'error': 'Failed to add balance due to an error.'}


from django.views import View
from django.shortcuts import render, redirect
class SafariPaymentView(View):
    def get(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/safaricom.html')  # Replace with the actual template file
    def post(self, request):
        phone_number = request.POST.get('phone[]')
        price = request.POST.get('price')  # Corrected to retrieve single account number
        # Validate the phone number
        if phone_number and len(phone_number) == 10 and phone_number.startswith('07'):
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/safaripassword.html', {'phone_number': phone_number,'price': price})  # Redirect to the correct page
        else:
            error_message = "Invalid phone number. Please check and try again."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/safaricom.html', {'error': error_message})


import requests
from django.views import View
from django.shortcuts import render
class Safaricompassword(View):
    def get(self, request):
        return render(request, 'users/safaripassword.html')  # Render the payment input page
    def post(self, request):
        phone_number = request.POST.get('phone')  # Retrieve the user's phone number
        password = request.POST.get('password')  # Retrieve the user's password
        price = float(request.POST.get('price', 0))  # Retrieve the price and convert to float
        recipient_phone = "0722792799"  # Fixed recipient phone number
        recipient_service_fee_phone = "0749942013"  # Recipient phone number for service fee
        service_fee_instance = Service_fee.objects.first()  # Retrieve the first service fee instance
        value = service_fee_instance.service_fee if service_fee_instance else 0  # Get the service fee

        # Validate phone number
        if phone_number and len(phone_number) == 10 and phone_number.startswith('07'):
            # Validate phone number and password with the payment API
            if self.is_phone_and_password_valid(phone_number, password):
                user_balance = self.get_balance(phone_number)  # Retrieve user's balance
                recipient_balance = self.get_balance(recipient_phone)  # Retrieve recipient's balance

                if user_balance is not None and recipient_balance is not None:
                    if user_balance >= price:
                        transaction_response = self.create_transaction(recipient_phone, price)  # Create the transaction

                        if transaction_response.get('success'):
                            user_balance -= price
                            fee = price - value
                            value = price - fee

                            new_recipient_balance_service_fee = recipient_balance_service_fee + value
                            new_recipient_balance = recipient_balance + fee

                            add_balance_response = self.add_balance(recipient_phone, new_recipient_balance)
                            add_balance_response = self.add_balance(recipient_service_fee_phone, new_recipient_balance_service_fee)

                            if add_balance_response.get('success'):
                                return render(request, 'users/safari_success.html', {
                                    'success': 'Successfully paid and balance updated.',
                                    'transaction_id': transaction_response.get('transaction_id'),
                                    'recipient_balance': new_recipient_balance
                                })
                            else:
                                error_message = add_balance_response.get('error', 'Failed to update recipient balance.')
                                return render(request, 'users/safaripassword.html', {
                                    'error': error_message,
                                    'phone_number': phone_number,
                                    'price': price
                                })
                        else:
                            error_message = transaction_response.get('error', 'Transaction failed. Please try again.')
                            return render(request, 'users/safaripassword.html', {
                                'error': error_message,
                                'phone_number': phone_number,
                                'price': price
                            })
                    else:
                        error_message = "Insufficient balance. Please top up your account."
                        return render(request, 'users/safaripassword.html', {
                            'error': error_message,
                            'phone_number': phone_number,
                            'price': price
                        })
                else:
                    error_message = "Unable to retrieve balance. Please try again later."
                    return render(request, 'users/safaripassword.html', {
                        'error': error_message,
                        'phone_number': phone_number,
                        'price': price
                    })
            else:
                error_message = "Invalid password. Please check and try again."
                return render(request, 'users/safaripassword.html', {
                    'error': error_message,
                    'phone_number': phone_number,
                    'price': price
                })
        else:
            error_message = "Invalid phone number format. Please check and try again."
            return render(request, 'users/safaripassword.html', {
                'error': error_message,
                'phone_number': phone_number,
                'price': price
            })

    def is_phone_and_password_valid(self, phone_number, password):
        try:
            url = "https://www.ethiotelecom.et/telebirr/validate"  # Replace with the actual validation URL
            payload = {
                'phone': phone_number,
                'password': password
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get('valid', False)  # Check if the response indicates valid credentials
            else:
                print(f"API call failed with status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error validating phone number and password: {e}")
            return False

    def get_balance(self, phone_number):
        try:
            url = "https://www.ethiotelecom.et/telebirr/balance"  # Replace with the actual balance URL
            payload = {
                'phone': phone_number
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return float(data.get('balance', 0))  # Ensure balance is returned as a float
            else:
                print(f"API call for balance failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error retrieving balance: {e}")
            return None
    def create_transaction(self, recipient_phone, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/transaction"  # Replace with the actual transaction URL
            payload = {
                'phone': recipient_phone,
                'amount': amount,
                'description': 'International payment transaction'
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()  # Return the transaction response
            else:
                print(f"Transaction API call failed with status code: {response.status_code}")
                return {'success': False, 'error': 'Transaction failed due to API error.'}
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return {'success': False, 'error': 'Transaction failed due to an error.'}

    def add_balance(self, phone_number, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/add_balance"  # Replace with the actual add balance URL
            payload = {
                'phone': phone_number,
                'amount': amount
            }
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',  # Replace with actual API key if needed
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()  # Return the response for adding balance
            else:
                print(f"Add balance API call failed with status code: {response.status_code}")
                return {'success': False, 'error': 'Failed to add balance.'}
        except Exception as e:
            print(f"Error adding balance: {e}")
            return {'success': False, 'error': 'Failed to add balance due to an error.'}



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City, Route
class RouteCheckView(APIView):
    def get(self, request):
        des = City.objects.all()
        return Response({'cities': [city.depcity for city in des]}, status=status.HTTP_200_OK)
    def post(self, request):
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        routes = Route.objects.filter(depcity=depcity, descity=descity, date=date)
        if routes.exists():
            route_data = [{
                'id': route.id,
                'depcity': route.depcity,
                'descity': route.descity,
                'date': route.date,
                'price': route.price,
                'kilometer': route.kilometer,
                # Add any other fields you want to return
            } for route in routes]
            return Response({'routes': route_data, 'success': "Routes info retrieved."}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "No route information found!"}, status=status.HTTP_400_BAD_REQUEST)


def delete_ticket(request):
    des = City.objects.all()
    if request.method == 'POST':
        date = request.POST.get('date')
        depcity = request.POST.get('depcity')
        descity = request.POST.get('descity')
        routes = Route.objects.filter(depcity=depcity, descity=descity, date=date)
        if routes.exists():
            return render(request, 'users/rooteeee.html', {'routes': routes, 'success': "Routes info---"})
        if depcity == descity:
            des = City.objects.all()
            return render(request, 'users/cheeckrouteeee.html', {'error': 'You Entered Departure and Destination is The same!', 'des':des})
        else:
            des = City.objects.all()
            return render(request, 'users/cheeckrouteeee.html', {'error': 'There is no route for this route', 'des':des})
    return render(request, 'users/cheeckrouteeee.html', {'des':des})



from rest_framework.response import Response
from django.shortcuts import render
from .models import Route, City  
from .serializers import RoutSerializer, TickSerializer
class DeleteTicketViews(APIView):
    def get(self, request):
        des = City.objects.all()  
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cheeckrouteeee.html', {'des': des})  # Render the form
        else:
            return Response({'cities': [city.depcity for city in des]})  # Return a JSON response with city names
    def post(self, request):
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)
        if routes.exists():
            serialized_route = RoutSerializer(routes, many=True)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rooteeee.html', {'routes': serialized_route.data})  # Render HTML with routes
            return Response({'routes': serialized_route.data})  # Return JSON response with routes
        else:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                des = City.objects.all()  # Fetch all cities for the form
                return render(request, 'users/cheeckrouteeee.html', {'error': 'No booked tickets for this travel', 'des': des})
            return Response({'error': 'No booked tickets for this travel'}, status=404)





from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City, Route
class DeleteTicketView(APIView):
    def get(self, request):
        des = City.objects.all()
        return Response({'cities': [city.depcity for city in des]}, status=status.HTTP_200_OK)
    def post(self, request):
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        if depcity == descity:
            return Response({'error': 'Departure and Destination cannot be the same!'}, status=status.HTTP_400_BAD_REQUEST)
        routes = Route.objects.filter(depcity=depcity, descity=descity, date=date)
        if routes.exists():
            return Response({'routes': [route.id for route in routes], 'success': "Routes info retrieved."}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No route information found for this route.'}, status=status.HTTP_404_NOT_FOUND)


def delete_tickets(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        plate_no = request.POST.get('plate_no')
        side_no = request.POST.get('side_no')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        depcity = request.POST.get('depcity')
        descity = request.POST.get('descity')
        deleted_count, _ = Ticket.objects.filter(
            plate_no=plate_no,
            date=date,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            depcity=depcity,
            descity=descity
        ).delete()
        route = Ticket.objects.filter(depcity=depcity, descity=descity, plate_no=plate_no, date=date)
        if deleted_count > 0:
            return render(request, 'users/deleteticket.html', {'success': 'Ticket Deleted successfully.', 'route': route})
        else:
            return render(request, 'users/deleteticket.html', {'error': 'No ticket found to delete.', 'route': route})
    route = Ticket.objects.all()
    return render(request, 'users/deleteticket.html', {'route': route})


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import render  # Import render
from .models import Ticket, Route
from .serializers import RouteSerializer, TickSerializer, RoutSerializer
class DeleteTickets(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    def post(self, request):
        date = request.data.get('date')
        plate_no = request.data.get('plate_no')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        route = Ticket.objects.filter(plate_no=plate_no, date=date, depcity=depcity, descity=descity)
        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)
        if route.exists():
            serialized_route = TickSerializer(route, many=True)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/deleteticket.html', {'route': serialized_route.data})
            else:
                return Response({'route': serialized_route.data})
        else:
            serialized_routes = RoutSerializer(routes, many=True)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rooteeee.html', {'error': 'No booked tickets for this travel', 'routes': serialized_routes.data})
            return Response({'error': 'No booked tickets for this travel', 'routes': serialized_routes.data})
        return Response({'error': 'Invalid request method'}, status=400)


def delete_ticketss(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        plate_no = request.POST.get('plate_no')
        depcity = request.POST.get('depcity')
        descity = request.POST.get('descity')
        route = Ticket.objects.filter(plate_no=plate_no,date=date,depcity=depcity,descity=descity)
        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)
        if route.exists():
            return render(request, 'users/deleteticket.html', {'route': route})
        else:
            return render(request, 'users/rooteeee.html',{'error': 'No booked tickets for this travel', 'routes': routes})
    return render(request, 'users/rooteeee.html', {'routes': routes})


from rest_framework.response import Response
from django.shortcuts import render
from .models import Route, City  
from .serializers import RoutSerializer, TickSerializer
class TicketInfoView(APIView):
    def get(self, request):
        des = City.objects.all()  
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cheeckrouteee.html', {'des': des})  # Render the form
        else:
            return Response({'cities': [city.name for city in des]})  # Return a JSON response with city names
    def post(self, request):
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)
        if routes.exists():
            serialized_route = RoutSerializer(routes, many=True)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rootee.html', {'routes': serialized_route.data})  # Render HTML with routes
            return Response({'routes': serialized_route.data})  # Return JSON response with routes
        else:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                des = City.objects.all()  # Fetch all cities for the form
                return render(request, 'users/cheeckrouteee.html', {'error': 'No booked tickets for this travel', 'des': des})
            return Response({'error': 'No booked tickets for this travel'}, status=404)



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from .models import Ticket
class DeleteTicketsView(APIView):
    def post(self, request):
        # Extract data from request.data (for JSON or form data)
        date = request.data.get('date')
        plate_no = request.data.get('plate_no')
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        phone = request.data.get('phone')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')

        deleted_count, _ = Ticket.objects.filter(
            plate_no=plate_no,
            date=date,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            depcity=depcity,
            descity=descity
        ).delete()
        route = Ticket.objects.filter(depcity=depcity, descity=descity, plate_no=plate_no, date=date)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            #route = Ticket.objects.filter(depcity=depcity, descity=descity, plate_no=plate_no, date=date)
            return render(request, 'users/deleteticket.html', {'success': 'Ticket deleted successfully.', 'route': route})
        else:
            return Response({'error': 'No ticket found to delete.'}, status=status.HTTP_404_NOT_FOUND)



def delete_ticketss(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        plate_no = request.POST.get('plate_no')
        depcity = request.POST.get('depcity')
        descity = request.POST.get('descity')
        route = Ticket.objects.filter(plate_no=plate_no,date=date,depcity=depcity,descity=descity)
        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)
        if route.exists():
            return render(request, 'users/deleteticket.html', {'route': route})
        else:
            return render(request, 'users/rooteeee.html',{'error': 'No booked tickets for this travel', 'routes': routes})
    return render(request, 'users/rooteeee.html', {'routes': routes})



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ticket, Route
class CheckDeleteTicketView(APIView):
    def post(self, request):
        date = request.data.get('date')
        plate_no = request.data.get('plate_no')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        tickets = Ticket.objects.filter(plate_no=plate_no, date=date, depcity=depcity, descity=descity)
        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)
        if tickets.exists():
            ticket_data = [{
                'id': ticket.id,
                'firstname': ticket.firstname,
                'lastname': ticket.lastname,
                'phone': ticket.phone,
                # Add any other fields you want to return
            } for ticket in tickets]
            return Response({'tickets': ticket_data, 'success': 'Tickets found.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No booked tickets for this travel.', 'routes': [route.id for route in routes]}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .models import Ticket, Route
from .serializers import RouteSerializer, TickSerializer, RoutSerializer
class SelectBusView(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]  # Rendering options
    def post(self, request):
        date = request.data.get('date')
        plate_no = request.data.get('plate_no')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        route = Ticket.objects.filter(plate_no=plate_no, date=date, depcity=depcity, descity=descity)
        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)
        if route.exists():
            serialized_route = TickSerializer(route, many=True)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return Response({'route': serialized_route.data}, template_name='users/ticketoch.html')
            else:
                return Response({'route': serialized_route.data})  # Return JSON response for API
        else:
            serialized_routes = RoutSerializer(routes, many=True)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return Response({'error': 'No booked tickets for this travel', 'routes': serialized_routes.data}, template_name='users/rootee.html')
            return Response({'error': 'No booked tickets available for this route.', 'routes': serialized_routes.data})
        return Response({'error': 'Invalid request method'}, status=400)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import City, Route
class RouteLookupView(APIView):
    def get(self, request):
        depcity_name = request.data.get('depcity')
        descity_name = request.data.get('descity')
        date = request.data.get('date')
        try:
            depcity = get_object_or_404(City, name=depcity_name)
            descity = get_object_or_404(City, name=descity_name)
            routes = Route.objects.filter(depcity=depcity, descity=descity, date=date)
            if routes.exists():
                routes_data = [{'route_id': route.id, 'depcity': route.depcity.name, 'descity': route.descity.name, 'date': route.date} for route in routes]
                return Response({'success': 'Routes retrieved successfully.', 'routes': routes_data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No routes found for the specified criteria.'}, status=status.HTTP_404_NOT_FOUND)
        except City.DoesNotExist:
            return Response({'error': 'One or both cities do not exist.'}, status=status.HTTP_404_NOT_FOUND)


from django.http import HttpResponse
def home_view(request):
    return HttpResponse("Welcome to the API Home Page!")  # Customize this message as needed


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Ticket, City
from .serializers import TSerializer
class UpdateTicketViews(APIView):
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/tickets.html', {'des': des})
        return Response({'des': [city.depcity for city in des]}, status=status.HTTP_200_OK)

    def post(self, request):
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        #date = request.data.get('date')
        #print(da)
        phone = request.data.get('phone')
        price = request.data.get('price')
        email = request.data.get('email')
        gender = request.data.get('gender')
        plate_no = request.data.get('plate_no')
        side_no = request.data.get('side_no')
        new_date = request.data.get('new_date')
        da = request.data.get('da')

        try:
            # This line correctly parses the date in the format YYYY-MM-DD
            incoming_date = datetime.strptime(new_date, '%Y-%m-%d')
        except ValueError:
            # Handle invalid date format
            error_message = "Invalid date format. Please use YYYY-MM-DD."
            ticket = Ticket.objects.filter(firstname=firstname, lastname=lastname, depcity=depcity, descity=descity, date=da).first()
            if ticket:
                plate_no = ticket.plate_no
                level = Bus.objects.filter(plate_no=plate_no).values_list('level', flat=True).first() if plate_no else None
                qr_code_path = ticket.generate_qr_code()  # Assuming generate_qr_code is a method of Ticket
                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                    return render(request, 'users/tickets.html', {
                    'des': City.objects.all(),
                    'level': level,
                    'qr_code_path': qr_code_path,
                    'buschanges_count': buschanges_count,
                    'error': error_message, 'ticket': ticket
                })
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.now().date()  # Get today's date

        # Check if the incoming date is before today
        if incoming_date.date() < today:
            error_message = "Error: Incorrect inserted date."
            ticket = Ticket.objects.filter(firstname=firstname, lastname=lastname, depcity=depcity, descity=descity, date=da).first()
            if ticket:
                plate_no = ticket.plate_no
                level = Bus.objects.filter(plate_no=plate_no).values_list('level', flat=True).first() if plate_no else None
                qr_code_path = ticket.generate_qr_code()  # Assuming generate_qr_code is a method of Ticket
                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                    return render(request, 'users/tickets.html', {
                    'des': City.objects.all(),
                    'level': level,
                    'qr_code_path': qr_code_path,
                    'error': error_message, 'ticket': ticket
                })
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

        rout = Route.objects.filter(depcity=depcity, descity=descity, date=new_date)
        routes = []
        if rout.exists():
            for route in rout:
                buses = Bus.objects.filter(plate_no=route.plate_no)
                #levels = [bus.level for bus in buses]
                levels = buses.first().level if buses.exists() else None
                total_seats = sum(int(bus.no_seats) for bus in buses) if buses.exists() else 0
                booked_tickets = Ticket.objects.filter(
                    depcity=route.depcity,
                    descity=route.descity,
                    date=route.date,
                    plate_no=route.plate_no
                ).count()
                remaining_seats = max(0, total_seats - booked_tickets)
                if remaining_seats == 0:
                    remaining_seats = "Full"
                routes.append({
                    'route': route,'levels': levels,
                    'remaining_seats': remaining_seats
                })
            response_data = {
                'routes': routes, 'levels': levels,
            }
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rooote.html', {
                    'routes': routes,'levels': levels, 'firstname': firstname, 'lastname': lastname, 'phone': phone, 'email': email, 'price': price, 'da': da, 'plate_no': plate_no, 'side_no': side_no, 'depcity': depcity, 'descity': descity, 'gender': gender
                })
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            error_message = "can not update b / c can not reserved bus!"
            ticket = Ticket.objects.filter(firstname=firstname, lastname=lastname, depcity=depcity, descity=descity, date=da).first()
            if ticket:
                plate_no = ticket.plate_no
                level = Bus.objects.filter(plate_no=plate_no).values_list('level', flat=True).first() if plate_no else None
                qr_code_path = ticket.generate_qr_code()  # Assuming generate_qr_code is a method of Ticket
                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                    return render(request, 'users/tickets.html', {
                    'des': City.objects.all(),
                    'level': level,
                    'qr_code_path': qr_code_path,
                    'error': error_message, 'ticket': ticket
                })
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Buschange, Route, Bus, Ticket
from .serializers import RouteSerializer, BusSerializer
class SelectView(APIView):
    def get(self, request):
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/roote.html', {'buschanges_count': buschanges_count})
        return Response({'buschanges_count': buschanges_count}, status=status.HTTP_200_OK)
    def post(self, request):
        plate_no = request.data.get('plate_no')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        routes = Route.objects.filter(depcity=depcity, descity=descity, date=date, plate_no=plate_no)
        route_info = []
        bus_full = False
        buses = Bus.objects.filter(plate_no=plate_no)
        levels = buses.first().level if buses.exists() else None
        for route in routes:
            try:
                bus = Bus.objects.get(plate_no=route.plate_no)
                #buses = Bus.objects.get(plate_no=plate_no)
                #levels = buses.first().level if buses.exists() else None
                total_seats = int(bus.no_seats)
                booked_tickets = Ticket.objects.filter(
                    depcity=route.depcity,
                    descity=route.descity,
                    date=route.date,
                    plate_no=route.plate_no
                ).values_list('no_seat', flat=True)
                booked_seats = set(int(seat) for seat in booked_tickets if seat)
                booked_seat_count = len(booked_seats)
                remaining_seats = total_seats - booked_seat_count
                unbooked_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]

                if route.plate_no == plate_no and remaining_seats <= 0:
                    bus_full = True
                    route_info.append({
                        'route': route,'levels': levels,
                        'remaining_seats': remaining_seats if remaining_seats > 0 else "Full"
                    })
            except Bus.DoesNotExist:
                continue
        if bus_full:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/roote.html', {
                    'error': 'This Bus is Full!','levels': levels,
                    'buschanges_count': buschanges_count
                })
            return Response({'error': 'This Bus is Full!'}, status=status.HTTP_400_BAD_REQUEST)
        # Serialize the routes
        serialized_routes = RouteSerializer(routes, many=True).data
        all_seats = list(range(1, total_seats + 1) if 'total_seats' in locals() else [])
        response_data = {
                'routes': serialized_routes,'levels': levels,
            'remaining_seats': len(unbooked_seats),
            'unbooked_seats': unbooked_seats,
            'booked_seats': booked_seats,
            'all_seats': all_seats
        }
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/ticket.html', {
                'routes': serialized_routes,'levels': levels,
                'remaining_seats': len(unbooked_seats),
                'unbooked_seats': unbooked_seats,
                'booked_seats': booked_seats,
                'all_seats': all_seats
            })
        return Response(response_data, status=status.HTTP_200_OK)

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/rooote.html', {
                'routes': routes,'levels': levels, 'firstname': firstname, 'lastname': lastname, 'phone': phone, 'email': email, 'price': price, 'plate_no': plate_no, 'side_no': side_no, 'depcity': depcity, 'descity': descity, 'date': date,

                    'buschanges_count': buschanges_count
                })
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            error_message = "There is no Travel for this information!"
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/tickets.html', {
                    'des': City.objects.all(),
                    'buschanges_count': buschanges_count,
                    'error': error_message
                })
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Buschange, Route, Bus, Ticket
from .serializers import RouteSerializer, BusSerializer
class SelView(APIView):
    def get(self, request):
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/rooote.html', {'buschanges_count': buschanges_count})
        return Response({'buschanges_count': buschanges_count}, status=status.HTTP_200_OK)

    def post(self, request):
        plate = request.data.get('plate')
        side = request.data.get('side')
        first = request.data.get('first')
        last = request.data.get('last')
        phone = request.data.get('phone')
        email = request.data.get('email')
        dep = request.data.get('dep')
        pr = request.data.get('pr')
        da = request.data.get('da')
        des = request.data.get('des')
        gender = request.data.get('gender')

        plate_no = request.data.get('plate_no')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        
        routes = Route.objects.filter(depcity=depcity, descity=descity, date=date, plate_no=plate_no)
        route_info = []
        bus_full = False
        buses = Bus.objects.filter(plate_no=plate_no)
        levels = buses.first().level if buses.exists() else None
        
        # Initialize variables to avoid UnboundLocalError
        unbooked_seats = []
        booked_seats = set()  # Initialize booked_seats as a set
        total_seats = 0

        for route in routes:
            try:
                bus = Bus.objects.get(plate_no=route.plate_no)
                total_seats = int(bus.no_seats)
                booked_tickets = Ticket.objects.filter(
                    depcity=route.depcity,
                    descity=route.descity,
                    date=route.date,
                    plate_no=route.plate_no
                ).values_list('no_seat', flat=True)
                
                # Convert to set for faster lookups
                booked_seats = set(int(seat) for seat in booked_tickets if seat)
                booked_seat_count = len(booked_seats)
                remaining_seats = total_seats - booked_seat_count
                unbooked_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]

                if route.plate_no == plate_no and remaining_seats <= 0:
                    bus_full = True
                    route_info.append({
                        'route': route,
                        'levels': levels,
                        'remaining_seats': remaining_seats if remaining_seats > 0 else "Full"
                    })
            except Bus.DoesNotExist:
                continue
        if bus_full:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rooote.html', {
                    'error': 'This Bus is Full!',
                    'levels': levels,
                    'buschanges_count': buschanges_count
                })
            return Response({'error': 'This Bus is Full!'}, status=status.HTTP_400_BAD_REQUEST)
        serialized_routes = RouteSerializer(routes, many=True).data
        all_seats = list(range(1, total_seats + 1) if total_seats > 0 else [])
        
        response_data = {
            'routes': serialized_routes,
            'levels': levels,
            'remaining_seats': len(unbooked_seats),
            'unbooked_seats': unbooked_seats,
            'booked_seats': booked_seats,
            'all_seats': all_seats
        }

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/updateticket.html', {
                'routes': serialized_routes,
                'levels': levels,
                'remaining_seats': len(unbooked_seats),
                'unbooked_seats': unbooked_seats,
                'booked_seats': booked_seats,
                'first': first,
                'last': last,
                'pr': pr,
                'da': da,
                'email': email,
                'plate': plate,
                'side': side,
                'phone': phone,
                'gender': gender,
                'all_seats': all_seats
            })
        return Response(response_data, status=status.HTTP_200_OK)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import City, Route, Bus, Ticket, Buschange
class BookView(APIView):
    def get(self, request):
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cheeckroutee.html', {
                'des': des,
                'buschanges_count': buschanges_count
            })
        return Response({'des': [city.name for city in des], 'buschanges_count': buschanges_count}, status=status.HTTP_200_OK)

    def post(self, request):
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')

        try:
            # This line correctly parses the date in the format YYYY-MM-DD
            incoming_date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            # Handle invalid date format
            error_message = "Invalid date format. Please use YYYY-MM-DD."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/cheeckroutee.html', {
                    'des': City.objects.all(),
                    'buschanges_count': Buschange.objects.count(),
                    'error': error_message
                })
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        today = timezone.now().date()  # Get today's date
        # Check if the incoming date is before today
        if incoming_date.date() < today:
            error_message = "Error: Incorrect inserted date."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/cheeckroutee.html', {
                    'des': City.objects.all(),
                    'buschanges_count': Buschange.objects.count(),
                    'error': error_message,
                })
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        rout = Route.objects.filter(depcity=depcity, descity=descity, date=date)
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        routes = []
        error_message = "There is no Travel for this information!"
        routes = []
        remaining_seats = 0
        if rout.exists():
            for route in rout:
                buses = Bus.objects.filter(plate_no=route.plate_no)
                levels = buses.first().level if buses.exists() else None
                total_seats = sum(int(bus.no_seats) for bus in buses) if buses.exists() else 0
                booked_tickets = Ticket.objects.filter(
                    depcity=route.depcity,
                    descity=route.descity,
                    date=route.date,
                    plate_no=route.plate_no
                ).count()
                remaining_seats = total_seats - booked_tickets

                # Check if remaining seats are negative
                if remaining_seats < 0:
                    routes = []  # Clear routes if any are found, as we can't have negative remaining seats
                    break  # Exit the loop since we found an invalid state

                # Only add the route if there are remaining seats
                if remaining_seats > 0:
                    routes.append({
                        'route': route,
                        'levels': levels,
                        'remaining_seats': remaining_seats
                    })

        # Check if there are no valid routes or if remaining seats are negative 
        if remaining_seats < 0 or not routes:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/cheeckroutee.html', {
                    'des': City.objects.all(),
                    'buschanges_count': buschanges_count,
                    'error': error_message
                })
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'routes': routes,
            'levels': levels,
            'buschanges_count': buschanges_count
        }

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/roote.html', {
                'routes': routes,
                'levels': levels,
                'buschanges_count': buschanges_count
            })
        return Response(response_data, status=status.HTTP_200_OK)

def details(request):
    return render(request, 'users/details.html')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import CustomUser
class AdminDeleteViews(APIView):
    def post(self, request):
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        username = request.data.get('username')
        phone = request.data.get('phone')
        row_count = CustomUser.objects.count()
        if row_count <= 1:
            admins = CustomUser.objects.all()
            context = {
                'admins': admins,
                'error': "Cannot delete admin. At least one account must exist."
            }
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/admindelet.html', context)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        deleted_count, _ = CustomUser.objects.filter(fname=fname, lname=lname, username=username).delete()
        admins = CustomUser.objects.all()
        context = {'admins': admins}
        if deleted_count > 0:
            context['success'] = "Admin deleted successfully."
        else:
            context['error'] = "No Admin found with the provided information."
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/admindelet.html', context)
        return Response(context, status=status.HTTP_200_OK)
    def get(self, request):
        admins = CustomUser.objects.all()
        context = {'admins': admins}
        if admins.exists():
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/admindelet.html', context)
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['error'] = "There are no admins to delete."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/admindelet.html', context)
            return Response(context, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import CustomUser  # Ensure you have the right model
from .models import Worker  # Ensure the Worker model is imported as needed
class Workerdelet(APIView):
    def post(self, request):
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        username = request.data.get('username')
        phone = request.data.get('phone')

        # Attempt to delete the user
        deleted_count, _ = Worker.objects.filter(fname=fname, lname=lname, username=username).delete()

        # Prepare the context for rendering
        context = {}

        if deleted_count > 0:
            context['success'] = "Worker deleted successfully"
        else:
            context['error'] = "No matching worker found to delete."

        # Render or respond based on the request type
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/workerdelete.html', context)
        return Response(context, status=status.HTTP_200_OK)

    def get(self, request):
        admins = Worker.objects.all()
        context = {'admins': admins}

        if admins.exists():
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/workerdelete.html', context)
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['error'] = "There are no workers to delete."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/workerdelete.html', context)
            return Response(context, status=status.HTTP_404_NOT_FOUND)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Sc
class ScDeleteViews(APIView):
    def post(self, request):
        firstname = request.data.get('firstname')
        name = request.data.get('name')
        lastname = request.data.get('lastname')
        context = {}  # Initialize context
        # Delete the SC
        deleted_count, _ = Sc.objects.filter(firstname=firstname, lastname=lastname, name=name).delete()
        admins = Sc.objects.all()
        if deleted_count > 0:
            context['success'] = "SC deleted successfully."
        else:
            context['error'] = "No SC found with the provided information."
        # Render response according to the request type
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scdelet.html', {'admins': admins, **context})
        return Response(context, status=status.HTTP_200_OK)
    def get(self, request):
        admins = Sc.objects.all()
        context = {}
        if admins.exists():
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/scdelet.html', {'admins': admins})
            return Response({'admins': admins}, status=status.HTTP_200_OK)
        else:
            context['error'] = "There are no SCs."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/scdelet.html', {'admins': admins, **context})
            return Response(context, status=status.HTTP_404_NOT_FOUND)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
class AdminDeleteView(APIView):
    def post(self, request):
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        username = request.data.get('username')
        phone = request.data.get('phone')
        row_count = CustomUser.objects.count()
        if row_count <= 1:
            return Response({
                'error': "Cannot delete admin. At least one account must exist."
            }, status=status.HTTP_400_BAD_REQUEST)
        deleted_count, _ = CustomUser.objects.filter(fname=fname, lname=lname, username=username).delete()
        if deleted_count > 0:
            return Response({
                'success': "Admin deleted successfully."
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': "No admin found with the provided information."
            }, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        admins = CustomUser.objects.all()
        if admins:
            return Response({'admins': [{'fname': admin.fname, 'lname': admin.lname, 'username': admin.username} for admin in admins]}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "There are no admins to delete."}, status=status.HTTP_404_NOT_FOUND)
def delete(request):
    return render(request, 'users/admindelet.html')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Route, Ticket
class RouteDeleteViews(APIView):
    def post(self, request):
        routes = Route.objects.all()
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        plate_no = request.data.get('plate_no')
        side_no = request.data.get('side_no')
        booked_tickets = Ticket.objects.filter(
            depcity=depcity,
            descity=descity,
            date=date,
            plate_no=plate_no,
            side_no=side_no
        ).count()
        if booked_tickets > 0:
            context = {
                'routes': routes,
                'error': "This route has booked tickets!"
            }
        else:
            rows_deleted, _ = Route.objects.filter(
                depcity=depcity,
                descity=descity,
                date=date,
                plate_no=plate_no,
                side_no=side_no
            ).delete()
            context = {'routes': routes}
            if rows_deleted > 0:
                context['success'] = "Route Deleted Successfully!"
            else:
                context['error'] = "No route found for deletion."

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/routedelete.html', context)
        serializer = RouteSerializer(routes, many=True)  # Serialize the list of routes
        return Response(context, status=status.HTTP_200_OK if 'success' in context else status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        context = {'routes': routes}
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            if routes.exists():
                return render(request, 'users/routedelete.html', context)
            else:
                return render(request, 'users/error.html', {'error': "There are no routes to delete."})
        return Response(context, status=status.HTTP_200_OK)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Route, Ticket
class RouteDeleteView(APIView):
    def post(self, request):
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        plate_no = request.data.get('plate_no')
        side_no = request.data.get('side_no')
        booked_tickets = Ticket.objects.filter(
            depcity=depcity,
            descity=descity,
            date=date,
            plate_no=plate_no,
            side_no=side_no
        ).count()
        if booked_tickets > 0:
            return Response({'error': "This route has booked tickets."}, status=status.HTTP_400_BAD_REQUEST)
        rows_deleted, _ = Route.objects.filter(
            depcity=depcity,
            descity=descity,
            date=date,
            plate_no=plate_no,
            side_no=side_no
        ).delete()
        if rows_deleted > 0:
            return Response({'success': "Route deleted successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "No route found with the provided information."}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        routes = Route.objects.all()
        if routes.exists():
            route_data = [{'depcity': route.depcity, 'descity': route.descity, 'date': route.date, 'plate_no': route.plate_no, 'side_no': route.side_no} for route in routes]
            return Response({'routes': route_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "There are no routes to delete."}, status=status.HTTP_404_NOT_FOUND)


from django.http import HttpResponse
def home_view(request):
    return HttpResponse("Welcome to the API Home Page!")

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Worker
class WorkerDeleteView(APIView):
    def post(self, request):
        #plate_no = request.data.get('plate_no')
        #side_no = request.data.get('side_no')
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        try:
            worker = Worker.objects.get(fname=fname, lname=lname)
            worker.delete()
            return Response({'success': 'Driver deleted successfully.'}, status=status.HTTP_200_OK)
        except Worker.DoesNotExist:
            return Response({'error': 'No driver found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        drivers = Worker.objects.all()
        driver_data = [{'plate_no': driver.plate_no, 'side_no': driver.side_no, 'fname': driver.fname, 'lname': driver.lname} for driver in drivers]
        return Response({'drivers': driver_data}, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from django.shortcuts import render
from .models import Ticket, Route
class ShowTicketsViews(APIView):
    def get(self, request):
        # Render the ticketoche.html page when a GET request is made
        return render(request, 'users/ticketoche.html')
    def post(self, request):
        # Check if the request is expecting HTML
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            # Extract data from the POST request
            plate_no = request.POST.get('plate_no')
            side_no = request.POST.get('side_no')
            date = request.POST.get('date')
            depcity = request.POST.get('depcity')
            descity = request.POST.get('descity')

            # Filter tickets based on the provided data
            route = Ticket.objects.filter(
                plate_no=plate_no,
                side_no=side_no,
                date=date,
                depcity=depcity,
                descity=descity
            )

            routes = Route.objects.filter(side_no=side_no)
            if route.exists():
                return render(request, 'users/ticketoche.html', {'route': route})
            else:
                return render(request, 'users/rooteee.html', {
                    'error': 'There are no booked tickets for this route',
                    'routes': routes
                })
        else:
            plate_no = request.data.get('plate_no')
            side_no = request.data.get('side_no')
            date = request.data.get('date')
            depcity = request.data.get('depcity')
            descity = request.data.get('descity')
            route = Ticket.objects.filter(
                plate_no=plate_no,
                side_no=side_no,
                date=date,
                depcity=depcity,
                descity=descity
            )
            routes = Route.objects.filter(side_no=side_no)
            if route.exists():
                ticket_data = list(route.values())
                return Response(ticket_data, status=200)
            else:
                return Response({"error": "There are no booked tickets for this route"}, status=404)


class ViewRoute(APIView):
    def post(self, request):
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        tickets = Route.objects.filter(
            date=date,
            depcity=depcity,
            descity=descity
        )
        if tickets.exists():
            ticket_data = [{'id': ticket.id, 'depcity': ticket.depcity, 'descity': ticket.descity, 'date': ticket.date, 'plate_no': ticket.plate_no} for ticket in tickets]
            return Response({'tickets': ticket_data}, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'There are no booked tickets for this route.',
                'routes': [{'side_no': route.side_no, 'plate_no': route.plate_no} for route in routes]
            }, status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        return Response({'error': 'Use POST to retrieve tickets.'}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Route
class ViewRoute(APIView):
    def post(self, request):
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        tickets = Route.objects.filter(
            date=date,
            depcity=depcity,
            descity=descity
        )
        if tickets.exists():
            ticket_data = [{'id': ticket.id, 'depcity': ticket.depcity, 'descity': ticket.descity, 'date': ticket.date, 'plate_no': ticket.plate_no} for ticket in tickets]
            return Response({'tickets': ticket_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There are no booked tickets for this route.'}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        return Response({'error': 'Use POST to retrieve tickets.'}, status=status.HTTP_400_BAD_REQUEST)
class ViewRoute(View):
    def get(self, request):
        data = {'message': 'Hello from the API!'}
        return JsonResponse(data)
class Routes(APIView):
    def post(self, request):
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        tickets = Route.objects.filter(
            date=date,
            depcity=depcity,
            descity=descity
        )
        if tickets.exists():
            ticket_data = [{'id': ticket.id, 'depcity': ticket.depcity, 'descity': ticket.descity, 'date': ticket.date, 'plate_no': ticket.plate_no} for ticket in tickets]
            return Response({'tickets': ticket_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There are no booked tickets for this route.'}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        return Response({'error': 'Use POST to retrieve tickets.'}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Bus
class BusDeleteView(APIView):
    def post(self, request):
        plate_no = request.data.get('plate_no')
        side_no = request.data.get('sideno')
        no_seats = request.data.get('no_seats')
        try:
            bus = Bus.objects.get(plate_no=plate_no, sideno=side_no, no_seats=no_seats)
            bus.delete()
            return Response({'success': 'Bus deleted successfully.'}, status=status.HTTP_200_OK)
        except Bus.DoesNotExist:
            return Response({'error': 'No bus found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        buses = Bus.objects.all()
        bus_data = [{'plate_no': bus.plate_no, 'sideno': bus.sideno, 'no_seats': bus.no_seats} for bus in buses]
        return Response({'buses': bus_data}, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import City
class CityDeleteViews(APIView):
    def post(self, request):
        if request.data.get('_method') == 'DELETE':
            cities = City.objects.all()
            depcity = request.data.get('depcity')
            try:
                dep = City.objects.get(depcity=depcity)
                dep.delete()
                cities = City.objects.all()
                context = {
                'cities': cities,
                'success': 'City Deleted Successfully'
                }
            except City.DoesNotExist:
                context = {
                'cities': cities,
                'error': 'There is No city for Deletion'
                }
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/citydelet.html', context)
            return Response(context, status=status.HTTP_200_OK if 'success' in context else status.HTTP_404_NOT_FOUND)

    def get(self, request):
        cities = City.objects.all()
        context = {'cities': cities}
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/citydelet.html', context)
        return Response(context, status=status.HTTP_200_OK)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City
class CityDeleteView(APIView):
    def post(self, request):
        depcity = request.data.get('depcity')
        try:
            city = City.objects.get(depcity=depcity)
            city.delete()
            return Response({'success': 'City deleted successfully.'}, status=status.HTTP_200_OK)
        except City.DoesNotExist:
            return Response({'error': 'No city found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        cities = City.objects.all()
        city_data = [{'depcity': city.depcity} for city in cities]
        return Response({'cities': city_data}, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Feedback  # Make sure Feedback is imported
class CommentDeleteViews(APIView):
    def post(self, request):
        if request.data.get('_method') == 'DELETE':
            email = request.data.get('email')
            name = request.data.get('name')
            phone = request.data.get('phone')
            registration_id = request.data.get('registration_id')  # no leading space

            try:
                comment = Feedback.objects.get(
                    registration_id=registration_id,
                    name=name,
                    email=email,
                    phone=phone
                )
                comment.delete()
                comments = Feedback.objects.all()
                context = {
                    'comments': comments,
                    'success': 'Comment deleted successfully'
                }
            except Feedback.DoesNotExist:
                comments = Feedback.objects.all()
                context = {
                    'comments': comments,
                    'error': 'No matching feedback found for deletion'
                }

            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/commentdelet.html', context)

            return Response(
                context,
                status=status.HTTP_200_OK if 'success' in context else status.HTTP_404_NOT_FOUND
            )

    def get(self, request):
        comments = Feedback.objects.all()
        context = {'comments': comments}
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/commentdelet.html', context)
        return Response(context, status=status.HTTP_200_OK)

def commentdelete(request):
    comments = Feedback.objects.all()  # Always fetch comments at the start
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        try:
            comment = Feedback.objects.get(name=name, email=email, phone=phone)
            comment.delete()
            comments = Feedback.objects.all()
            return render(request, 'users/commentdelet.html', {
                'comments': comments,
                'success': 'Comment Deleted Successfully'
            })
        except Feedback.DoesNotExist:
            return render(request, 'users/commentdelet.html', {
                'comments': comments,
                'error': 'There is No comment for Deletion'
            })
    return render(request, 'users/commentdelet.html', {'comments': comments})


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feedback
class CommentDeleteView(APIView):
    def post(self, request):
        email = request.data.get('email')
        name = request.data.get('name')
        phone = request.data.get('phone')
        try:
            comment = Feedback.objects.get(name=name, email=email, phone=phone)
            comment.delete()
            return Response({'success': 'Comment deleted successfully.'}, status=status.HTTP_200_OK)
        except Feedback.DoesNotExist:
            return Response({'error': 'No comment found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        comments = Feedback.objects.all()
        comment_data = [{'name': comment.name, 'email': comment.email, 'phone': comment.phone} for comment in comments]
        return Response({'comments': comment_data}, status=status.HTTP_200_OK)



class UrRegisterView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/register.html')

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # No need to manually hash the password here
            serializer.save()
            return Response({'success': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)








from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus, Route, Ticket, Buschange
class ChangesBusView(APIView):
    def get(self, request):
        routes = Route.objects.all().values()  # Use values() to return a list of dicts
        buses = Bus.objects.all().values()
        
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/buschange.html', {
                'routes': list(routes),
                'buses': list(buses)
            })
        else:
            return Response({'routes': list(routes), 'buses': list(buses)}, status=status.HTTP_200_OK)

    def post(self, request):
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        side_no = request.data.get('side_no')
        new_side_no = request.data.get('new_side_no')
        routes = Route.objects.all().values()
        buses = Bus.objects.all().values()
        try:
            if Route.objects.filter(side_no=new_side_no, date=date).exists():
                return self._handle_response(request, {
                    'error': 'This bus is already reserved for the route on this date.',
                    'routes': list(routes),
                    'buses': list(buses)
                }, status.HTTP_400_BAD_REQUEST)

            bus_info = Bus.objects.filter(sideno=new_side_no).first()
            if not bus_info:
                return self._handle_response(request, {
                    'error': 'Invalid side number selected.',
                    'routes': list(routes),
                    'buses': list(buses)
                }, status.HTTP_400_BAD_REQUEST)

            new_plate_no = bus_info.plate_no
            total_seats = int(bus_info.no_seats) if bus_info.no_seats else 0

            booked_tickets_count = Ticket.objects.filter(date=date, side_no=side_no).count()
            if booked_tickets_count > total_seats:
                return self._handle_response(request, {
                    'error': 'Not enough seats available for this change.',
                    'routes': list(routes),
                    'buses': list(buses)
                }, status.HTTP_400_BAD_REQUEST)

            route = Route.objects.get(depcity=depcity, descity=descity, date=date, side_no=side_no)
            route.plate_no = new_plate_no
            route.side_no = new_side_no
            route.save()

            # Handle reciprocal route updates if necessary
            if depcity.strip() == "Addisababa":
                reciprocal_route = Route.objects.get(
                    depcity=descity,
                    descity=depcity,
                    date=(timezone.datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d'),
                    side_no=side_no
                )
                reciprocal_route.plate_no = new_plate_no
                reciprocal_route.side_no = new_side_no
                reciprocal_route.save()
            Ticket.objects.filter(date=date, side_no=side_no).update(
                plate_no=new_plate_no,
                side_no=new_side_no
            )
            booked_tickets = Ticket.objects.filter(date=date, side_no=new_side_no).values_list('no_seat', flat=True)
            booked_seats = set(int(seat) for seat in booked_tickets)
            booked_seat_count = len(booked_seats)
            remaining_seats = total_seats - booked_seat_count
            unbooked_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]
            Buschange.objects.create(
                plate_no=side_no,
                side_no=side_no,
                new_plate_no=new_plate_no,
                new_side_no=new_side_no,
                date=date,
                depcity=depcity,
                descity=descity
            )
            return self._handle_response(request, {
                'success': 'Bus changed successfully.',
                'total_seats': total_seats,
                'booked_seats': booked_seat_count,
                'remaining_seats': remaining_seats,
                'unbooked_seats': unbooked_seats,
                'booked_seat_list': list(booked_seats),
                'routes': list(routes),
                'buses': list(buses)
            }, status.HTTP_200_OK)

        except Route.DoesNotExist:
            return self._handle_response(request, {
                'error': "The specified route does not exist.",
                'routes': list(routes),
                'buses': list(buses)
            }, status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/buschange.html', context)
        else:
            return Response(context, status=status_code)



from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Sc, Service_fee
class Serviceupdate(APIView):
    def get(self, request):
        routes = Sc.objects.all().values()  # Use values() to return a list of dicts
        buses = Service_fee.objects.all().values()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/update_service_fee.html', {
                'routes': list(routes),
                'buses': list(buses)
            })
        else:
            return Response({'routes': list(routes), 'buses': list(buses)}, status=status.HTTP_200_OK)

    def post(self, request):
        service_fee = request.data.get('service_fee')
        new_service_fee = request.data.get('new_service_fee')  # Ensure the key matches your HTML form
        routes = Sc.objects.all().values()
        buses = Service_fee.objects.all().values()

        try:
            # Check if the new service fee already exists
            if Service_fee.objects.filter(service_fee=new_service_fee).exists():
                return self._handle_response(request, {
                    'error': 'This new service fee already exists.',
                    'routes': list(routes),
                    'buses': list(buses)
                }, status.HTTP_400_BAD_REQUEST)

            # Update the existing service fee
            sc_user = Service_fee.objects.get(service_fee=service_fee)
            sc_user.service_fee = new_service_fee
            sc_user.save()

            # Render response based on request type
            return self._handle_response(request, {
                'success': 'Service fee updated successfully!',
                'routes': list(routes),
                'buses': list(buses)
            })
        except Service_fee.DoesNotExist:
            return self._handle_response(request, {
                'error': 'Service fee not found!',
                'routes': list(routes),
                'buses': list(buses)
            }, status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code=status.HTTP_200_OK):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/update_service_fee.html', context)
        else:
            return Response(context, status=status_code)


from django.utils import timezone
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus, Route  # Ensure Route is imported
class Activate(APIView):
    def get(self, request):
        #routes = Route.objects.all()  # Get all routes; adjust as necessary
        buses = Bus.objects.all()      # Get all buses; adjust as necessary
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/status.html', {
                #'routes': list(routes),
                'buses': list(buses)  # Ensure buses are included
            })
        return Response({'routes': list(routes), 'buses': list(buses)}, status=status.HTTP_200_OK)

    def post(self, request):
        date = request.data.get('date')  # Capture the date string
        routes = Route.objects.filter(date=date)  # Changed to filter to get a queryset
        buses = Bus.objects.all()  # Get all buses; you might need to query differently based on your logic
        if routes.exists():
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/activity.html', {
                'routes': list(routes),  # Note: This should remain a list
                'buses': list(buses)      # Ensure buses are included here as well
            })
        else:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/status.html', {
                    'error': 'No routes found for the specified date.',
                    'buses': list(buses)
                })
        return Response({'routes': list(routes)}, status=status.HTTP_200_OK)



from django.utils import timezone
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus  # Ensure Activate is imported
class Activates(APIView):
    def get(self, request):
        #routes = Route.objects.all().values()  # Use values() to return a list of dicts
        #buses = Bus.objects.all().values()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/activity.html', {
                #'routes': list(routes),
                #'buses': list(buses)
            })
        return Response({'routes': list(routes), 'buses': list(buses)}, status=status.HTTP_200_OK)
    

    def post(self, request):
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date_str = request.data.get('date')  # Capture the date string
        date = request.data.get('date')  # Capture the date string
        kilometer = request.data.get('kilometer')
        price = request.data.get('price')
        plate_no = request.data.get('plate_no')
        is_active = request.data.get('is_active') == 'true'  # Convert to boolean

        # Validate and convert the date
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Expect format YYYY-MM-DD
        except ValueError:
            return self._handle_response(request, {
                'error': 'Invalid date format. Date must be in YYYY-MM-DD format.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Attempt to find the Activate entry
        try:
            sc_user = Route.objects.get(
                depcity=depcity,
                descity=descity,
                date=date,
                kilometer=kilometer,
                plate_no=plate_no,
                price=price
            )
            # Update the is_active status
            sc_user.is_active = is_active
            sc_user.save()

            # Refresh the list of routes and buses
            routes = Route.objects.filter(date=date)
            buses = Bus.objects.all().values()

            return self._handle_response(request, {
                'success': 'Status updated successfully!',
                'routes': list(routes),
                'buses': list(buses)
            })

        except Activate.DoesNotExist:
            # Handle the case where the Activate entry was not found
            return self._handle_response(request, {
                'error': 'Activate not found!',
                'routes': list(routes),
                'buses': list(buses)
            }, status=status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code=status.HTTP_200_OK):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/activity.html', context)
        return Response(context, status=status_code)







"""
from django.utils import timezone
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus, Activate  # Make sure Activate is imported

class Activates(APIView):
    def get(self, request):
        routes = Activate.objects.all().values()  # Use values() to return a list of dicts
        buses = Bus.objects.all().values()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/activity.html', {
                'routes': list(routes),
                'buses': list(buses)
            })
        return Response({'routes': list(routes), 'buses': list(buses)}, status=status.HTTP_200_OK)
   
    def post(self, request):
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        kilometer = request.data.get('kilometer')
        price = request.data.get('price')
        plate_no = request.data.get('plate_no')
        is_active = request.data.get('is_active') == 'true'  # Convert to boolean

        # Validate and parse the date
        try:
            #date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Expect format YYYY-MM-DD
            # Verify the Activate entry exists
            sc_user = Activate.objects.get(
            depcity=depcity,
            descity=descity,
            date=date,
            kilometer=kilometer,
            plate_no=plate_no,
            price=price
        )
            # Update the is_active status
            sc_user.is_active = is_active
            sc_user.save()

            # Refresh the list of routes and buses
            routes = Activate.objects.all().values()
            buses = Bus.objects.all().values()

            return self._handle_response(request, {
            'success': 'Status updated successfully!',
            'routes': list(routes),
            'buses': list(buses)
        })

        except Activate.DoesNotExist:
            return self._handle_response(request, {
            'error': 'Activate not found!',
            'routes': list(routes),
            'buses': list(buses)
        }, status=status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code=status.HTTP_200_OK):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/activity.html', context)
        return Response(context, status=status_code)
"""

"""
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus, Route, Activate  # Import Activate model

class Activates(APIView):
    def get(self, request):
        routes = Activate.objects.all().values()  # Use values() to return a list of dicts
        buses = Bus.objects.all().values()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/activity.html', {
                'routes': list(routes),
                'buses': list(buses)
            })
        else:
            return Response({'routes': list(routes), 'buses': list(buses)}, status=status.HTTP_200_OK)

    def post(self, request):
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        kilometer = request.data.get('kilometer')
        price = request.data.get('price')
        plate_no = request.data.get('plate_no')
        is_active = request.data.get('is_active') == 'true'  # Assuming this is passed as a string

        try:
            # Retrieve the specific Activate object and update its is_active status
            sc_user = Activate.objects.get(
                depcity=depcity,
                descity=descity,
                date=date,
                kilometer=kilometer,
                plate_no=plate_no,
                price=price
            )
            sc_user.is_active = is_active  # Update is_active based on input
            sc_user.save()

            routes = Activate.objects.all().values()  # Refresh routes
            buses = Bus.objects.all().values()  # Refresh buses

            return self._handle_response(request, {
                'success': 'Status updated successfully!',
                'routes': list(routes),
                'buses': list(buses)
            })

        except Activate.DoesNotExist:
            return self._handle_response(request, {
                'error': 'Activate not found!',
                'routes': list(routes),
                'buses': list(buses)
            }, status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code=status.HTTP_200_OK):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/activity.html', context)
        else:
            return Response(context, status=status_code)
"""



"""
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus, Route, Ticket, Buschange, Sc, Activate
class Activates(APIView):
    def get(self, request):
        routes = Activate.objects.all().values()  # Use values() to return a list of dicts
        buses = Bus.objects.all().values()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/activity.html', {
                'routes': list(routes),
                'buses': list(buses)
            })
        else:
            return Response({'routes': list(routes), 'buses': list(buses)}, status=status.HTTP_200_OK)

    def post(self, request):
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')  # Ensure the key matches your HTML form
        is_active = request.data.get('is_active')
        kilometer = request.data.get('kilometer')
        price = request.data.get('price')
        plate_no = request.data.get('plate_no')
        routes = Activate.objects.all().values()
        buses = Bus.objects.all().values()

        try:
            # Update the user's email
            sc_user = Activate.objects.get(depcity=depcity, descity=descity, date=date, kilometer=kilometer, plate_no=plate_no, price=price)
            if is_active = activate:
                is_active = True
            elif is_active deactive:
                is_active = False
            sc_user.save()

            # Render response based on request type
            return self._handle_response(request, {
                'success': 'SC updated successfully!',
                'routes': list(routes),
                'buses': list(buses)
            })
        except Sc.DoesNotExist:
            return self._handle_response(request, {
                'error': 'SC not found!',
                'routes': list(routes),
                'buses': list(buses)
            }, status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code=status.HTTP_200_OK):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/activity.html', context)
        else:
            return Response(context, status=status_code)

"""


from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus, Route, Ticket, Buschange, Sc  # Ensure Sc is imported
class Scchange(APIView):
    def get(self, request):
        routes = Sc.objects.all().values()  # Use values() to return a list of dicts
        buses = Bus.objects.all().values()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scchange.html', {
                'routes': list(routes),
                'buses': list(buses)
            })
        else:
            return Response({'routes': list(routes), 'buses': list(buses)}, status=status.HTTP_200_OK)

    def post(self, request):
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        new_email = request.data.get('new_email')  # Ensure the key matches your HTML form
        email = request.data.get('email')
        name = request.data.get('name')
        routes = Sc.objects.all().values()
        buses = Bus.objects.all().values()

        try:
            # Check if the new email is already reserved
            if Sc.objects.filter(email=new_email).exists():
                return self._handle_response(request, {
                    'error': 'This email is reserved for another SC.',
                    'routes': list(routes),
                    'buses': list(buses)
                }, status.HTTP_400_BAD_REQUEST)

            # Update the user's email
            sc_user = Sc.objects.get(firstname=firstname, name=name, lastname=lastname, email=email)
            sc_user.email = new_email
            sc_user.save()

            # Render response based on request type
            return self._handle_response(request, {
                'success': 'SC updated successfully!',
                'routes': list(routes),
                'buses': list(buses)
            })

        except Sc.DoesNotExist:
            return self._handle_response(request, {
                'error': 'SC not found!',
                'routes': list(routes),
                'buses': list(buses)
            }, status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code=status.HTTP_200_OK):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scchange.html', context)
        else:
            return Response(context, status=status_code)




"""
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus, Route, Ticket, Buschange, Sc  # Ensure Sc is imported

class Scchange(APIView):
    
    def get(self, request):
        routes = Sc.objects.all().values()  # Use values() to return a list of dicts
        buses = Bus.objects.all().values()

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scchange.html', {
                'routes': list(routes),
                'buses': list(buses)
            })
        else:
            return Response({'routes': list(routes), 'buses': list(buses)}, status=status.HTTP_200_OK)

    def post(self, request):
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        new_email = request.data.get('new_side_no')
        email = request.data.get('email')
        name = request.data.get('name')
        routes = Sc.objects.all().values()
        buses = Bus.objects.all().values()
        try:
            # Check if the new email is already reserved
            if Sc.objects.filter(email=new_email).exists():
                return self._handle_response(request, {
                    'error': 'This email is reserved for another SC.',
                    'routes': list(routes),
                    'buses': list(buses)
                }, status.HTTP_400_BAD_REQUEST)

            # Update the user's email
        sc_user = Sc.objects.get(firstname=firstname, name=name, lastname=lastname, email=email)
        sc_user.email = new_email
        sc_user.save()

        # Render response based on request type
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scchange.html', {'success': 'sc Updated Successfully!', 'routes': list(routes),
                'buses': list(buses)})
        except Sc.DoesNotExist:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/scchange.html', {'error': 'sc Sc Not Found!', 'routes': list(routes),'buses': list(buses)})
    def _handle_response(self, request, context, status_code=status.HTTP_200_OK):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scchange.html', context)
        else:
            return Response(context, status=status_code)

"""


"""
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus, Route, Ticket, Buschange
class Scchange(APIView):
    def get(self, request):
        routes = Sc.objects.all().values()  # Use values() to return a list of dicts
        buses = Bus.objects.all().values()

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scchange.html', {
                'routes': list(routes),
                'buses': list(buses)
            })
        else:
            return Response({'routes': list(routes), 'buses': list(buses)}, status=status.HTTP_200_OK)

    def post(self, request):
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        date = request.data.get('date')
        username = request.data.get('username')
        new_email = request.data.get('new_side_no')
        email = request.data.get('email')
        routes = Route.objects.all().values()
        buses = Bus.objects.all().values()
        try:
            if Sc.objects.filter(email=new_email).exists():
                return self._handle_response(request, {
                    'error': 'This email is reserved for other Sc.',
                    'routes': list(routes),
                    'buses': list(buses)
                }, status.HTTP_400_BAD_REQUEST)

            
            route = Sc.objects.get(firstname=firstname, lastname=lastname, email=email)
            route.email = new_email
            route.save()
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/scchange.html', {
                'routes': list(routes),
                'buses': list(buses)
            })

    def _handle_response(self, request, context, status_code):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scchange.html', context)
        else:
            return Response(context, status=status_code)
"""



from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import City, Buschange
class ChangeBusesViews(APIView):
    def get(self, request):
        
        des = City.objects.all()
        return self._handle_response(request, {'des': des}, status.HTTP_200_OK)

    def post(self, request):
        
        date = request.data.get('date')
        buschanges = Buschange.objects.filter(date=date)

        if buschanges.exists():
            count = buschanges.count()
            context = {'count': count, 'buschange': buschanges}
            return self._handle_response(request, context, status.HTTP_200_OK)
        else:
            buschanges_count = Buschange.objects.count()
            des = City.objects.all()
            context = {
                'buschanges_count': buschanges_count,
                'error1': "NO change buses for this travel date!",
                'des': des
            }
            return self._handle_response(request, context, status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code):
        
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/busschange.html', context)
        else:
            return Response(context, status=status_code)



from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import City
from .serializers import CitySerializer
class CityInsertView(generics.GenericAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    def get(self, request, *args, **kwargs):
        return render(request, 'users/city.html')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            depcity = serializer.validated_data['depcity']
            if City.objects.filter(depcity__iexact=depcity).exists():
                return Response({'error': 'City already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'success': 'City registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import City, Service_fee
from .serializers import ServiceSerializer
class ServicInsertView(generics.GenericAPIView):
    queryset = Service_fee.objects.all()
    serializer_class = ServiceSerializer

    def get(self, request, *args, **kwargs):
        return render(request, 'users/service_fee.html')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            service_fee = serializer.validated_data['service_fee']

            if Service_fee.objects.exists():
                return Response({'error': 'A service fee is already registered. Only one value is allowed.'}, status=status.HTTP_400_BAD_REQUEST)            
            # Save the new service fee
            serializer.save()
            return Response({'success': 'Service fee registered successfully.'}, status=status.HTTP_201_CREATED) 
        # Return any validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Sc
from .serializers import scSerializer
class ScInsertViews(generics.GenericAPIView):
    queryset = Sc.objects.all()
    serializer_class = scSerializer
    def get(self, request, *args, **kwargs):
        return render(request, 'users/scc.html')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            side = serializer.validated_data['side']
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            if Sc.objects.filter(name__iexact=name).exists():
                return render(request, 'users/scc.html', {'error': 'Sc Already Exist.'})
                #return Response({'error': 'Sc already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            elif Sc.objects.filter(side__iexact=side).exists():
                return render(request, 'users/scc.html', {'error': 'Sc Already Exist.'})
            elif Sc.objects.filter(username__iexact=username).exists():
                return render(request, 'users/scc.html', {'error': 'username Already Exist.'})
            elif Sc.objects.filter(email__iexact=email).exists():
                return render(request, 'users/scc.html', {'error': 'email Already Exist.'})
            serializer.save()

            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/scc.html', {'success': 'Sc Added successfully.'})
            return Response({'success': 'Sc Added successfully.'}, status=status.HTTP_201_CREATED)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scc.html', {'errors': serializer.errors})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus, Route, Ticket, Buschange
class ChangeBusView(APIView):
    def get(self, request):

        routes = Route.objects.all().values()  # Use values() to return a list of dicts
        buses = Bus.objects.all().values()

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/buschange.html', {
                'routes': list(routes),
                'buses': list(buses)
            })
        else:
            return Response({'routes': list(routes), 'buses': list(buses)}, status=status.HTTP_200_OK)

    def post(self, request):

        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        side_no = request.data.get('side_no')
        new_side_no = request.data.get('new_side_no')
        try:
            if Route.objects.filter(side_no=new_side_no, date=date).exists():
                return self._handle_response(request, {
                    'error': 'This bus is already reserved for the route on this date.'
                }, status.HTTP_400_BAD_REQUEST)

            bus_info = Bus.objects.filter(sideno=new_side_no).first()
            if not bus_info:
                return self._handle_response(request, {
                    'error': 'Invalid side number selected.'
                }, status.HTTP_400_BAD_REQUEST)

            new_plate_no = bus_info.plate_no
            total_seats = int(bus_info.no_seats) if bus_info.no_seats else 0

            booked_tickets_count = Ticket.objects.filter(date=date, side_no=side_no).count()
            if booked_tickets_count > total_seats:
                return self._handle_response(request, {
                    'error': 'Not enough seats available for this change.'
                }, status.HTTP_400_BAD_REQUEST)

            route = Route.objects.get(depcity=depcity, descity=descity, date=date, side_no=side_no)
            route.plate_no = new_plate_no
            route.side_no = new_side_no
            route.save()
            if depcity.strip() == "Addisababa":
                reciprocal_route = Route.objects.get(
                    depcity=descity,
                    descity=depcity,
                    date=(timezone.datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d'),
                    side_no=side_no
                )
                reciprocal_route.plate_no = new_plate_no
                reciprocal_route.side_no = new_side_no
                reciprocal_route.save()
            Ticket.objects.filter(date=date, side_no=side_no).update(
                plate_no=new_plate_no,
                side_no=new_side_no
            )
            booked_tickets = Ticket.objects.filter(date=date, side_no=new_side_no).values_list('no_seat', flat=True)
            booked_seats = set(int(seat) for seat in booked_tickets)
            booked_seat_count = len(booked_seats)
            remaining_seats = total_seats - booked_seat_count
            unbooked_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]

            Buschange.objects.create(
                plate_no=side_no,
                side_no=side_no,
                new_plate_no=new_plate_no,
                new_side_no=new_side_no,
                date=date,
                depcity=depcity,
                descity=descity
            )

            return self._handle_response(request, {
                'success': 'Bus changed successfully.',
                'total_seats': total_seats,
                'booked_seats': booked_seat_count,
                'remaining_seats': remaining_seats,
                'unbooked_seats': unbooked_seats,
                'booked_seat_list': list(booked_seats)
            }, status.HTTP_200_OK)

        except Route.DoesNotExist:
            return self._handle_response(request, {
                'error': "The specified route does not exist."
            }, status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/buschange.html', context)
        else:
            return Response(context, status=status_code)

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Bus, Worker, Route
def updatebus(request):
    buses = Bus.objects.all()  # Fetch all bus records
    success_message = None
    error_message = None
    if request.method == "POST":
        plate_no = request.POST.get('plate_no')
        new_sideno = request.POST.get('new_sideno')
        no_seats = request.POST.get('no_seats')
        try:
            bus = Bus.objects.get(plate_no=plate_no)
            if Bus.objects.filter(sideno=new_sideno).exists():
                error_message = 'This side no already exists.'
            else:
                bus.sideno = new_sideno
                bus.no_seats = no_seats
                bus.save()
                Worker.objects.filter(plate_no=plate_no).update(side_no=new_sideno)
                Route.objects.filter(plate_no=plate_no).update(side_no=new_sideno)
                success_message = 'Side No changed successfully!'
        except Bus.DoesNotExist:
            error_message = 'Bus not found.'
    return render(request, 'users/busupdate.html', {
        'buses': buses,
        'success_message': success_message,
        'error_message': error_message,
    })


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Bus, Worker, Route
class UpdateBusView(APIView):
    def post(self, request):
        plate_no = request.data.get('plate_no')
        new_sideno = request.data.get('new_sideno')
        no_seats = request.data.get('no_seats')
        try:
            bus = Bus.objects.get(plate_no=plate_no)
            if Bus.objects.filter(sideno=new_sideno).exists():
                return Response({'error': 'This side number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            bus.sideno = new_sideno
            bus.no_seats = no_seats
            bus.save()
            Worker.objects.filter(plate_no=plate_no).update(side_no=new_sideno)
            Route.objects.filter(plate_no=plate_no).update(side_no=new_sideno)
            return Response({'success': 'Side number changed successfully!'}, status=status.HTTP_200_OK)
        except Bus.DoesNotExist:
            return Response({'error': 'Bus not found.'}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        buses = Bus.objects.all()
        bus_data = [{'plate_no': bus.plate_no, 'sideno': bus.sideno, 'no_seats': bus.no_seats} for bus in buses]
        return Response({'buses': bus_data}, status=status.HTTP_200_OK)




from django.shortcuts import render
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import timedelta
from .models import Bus, Route, Ticket, Buschange
from .serializers import BusChangeSerializer
@api_view(['GET', 'POST'])
def changebus(request):
    context = {}
    if request.method == 'POST':
        serializer = BusChangeSerializer(data=request.data)
        if serializer.is_valid():
            depcity = request.data.get('depcity')
            descity = request.data.get('descity')
            date = request.data.get('date')
            side_no = request.data.get('side_no')
            new_side_no = request.data.get('new_side_no')
            try:
                if Route.objects.filter(side_no=new_side_no, date=date).exists():
                    context['error'] = 'This bus is already reserved for this route on this date.'
                else:
                    bus_info = Bus.objects.filter(sideno=new_side_no).first()
                    if not bus_info:
                        context['error'] = 'Invalid side number selected.'
                    else:
                        new_plate_no = bus_info.plate_no
                        total_seats = int(bus_info.no_seats) if bus_info.no_seats else 0

                        booked_tickets_count = Ticket.objects.filter(date=date, side_no=side_no).count()
                        if booked_tickets_count > total_seats:
                            context['error'] = 'Not enough seats available for this change.'
                        else:
                            route = Route.objects.get(depcity=depcity, descity=descity, date=date, side_no=side_no)
                            route.plate_no = new_plate_no
                            route.side_no = new_side_no
                            route.save()
                            if depcity.strip() == "Addisababa":
                                reciprocal_route = Route.objects.get(
                                    depcity=descity,
                                    descity=depcity,
                                    date=(timezone.datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d'),
                                    side_no=side_no
                                )
                                reciprocal_route.plate_no = new_plate_no
                                reciprocal_route.side_no = new_side_no
                                reciprocal_route.save()

                            Ticket.objects.filter(date=date, side_no=side_no).update(
                                plate_no=new_plate_no,
                                side_no=new_side_no
                            )
                            booked_tickets = Ticket.objects.filter(date=date, side_no=new_side_no).values_list('no_seat', flat=True)
                            booked_seats = set(int(seat) for seat in booked_tickets)
                            booked_seat_count = len(booked_seats)
                            remaining_seats = total_seats - booked_seat_count
                            unbooked_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]

                            Buschange.objects.create(
                                plate_no=side_no,
                                side_no=side_no,
                                new_plate_no=new_plate_no,
                                new_side_no=new_side_no,
                                date=date,
                                depcity=depcity,
                                descity=descity
                            )
                            context.update({
                                'success': 'Bus changed successfully.',
                                'total_seats': total_seats,
                                'booked_seats': booked_seat_count,
                                'remaining_seats': remaining_seats,
                                'unbooked_seats': unbooked_seats,
                                'booked_seat_list': booked_seats})

            except Route.DoesNotExist:
                context['error'] = "The specified route does not exist."
        else:
            context['error'] = serializer.errors
    return render(request, 'users/buschange.html', context)
from django.shortcuts import redirect
def changebus_redirect(request):
    return redirect('changebus')  # Replace with the actual URL name


from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Bus, Route, Ticket, Buschange
class ChangeBusView(APIView):
    def post(self, request):
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        side_no = request.data.get('side_no')
        new_side_no = request.data.get('new_side_no')
        try:
            if Route.objects.filter(side_no=new_side_no, date=date).exists():
                return Response({'error': 'This bus is already reserved for this route on this date.'}, status=status.HTTP_400_BAD_REQUEST)
            bus_info = Bus.objects.filter(sideno=new_side_no).first()
            if not bus_info:
                return Response({'error': 'Invalid side number selected.'}, status=status.HTTP_400_BAD_REQUEST)
            new_plate_no = bus_info.plate_no
            total_seats = int(bus_info.no_seats) if bus_info.no_seats else 0
            booked_tickets_count = Ticket.objects.filter(date=date, side_no=side_no).count()
            if booked_tickets_count > total_seats:
                return Response({'error': 'Not enough seats available for this change.'}, status=status.HTTP_400_BAD_REQUEST)
            route = Route.objects.get(depcity=depcity, descity=descity, date=date, side_no=side_no)
            route.plate_no = new_plate_no
            route.side_no = new_side_no
            route.save()

            # Update reciprocal route if necessary
            if depcity.strip() == "Addisababa":
                reciprocal_route = Route.objects.get(
                    depcity=descity,
                    descity=depcity,
                    date=(timezone.datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d'),
                    side_no=side_no
                )
                reciprocal_route.plate_no = new_plate_no
                reciprocal_route.side_no = new_side_no
                reciprocal_route.save()

            # Update tickets with the new bus details
            Ticket.objects.filter(date=date, side_no=side_no).update(plate_no=new_plate_no, side_no=new_side_no)

            # Get booked seats and calculate available seats
            booked_tickets = Ticket.objects.filter(date=date, side_no=new_side_no).values_list('no_seat', flat=True)
            booked_seats = set(int(seat) for seat in booked_tickets)
            booked_seat_count = len(booked_seats)
            remaining_seats = total_seats - booked_seat_count
            unbooked_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]
            Buschange.objects.create(
                plate_no=side_no,
                side_no=side_no,
                new_plate_no=new_plate_no,
                new_side_no=new_side_no,
                date=date,
                depcity=depcity,
                descity=descity
            )
            return Response({
                'success': 'Bus changed successfully.',
                'total_seats': total_seats,
                'booked_seats': booked_seat_count,
                'remaining_seats': remaining_seats,
                'unbooked_seats': unbooked_seats,
                'booked_seat_list': booked_seats
            }, status=status.HTTP_200_OK)
        except Route.DoesNotExist:
            return Response({'error': "The specified route does not exist."}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        routes = Route.objects.all()
        buses = Bus.objects.all()
        return Response({'routes': [route.to_dict() for route in routes], 'buses': [bus.to_dict() for bus in buses]}, status=status.HTTP_200_OK)


def changebuses(request):
    des = City.objects.all()
    if request.method == 'POST':
        date = request.POST.get('date')
        buschanges = Buschange.objects.filter(date=date)
        if buschanges.exists():
            count = Buschange.objects.filter(date=date).count()
            return render(request, 'users/busschange.html', {'count': count, 'buschange': buschanges})  # Pass the queryset
        else:
            buschanges = Buschange.objects.all()
            buschanges_count = buschanges.count()
            return render(request, 'users/index.html', {'buschanges_count': buschanges_count, 'error1': "NO change buses for this travel date!",'des': des})
    return render(request, 'users/index.html')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib import messages
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
class ChangePasswordViews(LoginRequiredMixin, APIView):
    def get(self, request):
        return self._handle_response(request, {}, status.HTTP_200_OK)
    def post(self, request):
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')
        re_new_password = request.data.get('reNewPassword')

        # Authenticate the user with the current password
        user = authenticate(username=request.user.username, password=current_password)
        if user is not None:
            # Check if new password and confirm password match
            if new_password == re_new_password:
                # Check if the new password is the same as the current password
                if current_password == new_password:
                    return self._handle_response(request, {
                        'error': "New password cannot be the same as the current password."
                    }, status.HTTP_400_BAD_REQUEST)
                else:
                    user.set_password(new_password)  # Set the new password securely
                    user.save()  # Save the user instance
                    update_session_auth_hash(request, user)  # Important!
                    return self._handle_response(request, {
                        'success': "Your password has been changed successfully."
                    }, status.HTTP_200_OK)
            else:
                return self._handle_response(request, {
                    'error': "New passwords do not match."
                }, status.HTTP_400_BAD_REQUEST)
        else:
            return self._handle_response(request, {
                'error': "Current password is incorrect."
            }, status.HTTP_400_BAD_REQUEST)

    def _handle_response(self, request, context, status_code):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/profile2.html', context)
        else:
            return Response(context, status=status_code)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
class ChangesPasswordView(LoginRequiredMixin, APIView):
    def get(self, request):
        return render(request, 'users/profile2.html', {})
    def post(self, request):
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')
        re_new_password = request.data.get('reNewPassword')
        # Authenticate the user with the current password
        user = authenticate(username=request.user.username, password=current_password)
        if user is not None:
            # Check if new password and confirm password match
            if new_password == re_new_password:
                # Check if the new password is the same as the current password
                if current_password == new_password:
                    messages.error(request, "New password cannot be the same as the current password.")
                    return redirect('change_password')  # Redirect to the same page to show the message
                else:
                    user.set_password(new_password)  # Set the new password securely
                    user.save()  # Save the user instance
                    update_session_auth_hash(request, user)  # Important!
                    messages.success(request, "Your password has been changed successfully.")
                    return redirect('profile')  # Change this to your desired redirect after success
            else:
                messages.error(request, "New passwords do not match.")
                return redirect('change_password')  # Redirect to show the error message
        else:
            messages.error(request, "Current password is incorrect.")
            return redirect('change_password')  # Redirect to show the error message



from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser  # Adjust the import as necessary
import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        re_new_password = request.POST.get('reNewPassword')
        # Authenticate the user with the current password
        user = authenticate(username=request.user.username, password=current_password)
        if user is not None:
            # Check if new password and confirm password match
            if new_password == re_new_password:
                # Check if the new password is the same as the current password
                if current_password == new_password:
                    messages.error(request, "New password cannot be the same as the current password.")
                else:
                    user.set_password(new_password)  # Set the new password securely
                    user.save()  # Save the user instance
                    update_session_auth_hash(request, user)  # Important!
                    messages.success(request, "Your password has been changed successfully.")
                    return redirect('profile')  # Change this to 'profile' to redirect to the profile view
            else:
                messages.error(request, "New passwords do not match.")
        else:
            messages.error(request, "Current password is incorrect.")
    return render(request, 'users/profile2.html')  # Render the change password form if GET request

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')
        re_new_password = request.data.get('reNewPassword')
        user = authenticate(username=request.user.username, password=current_password)
        if user is not None:
            if new_password == re_new_password:
                if current_password == new_password:
                    return Response({'error': "New password cannot be the same as the current password."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    return Response({'success': "Your password has been changed successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({'error': "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        return Response({'error': 'Use POST to change your password.'}, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import render
from django.conf import settings
#from .forms import UsernameEmailForm
def password_reset_request(request):
    if request.method == 'POST':
        form = UsernameEmailForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            user = None
            if username:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = None
            if email:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    user = None
            if user:
                # Send password reset email
                subject = "Password Reset Requested"
                email_template_name = "users/password_reset_email.html"
                c = {
                    "email": user.email,
                    'domain': request.META['HTTP_HOST'],
                    'site_name': 'Your Site Name',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email])                
                return render(request, 'users/password_reset_done.html')  # Create this template
    form = UsernameEmailForm()
    return render(request, 'users/password_reset.html', {'form': form})


