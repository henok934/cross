from drf_spectacular.utils import extend_schema
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import CustomUser
from .models import Feedback
from .models import Bus
from .models import Route
from django.db import IntegrityError
from .models import City
from .models import Buschange
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



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .serializers import PaymentRequestSerializer
@extend_schema(tags=['Payment Auth'])
class ProcessPaymentView(APIView):
    serializer_class = PaymentRequestSerializer
    @extend_schema(
        summary="Process payment method selection",
        description="Redirects web users to bank pages or returns JSON instructions for API clients.",
        request=PaymentRequestSerializer
    )
    def post(self, request, *args, **kwargs):
        payment_method = request.data.get('payment_method')
        price = request.data.get('price')
        templates = {
            'cbe': 'users/cbe.html',
            'boa': 'users/boa.html',
            'telebirr': 'users/tele.html',
            'safaricom': 'users/safaricom.html',
            'awash': 'users/awash.html'
        }
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            template_name = templates.get(payment_method, 'users/payment.html')
            return render(request, template_name, {'price': price})
        if payment_method in templates:
            return Response({
                'payment_method': payment_method,
                'price': price,
                'status': 'redirect_to_gateway',
                'message': f'Please proceed with {payment_method.upper()} payment.'
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid payment method selected'}, status=status.HTTP_400_BAD_REQUEST)






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Buschange  # Adjust based on your actual model imports
@extend_schema(tags=['Routes & Cities'])
class About(APIView):
    def get(self, request):
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
from drf_spectacular.utils import extend_schema
from .models import Buschange
from .serializers import AboutSerializer # Import the new serializer

class AboutViews(APIView):
    @extend_schema(
        tags=['Routes & Cities'],
        summary="Get about page information",
        description="Returns the count of all bus changes for both API and HTML views.",
        responses={200: AboutSerializer}
    )
    def get(self, request):
        buschanges_count = Buschange.objects.count()

        context = {
            'buschanges_count': buschanges_count
        }
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/about.html', context)
        serializer = AboutSerializer(context)
        return Response(serializer.data, status=status.HTTP_200_OK)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import City, Buschange  # Adjust based on your actual model imports
@extend_schema(tags=['Routes & Cities'])
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

@extend_schema(tags=['Routes & Cities'])
class About(APIView):
    def get(self, request):
        buschanges = Buschange.objects.all()
        buschanges_count = buschanges.count()
        des = City.objects.all()

        context = {
            'des': des,
            'buschanges_count': buschanges_count if buschanges_count > 0 else None
        }
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/about.html', context)
        response_data = {
            'des': [city.depcity for city in des],
            'buschanges_count': buschanges_count
        }
        return Response(response_data, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Worker
from django.contrib.auth.hashers import make_password
@extend_schema(tags=['Bus & Driver Management'])
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
@extend_schema(tags=['Bus & Driver Management'])
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
@extend_schema(tags=['Routes & Cities'])
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
@extend_schema(tags=['Bus & Driver Management'])
class BusInsertViews(APIView):

    def get(self, request, *args, **kwargs):
        return render(request, 'users/Businsert.html')
    def post(self, request, *args, **kwargs):
        print(request.data)
        plate_no = request.data.get('plate_no')
        sideno = request.data.get('sideno')
        no_seats = request.data.get('no_seats')
        level = request.data.get('level', 'unknown')  # Default to 'unknown' if not provided
        if not plate_no or not sideno or not no_seats:
            error_message = 'Plate number, Side number, and Number of seats are required.'
            return self.render_response(request, error=error_message)
        if Bus.objects.filter(plate_no=plate_no).exists():
            return self.render_response(request, error='Plate number already exists.')

        if Bus.objects.filter(sideno=sideno).exists():
            return self.render_response(request, error='Side number already exists.')
        Bus.objects.create(
            plate_no=plate_no,
            sideno=sideno,
            no_seats=no_seats,
            level=level
        )
        return self.render_response(request, success='Bus registered successfully.')

    def render_response(self, request, success=None, error=None):
        context = {}
        if success:
            context['success'] = success
        if error:
            context['error'] = error
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/Businsert.html', context)
        else:
            response_data = {'success': success} if success else {'error': error}
            return Response(response_data, status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST)



from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Route, City, Bus
from .serializers import RouteSerializer
@extend_schema(tags=['Routes & Cities'])
class RoutesInsertView(generics.GenericAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    def get(self, request, *args, **kwargs):
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
@extend_schema(tags=['Routes & Cities'])
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



"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Ticket, Buschange, City  # Ensure you import your models
def get_ticket(request):
    return render(request, 'users/getticket.html')
@extend_schema(tags=['Booking & Tickets'])
class TicketGetAPI(View):
    def get(self, request):
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
"""


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import CustomUser
from .serializers import USerializer
from drf_spectacular.utils import extend_schema
@extend_schema(tags=['User Management'])
class Use(APIView):
    serializer_class = USerializer

    def get(self, request):
        users = CustomUser.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/users.html', {'users': users})
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import Sc, Worker, CustomUser
from .serializers import ScSerializer

@extend_schema(tags=['SC Management'])
class Sce(APIView):

    @extend_schema(
        summary="List all SC users",
        responses={200: ScSerializer(many=True)}
    )
    def get(self, request):
        users = Sc.objects.all()
        serializer = ScSerializer(users, many=True)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/sce.html', {'users': users})
        return Response(serializer.data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema

from .models import Bus
from .serializers import BusesSerializer

@extend_schema(tags=['Bus & Driver Management'])
class Buse(APIView):
    serializer_class = BusesSerializer

    @extend_schema(
        summary="List all buses",
        responses={200: BusesSerializer(many=True)}
    )
    def get(self, request):
        buses = Bus.objects.all()
        serializer = BusesSerializer(buses, many=True)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/buses.html', {'buses': buses})
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import Worker
from .serializers import WorkSerializer

@extend_schema(tags=['Bus & Driver Management'])
class Drivers(APIView):
    serializer_class = WorkSerializer

    @extend_schema(
        summary="List all Drivers (Workers)",
        responses={200: WorkSerializer(many=True)}
    )
    def get(self, request):
        drivers = Worker.objects.all()
        serializer = WorkSerializer(drivers, many=True)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/drivers.html', {'driver': drivers})
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import Feedback
from .serializers import CommentteSerializer
@extend_schema(tags=['Feedback & Support'])
class Com(APIView):
    serializer_class = CommentteSerializer

    @extend_schema(
        summary="List all user feedback/comments",
        responses={200: CommentteSerializer(many=True)}
    )
    def get(self, request):
        comments = Feedback.objects.all()
        serializer = CommentteSerializer(comments, many=True)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/comments.html', {'comments': comments})
        return Response(serializer.data, status=status.HTTP_200_OK)




from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Route
from .serializers import RouteSerializer
from drf_spectacular.utils import extend_schema
@extend_schema(tags=['Routes Management'])
class Rout(APIView):
    serializer_class = RouteSerializer

    def get(self, request):
        routes = Route.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/routes.html', {'routes': routes})
        serializer = self.serializer_class(routes, many=True)
        return Response(serializer.data)


"""
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bus  # Assuming you have a Bus model
from .serializers import BusSerializer  # Assuming you have a BusSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
@extend_schema(tags=['Bus & Driver Management'])
class BusesView(APIView):
    def get(self, request):
        buses = Bus.objects.all()  # Fetch all Bus instances
        serializer = BusSerializer(buses, many=True)  # Serialize the data
        return Response(serializer.data)  # Return JSON response
"""


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import render  # Import render
from .models import Ticket, Route
from .serializers import RouteSerializer, TickSerializer, RoutSerializer
@extend_schema(tags=['Booking & Tickets'])
@extend_schema(tags=['Bus & Driver Management'])
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

class Changepassenger(APIView):
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/changepassenger.html', {'des': des})
        return Response({'des': [city.depcity for city in des]}, status=status.HTTP_200_OK)

    def post(self, request):
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        new_firstname = request.data.get('new_firstname')
        new_lastname = request.data.get('new_lastname')
        new_phone = request.data.get('new_phone')

        error_message = None
        success_message = None
        current_ticket = Ticket.objects.filter(
            firstname=firstname,
            lastname=lastname,
            depcity=depcity,
            descity=descity,
            date=date
        ).first()

        if current_ticket:
            if not new_firstname or not new_lastname or not new_phone:
                error_message = 'All fields are required!'
            elif new_firstname.strip().lower() == new_lastname.strip().lower():
                error_message = 'Firstname and Lastname cannot be the same!'
            else:
                duplicate_exists = Ticket.objects.filter(
                    firstname=new_firstname,
                    lastname=new_lastname,
                    phone=new_phone,
                    depcity=depcity,
                    descity=descity,
                    date=date
                ).exclude(id=current_ticket.id).exists()

                if duplicate_exists:
                    error_message = 'A ticket with these details already exists for this trip!'
                else:
                    current_ticket.firstname = new_firstname
                    current_ticket.lastname = new_lastname
                    current_ticket.phone = new_phone
                    current_ticket.save()
                    qr_code_path = current_ticket.generate_qr_code()

                    success_message = 'Passenger details updated successfully!'
                    level = Bus.objects.filter(plate_no=current_ticket.plate_no).values_list('level', flat=True).first()

                    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                        return render(request, 'users/passenger.html', {
                            'ticket': current_ticket,
                            'level': level,
                            'qr_code_path': qr_code_path,
                            'success': success_message
                        })
                    return Response(TSerializer(current_ticket).data, status=status.HTTP_200_OK)
        if error_message:
            level = Bus.objects.filter(plate_no=current_ticket.plate_no).values_list('level', flat=True).first() if current_ticket else None
            qr_code_path = current_ticket.generate_qr_code() if current_ticket else None

            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/passenger.html', {
                    'error': error_message,
                    'ticket': current_ticket,
                    'level': level,
                    'qr_code_path': qr_code_path,
                    'des': City.objects.all()
                })
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Original ticket not found'}, status=status.HTTP_404_NOT_FOUND)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema

from .models import Ticket, City, Bus
from .serializers import TSerializer, ChangePassengerRequestSerializer

@extend_schema(tags=['Booking & Tickets'])
class Changepassenger(APIView):
    serializer_class = ChangePassengerRequestSerializer

    @extend_schema(summary="Get passenger change page")
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/changepassenger.html', {'des': des})
        return Response({'cities': [city.depcity for city in des]}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update passenger details on a ticket",
        request=ChangePassengerRequestSerializer,
        responses={200: TSerializer, 400: dict}
    )
    def post(self, request):
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')

        new_firstname = request.data.get('new_firstname')
        new_lastname = request.data.get('new_lastname')
        new_phone = request.data.get('new_phone')

        error_message = None
        current_ticket = Ticket.objects.filter(
            firstname=firstname,
            lastname=lastname,
            depcity=depcity,
            descity=descity,
            date=date
        ).first()

        if not current_ticket:
            return self._handle_response(request, None, "Original ticket not found", status.HTTP_404_NOT_FOUND)
        if not all([new_firstname, new_lastname, new_phone]):
            error_message = 'All fields are required!'
        elif new_firstname.strip().lower() == new_lastname.strip().lower():
            error_message = 'Firstname and Lastname cannot be the same!'
        else:
            duplicate_exists = Ticket.objects.filter(
                firstname=new_firstname,
                lastname=new_lastname,
                phone=new_phone,
                depcity=depcity,
                descity=descity,
                date=date
            ).exclude(id=current_ticket.id).exists()

            if duplicate_exists:
                error_message = 'A ticket with these details already exists for this trip!'
            else:
                current_ticket.firstname = new_firstname
                current_ticket.lastname = new_lastname
                current_ticket.phone = new_phone
                current_ticket.save()
                qr_code_path = current_ticket.generate_qr_code()
                level = Bus.objects.filter(plate_no=current_ticket.plate_no).values_list('level', flat=True).first()

                return self._handle_response(request, current_ticket, "Updated successfully!", status.HTTP_200_OK, qr_code_path, level)
        return self._handle_response(request, current_ticket, error_message, status.HTTP_400_BAD_REQUEST)

    def _handle_response(self, request, ticket, message, status_code, qr_path=None, level=None):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            context = {
                'ticket': ticket,
                'level': level,
                'qr_code_path': qr_path or (ticket.generate_qr_code() if ticket else None),
                'des': City.objects.all()
            }
            if status_code >= 400:
                context['error'] = message
            else:
                context['success'] = message
            return render(request, 'users/passenger.html', context)
        if status_code >= 400:
            return Response({'error': message}, status=status_code)
        return Response(TSerializer(ticket).data, status=status_code)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import Ticket, City, Bus
from .serializers import TSerializer, TicketSearchSerializer

class GetTicketViews(APIView):
    
    @extend_schema(
        tags=['Booking & Tickets'],
        summary="Search tickets via URL parameters",
        parameters=[TicketSearchSerializer], # Displays fields in Swagger GET
        responses={200: TSerializer(many=True)}
    )
    def get(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            des = City.objects.all()
            return render(request, 'users/getticket.html', {'des': des})
        serializer = TicketSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            tickets = Ticket.objects.filter(**serializer.validated_data)
            output_serializer = TSerializer(tickets, many=True)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Booking & Tickets'],
        summary="Search tickets via JSON body",
        request=TicketSearchSerializer, # Displays fields in Swagger POST body
        responses={200: TSerializer}
    )
    def post(self, request):
        is_html = 'text/html' in request.META.get('HTTP_ACCEPT', '')
        serializer = TicketSearchSerializer(data=request.data)
        if not serializer.is_valid():
            error_message = list(serializer.errors.values())[0][0]
            return self._handle_error(request, error_message, is_html)
        data = serializer.validated_data
        ticket = Ticket.objects.filter(
            firstname=data['firstname'],
            lastname=data['lastname'],
            depcity=data['depcity'],
            descity=data['descity'],
            date=data['date']
        ).first()

        if ticket:
            plate_no = ticket.plate_no
            level = Bus.objects.filter(plate_no=plate_no).values_list('level', flat=True).first() if plate_no else None
            qr_code_path = ticket.generate_qr_code()

            if is_html:
                return render(request, 'users/tickets.html', {
                    'ticket': ticket,
                    'level': level,
                    'qr_code_path': qr_code_path
                })
            
            return Response(TSerializer(ticket).data, status=status.HTTP_200_OK)

        return self._handle_error(request, 'No booked tickets found for this travel', is_html, status_code=404)

    def _handle_error(self, request, message, is_html, status_code=400):
        if is_html:
            des = City.objects.all()
            return render(request, 'users/getticket.html', {'error': message, 'des': des})
        return Response({'error': message}, status=status_code)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema

from .models import Route, City
from .serializers import RoutSerializer, TicketSearchRequestSerializer

@extend_schema(tags=['Booking & Tickets'])
class TicketInfoView(APIView):
    serializer_class = TicketSearchRequestSerializer

    @extend_schema(summary="Get ticket search page or city list")
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cheeckrouteee.html', {'des': des})
        return Response({'cities': [city.name for city in des]}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Search for routes by date and cities",
        request=TicketSearchRequestSerializer,
        responses={200: RoutSerializer(many=True), 404: dict}
    )
    def post(self, request):
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')

        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)

        if routes.exists():
            serialized_route = RoutSerializer(routes, many=True)

            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rootee.html', {'routes': serialized_route.data})

            return Response({'routes': serialized_route.data}, status=status.HTTP_200_OK)

        else:
            error_msg = 'No booked tickets for this travel'

            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                des = City.objects.all()
                return render(request, 'users/cheeckrouteee.html', {
                    'error': error_msg,
                    'des': des
                })

            return Response({'error': error_msg}, status=status.HTTP_404_NOT_FOUND)



"""
from .serializers import TicketSerializer
@extend_schema(tags=['Booking & Tickets'])
class TicketListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


    from rest_framework import generics
from .models import Worker
from .serializers import WorkSerializer  # Ensure this matches your filename
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Bus & Driver Management'])
class WorkerView(generics.CreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkSerializer
"""


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from drf_spectacular.utils import extend_schema

from .models import Buschange, Route, Worker, Sc
from .serializers import LoginRequestSerializer

class LoginView(APIView):
    serializer_class = LoginRequestSerializer

    @extend_schema(tags=['Authentication'], summary="Get login page or bus counts")
    def get(self, request):
        buschanges_count = Buschange.objects.count()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/login.html', {'buschanges_count': buschanges_count})
        return Response({'buschanges_count': buschanges_count}, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Authentication'],
        summary="Login for Workers, Users, or SCs",
        request=LoginRequestSerializer
    )
    def post(self, request):
        buschanges_count = Buschange.objects.count()
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
                raise Worker.DoesNotExist

            request.session['worker_id'] = worker.id
            request.session['username'] = worker.username

            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rooteee.html', {'username': worker.username})
            return Response({'username': worker.username}, status=status.HTTP_200_OK)
        except Worker.DoesNotExist:
            return self.handle_login_error(buschanges_count, request, 'Worker credentials not found')

    def handle_user_login(self, username, password, buschanges_count, request):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/profile.html', {'user': user})
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return self.handle_login_error(buschanges_count, request, 'Invalid user credentials')

    def handle_sc_login(self, username, password, buschanges_count, request):
        try:
            sc_user = Sc.objects.get(username=username)
            if not check_password(password, sc_user.password):
                return self.handle_login_error(buschanges_count, request, 'Invalid password')

            request.session['sc_id'] = sc_user.id
            request.session['username'] = sc_user.username

            side_parts = sc_user.side.split('/')
            first_part = side_parts[0].strip()
            second_part = side_parts[1].strip() if len(side_parts) == 2 else None

            if first_part == '3' or second_part == '3':
                routes = Route.objects.filter(side_no__regex=r'^\d{3}$')
            else:
                filters = Q(side_no__startswith=first_part, side_no__regex=r'^\d{4}$')
                if second_part:
                    filters |= Q(side_no__startswith=second_part, side_no__regex=r'^\d{4}$')
                routes = Route.objects.filter(filters)

            serialized_routes = self.serialize_routes(routes)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rooteeess.html', {
                    'routes': serialized_routes,
                    'name': sc_user.name,
                    'side': sc_user.side
                })
            return Response({'routes': serialized_routes}, status=status.HTTP_200_OK)
        except Sc.DoesNotExist:
            return self.handle_login_error(buschanges_count, request, 'SC user not found')

    def serialize_routes(self, routes):
        return [{'id': r.id, 'depcity': r.depcity, 'plate_no': r.plate_no, 'side_no': r.side_no} for r in routes]

    def handle_login_error(self, buschanges_count, request, error_message):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/login.html', {'error': error_message, 'buschanges_count': buschanges_count})
        return Response({'error': error_message}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from drf_spectacular.utils import extend_schema

from .models import City, Route, Bus, Ticket, Buschange, Worker
from .serializers import BooksSearchRequestSerializer

@extend_schema(tags=['Booking & Tickets'])
class Books(APIView):
    serializer_class = BooksSearchRequestSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('worker_id')
        if user_id:
            try:
                return Worker.objects.get(id=user_id)
            except Worker.DoesNotExist:
                return None
        return None

    def get_standardized_city(self, city_name):
        addis_neighborhoods = ['Kality', 'Ayertena', 'Lamberet', 'Autobustera']
        if city_name in addis_neighborhoods:
            return 'Addisababa'
        return city_name

    @extend_schema(summary="Get booking search page for workers")
    def get(self, request):
        worker = self.get_user_from_session(request)
        if not worker:
            return Response({'error': 'Worker session not found'}, status=status.HTTP_404_NOT_FOUND)

        buschanges_count = Buschange.objects.count()
        city = self.get_standardized_city(worker.city)
        username = worker.username.strip()

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/book.html', {
                'des': City.objects.all(),
                'username': username,
                'city': city,
                'buschanges_count': buschanges_count
            })

        return Response({
            'des': [c.name for c in City.objects.all()],
            'buschanges_count': buschanges_count,
            'city': city
        }, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Search routes (Worker specific)",
        request=BooksSearchRequestSerializer
    )
    def post(self, request):
        worker = self.get_user_from_session(request)
        if not worker:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        username = worker.username.strip()
        city = self.get_standardized_city(worker.city)

        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        try:
            incoming_date = datetime.strptime(date, '%Y-%m-%d').date()
            if incoming_date < timezone.now().date():
                raise ValueError("Past date")
        except (ValueError, TypeError):
            error_message = "Invalid or past date. Please use YYYY-MM-DD."
            return self._handle_error_response(request, error_message, city, username)
        rout_qs = Route.objects.filter(depcity=depcity, descity=descity, date=date)
        buschanges_count = Buschange.objects.count()
        routes_data = []
        levels = None

        for route in rout_qs:
            buses = Bus.objects.filter(plate_no=route.plate_no)
            levels = buses.first().level if buses.exists() else None
            total_seats = sum(int(b.no_seats) for b in buses if b.no_seats.isdigit())

            booked_count = Ticket.objects.filter(
                depcity=route.depcity,
                descity=route.descity,
                date=route.date,
                plate_no=route.plate_no
            ).count()

            remaining_seats = total_seats - booked_count

            if remaining_seats > 0:
                routes_data.append({
                    'route_id': route.id,
                    'route_obj': route, # For template
                    'levels': levels,
                    'remaining_seats': remaining_seats
                })

        if not routes_data:
            return self._handle_error_response(request, "No available travels found.", city, username)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/roo.html', {
                'routes': [r['route_obj'] for r in routes_data], # Passing actual objects to template
                'levels': levels,
                'username': username,
                'buschanges_count': buschanges_count
            })

        return Response({
            'routes': routes_data,
            'buschanges_count': buschanges_count
        }, status=status.HTTP_200_OK)

    def _handle_error_response(self, request, message, city, username):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/book.html', {
                'des': City.objects.all(),
                'city': city,
                'username': username,
                'buschanges_count': Buschange.objects.count(),
                'error': message
            })
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus, Route, Ticket, Worker, Buschange
from .serializers import RouteSerializer, SeatLookupRequestSerializer, SeatInfoResponseSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Ticket Booking'])
class SelView(APIView):
    serializer_class = SeatLookupRequestSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('worker_id')
        if user_id:
            try:
                return Worker.objects.get(id=user_id)
            except Worker.DoesNotExist:
                return None
        return None

    @extend_schema(summary="Get current worker session and notification count")
    def get(self, request):
        buschanges_count = Buschange.objects.count()
        worker = self.get_user_from_session(request)

        if not worker:
            return Response({'error': 'User session not found'}, status=status.HTTP_404_NOT_FOUND)

        username = worker.username.strip()

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/roo.html', {
                'buschanges_count': buschanges_count,
                'username': username
            })
        return Response({'username': username, 'buschanges_count': buschanges_count}, status=status.HTTP_200_OK)

    @extend_schema(
        request=SeatLookupRequestSerializer,
        responses={200: SeatInfoResponseSerializer},
        summary="Lookup available seats for a specific route"
    )
    def post(self, request):
        plate_no = request.data.get('plate_no')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')

        buschanges_count = Buschange.objects.count()
        routes = Route.objects.filter(depcity=depcity, descity=descity, date=date, plate_no=plate_no)

        if not routes.exists():
            return Response({'error': 'No Travel found for this information!'}, status=status.HTTP_404_NOT_FOUND)
        bus = Bus.objects.filter(plate_no=plate_no).first()
        if not bus:
            return Response({'error': 'Bus not found'}, status=status.HTTP_404_NOT_FOUND)

        total_seats = int(bus.no_seats)
        levels = bus.level

        booked_tickets = Ticket.objects.filter(
            depcity=depcity, descity=descity, date=date, plate_no=plate_no
        ).values_list('no_seat', flat=True)

        booked_seats = sorted([int(seat) for seat in booked_tickets if seat and str(seat).isdigit()])
        unbooked_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]
        remaining_seats_count = len(unbooked_seats)

        if remaining_seats_count <= 0:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/roo.html', {'error': 'This Bus is Full!', 'buschanges_count': buschanges_count})
            return Response({'error': 'This Bus is Full!'}, status=status.HTTP_400_BAD_REQUEST)
        serialized_routes = RouteSerializer(routes, many=True).data
        response_data = {
            'routes': serialized_routes,
            'levels': levels,
            'remaining_seats': remaining_seats_count,
            'unbooked_seats': unbooked_seats,
            'booked_seats': booked_seats,
            'all_seats': list(range(1, total_seats + 1))
        }
        worker = self.get_user_from_session(request)
        username = worker.username if worker else "Guest"

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/booker.html', {
                **response_data,
                'username': username,
                'buschanges_count': buschanges_count
            })
        return Response(response_data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Bus, Route, Ticket, Worker, Buschange
from .serializers import (
    RouteSerializer,
    SeatLookupRequestSerializer,
    SeatInfoResponseSerializer
)
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Seat Management'])
class SeeView(APIView):
    serializer_class = SeatLookupRequestSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('worker_id')
        if user_id:
            try:
                return Worker.objects.get(id=user_id)
            except Worker.DoesNotExist:
                return None
        return None

    @extend_schema(summary="Check current worker session")
    def get(self, request):
        buschanges_count = Buschange.objects.count()
        worker = self.get_user_from_session(request)

        if not worker:
            return Response({'error': 'User session not found'}, status=status.HTTP_404_NOT_FOUND)

        username = worker.username.strip()

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/roo.html', {
                'buschanges_count': buschanges_count,
                'username': username
            })
        return Response({'username': username, 'buschanges_count': buschanges_count}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Lookup available seats",
        request=SeatLookupRequestSerializer,
        responses={200: SeatInfoResponseSerializer}
    )
    def post(self, request):
        plate_no = request.data.get('plate_no')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')

        buschanges_count = Buschange.objects.count()
        routes = Route.objects.filter(depcity=depcity, descity=descity, date=date, plate_no=plate_no)

        if not routes.exists():
            return Response({'error': 'No Travel found'}, status=status.HTTP_404_NOT_FOUND)

        bus = Bus.objects.filter(plate_no=plate_no).first()
        if not bus:
            return Response({'error': 'Bus not found'}, status=status.HTTP_404_NOT_FOUND)
        total_seats = int(bus.no_seats)
        levels = bus.level
        booked_tickets = Ticket.objects.filter(
            depcity=depcity, descity=descity, date=date, plate_no=plate_no
        ).values_list('no_seat', flat=True)

        booked_seats = sorted([int(seat) for seat in booked_tickets if seat])
        unbooked_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]

        response_data = {
            'routes': RouteSerializer(routes, many=True).data,
            'levels': levels,
            'remaining_seats': len(unbooked_seats),
            'unbooked_seats': unbooked_seats,
            'booked_seats': booked_seats,
            'all_seats': list(range(1, total_seats + 1))
        }

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            worker = self.get_user_from_session(request)
            return render(request, 'users/booker.html', {
                **response_data,
                'username': worker.username if worker else "Guest",
                'buschanges_count': buschanges_count
            })
        return Response(response_data, status=status.HTTP_200_OK)





from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Bus, Sc
from .serializers import BusDeleteActionSerializer, BusDeleteDisplaySerializer
@extend_schema(tags=['Bus & Driver Management'])
class BusDeleteViews(APIView):
    serializer_class = BusDeleteActionSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')
        return Sc.objects.filter(id=user_id).first() if user_id else None

    @extend_schema(
        summary="List buses for deletion",
        responses={200: BusDeleteDisplaySerializer(many=True)}
    )
    def get(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return render(request, 'users/login.html', {'error': 'Please login'})
        buses = Bus.objects.filter(sideno__startswith=sc_user.side[:1])
        data = BusDeleteDisplaySerializer(buses, many=True).data
        if 'text/html' in request.META.get('HTTP_ACCEPT', '') or request.GET.get('format') == 'html':
            return render(request, 'users/busdelet.html', {
                'buses': data, 
                'name': sc_user.name
            })
            
        return Response(data)

    @extend_schema(
        summary="Delete a bus",
        request=BusDeleteActionSerializer,
        responses={200: BusDeleteDisplaySerializer(many=True)}
    )
    def post(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({"error": "Unauthorized"}, status=401)
        plate_no = request.data.get('plate_no')
        Bus.objects.filter(plate_no=plate_no).delete()
        updated_buses = Bus.objects.filter(sideno__startswith=sc_user.side[:1])
        data = BusDeleteDisplaySerializer(updated_buses, many=True).data
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/busdelet.html', {
                'buses': data,
                'success': f'Bus {plate_no} deleted successfully'
            })
        return Response(data, status=200)

@extend_schema(tags=['Routes & Cities'])
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


from rest_framework import generics, status, serializers
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Route, Sc
from .serializers import RoutSerializer, SpecificFilterSerializer

@extend_schema(tags=['Routes & Cities'])
class Specific(generics.GenericAPIView):
    queryset = Route.objects.all()
    serializer_class = RoutSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')
        try:
            return Sc.objects.get(id=user_id) if user_id else None
        except Sc.DoesNotExist:
            return None

    def get_side_parts(self, side):
        side_parts = side.split('/')
        if len(side_parts) == 1:
            return side_parts[0].strip(), None
        elif len(side_parts) == 2:
            return side_parts[0].strip(), side_parts[1].strip()
        return None, None

    def get_filtered_routes(self, sc_user, start_date, end_date):
        side = sc_user.side.strip()
        first_part, second_part = self.get_side_parts(side)
        
        if first_part is None:
            return None

        filters = Q(date__gte=start_date, date__lte=end_date)
        if first_part == '3' or second_part == '3':
            filters &= Q(side_no__regex=r'^\d{3}$')
        else:
            base_filter = Q(side_no__startswith=first_part) & Q(side_no__regex=r'^\d{4}$')
            if second_part:
                base_filter |= Q(side_no__startswith=second_part) & Q(side_no__regex=r'^\d{4}$')
            filters &= base_filter

        return Route.objects.filter(filters)

    @extend_schema(
        summary="Filter routes via Query Parameters (GET)",
        parameters=[
            OpenApiParameter(name='from', description="Start Date", required=True, type=str),
            OpenApiParameter(name='to', description="End Date", required=True, type=str),
        ],
        responses={200: RoutSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found or session expired'}, status=status.HTTP_404_NOT_FOUND)

        start_date = request.query_params.get('from')
        end_date = request.query_params.get('to')

        if not start_date or not end_date:
            return Response({'error': 'Please provide from and to dates.'}, status=status.HTTP_400_BAD_REQUEST)

        routes = self.get_filtered_routes(sc_user, start_date, end_date)
        if routes is None:
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)

        serialized_data = RoutSerializer(routes, many=True).data
        
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/specific.html', {'routes': serialized_data})
        return Response(serialized_data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Filter routes via Request Body (POST)",
        request=SpecificFilterSerializer,
        responses={200: RoutSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        start_date = request.data.get('from')
        end_date = request.data.get('to')

        routes = self.get_filtered_routes(sc_user, start_date, end_date)
        if routes is None:
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)

        serialized_data = RoutSerializer(routes, many=True).data

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/specific.html', {'routes': serialized_data})
        return Response(serialized_data, status=status.HTTP_200_OK)





from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from .models import Bus, Worker, Route, Sc
from .serializers import BusSerializer
@extend_schema(tags=['Bus & Driver Management'])
class DriverUpdateViewss(generics.GenericAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')  # Get SC ID from session
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
            return render(request, 'users/driverupdate.html', {
                'name': sc_user.name,
                'side': side,
                'buses': buses
            })
        return Response(BusSerializer(buses, many=True).data)  # Return JSON response

    def post(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
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
            return render(request, 'users/driverupdate.html', {
                'name': sc_user.name,
                'side': side,
                'buses': buses
            })
        return Response(BusSerializer(buses, many=True).data)  # Return JSON response

    def post(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
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

        plate_no = request.data.get('plate_no')
        side_no = request.data.get('side_no')
        username = request.data.get('username')
        new_username = request.data.get('new_username')
        new_phone = request.POST.get('new_phone')
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
            bus_exists.side_no = side_no
            bus_exists.plate_no = plate_no
            bus_exists.username = new_username
            bus_exists.phone = new_phone
            bus_exists.save()
            sc_user = self.get_user_from_session(request)
            if not sc_user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            sc_user = self.get_user_from_session(request)
            if not sc_user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            sc_user = self.get_user_from_session(request)
            if not sc_user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
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
            return render(request, 'users/driverupdate.html', {
                    'buses': buses,
                    'success': 'Driver updated successfully.'
                })
        else:
            buses = Bus.objects.filter(filters)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/driverupdate.html', {
                    'buses': buses,
                    'error_message': 'Bus not found.'
                })
        return Response({'message': 'Request processed successfully'}, status=status.HTTP_200_OK)

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import Bus, Sc, Route
from .serializers import BusUpdateActionSerializer, BusTableResponseSerializer

@extend_schema(tags=['Bus & Driver Management'])
class BusUpdateViewss(APIView):
    serializer_class = BusUpdateActionSerializer

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')
        return Sc.objects.filter(id=user_id).first() if user_id else None

    def get_side_parts(self, side):
        parts = side.split('/')
        return (parts[0].strip(), parts[1].strip() if len(parts) > 1 else None)
    def get_buses(self, side):
        first_part, second_part = self.get_side_parts(side)
        if not first_part:
            return None, {'error': 'Invalid side format'}

        if first_part == '3' or second_part == '3':
            return Bus.objects.filter(sideno__regex=r'^\d{3}$'), None

        filters = Q(sideno__startswith=first_part) & Q(sideno__regex=r'^\d{4}$')
        if second_part:
            filters |= Q(sideno__startswith=second_part) & Q(sideno__regex=r'^\d{4}$')

        return Bus.objects.filter(filters), None

    @extend_schema(responses={200: BusTableResponseSerializer(many=True)})
    def get(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'Unauthorized'}, status=401)

        buses, error = self.get_buses(sc_user.side)
        if error: return Response(error, status=400)

        data = BusTableResponseSerializer(buses, many=True).data
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/busupdate.html', {'buses': data, 'side': sc_user.side})
        return Response(data)

    @extend_schema(request=BusUpdateActionSerializer, responses={200: BusTableResponseSerializer(many=True)})
    def post(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({'error': 'Unauthorized'}, status=401)

        plate_no = request.data.get('plate_no')
        new_sideno = request.data.get('new_sideno')
        no_seats = request.data.get('no_seats')
        Bus.objects.filter(plate_no=plate_no).update(sideno=new_sideno, no_seats=no_seats)
        Route.objects.filter(plate_no=plate_no).update(side_no=new_sideno)
        buses, _ = self.get_buses(sc_user.side)
        data = BusTableResponseSerializer(buses, many=True).data

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/busupdate.html', {'buses': data,  'side': sc_user.side, 'success': 'Updated!'})
        return Response(data, status=200)



from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Worker, City # Ensure City is imported
from .serializers import WorkerSerializer
from rest_framework import status
from drf_spectacular.utils import extend_schema
@extend_schema(tags=['Bus & Driver Management'])
class Workers(APIView):
    serializer_class = WorkerSerializer

    def get(self, request, *args, **kwargs):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            des = City.objects.all()
            return render(request, 'users/worker.html', {'des': des})
        workers = Worker.objects.all()
        serializer = WorkerSerializer(workers, many=True)
        return Response(serializer.data)
    def post(self, request, *args, **kwargs):
        serializer = WorkerSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            phone = serializer.validated_data.get('phone')
            if Worker.objects.filter(username=username).exists():
                return Response({'error': 'User name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            if Worker.objects.filter(phone=phone).exists():
                return Response({'error': 'Phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'success': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.db.models import Q  # Make sure to import Q if you are using it
from .models import Worker, Sc  # Ensure Sc is imported
@extend_schema(tags=['Bus & Driver Management'])
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
        return render(request, 'users/driverdelete.html', {'driver': driver})

    def post(self, request):
        if request.data.get('_method') == 'DELETE':
            plate_no = request.data.get('plate_no')
            side_no = request.data.get('side_no')
            fname = request.data.get('fname')
            lname = request.data.get('lname')
            print(f"Received data: plate_no={plate_no}, side_no={side_no}, fname={fname}, lname={lname}")
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
            context = {
                'driver': Worker.objects.all(),
                'error': 'Driver not found'  # Optional error message
            }
            return self._render_response(request, context, status.HTTP_200_OK)
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
@extend_schema(tags=['Bus & Driver Management'])
class MyDriver(generics.GenericAPIView):
    queryset = Worker.objects.all()

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
@extend_schema(tags=['Bus & Driver Management'])
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
        side = sc_user.side.strip()  # Get the side of buses
        first_part, second_part = self.get_side_parts(side)
        if first_part is None:  # Invalid side format
            return Response({'error': 'Invalid side format'}, status=status.HTTP_400_BAD_REQUEST)
        if first_part == '3' or second_part == '3':
            buses = Bus.objects.filter(sideno__regex=r'^\d{3}$')
        else:
            filters = Q(sideno__startswith=first_part) & Q(sideno__regex=r'^\d{4}$')
            if second_part:
                filters |= Q(sideno__startswith=second_part) & Q(sideno__regex=r'^\d{4}$')
            buses = Bus.objects.filter(filters)
        serialized_routes = BusSerializer(buses, many=True).data
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/mybus.html', {
                'name': sc_user.name,
                'side': side,
                'buses': serialized_routes
            })
        return Response(BusSerializer(buses, many=True).data)  # Return JSON response

from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.db.models import Q
from .models import Ticket, Route, Sc
from .serializers import (
    TicketSearchRequestSerializer,
    AvailableRouteSerializer,
    TicketNotFoundErrorSerializer
)

@extend_schema(tags=['Booking & Tickets'])
class ShowTicketsViewss(APIView):
    serializer_class = TicketSearchRequestSerializer

    @extend_schema(summary="Get the ticket search page")
    def get(self, request):
        return render(request, 'users/ourticketoche.html')

    @extend_schema(
        summary="Search tickets (API & Web)",
        request=TicketSearchRequestSerializer,
        responses={
            200: TicketSearchRequestSerializer(many=True), # Replace with your Ticket Serializer
            404: TicketNotFoundErrorSerializer
        }
    )
    def post(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return self.handle_html_post(request) # This was missing!
        else:
            return self.handle_json_request(request)
    def handle_html_post(self, request):
        plate_no = request.POST.get('plate_no')
        side_no = request.POST.get('side_no')
        date = request.POST.get('date')
        depcity = request.POST.get('depcity')
        descity = request.POST.get('descity')

        tickets = Ticket.objects.filter(
            plate_no=plate_no,
            side_no=side_no,
            date=date,
            depcity=depcity,
            descity=descity
        )

        if tickets.exists():
            return render(request, 'users/ourticketoche.html', {'route': tickets})
        else:
            return self.handle_no_tickets(request)

    def handle_no_tickets(self, request):
        sc_id = request.session.get('sc_id')
        if not sc_id:
            return render(request, 'users/login.html', {'error': 'Session expired'})

        try:
            sc_user = Sc.objects.get(id=sc_id)
            side_parts = [s.strip() for s in sc_user.side.split('/')]
            if '3' in side_parts:
                routes = Route.objects.filter(side_no__regex=r'^\d{3}$')
            else:
                filters = Q(side_no__startswith=side_parts[0])
                if len(side_parts) > 1:
                    filters |= Q(side_no__startswith=side_parts[1])
                routes = Route.objects.filter(filters)

            return render(request, 'users/rooteees.html', {
                'error': 'No booked tickets found',
                'routes': self.serialize_routes(routes),
                'name': sc_user.name
            })
        except Sc.DoesNotExist:
            return render(request, 'users/login.html', {'error': 'User not found'})

    def serialize_routes(self, routes):
        return [
            {
                'id': r.id,
                'depcity': r.depcity,
                'descity': r.descity,
                'date': r.date,
                'plate_no': r.plate_no,
                'side_no': r.side_no,
            } for r in routes
        ]

    def handle_json_request(self, request):
        plate_no = request.data.get('plate_no')
        date = request.data.get('date')

        tickets = Ticket.objects.filter(plate_no=plate_no, date=date)

        if tickets.exists():
            return Response(list(tickets.values()), status=200)

        return self.handle_no_tickets_json(request)

    def handle_no_tickets_json(self, request):
        sc_id = request.session.get('sc_id')
        sc_user = Sc.objects.filter(id=sc_id).first()
        if not sc_user:
            return Response({"error": "Auth required"}, status=401)
        return Response({"error": "No tickets found"}, status=404)


from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import render
from .models import Bus, Sc
from .serializers import BusSerializer
@extend_schema(tags=['Bus & Driver Management'])
class BusInsertView(generics.GenericAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    def get(self, request, *args, **kwargs):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return self.handle_error(request, 'User not found.')

        name = sc_user.name
        side = sc_user.side
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
            plate_no = serializer.validated_data['plate_no']
            sideno = serializer.validated_data['sideno']

            if Bus.objects.filter(plate_no=plate_no).exists():
                return self.handle_error(request, 'Plate number already exists.')
            if Bus.objects.filter(sideno=sideno).exists():
                return self.handle_error(request, 'Side number already exists.')

            serializer.save()
            return self.handle_success(request, 'Bus registered successfully.')
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
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import extend_schema

from .models import CustomUser, Sc
from .serializers import ForgotPasswordSerializer

@extend_schema(tags=['Authentication'])
class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer

    @extend_schema(summary="Get forgot password page")
    def get(self, request):
        return render(request, 'users/forgot_password.html')

    @extend_schema(
        summary="Reset password and send via email",
        request=ForgotPasswordSerializer
    )
    def post(self, request):
        username_or_email = request.data.get('username_or_email')
        role = request.data.get('role')
        error_message = None
        user_obj = None
        if role == 'user':
            user_obj = CustomUser.objects.filter(username=username_or_email).first() or \
                       CustomUser.objects.filter(email=username_or_email).first()
        elif role == 'sc':
            user_obj = Sc.objects.filter(username=username_or_email).first() or \
                       Sc.objects.filter(email=username_or_email).first()
        if user_obj:
            new_password = get_random_string(length=12)
            if role == 'user':
                user_obj.set_password(new_password)
            else:
                user_obj.password = make_password(new_password)

            user_obj.save()
            try:
                send_mail(
                    'Password Reset Request',
                    f'Hello, your new temporary password is: {new_password}\n'
                    f'Please login and change it immediately.',
                    'teklemariammossie1@gmail.com',
                    [user_obj.email],
                    fail_silently=False,
                )

                success_msg = "Password reset successfully. Check your email."
                return self._handle_response(request, {"message": success_msg}, status.HTTP_200_OK)

            except Exception as e:
                error_message = "Email could not be sent. Please contact support."
        else:
            error_message = f"No {role} found with that username or email."

        return self._handle_response(request, {"error": error_message}, status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/forgot_password.html', context)
        return Response(context, status=status_code)



"""
from django.http import JsonResponse
from django.views import View
from .models import Buschange, City  # Ensure you import your models
@extend_schema(tags=['Routes & Cities'])
class HomePageAPI(View):
    def get(self, request):
        try:
            buschanges = Buschange.objects.all().values()
            buschanges_count = buschanges.count()  # Count of bus changes
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
"""


"""
def root(request):
    return render(request, 'users/checkroot.html')
def selectbus(request):
    return render(request, 'users/route.html')
"""


from django.shortcuts import render
from django.views import View
class MainPageView(View):  # Your view class
    def get(self, request):
        print("MainPageView called")  # Debugging line
        return render(request, 'users/index.html')  # Ensure this path is correct


"""
from django.http import JsonResponse
from django.views import View
from .models import Buschange, City
@extend_schema(tags=['Bus & Driver Management'])
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


@extend_schema(tags=['Routes & Cities'])
class RoutesView(APIView):
    def get(self, request):
        routes = Route.objects.all()
        route_data = [{'id': route.id, 'depcity': route.depcity, 'descity': route.descity} for route in routes]
        return Response({'routes': route_data}, status=status.HTTP_200_OK)

@extend_schema(tags=['Booking & Tickets'])
@extend_schema(tags=['Bus & Driver Management'])
class SelectBusView(APIView):
    def get(self, request):
        return Response({'message': 'Select a bus for your route.'}, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ticket, Service_fee
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
"""



"""
from .serializers import BuschangeSerializer, ServiceFeeSerializer
@extend_schema(tags=['Admin Logic'])
class BuschangeList(generics.ListAPIView):
    queryset = Buschange.objects.all()
    serializer_class = BuschangeSerializer

@extend_schema(tags=['Finance'])
class ServiceFeeList(generics.ListAPIView):
    queryset = Service_fee.objects.all()
    serializer_class = ServiceFeeSerializer
"""




from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Ticket, City, Bus
from .serializers import TicketSerializer

@extend_schema(tags=['Booking & Tickets'])
class TicketBookingViews(APIView):
    serializer_class = TicketSerializer 

    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/ticket.html', {'des': des})
        return Response({'cities': [city.depcity for city in des]})
    @extend_schema(
        description="Book multiple tickets using list arrays (form-data).",
        responses={201: TicketSerializer(many=True)}
    )
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
        try:
            total_price = sum(float(price) for price in prices)
            if prs:
                total_price -= sum(float(p) for p in prs)
        except ValueError:
            return Response({'error': 'Invalid price format'}, status=400)

        min_length = min(
            len(firstnames), len(lastnames), len(emails), len(genders),
            len(phones), len(prices), len(side_nos), len(plate_nos),
            len(depcitys), len(descitys), len(dates), len(no_seats)
        )

        used_seats = set()
        tickets = []

        with transaction.atomic():
            for i in range(min_length):
                current_seat = no_seats[i]

                if current_seat in used_seats:
                    return Response({'error': f'Seat {current_seat} already selected.'}, status=400)

                used_seats.add(current_seat)
                bus_info = Bus.objects.filter(sideno=side_nos[i]).first()
                
                level = bus_info.level if bus_info else "Unknown"
                name = bus_info.name if bus_info else "Unknown"

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
                    'username': usernames[i] if i < len(usernames) else None,
                    'no_seat': current_seat,
                }
                ticket_instance = Ticket(**validated_data)
                ticket_instance.save() 
                tickets.append(ticket_instance)
                self.send_ticket_email(validated_data, ticket_instance.qr_code)
            if prs:
                for i in range(min_length):
                    Ticket.objects.filter(firstname=firstnames[i], date=das[i]).delete()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            template = 'users/myticket.html' if (usernames and usernames[0]) else 'users/payment.html'
            return render(request, template, {
                'success': 'Booked successfully!',
                'tickets': tickets,
                'total_price': total_price,
                'level': level,
                'name': name
            })

        serializer = TicketSerializer(tickets, many=True)
        return Response({'message': 'Booking successful.', 'tickets': serializer.data}, status=201)
    def send_ticket_email(self, data, qr):
        subject = 'Ticket Booking Confirmation'
        message = f"Hello {data['firstname']}, your ticket is confirmed. QR: {qr}"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [data['email']], fail_silently=True)


from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import Ticket, City, Bus
from .serializers import TicketSerializer
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Booking & Tickets'])
class TicketBookingViews(APIView):
    serializer_class = TicketSerializer

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
        try:
            total_price = sum(float(price) for price in prices)
            if prs: 
                total_price -= sum(float(p) for p in prs)
        except ValueError:
            total_price = 0

        min_length = min(
            len(firstnames), len(lastnames), len(emails), len(genders),
            len(phones), len(prices), len(side_nos), len(plate_nos),
            len(depcitys), len(descitys), len(dates), len(no_seats)
        )

        used_seats = set()
        tickets = []  

        with transaction.atomic():
            for i in range(min_length):
                current_seat = no_seats[i]
                if current_seat in used_seats:
                    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                        return render(request, 'users/ticket.html', {'des': City.objects.all(), 'error': f'Seat {current_seat} already selected.'}, status=400)
                    return Response({'error': f'Seat {current_seat} already selected.'}, status=400)

                used_seats.add(current_seat)
                bus_info = Bus.objects.filter(sideno=side_nos[i]).first()
                
                level = bus_info.level if bus_info else "Unknown"
                name = bus_info.name if bus_info else "Unknown"

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
                    'username': usernames[i] if i < len(usernames) else "",
                    'no_seat': current_seat,
                }
                ticket_instance = Ticket(**validated_data)
                ticket_instance.save() 
                tickets.append(ticket_instance)
                subject = 'Ticket Booking Confirmation'
                message = f"Hello {validated_data['firstname']}, your booking for {validated_data['depcity']} to {validated_data['descity']} is confirmed."
                send_mail(subject, message, settings.EMAIL_HOST_USER, [validated_data['email']], fail_silently=True)
            if prs:
                for i in range(min_length):
                    Ticket.objects.filter(firstname=firstnames[i], date=das[i]).delete()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            if not usernames or not usernames[0]:
                return render(request, 'users/payment.html', {
                    'success': 'Ticket(s) booked successfully!',
                    'tickets': tickets,
                    'total_price': total_price
                })
            else:
                return render(request, 'users/myticket.html', {
                    'success': 'Ticket(s) booked successfully!',
                    'tickets': tickets,
                    'level': level,
                    'name': name
                })
        serializer = TicketSerializer(tickets, many=True)
        return Response({'message': 'Booking successful.', 'tickets': serializer.data}, status=status.HTTP_201_CREATED)

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers  # Added serializers here
from drf_spectacular.utils import extend_schema

from .models import Ticket, City, Worker
from .serializers import (
    TSerializer, 
    BalanceSearchSerializer, 
    TotalBalanceResponseSerializer
)

@extend_schema(tags=['Finance & Accounting'])
class Totalballance(APIView):
    
    @extend_schema(
        summary="Get balance page or city list",
        responses={200: serializers.Serializer} 
    )
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/ballance.html', {'des': des})
        return Response({'cities': [city.depcity for city in des]}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Calculate total balance by username and city",
        request=BalanceSearchSerializer,
        responses={200: TotalBalanceResponseSerializer}
    )
    def post(self, request):
        dates = request.data.getlist('date[]') if 'date[]' in request.data else request.data.get('date', [])

        if not dates:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/ballance.html', {'error': 'No dates provided', 'des': City.objects.all()})
            return Response({'error': 'No dates provided'}, status=status.HTTP_400_BAD_REQUEST)

        totals_by_username = {}
        tickets = Ticket.objects.filter(booked_time__date__in=dates)

        for ticket in tickets:
            username = ticket.username if ticket.username else "Selfbook"
            
            try:
                price = float(ticket.price)
            except (ValueError, TypeError):
                continue
            totals_by_username[username] = totals_by_username.get(username, 0) + price
        workers = Worker.objects.filter(username__in=totals_by_username.keys())
        username_city_map = {worker.username: worker.city for worker in workers}
        total_data = {
            username: {
                'total_balance': total,
                'city': username_city_map.get(username, 'Unknown')
            } 
            for username, total in totals_by_username.items() if total > 0
        }
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/totalballance.html', {
                'totals': total_data
            })
            
        return Response({'totals': total_data}, status=status.HTTP_200_OK)






"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City, Buschange, Ticket
@extend_schema(tags=['Booking & Tickets'])
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
"""





"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City, Buschange, Ticket
@extend_schema(tags=['Booking & Tickets'])
class GetTicketView(APIView):
    def get(self, request):
        buschanges_count = Buschange.objects.count()
        return Response({
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
"""


"""
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
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City, Bus
from .serializers import WorkSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from .models import City, Bus, Route
@extend_schema(tags=['Routes & Cities'])
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


"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City
@extend_schema(tags=['Routes & Cities'])
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
"""



"""
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .models import City, Bus
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
"""



"""
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
"""


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .serializers import TelebirrInitiateSerializer

@extend_schema(tags=['Payment Auth'])
class TelebirrPaymentView(APIView):
    serializer_class = TelebirrInitiateSerializer

    def get(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/tele.html')
        return Response({"message": "Use POST to initiate payment"}, status=200)

    @extend_schema(
        summary="Initiate Telebirr Payment",
        request=TelebirrInitiateSerializer,
        responses={200: TelebirrInitiateSerializer}
    )
    def post(self, request):
        phone_number = request.data.get('phone') or request.data.get('phone[]')
        price = request.data.get('price')
        if phone_number and len(phone_number) == 10 and phone_number.startswith('09'):
            context = {'phone_number': phone_number, 'price': price}
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/telepassword.html', context)
            return Response(context, status=status.HTTP_200_OK)

        else:
            error_message = "Invalid phone number. Please check and try again."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/tele.html', {'error': error_message})

            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)


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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import Service_fee
from .serializers import TelebirrAuthSerializer
@extend_schema(tags=['Payment Auth'])
class Telebirrpassword(APIView):
    serializer_class = TelebirrAuthSerializer

    def get(self, request):
        return render(request, 'users/telepassword.html')

    @extend_schema(
        summary="Process Telebirr Payment",
        request=TelebirrAuthSerializer,
        responses={200: dict}
    )
    def post(self, request):
        phone_number = request.data.get('phone')
        password = request.data.get('password')
        
        try:
            price_raw = request.data.get('price', 0)
            price = float(price_raw) if price_raw else 0.0
        except (ValueError, TypeError):
            price = 0.0

        recipient_phone = "0975143134"
        recipient_service_fee_phone = "0949949849"
        
        service_fee_instance = Service_fee.objects.first()
        value = service_fee_instance.service_fee if service_fee_instance else 0
        if phone_number and len(phone_number) == 10 and phone_number.startswith('09'):
            if self.is_phone_and_password_valid(phone_number, password):
                user_balance = self.get_balance(phone_number)
                recipient_balance = self.get_balance(recipient_phone)
                recipient_balance_service_fee = self.get_balance(recipient_service_fee_phone)

                if user_balance is not None and recipient_balance is not None:
                    if user_balance >= price:
                        transaction_response = self.create_transaction(recipient_phone, price)
                        
                        if transaction_response.get('success'):
                            fee = price - value
                            share_value = price - fee # Your original logic kept exactly
                            
                            new_recipient_balance_service_fee = (recipient_balance_service_fee or 0) + share_value
                            new_recipient_balance = (recipient_balance or 0) + fee
                            res1 = self.add_balance(recipient_phone, new_recipient_balance)
                            res2 = self.add_balance(recipient_service_fee_phone, new_recipient_balance_service_fee)

                            if res1.get('success') and res2.get('success'):
                                context = {
                                    'success': 'Successfully paid and balances updated.',
                                    'transaction_id': transaction_response.get('transaction_id'),
                                    'recipient_balance': new_recipient_balance
                                }
                                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                                    return render(request, 'users/payment_success.html', context)
                                return Response(context, status=status.HTTP_200_OK)
                            else:
                                return self.render_error(request, "Failed to update balances.", phone_number, price)
                        else:
                            return self.render_error(request, "Transaction failed.", phone_number, price)
                    else:
                        return self.render_error(request, "Insufficient balance.", phone_number, price)
                else:
                    return self.render_error(request, "Unable to retrieve balance.", phone_number, price)
            else:
                return self.render_error(request, "Invalid password.", phone_number, price)
        else:
            return self.render_error(request, "Invalid phone number format.", phone_number, price)

    def render_error(self, request, message, phone, price):
        context = {'error': message, 'phone_number': phone, 'price': price}
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/telepassword.html', context)
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    def is_phone_and_password_valid(self, phone_number, password):
        try:
            url = "https://www.ethiotelecom.et/telebirr/validate"
            payload = {'phone': phone_number, 'password': password}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            return response.json().get('valid', False) if response.status_code == 200 else False
        except Exception: return False

    def get_balance(self, phone_number):
        try:
            url = "https://www.ethiotelecom.et/telebirr/balance"
            payload = {'phone': phone_number}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            return float(response.json().get('balance', 0)) if response.status_code == 200 else None
        except Exception: return None

    def create_transaction(self, recipient_phone, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/transaction"
            payload = {'phone': recipient_phone, 'amount': amount, 'description': 'Payment'}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            return response.json() if response.status_code == 200 else {'success': False}
        except Exception: return {'success': False}

    def add_balance(self, phone_number, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/add_balance"
            payload = {'phone': phone_number, 'amount': amount}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            return response.json() if response.status_code == 200 else {'success': False}
        except Exception: return {'success': False}
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .serializers import CbeInputSerializer  # Import the serializer defined above

@extend_schema(tags=['Payment Auth'])
class CbePaymentView(APIView):
    serializer_class = CbeInputSerializer

    def get(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cbe.html')
        return Response({"message": "Please use a POST request to initiate payment."}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Initiate CBE Payment",
        request=CbeInputSerializer,
        responses={
            200: CbeInputSerializer, 
            400: dict
        }
    )
    def post(self, request):
        account_number = request.data.get('account')
        price = request.data.get('price')
        
        print(f"Processing payment: Account {account_number}, Price {price}")
        if account_number and len(account_number) == 13 and account_number.startswith('1000'):
            context = {'account_number': account_number, 'price': price}
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/cbepassword.html', context)
            
            return Response(context, status=status.HTTP_200_OK)
        
        else:
            error_message = "Invalid Account number. Please check and try again."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/cbe.html', {'error': error_message})
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)





import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from users.models import Service_fee
from .serializers import CbeAuthSerializer
@extend_schema(tags=['Payment Auth'])
class Cbepassword(APIView):
    serializer_class = CbeAuthSerializer

    def get(self, request):
        return render(request, 'users/cbepassword.html')

    @extend_schema(
        summary="Process CBE Payment",
        request=CbeAuthSerializer,
        responses={200: dict}
    )
    def post(self, request):
        account_number = request.data.get('account')
        password = request.data.get('password')
        
        try:
            price_raw = request.data.get('price', '0')
            price = float(price_raw)
        except (ValueError, TypeError):
            price = 0.0

        recipient_account = "1000327248549"
        recipient_service_fee_account = "1000136832598"
        
        service_fee_instance = Service_fee.objects.first()
        value = service_fee_instance.service_fee if service_fee_instance else 0
        if account_number and len(account_number) == 13 and account_number.startswith('1000'):
            if self.is_phone_and_password_valid(account_number, password):
                user_balance = self.get_balance(account_number)
                recipient_balance = self.get_balance(recipient_account)
                recipient_balance_service_fee = self.get_balance(recipient_service_fee_account)

                if user_balance is not None and recipient_balance is not None:
                    if user_balance >= price:
                        transaction_response = self.create_transaction(recipient_account, price)

                        if transaction_response.get('success'):
                            fee = price - value
                            share_value = price - fee
                            
                            new_recipient_balance_service_fee = (recipient_balance_service_fee or 0) + share_value
                            new_recipient_balance = (recipient_balance or 0) + fee
                            self.add_balance(recipient_account, new_recipient_balance)
                            add_balance_response = self.add_balance(recipient_service_fee_account, new_recipient_balance_service_fee)

                            if add_balance_response.get('success'):
                                context = {
                                    'success': 'Successfully paid and balance updated.',
                                    'transaction_id': transaction_response.get('transaction_id'),
                                    'recipient_balance': new_recipient_balance
                                }
                                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                                    return render(request, 'users/cbe_success.html', context)
                                return Response(context, status=status.HTTP_200_OK)
                            else:
                                return self.render_error(request, "Failed to update recipient balance.", account_number, price)
                        else:
                            return self.render_error(request, "Transaction failed. Please try again.", account_number, price)
                    else:
                        return self.render_error(request, "Insufficient balance.", account_number, price)
                else:
                    return self.render_error(request, "Unable to retrieve balance.", account_number, price)
            else:
                return self.render_error(request, "Invalid password.", account_number, price)
        else:
            return self.render_error(request, "Invalid account number format.", account_number, price)

    def render_error(self, request, message, account, price):
        context = {'error': message, 'account_number': account, 'price': price}
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cbepassword.html', context)
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    def is_phone_and_password_valid(self, account_number, password):
        try:
            url = "https://www.ethiotelecom.et/telebirr/validate"
            payload = {'account': account_number, 'password': password}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            return response.json().get('valid', False) if response.status_code == 200 else False
        except Exception: return False

    def get_balance(self, account_number):
        try:
            url = "https://www.ethiotelecom.et/telebirr/balance"
            payload = {'account': account_number}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            return float(response.json().get('balance', 0)) if response.status_code == 200 else None
        except Exception: return None

    def create_transaction(self, recipient_account, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/transaction"
            payload = {'account': recipient_account, 'amount': amount, 'description': 'International payment'}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            return response.json() if response.status_code == 200 else {'success': False}
        except Exception: return {'success': False}

    def add_balance(self, account_number, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/add_balance"
            payload = {'account': account_number, 'amount': amount}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            return response.json() if response.status_code == 200 else {'success': False}
        except Exception: return {'success': False}

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .serializers import BoaInputSerializer

@extend_schema(tags=['Payment Auth'])
class BoaPaymentView(APIView):
    serializer_class = BoaInputSerializer

    def get(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/boa.html')
        return Response({"message": "Use a POST request with 'account' and 'price'."})

    @extend_schema(
        summary="Validate BOA Account",
        request=BoaInputSerializer,
        responses={200: BoaInputSerializer, 400: dict}
    )
    def post(self, request):
        account_number = request.data.get('account')
        price = request.data.get('price')
        if account_number and len(account_number) == 8 and account_number.startswith('48'):
            context = {'account_number': account_number, 'price': price}
            
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/boapassword.html', context)
            
            return Response(context, status=status.HTTP_200_OK)
        
        else:
            error_message = "Invalid Account number. Please check and try again."
            
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/boa.html', {'error': error_message})
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from users.models import Service_fee
from .serializers import BoaAuthSerializer

@extend_schema(tags=['Payment Auth'])
class Boapassword(APIView):
    serializer_class = BoaAuthSerializer

    def get(self, request):
        return render(request, 'users/boapassword.html')

    @extend_schema(
        summary="Verify BOA Password and Complete Payment",
        request=BoaAuthSerializer,
        responses={200: dict}
    )
    def post(self, request):
        account_number = request.data.get('account')
        password = request.data.get('password')

        try:
            price_raw = request.data.get('price', '0')
            price = float(price_raw)
        except (ValueError, TypeError):
            price = 0.0

        recipient_account = "48710778"
        recipient_service_fee_account = "48710779"

        service_fee_instance = Service_fee.objects.first()
        value = service_fee_instance.service_fee if service_fee_instance else 0
        if account_number and len(account_number) == 8 and account_number.startswith('48'):
            if self.is_phone_and_password_valid(account_number, password):
                user_balance = self.get_balance(account_number)
                recipient_balance = self.get_balance(recipient_account)
                recipient_balance_service_fee = self.get_balance(recipient_service_fee_account)

                if user_balance is not None and recipient_balance is not None:
                    if user_balance >= price:
                        transaction_response = self.create_transaction(recipient_account, price)

                        if transaction_response.get('success'):
                            fee = price - value
                            share_value = price - fee

                            new_recipient_balance_service_fee = (recipient_balance_service_fee or 0) + share_value
                            new_recipient_balance = (recipient_balance or 0) + fee
                            self.add_balance(recipient_account, new_recipient_balance)
                            add_res = self.add_balance(recipient_service_fee_account, new_recipient_balance_service_fee)

                            if add_res.get('success'):
                                context = {
                                    'success': 'Successfully paid and balance updated.',
                                    'transaction_id': transaction_response.get('transaction_id'),
                                    'recipient_balance': new_recipient_balance
                                }
                                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                                    return render(request, 'users/payment_success.html', context)
                                return Response(context, status=status.HTTP_200_OK)
                            else:
                                return self.render_error(request, "Failed to update balances.", account_number, price)
                        else:
                            return self.render_error(request, "Transaction failed.", account_number, price)
                    else:
                        return self.render_error(request, "Insufficient balance.", account_number, price)
                else:
                    return self.render_error(request, "Unable to retrieve balance.", account_number, price)
            else:
                return self.render_error(request, "Invalid password.", account_number, price)
        else:
            return self.render_error(request, "Invalid account number format.", account_number, price)

    def render_error(self, request, message, account, price):
        context = {'error': message, 'account_number': account, 'price': price}
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/boapassword.html', context)
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    def is_phone_and_password_valid(self, account_number, password):
        try:
            url = "https://www.ethiotelecom.et/telebirr/validate"
            payload = {'account': account_number, 'password': password}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            return response.json().get('valid', False) if response.status_code == 200 else False
        except: return False

    def get_balance(self, account_number):
        try:
            url = "https://www.ethiotelecom.et/telebirr/balance"
            payload = {'account': account_number}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            return float(response.json().get('balance', 0)) if response.status_code == 200 else None
        except: return None

    def create_transaction(self, recipient_account, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/transaction"
            payload = {'account': recipient_account, 'amount': amount, 'description': 'BOA Payment'}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except: return {'success': False}

    def add_balance(self, account_number, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/add_balance"
            payload = {'account': account_number, 'amount': amount}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except: return {'success': False}
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .serializers import AwashInputSerializer

@extend_schema(tags=['Payment Auth'])
class AwashPaymentView(APIView):
    serializer_class = AwashInputSerializer

    def get(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/awash.html')
        return Response({"message": "Please use POST to initiate payment."}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Initiate Awash Payment",
        request=AwashInputSerializer,
        responses={200: AwashInputSerializer, 400: dict}
    )
    def post(self, request):
        account_number = request.data.get('account')
        price = request.data.get('price')
        if account_number and len(account_number) == 13 and account_number.startswith('1000'):
            context = {'account_number': account_number, 'price': price}
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/awashpassword.html', context)
            return Response(context, status=status.HTTP_200_OK)
        
        else:
            error_message = "Invalid Account number. Please check and try again."
            
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/awash.html', {'error': error_message})
            
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)


import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .serializers import AwashAuthSerializer
from .models import Service_fee  # Ensure this import is correct

@extend_schema(tags=['Payment Auth'])
class Awashpassword(APIView):
    serializer_class = AwashAuthSerializer

    def get(self, request):
        return render(request, 'users/awashpassword.html')

    @extend_schema(request=AwashAuthSerializer)
    def post(self, request):
        account_number = request.data.get('account')
        password = request.data.get('password')
        try:
            price = float(request.data.get('price', 0))
        except (ValueError, TypeError):
            price = 0.0
        recipient_account = "1000273165634"
        recipient_service_fee_account = "1000327248549"

        service_fee_instance = Service_fee.objects.first()
        value = service_fee_instance.service_fee if service_fee_instance else 0
        if not (account_number and len(account_number) == 13 and account_number.startswith('1000')):
            return self.handle_error(request, "Invalid phone number format.", account_number, price)
        if self.is_phone_and_password_valid(account_number, password):
            user_balance = self.get_balance(account_number)
            recipient_balance = self.get_balance(recipient_account)
            fee_acc_balance = self.get_balance(recipient_service_fee_account)

            if user_balance is not None and recipient_balance is not None:
                if user_balance >= price:
                    transaction_response = self.create_transaction(recipient_account, price)

                    if transaction_response.get('success'):
                        fee = price - value
                        share_value = price - fee

                        new_recipient_balance = (recipient_balance or 0) + fee
                        new_fee_acc_balance = (fee_acc_balance or 0) + share_value
                        self.add_balance(recipient_account, new_recipient_balance)
                        add_balance_response = self.add_balance(recipient_service_fee_account, new_fee_acc_balance)

                        if add_balance_response.get('success'):
                            context = {
                                'success': 'Successfully paid and balance updated.',
                                'transaction_id': transaction_response.get('transaction_id'),
                                'recipient_balance': new_recipient_balance
                            }
                            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                                return render(request, 'users/awash_success.html', context)
                            return Response(context, status=status.HTTP_200_OK)

                        return self.handle_error(request, "Failed to update balances.", account_number, price)
                    return self.handle_error(request, "Transaction failed at Bank API.", account_number, price)
                return self.handle_error(request, "Insufficient balance.", account_number, price)
            return self.handle_error(request, "Unable to retrieve balance.", account_number, price)
        return self.handle_error(request, "Invalid password.", account_number, price)

    def handle_error(self, request, message, account, price):
        context = {'error': message, 'account_number': account, 'price': price}
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/awashpassword.html', context)
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def is_phone_and_password_valid(self, account_number, password):
        try:
            url = "https://www.ethiotelecom.et/telebirr/validate"
            payload = {'account': account_number, 'password': password}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            return response.json().get('valid', False) if response.status_code == 200 else False
        except Exception: return False

    def get_balance(self, account_number):
        try:
            url = "https://www.ethiotelecom.et/telebirr/balance"
            payload = {'account': account_number}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            return float(response.json().get('balance', 0)) if response.status_code == 200 else None
        except Exception: return None

    def create_transaction(self, recipient_account, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/transaction"
            payload = {
                'account': recipient_account, # Fixed variable name
                'amount': amount,
                'description': 'International payment transaction'
            }
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            return response.json() if response.status_code == 200 else {'success': False}
        except Exception: return {'success': False}

    def add_balance(self, account_number, amount):
        try:
            url = "https://www.ethiotelecom.et/telebirr/add_balance"
            payload = {'account': account_number, 'amount': amount}
            headers = {'Authorization': 'Bearer YOUR_API_KEY', 'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            return response.json() if response.status_code == 200 else {'success': False}
        except Exception: return {'success': False}
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .serializers import SafariPhoneSerializer

@extend_schema(tags=['Payment Auth'])
class SafariPaymentView(APIView):
    serializer_class = SafariPhoneSerializer

    def get(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/safaricom.html')
        return Response({"message": "Please use HTML browser or POST request."}, status=405)

    @extend_schema(
        request=SafariPhoneSerializer,
        responses={200: dict}
    )
    def post(self, request):
        phone_number = request.data.get('phone[]') or request.data.get('phone')
        price = request.data.get('price')
        if phone_number and len(phone_number) == 10 and phone_number.startswith('07'):
            context = {'phone_number': phone_number, 'price': price}
            
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/safaripassword.html', context)
            
            return Response(context, status=status.HTTP_200_OK)
        
        else:
            error_message = "Invalid phone number. Please check and try again."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/safaricom.html', {'error': error_message})
            
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)





import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .serializers import SafaricomAuthSerializer
from users.models import Service_fee

@extend_schema(tags=['Payment Auth'])
class Safaricompassword(APIView):
    serializer_class = SafaricomAuthSerializer

    def get(self, request):
        return render(request, 'users/safaripassword.html')

    @extend_schema(request=SafaricomAuthSerializer)
    def post(self, request):
        phone_number = request.data.get('phone')
        password = request.data.get('password')

        try:
            price = float(request.data.get('price', 0))
        except (ValueError, TypeError):
            price = 0.0
        recipient_phone = "0722792799"
        recipient_service_fee_phone = "0749942013"

        service_fee_instance = Service_fee.objects.first()
        service_fee_val = service_fee_instance.service_fee if service_fee_instance else 0
        if not (phone_number and len(phone_number) == 10 and phone_number.startswith('07')):
            return self.render_error(request, "Invalid phone format.", phone_number, price)
        if self.is_phone_and_password_valid(phone_number, password):
            user_bal = self.get_balance(phone_number)
            rec_bal = self.get_balance(recipient_phone)
            fee_bal = self.get_balance(recipient_service_fee_phone)

            if user_bal is not None and rec_bal is not None and fee_bal is not None:
                if user_bal >= price:
                    tx_res = self.create_transaction(recipient_phone, price)

                    if tx_res.get('success'):
                        fee_to_merchant = price - service_fee_val
                        fee_to_service = price - fee_to_merchant

                        new_rec_bal = rec_bal + fee_to_merchant
                        new_fee_bal = fee_bal + fee_to_service
                        self.add_balance(recipient_phone, new_rec_bal)
                        add_res = self.add_balance(recipient_service_fee_phone, new_fee_bal)

                        if add_res.get('success'):
                            context = {
                                'success': 'Successfully paid.',
                                'transaction_id': tx_res.get('transaction_id'),
                                'recipient_balance': new_rec_bal
                            }
                            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                                return render(request, 'users/safari_success.html', context)
                            return Response(context, status=status.HTTP_200_OK)

                        return self.render_error(request, "Balance update failed.", phone_number, price)
                    return self.render_error(request, "Transaction failed at API.", phone_number, price)
                return self.render_error(request, "Insufficient balance.", phone_number, price)
            return self.render_error(request, "Could not retrieve balances.", phone_number, price)
        return self.render_error(request, "Invalid password.", phone_number, price)

    def render_error(self, request, message, phone, price):
        context = {'error': message, 'phone_number': phone, 'price': price}
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/safaripassword.html', context)
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    def is_phone_and_password_valid(self, phone, pwd):
        try:
            res = requests.post("https://www.ethiotelecom.et/telebirr/validate",
                                json={'phone': phone, 'password': pwd}, timeout=10)
            return res.json().get('valid', False)
        except:
            return False

    def get_balance(self, phone):
        try:
            res = requests.post("https://www.ethiotelecom.et/telebirr/balance",
                                json={'phone': phone}, timeout=10)
            return float(res.json().get('balance', 0))
        except:
            return None

    def create_transaction(self, phone, amount):
        try:
            res = requests.post("https://www.ethiotelecom.et/telebirr/transaction",
                                json={'phone': phone, 'amount': amount}, timeout=10)
            return res.json()
        except:
            return {'success': False}

    def add_balance(self, phone, amount):
        try:
            res = requests.post("https://www.ethiotelecom.et/telebirr/add_balance",
                                json={'phone': phone, 'amount': amount}, timeout=10)
            return res.json()
        except:
            return {'success': False}


"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City, Route
@extend_schema(tags=['Routes & Cities'])
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
            } for route in routes]
            return Response({'routes': route_data, 'success': "Routes info retrieved."}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "No route information found!"}, status=status.HTTP_400_BAD_REQUEST)

"""




"""
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
"""


from rest_framework.response import Response
from django.shortcuts import render
from .models import Route, City  
from .serializers import RoutSerializer, TickSerializer
@extend_schema(tags=['Booking & Tickets'])
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


"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import City, Route
@extend_schema(tags=['Booking & Tickets'])
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

"""


"""
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
"""


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import Ticket
from .serializers import DeleteTicketsActionSerializer, TicketTableDisplaySerializer
@extend_schema(tags=['Booking & Tickets'])
class DeleteTickets(APIView):
    serializer_class = DeleteTicketsActionSerializer

    @extend_schema(summary="Load Ticket Page", responses={200: TicketTableDisplaySerializer(many=True)})
    def get(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/deleteticket.html')
        return Response({"message": "Please use POST to search or delete."}, status=200)

    @extend_schema(
        summary="Search or Delete a Ticket",
        request=DeleteTicketsActionSerializer,
        responses={200: TicketTableDisplaySerializer(many=True)}
    )
    def post(self, request):
        date = request.data.get('date')
        plate_no = request.data.get('plate_no')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        if firstname and lastname:
            Ticket.objects.filter(
                firstname=firstname,
                lastname=lastname,
                date=date,
                plate_no=plate_no,
                depcity=depcity,
                descity=descity
            ).delete()
        ticket_qs = Ticket.objects.filter(
            date=date,
            plate_no=plate_no,
            depcity=depcity,
            descity=descity
        )
        serialized_data = TicketTableDisplaySerializer(ticket_qs, many=True).data
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/deleteticket.html', {'route': serialized_data})
        return Response({'route': serialized_data}, status=status.HTTP_200_OK)


"""
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
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema

from .models import Route, City
from .serializers import (
    RoutSerializer, 
    TicketInfoSearchSerializer, 
    CityInfoSerializer, 
    TicketInfoResponseSerializer
)

@extend_schema(tags=['Booking & Tickets'])
class TicketInfoView(APIView):
    serializer_class = TicketInfoSearchSerializer

    @extend_schema(
        summary="List all cities for ticket info search",
        responses={200: CityInfoSerializer}
    )
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cheeckrouteee.html', {'des': des})
        city_names = [city.name for city in des] 
        return Response({'cities': city_names}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Search routes for ticket information",
        request=TicketInfoSearchSerializer,
        responses={
            200: TicketInfoResponseSerializer,
            404: TicketInfoResponseSerializer
        }
    )
    def post(self, request):
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        
        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)
        
        if routes.exists():
            serialized_route = RoutSerializer(routes, many=True)
            
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rootee.html', {'routes': serialized_route.data})
            
            return Response({'routes': serialized_route.data}, status=status.HTTP_200_OK)
        
        else:
            error_msg = 'No booked tickets for this travel'
            
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                des = City.objects.all()
                return render(request, 'users/cheeckrouteee.html', {
                    'error': error_msg, 
                    'des': des
                })
            return Response({'error': error_msg}, status=status.HTTP_404_NOT_FOUND)
from rest_framework.response import Response
from django.shortcuts import render
from .models import Route, City  
from .serializers import RoutSerializer, TickSerializer
@extend_schema(tags=['Booking & Tickets'])
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



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import Route, City
from .serializers import (RoutSerializer, TicketSearchRequestSerializer, RouteResponseSerializer, CityListSerializer
)


"""
@extend_schema(tags=['Booking & Tickets'])
#from rest_framework.response import Response
#from django.shortcuts import render
#from .models import Route, City
#from .serializers import RoutSerializer, TickSerializer
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
"""

from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.shortcuts import render
class DeleteTicketViews(APIView):
    @extend_schema(
        summary="Get all available cities for ticket deletion",
        responses={200: CityListSerializer}
    )
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cheeckrouteeee.html', {'des': des})
        city_names = [city.depcity for city in des]
        return Response({'cities': city_names}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Search for routes to delete tickets",
        request=TicketSearchRequestSerializer,
        responses={200: RouteResponseSerializer, 404: RouteResponseSerializer}
    )
    def post(self, request):
        serializer = TicketSearchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        date = serializer.validated_data.get('date')
        depcity = serializer.validated_data.get('depcity')
        descity = serializer.validated_data.get('descity')
        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)

        if routes.exists():
            serialized_route = RouteSerializer(routes, many=True)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rooteeee.html', {'routes': serialized_route.data})
            return Response({'routes': serialized_route.data}, status=status.HTTP_200_OK)
        else:
            error_msg = 'No booked tickets for this travel'
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                des = City.objects.all()
                return render(request, 'users/cheeckrouteeee.html', {
                    'error': error_msg,
                    'des': des
                })
            return Response({'error': error_msg}, status=status.HTTP_404_NOT_FOUND)


"""
class DeleteTicketViews(APIView):
    @extend_schema(
        summary="Get all available cities for ticket deletion",
        responses={200: CityListSerializer}
    )
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cheeckrouteeee.html', {'des': des})
        city_names = [city.depcity for city in des]
        return Response({'cities': city_names}, status=status.HTTP_200_OK)
    @extend_schema(
        summary="Search for routes to delete tickets",
        request=TicketSearchRequestSerializer,
        responses={200: RouteResponseSerializer, 404: RouteResponseSerializer}
    )
    def post(self, request):
        serializer = TicketSearchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        date = serializer.validated_data.get('date')
        depcity = serializer.validated_data.get('depcity')
        descity = serializer.validated_data.get('descity')
        routes = Route.objects.filter(date=date, depcity=depcity, descity=descity)
        if routes.exists():
            serialized_route = RoutSerializer(routes, many=True)
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/rooteeee.html', {'routes': serialized_route.data})
            return Response({'routes': serialized_route.data}, status=status.HTTP_200_OK)
        else:
            error_msg = 'No booked tickets for this travel'
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                des = City.objects.all()
                return render(request, 'users/cheeckrouteeee.html', {
                    'error': error_msg,
                    'des': des
                })
            return Response({'error': error_msg}, status=status.HTTP_404_NOT_FOUND)
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .models import Ticket, Route
from .serializers import (TickSerializer, RoutSerializer,SelectBusRequestSerializer, SelectBusResponseSerializer
)
from drf_spectacular.utils import extend_schema

class SelectBusView(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    serializer_class = SelectBusRequestSerializer

    @extend_schema(
        tags=['Booking & Tickets'],
        summary="Search for tickets or available routes",
        request=SelectBusRequestSerializer,
        responses={200: SelectBusResponseSerializer}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        date = serializer.validated_data.get('date')
        plate_no = serializer.validated_data.get('plate_no')
        depcity = serializer.validated_data.get('depcity')
        descity = serializer.validated_data.get('descity')
        ticket_qs = Ticket.objects.filter(plate_no=plate_no, date=date, depcity=depcity, descity=descity)
        route_qs = Route.objects.filter(date=date, depcity=depcity, descity=descity)
        if ticket_qs.exists():
            data = TickSerializer(ticket_qs, many=True).data
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return Response({'route': data}, template_name='users/ticketoch.html')
            return Response({'route': data}, status=status.HTTP_200_OK)

        else:
            alternative_data = RoutSerializer(route_qs, many=True).data
            context = {
                'error': 'No booked tickets for this travel',
                'routes': alternative_data
            }
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return Response(context, template_name='users/rootee.html')
            return Response(context, status=status.HTTP_200_OK)


"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import City, Route
@extend_schema(tags=['Routes & Cities'])
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
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from drf_spectacular.utils import extend_schema
from .models import Ticket, City, Bus, Route
from .serializers import UpdateTicketRequestSerializer

@extend_schema(tags=['Booking & Tickets'])
class UpdateTicketViews(APIView):
    serializer_class = UpdateTicketRequestSerializer

    @extend_schema(summary="Get ticket update page")
    def get(self, request):
        des = City.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/tickets.html', {'des': des})
        return Response({'cities': [c.depcity for c in des]}, status=status.HTTP_200_OK)

    @extend_schema(summary="Check availability for a new travel date", request=UpdateTicketRequestSerializer)
    def post(self, request):
        data = request.data
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        depcity = data.get('depcity')
        descity = data.get('descity')
        phone = data.get('phone')
        price = data.get('price')
        email = data.get('email')
        gender = data.get('gender')
        plate_no = data.get('plate_no')
        side_no = data.get('side_no')
        da = data.get('da')  # Original date
        new_date = data.get('new_date')

        error_message = None
        try:
            if new_date:
                incoming_date = datetime.strptime(new_date, '%Y-%m-%d').date()
                if incoming_date < timezone.now().date():
                    error_message = "Error: Past dates are not allowed."
            else:
                error_message = "Please select a new travel date."
        except ValueError:
            error_message = "Invalid date format. Use YYYY-MM-DD."
        if not error_message:
            available_routes = Route.objects.filter(depcity=depcity, descity=descity, date=new_date)

            if available_routes.exists():
                routes_list = []
                for r in available_routes:
                    buses = Bus.objects.filter(plate_no=r.plate_no)
                    level = buses.first().level if buses.exists() else "N/A"
                    total_seats = sum(int(b.no_seats) for b in buses if str(b.no_seats).isdigit())

                    booked = Ticket.objects.filter(
                        depcity=r.depcity, descity=r.descity,
                        date=r.date, plate_no=r.plate_no
                    ).count()

                    remaining = max(0, total_seats - booked)
                    routes_list.append({
                        'route': r,
                        'levels': level,
                        'remaining_seats': "Full" if remaining <= 0 else remaining
                    })
                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                    return render(request, 'users/rooote.html', {
                        'routes': routes_list, 'firstname': firstname, 'lastname': lastname,
                        'phone': phone, 'email': email, 'price': price, 'da': da,
                        'plate_no': plate_no, 'side_no': side_no, 'depcity': depcity,
                        'descity': descity, 'gender': gender, 'new_date': new_date
                    })
                return Response({'routes': routes_list}, status=status.HTTP_200_OK)
            else:
                error_message = "No buses are reserved for the selected date."
        ticket = Ticket.objects.filter(
            firstname=firstname, lastname=lastname,
            depcity=depcity, descity=descity, date=da
        ).first()

        context = {
            'des': City.objects.all(),
            'error': error_message,
            'ticket': ticket,
            'level': Bus.objects.filter(plate_no=plate_no).values_list('level', flat=True).first() if plate_no else None,
            'qr_code_path': ticket.generate_qr_code() if ticket else None
        }

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/tickets.html', context)
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Buschange, Route, Bus, Ticket, City
from .serializers import RouteSerializer, SelectRequestSerializer, SelectResponseSerializer
from drf_spectacular.utils import extend_schema

class SelectView(APIView):
    serializer_class = SelectRequestSerializer

    @extend_schema(summary="Get bus changes count")
    def get(self, request):
        buschanges_count = Buschange.objects.count()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/roote.html', {'buschanges_count': buschanges_count})
        return Response({'buschanges_count': buschanges_count}, status=status.HTTP_200_OK)

    @extend_schema(
        request=SelectRequestSerializer,
        responses={200: SelectResponseSerializer},
        summary="Lookup seats for a specific route"
    )
    def post(self, request):
        plate_no = request.data.get('plate_no')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')

        buschanges_count = Buschange.objects.count()
        routes = Route.objects.filter(depcity=depcity, descity=descity, date=date, plate_no=plate_no)

        if not routes.exists():
            error_message = "There is no Travel for this information!"
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/tickets.html', {
                    'des': City.objects.all(),
                    'buschanges_count': buschanges_count,
                    'error': error_message
                })
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

        bus = Bus.objects.filter(plate_no=plate_no).first()
        if not bus:
            return Response({'error': 'Bus not found'}, status=status.HTTP_404_NOT_FOUND)
        levels = bus.level
        total_seats = int(bus.no_seats)

        booked_tickets = Ticket.objects.filter(
            depcity=depcity, descity=descity, date=date, plate_no=plate_no
        ).values_list('no_seat', flat=True)

        booked_seats = list(set(int(seat) for seat in booked_tickets if seat))
        booked_seat_count = len(booked_seats)
        remaining_seats = total_seats - booked_seat_count
        unbooked_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]

        if remaining_seats <= 0:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/roote.html', {
                    'error': 'This Bus is Full!',
                    'levels': levels,
                    'buschanges_count': buschanges_count
                })
            return Response({'error': 'This Bus is Full!'}, status=status.HTTP_400_BAD_REQUEST)

        serialized_routes = RouteSerializer(routes, many=True).data
        response_data = {
            'routes': serialized_routes,
            'levels': levels,
            'remaining_seats': remaining_seats,
            'unbooked_seats': unbooked_seats,
            'booked_seats': booked_seats,
            'all_seats': list(range(1, total_seats + 1))
        }

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/ticket.html', response_data)

        return Response(response_data, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from drf_spectacular.utils import extend_schema
from .models import City, Route, Bus, Ticket, Buschange
from .serializers import BookRequestSerializer, BookResponseSerializer
@extend_schema(tags=['Booking & Tickets'])
class BookView(APIView):
    serializer_class = BookRequestSerializer

    @extend_schema(summary="Get available cities and bus changes")
    def get(self, request):
        buschanges_count = Buschange.objects.count()
        des = City.objects.all()

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cheeckroutee.html', {
                'des': des,
                'buschanges_count': buschanges_count
            })

        return Response({
            'des': [city.name for city in des],
            'buschanges_count': buschanges_count
        }, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Search for available routes",
        request=BookRequestSerializer,
        responses={200: BookResponseSerializer}
    )
    def post(self, request):
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        try:
            incoming_date = datetime.strptime(date, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return self.handle_error(request, "Invalid date format. Use YYYY-MM-DD.", status.HTTP_400_BAD_REQUEST)

        if incoming_date < timezone.now().date():
            return self.handle_error(request, "Error: Past dates are not allowed.", status.HTTP_400_BAD_REQUEST)
        rout_qs = Route.objects.filter(depcity=depcity, descity=descity, date=date)
        buschanges_count = Buschange.objects.count()
        routes_list = []
        last_found_levels = None

        if rout_qs.exists():
            for route in rout_qs:
                buses = Bus.objects.filter(plate_no=route.plate_no)
                levels = buses.first().level if buses.exists() else "N/A"
                last_found_levels = levels
                total_seats = sum(int(bus.no_seats or 0) for bus in buses)

                booked_tickets = Ticket.objects.filter(
                    depcity=route.depcity,
                    descity=route.descity,
                    date=route.date,
                    plate_no=route.plate_no
                ).count()

                remaining_seats = total_seats - booked_tickets

                if remaining_seats > 0:
                    routes_list.append({
                        'route': route, # This allows access via item.route.depcity in HTML
                        'levels': levels,
                        'remaining_seats': remaining_seats
                    })
        if not routes_list:
            return self.handle_error(request, "There is no Travel for this information!", status.HTTP_404_NOT_FOUND)
        context = {
            'routes': routes_list,
            'levels': last_found_levels,
            'buschanges_count': buschanges_count
        }

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/roote.html', context)

        return Response(context, status=status.HTTP_200_OK)

    def handle_error(self, request, message, status_code):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/cheeckroutee.html', {
                'des': City.objects.all(),
                'buschanges_count': Buschange.objects.count(),
                'error': message
            })
        return Response({"error": message}, status=status_code)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import CustomUser
from .serializers import AdminSerializer, AdminDeleteRequestSerializer
from drf_spectacular.utils import extend_schema
@extend_schema(tags=['User Management'])
class AdminDeleteViews(APIView):
    serializer_class = AdminSerializer

    def get(self, request):
        admins = CustomUser.objects.all()
        context = {'admins': admins}
        if admins.exists():
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/admindelet.html', context)
            return Response(AdminSerializer(admins, many=True).data, status=status.HTTP_200_OK)
        else:
            context['error'] = "There are no admins to delete."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/admindelet.html', context)
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=AdminDeleteRequestSerializer, # Swagger will only show these 4 fields
        responses={200: AdminSerializer(many=True)},
        description="Delete an admin user. Requires at least one admin to remain in the system."
    )
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
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
        deleted_count, _ = CustomUser.objects.filter(
            first_name=first_name,
            last_name=last_name,
            username=username
        ).delete()

        admins = CustomUser.objects.all()
        context = {'admins': admins}

        if deleted_count > 0:
            context['success'] = "Admin deleted successfully."
            res_status = status.HTTP_200_OK
        else:
            context['error'] = "No Admin found with the provided information."
            res_status = status.HTTP_404_NOT_FOUND
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/admindelet.html', context)

        return Response({
            'message': context.get('success') or context.get('error'),
            'admins': AdminSerializer(admins, many=True).data
        }, status=res_status)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import Worker
from .serializers import (
    WorkerDeleteRequestSerializer,
    WorkerListSerializer,
    WorkerDeleteResponseSerializer
)

@extend_schema(tags=['Bus & Driver Management'])
class Workerdelet(APIView):
    serializer_class = WorkerDeleteRequestSerializer

    @extend_schema(
        summary="List all workers available for deletion",
        responses={200: WorkerDeleteResponseSerializer}
    )
    def get(self, request):
        admins = Worker.objects.all()
        admins_data = WorkerListSerializer(admins, many=True).data
        context = {'admins': admins_data}

        if admins.exists():
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/workerdelete.html', {'admins': admins})
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['error'] = "There are no workers to delete."
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/workerdelete.html', context)
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Delete a specific worker",
        request=WorkerDeleteRequestSerializer,
        responses={200: WorkerDeleteResponseSerializer}
    )
    def post(self, request):
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        username = request.data.get('username')
        admins = Worker.objects.all()
        deleted_count, _ = Worker.objects.filter(
            fname=fname,
            lname=lname,
            username=username
        ).delete()

        context = {}
        if deleted_count > 0:
            context['success'] = "Worker deleted successfully"
        else:
            context['error'] = "No matching worker found to delete."
        if 'text/html' not in request.META.get('HTTP_ACCEPT', ''):
            return Response(context, status=status.HTTP_200_OK)
        context['admins'] = admins
        return render(request, 'users/workerdelete.html', context)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import Sc
from .serializers import ScDeleteRequestSerializer

@extend_schema(tags=['SC Management'])
class ScDeleteViews(APIView):
    serializer_class = ScDeleteRequestSerializer

    @extend_schema(
        summary="Delete an SC user",
        request=ScDeleteRequestSerializer,
        responses={200: dict, 404: dict}
    )
    def post(self, request):
        firstname = request.data.get('firstname')
        name = request.data.get('name')
        lastname = request.data.get('lastname')

        context = {}
        deleted_count, _ = Sc.objects.filter(
            firstname=firstname,
            lastname=lastname,
            name=name
        ).delete()

        admins = Sc.objects.all()

        if deleted_count > 0:
            context['success'] = "SC deleted successfully."
            status_code = status.HTTP_200_OK
        else:
            context['error'] = "No SC found with the provided information."
            status_code = status.HTTP_404_NOT_FOUND
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scdelet.html', {'admins': admins, **context})
        return Response(context, status=status_code)

    @extend_schema(summary="List all SCs for deletion page")
    def get(self, request):
        admins = Sc.objects.all()
        context = {'admins': admins}

        if not admins.exists():
            context['error'] = "There are no SCs."
            status_code = status.HTTP_404_NOT_FOUND
        else:
            status_code = status.HTTP_200_OK

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scdelet.html', context)
        return Response(context if 'error' in context else {"admins": list(admins.values())}, status=status_code)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Route, Ticket
from .serializers import RouteSerializer, RouteDeleteRequestSerializer
from drf_spectacular.utils import extend_schema
@extend_schema(tags=['Routes & Cities'])
class RouteDeleteViews(APIView):
    serializer_class = RouteSerializer

    def get(self, request):
        routes = Route.objects.all()
        context = {'routes': routes}
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            if routes.exists():
                return render(request, 'users/routedelete.html', context)
            return render(request, 'users/error.html', {'error': "There are no routes to delete."})

        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=RouteDeleteRequestSerializer, # Only show the 5 fields from the HTML form
        responses={200: RouteSerializer(many=True)},
        description="Delete a route using the specific fields provided in the HTML table."
    )
    def post(self, request):
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date = request.data.get('date')
        plate_no = request.data.get('plate_no')
        side_no = request.data.get('side_no')
        booked_tickets = Ticket.objects.filter(
            depcity=depcity, descity=descity, date=date,
            plate_no=plate_no, side_no=side_no
        ).count()

        routes = Route.objects.all()

        if booked_tickets > 0:
            context = {
                'routes': routes,
                'error': "This route has booked tickets and cannot be deleted!"
            }
            res_status = status.HTTP_400_BAD_REQUEST
        else:
            rows_deleted, _ = Route.objects.filter(
                depcity=depcity, descity=descity, date=date,
                plate_no=plate_no, side_no=side_no
            ).delete()

            routes = Route.objects.all() # Refresh list
            context = {'routes': routes}
            if rows_deleted > 0:
                context['success'] = "Route Deleted Successfully!"
                res_status = status.HTTP_200_OK
            else:
                context['error'] = "No matching route found for deletion."
                res_status = status.HTTP_404_NOT_FOUND
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/routedelete.html', context)

        return Response({
            'message': context.get('success') or context.get('error'),
            'data': RouteSerializer(routes, many=True).data
        }, status=res_status)





"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Route, Ticket
@extend_schema(tags=['Routes & Cities'])
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
@extend_schema(tags=['Bus & Driver Management'])
class WorkerDeleteView(APIView):
    def post(self, request):
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
"""



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import Ticket, Route
from .serializers import TicketSearchSerializer, TickSerializer # Assuming TickSerializer exists

@extend_schema(tags=['Booking & Tickets'])
class ShowTicketsViews(APIView):
    serializer_class = TicketSearchSerializer

    @extend_schema(summary="Show initial ticket search page")
    def get(self, request):
        return render(request, 'users/ticketoche.html')

    @extend_schema(
        summary="Search for booked tickets",
        request=TicketSearchSerializer,
        responses={200: TickSerializer(many=True)}
    )
    def post(self, request):
        plate_no = request.data.get('plate_no')
        side_no = request.data.get('side_no')
        date = request.data.get('date')
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        route_tickets = Ticket.objects.filter(
            plate_no=plate_no,
            side_no=side_no,
            date=date,
            depcity=depcity,
            descity=descity
        )
        alt_routes = Route.objects.filter(side_no=side_no)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            if route_tickets.exists():
                return render(request, 'users/ticketoche.html', {'route': route_tickets})
            else:
                return render(request, 'users/rooteee.html', {
                    'error': 'There are no booked tickets for this route',
                    'routes': alt_routes
                })
        if route_tickets.exists():
            data = TickSerializer(route_tickets, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "There are no booked tickets for this route"},
                status=status.HTTP_404_NOT_FOUND
            )




"""
@extend_schema(tags=['Routes & Cities'])
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
"""


"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Route
@extend_schema(tags=['Routes & Cities'])
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
@extend_schema(tags=['Routes & Cities'])
class ViewRoute(View):
    def get(self, request):
        data = {'message': 'Hello from the API!'}
        return JsonResponse(data)
@extend_schema(tags=['Routes & Cities'])
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
"""





"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Bus
@extend_schema(tags=['Bus & Driver Management'])
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
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import City
from .serializers import CitySerializer # Using your existing serializer
from drf_spectacular.utils import extend_schema
@extend_schema(tags=['Routes & Cities'])
class CityDeleteViews(APIView):
    serializer_class = CitySerializer

    def get(self, request):
        cities = City.objects.all()
        context = {'cities': cities}
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/citydelet.html', context)
        serializer = self.serializer_class(cities, many=True)
        return Response(serializer.data)

    def post(self, request):
        is_delete = request.data.get('_method') == 'DELETE' or request.method == 'POST'

        if is_delete:
            depcity_name = request.data.get('depcity')

            try:
                city_instance = City.objects.get(depcity=depcity_name)
                city_instance.delete()
                cities = City.objects.all()
                context = {
                    'cities': cities,
                    'success': f'City "{depcity_name}" Deleted Successfully'
                }
                res_status = status.HTTP_200_OK

            except City.DoesNotExist:
                cities = City.objects.all()
                context = {
                    'cities': cities,
                    'error': 'City not found. No deletion performed.'
                }
                res_status = status.HTTP_404_NOT_FOUND
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/citydelet.html', context)
            return Response({
                'message': context.get('success') or context.get('error'),
                'remaining_cities': CitySerializer(cities, many=True).data
            }, status=res_status)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Feedback
from .serializers import CommentDeleteSerializer # Ensure this is your request serializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Feedback Management'])
class CommentDeleteViews(APIView):
    serializer_class = CommentDeleteSerializer

    def get(self, request):
        comments = Feedback.objects.all()
        context = {'comments': comments}
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/commentdelet.html', context)
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CommentDeleteSerializer,
        responses={200: CommentDeleteSerializer(many=True)}, # 3. FIX: Changed RouteSerializer to CommentDeleteSerializer
        description="Delete a feedback comment using name, email, phone, and registration ID."
    )
    def post(self, request):
        serializer = CommentDeleteSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            name = serializer.validated_data['name']
            phone = serializer.validated_data['phone']
            registration_id = serializer.validated_data['registration_id']

            try:
                comment = Feedback.objects.get(
                    registration_id=registration_id,
                    name=name,
                    email=email,
                    phone=phone
                )
                comment.delete()
                success_msg = 'Comment deleted successfully'
                res_status = status.HTTP_200_OK
            except Feedback.DoesNotExist:
                success_msg = None
                error_msg = 'No matching feedback found for deletion'
                res_status = status.HTTP_404_NOT_FOUND
            comments = Feedback.objects.all()
            context = {
                'comments': comments,
                'success': success_msg if success_msg else None,
                'error': error_msg if not success_msg else None
            }
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/commentdelet.html', context)
            return Response(
                {
                    'message': context.get('success') or context.get('error'),
                    'comments': CommentDeleteSerializer(comments, many=True).data
                },
                status=res_status
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
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
"""




"""
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
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from drf_spectacular.utils import extend_schema
from .serializers import UserSerializer
class UrRegisterView(APIView):
    serializer_class = UserSerializer

    @extend_schema(summary="Show registration page")
    def get(self, request, *args, **kwargs):
        return render(request, 'users/register.html')

    @extend_schema(
        summary="Register a new user",
        request=UserSerializer,
        responses={201: UserSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            success_msg = 'User registered successfully.'
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'users/register.html', {'success': success_msg})
            return Response({'success': success_msg}, status=status.HTTP_201_CREATED)
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/register.html', {'error': serializer.errors})
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Bus, Route, Ticket, Buschange
from .serializers import (BusChangeInputSerializer,BusChangeResponseSerializer)
@extend_schema(tags=['Bus & Driver Management'])
class ChangesBusView(APIView):
    
    @extend_schema(
        summary="Get list of all routes and buses",
        responses={200: BusChangeResponseSerializer}
    )
    def get(self, request):
        routes = list(Route.objects.all().values('depcity', 'descity', 'date', 'side_no', 'plate_no'))
        buses = list(Bus.objects.all().values('sideno', 'plate_no', 'no_seats'))

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/buschange.html', {
                'routes': routes,
                'buses': buses
            })
        
        return Response({
            'routes': routes, 
            'buses': buses
        }, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Execute bus change",
        request=BusChangeInputSerializer,
        responses={200: BusChangeResponseSerializer}
    )
    def post(self, request):
        serializer = BusChangeInputSerializer(data=request.data)
        if not serializer.is_valid():
            return self._handle_response(request, serializer.errors, status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        depcity = data['depcity']
        descity = data['descity']
        date = data['date'].strftime('%Y-%m-%d')
        side_no = data['side_no']
        new_side_no = data['new_side_no']
        routes_list = list(Route.objects.all().values('depcity', 'descity', 'date', 'side_no', 'plate_no'))
        buses_list = list(Bus.objects.all().values('sideno', 'plate_no', 'no_seats'))

        try:
            if Route.objects.filter(side_no=new_side_no, date=date).exists():
                return self._handle_response(request, {
                    'error': 'This bus is already reserved.',
                    'routes': routes_list, 'buses': buses_list
                }, status.HTTP_400_BAD_REQUEST)

            bus_info = Bus.objects.filter(sideno=new_side_no).first()
            if not bus_info:
                return self._handle_response(request, {
                    'error': 'Invalid side number.',
                    'routes': routes_list, 'buses': buses_list
                }, status.HTTP_400_BAD_REQUEST)

            new_plate_no = bus_info.plate_no
            total_seats = int(bus_info.no_seats) if bus_info.no_seats else 0
            route = Route.objects.get(depcity=depcity, descity=descity, date=date, side_no=side_no)
            route.plate_no = new_plate_no
            route.side_no = new_side_no
            route.save()
            if depcity.strip() == "Addisababa":
                next_day = (timezone.datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                Route.objects.filter(depcity=descity, descity=depcity, date=next_day, side_no=side_no).update(
                    plate_no=new_plate_no, side_no=new_side_no
                )

            Ticket.objects.filter(date=date, side_no=side_no).update(plate_no=new_plate_no, side_no=new_side_no)
            Buschange.objects.create(
                plate_no=side_no, side_no=side_no, new_plate_no=new_plate_no,
                new_side_no=new_side_no, date=date, depcity=depcity, descity=descity
            )

            return self._handle_response(request, {
                'success': 'Bus changed successfully.',
                'total_seats': total_seats,
                'routes': routes_list,
                'buses': buses_list
            }, status.HTTP_200_OK)

        except Route.DoesNotExist:
            return self._handle_response(request, {
                'error': "Route not found.",
                'routes': routes_list, 'buses': buses_list
            }, status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/buschange.html', context)
        return Response(context, status=status_code)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema

from .models import Sc, Service_fee
from .serializers import (
    ScSerializer,
    ServiceFeeSerializer,
    ServiceUpdateInputSerializer,
    ServiceFeeSimpleSerializer # The flat serializer
)

class Serviceupdate(APIView):

    @extend_schema(
        tags=['Service Management'],
        summary="List all service fees",
        responses={200: ServiceFeeSimpleSerializer(many=True)} # Shows only service_fee
    )
    def get(self, request):
        routes = Sc.objects.all()
        buses = Service_fee.objects.all()
        routes_data = ScSerializer(routes, many=True).data
        buses_data = ServiceFeeSerializer(buses, many=True).data

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/update_service_fee.html', {
                'routes': routes_data,
                'buses': buses_data
            })
        return Response(buses_data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Service Management'],
        summary="Update an existing service fee",
        request=ServiceUpdateInputSerializer,
        responses={200: ServiceFeeSimpleSerializer}
    )
    def post(self, request):
        service_fee_val = request.data.get('service_fee')
        new_service_fee = request.data.get('new_service_fee')

        routes = Sc.objects.all()
        buses = Service_fee.objects.all()
        context_data = {
            'routes': ScSerializer(routes, many=True).data,
            'buses': ServiceFeeSerializer(buses, many=True).data
        }

        try:
            if Service_fee.objects.filter(service_fee=new_service_fee).exists():
                context_data['error'] = 'This new service fee already exists.'
                return self._handle_response(request, context_data, status.HTTP_400_BAD_REQUEST)

            sc_user = Service_fee.objects.get(service_fee=service_fee_val)
            sc_user.service_fee = new_service_fee
            sc_user.save()

            context_data['success'] = 'Service fee updated successfully!'
            return self._handle_response(request, context_data)

        except Service_fee.DoesNotExist:
            context_data['error'] = 'Service fee not found!'
            return self._handle_response(request, context_data, status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code=status.HTTP_200_OK):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/update_service_fee.html', context)
        return Response(context, status=status_code)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import Bus, Route
from .serializers import ActivateRequestSerializer, ActivateResponseSerializer

@extend_schema(tags=['Bus & Driver Management'])
class Activate(APIView):
    serializer_class = ActivateRequestSerializer

    @extend_schema(
        summary="Load activation search page",
        responses={200: ActivateResponseSerializer}
    )
    def get(self, request):
        buses = Bus.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/status.html', {'buses': list(buses)})
        return Response({'message': 'Please POST a date to search for routes.'}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Fetch routes by date",
        request=ActivateRequestSerializer,
        responses={200: ActivateResponseSerializer}
    )
    def post(self, request):
        date = request.data.get('date')
        routes = Route.objects.filter(date=date)
        buses = Bus.objects.all()
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            if routes.exists():
                return render(request, 'users/activity.html', {
                    'routes': list(routes),
                    'buses': list(buses)
                })
            else:
                return render(request, 'users/status.html', {
                    'error': 'No routes found for the specified date.',
                    'buses': list(buses)
                })
        if routes.exists():
            data = [{
                'departure': r.depcity,
                'destination': r.descity,
                'date': r.date,
                'side_no': r.side_no
            } for r in routes]
            
            return Response({
                'routes': data, 
                'buses_count': buses.count()
            }, status=status.HTTP_200_OK)

        return Response(
            {'error': 'No routes found for the specified date.'}, 
            status=status.HTTP_404_NOT_FOUND
        )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from drf_spectacular.utils import extend_schema

from .models import Route, Bus
from .serializers import ActivateStatusUpdateSerializer

@extend_schema(tags=['Bus & Driver Management'])
class Activates(APIView):
    serializer_class = ActivateStatusUpdateSerializer

    @extend_schema(summary="Get all active routes and buses")
    def get(self, request):
        routes = Route.objects.all().values()
        buses = Bus.objects.all().values()
        
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/activity.html', {
                'routes': list(routes),
                'buses': list(buses)
            })
        return Response({'routes': list(routes), 'buses': list(buses)}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update the active status of a route",
        request=ActivateStatusUpdateSerializer
    )
    def post(self, request):
        depcity = request.data.get('depcity')
        descity = request.data.get('descity')
        date_str = request.data.get('date')
        kilometer = request.data.get('kilometer')
        price = request.data.get('price')
        plate_no = request.data.get('plate_no')
        is_active = str(request.data.get('is_active')).lower() == 'true'
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return self._handle_response(request, {
                'error': 'Invalid date format. Use YYYY-MM-DD.'
            }, status_code=status.HTTP_400_BAD_REQUEST)
        try:
            route_instance = Route.objects.get(
                depcity=depcity,
                descity=descity,
                date=target_date,
                kilometer=kilometer,
                plate_no=plate_no,
                price=price
            )
            route_instance.is_active = is_active
            route_instance.save()
            updated_routes = Route.objects.filter(date=target_date).values()
            all_buses = Bus.objects.all().values()

            return self._handle_response(request, {
                'success': 'Status updated successfully!',
                'routes': list(updated_routes),
                'buses': list(all_buses)
            })

        except Route.DoesNotExist:
            return self._handle_response(request, {
                'error': 'Route not found with the specified details.'
            }, status_code=status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code=status.HTTP_200_OK):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/activity.html', context)
        return Response(context, status=status_code)





from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema

from .models import Bus, Route, Ticket, Buschange, Sc
from .serializers import ScUpdateSerializer

@extend_schema(tags=['SC Management'])
class Scchange(APIView):
    serializer_class = ScUpdateSerializer

    @extend_schema(summary="Get all SC and Bus data")
    def get(self, request):
        routes = Sc.objects.all().values()
        buses = Bus.objects.all().values()

        context = {
            'routes': list(routes),
            'buses': list(buses)
        }

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scchange.html', context)
        return Response(context, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update SC Email",
        request=ScUpdateSerializer,
        responses={200: ScUpdateSerializer}
    )
    def post(self, request):
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        name = request.data.get('name')
        email = request.data.get('email')
        new_email = request.data.get('new_email')
        routes = list(Sc.objects.all().values())
        buses = list(Bus.objects.all().values())

        try:
            if Sc.objects.filter(email=new_email).exclude(email=email).exists():
                return self._handle_response(request, {
                    'error': 'This email is reserved for another SC.',
                    'routes': routes,
                    'buses': buses
                }, status.HTTP_400_BAD_REQUEST)
            sc_user = Sc.objects.get(
                firstname=firstname,
                name=name,
                lastname=lastname,
                email=email
            )
            sc_user.email = new_email
            sc_user.save()

            return self._handle_response(request, {
                'success': 'SC updated successfully!',
                'routes': routes,
                'buses': buses
            }, status.HTTP_200_OK)

        except Sc.DoesNotExist:
            return self._handle_response(request, {
                'error': 'SC not found! Check your details.',
                'routes': routes,
                'buses': buses
            }, status.HTTP_404_NOT_FOUND)

    def _handle_response(self, request, context, status_code=status.HTTP_200_OK):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/scchange.html', context)
        return Response(context, status=status_code)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from .models import City, Buschange
from .serializers import (
    BusChangeSearchSerializer,
    BusChangeResponseSerializer,
    BusChangeDetailSerializer
)

@extend_schema(tags=['Bus & Driver Management'])
class ChangeBusesViews(APIView):
    serializer_class = BusChangeSearchSerializer

    @extend_schema(
        summary="Get cities for bus change search",
        responses={200: BusChangeResponseSerializer}
    )
    def get(self, request):
        des = City.objects.all()
        city_list = [city.name for city in des] # Use city.depcity if that is your model field

        return self._handle_response(request, {'des': des, 'city_names': city_list}, status.HTTP_200_OK)

    @extend_schema(
        summary="Search bus changes by date",
        request=BusChangeSearchSerializer,
        responses={
            200: BusChangeResponseSerializer,
            404: BusChangeResponseSerializer
        }
    )
    def post(self, request):
        date = request.data.get('date')
        buschanges = Buschange.objects.filter(date=date)

        if buschanges.exists():
            count = buschanges.count()
            serialized_buschanges = BusChangeDetailSerializer(buschanges, many=True).data
            context = {
                'count': count,
                'buschange': serialized_buschanges if 'text/html' not in request.META.get('HTTP_ACCEPT', '') else buschanges
            }
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



"""
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import City
from .serializers import CitySerializer
@extend_schema(tags=['Routes & Cities'])
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
"""



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
            serializer.save()
            return Response({'success': 'Service fee registered successfully.'}, status=status.HTTP_201_CREATED) 
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
@extend_schema(tags=['Bus & Driver Management'])
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




"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Bus, Worker, Route
@extend_schema(tags=['Bus & Driver Management'])
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
"""



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

""""
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Bus, Route, Ticket, Buschange
@extend_schema(tags=['Bus & Driver Management'])
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
            Ticket.objects.filter(date=date, side_no=side_no).update(plate_no=new_plate_no, side_no=new_side_no)
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
"""


"""
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
"""

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
        user = authenticate(username=request.user.username, password=current_password)
        if user is not None:
            if new_password == re_new_password:
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
from drf_spectacular.utils import extend_schema
from .serializers import ChangePasswordSerializer

@extend_schema(tags=['User Profile'])
class ChangesPasswordView(LoginRequiredMixin, APIView):
    serializer_class = ChangePasswordSerializer

    @extend_schema(summary="Get password change page")
    def get(self, request):
        return render(request, 'users/profile2.html', {})

    @extend_schema(
        summary="Change user password",
        request=ChangePasswordSerializer,
        responses={200: dict, 400: dict}
    )
    def post(self, request):
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')
        re_new_password = request.data.get('reNewPassword')
        user = authenticate(username=request.user.username, password=current_password)

        error_msg = None

        if user is None:
            error_msg = "Current password is incorrect."
        elif new_password != re_new_password:
            error_msg = "New passwords do not match."
        elif current_password == new_password:
            error_msg = "New password cannot be the same as the current password."
        if error_msg:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                messages.error(request, error_msg)
                return redirect('change_password')
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Keep the user logged in
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            messages.success(request, "Your password has been changed successfully.")
            return redirect('profile') # Make sure 'profile' URL name exists
        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)


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
        user = authenticate(username=request.user.username, password=current_password)
        if user is not None:
            if new_password == re_new_password:
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


