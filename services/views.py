from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.templatetags.static import static
from django.core.mail import send_mail
#from django_renderpdf.views import PDFView
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db.models import Sum 
import json

def home(request):
    user = Person.objects.filter(username=request.user.username).first()

    if not user:
        # Render the custom "Student Not Found" template
        return render(request, 'error_404.html', {'user': request.user})
    #user = get_object_or_404(Person, id_number=request.user.username)  # Assuming `username` is used for id_number
    payments = TaxPayment.objects.filter(user=request.user)
    context = {
        'user': user,
        'payments': payments
    }
    return render(request, 'home.html', context)

def search_vehicle(request):
    query = request.GET.get('number_plate', '')
    if query:
        vehicles = Vehicle.objects.filter(number_plate__icontains=query)
    else:
        vehicles = Vehicle.objects.all()
    form = VehicleSearchForm(initial={'number_plate': query})
    return render(request, 'search_vehicle.html', {'form': form, 'vehicles': vehicles})

def list_vehicles(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'list_vehicles.html', {'vehicles': vehicles})

def view_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    return render(request, 'view_vehicle.html', {'vehicle': vehicle})

def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_vehicles')
    else:
        form = VehicleForm()
    return render(request, 'create_vehicle.html', {'form': form})

def update_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('list_vehicles')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'update_vehicle.html', {'form': form})

def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('list_vehicles')
    return render(request, 'delete_vehicle.html', {'vehicle': vehicle})

def create_public_record(request):
    if request.method == 'POST':
        form = PublicRecordForm(request.POST, request.FILES)
        if form.is_valid():
            public_record = form.save(commit=False)
            public_record.created_by = request.user
            public_record.save()
            return redirect('list_public_records')
    else:
        form = PublicRecordForm()
    return render(request, 'create_public_record.html', {'form': form})


def list_public_records(request):
    records = PublicRecord.objects.all()
    return render(request, 'list_public_records.html', {'records': records})


def create_marriage_license(request):
    if request.method == 'POST':
        form = MarriageLicenseForm(request.POST, request.FILES)
        if form.is_valid():
            marriage_license = form.save(commit=False)
            marriage_license.issued_by = request.user
            marriage_license.save()
            return redirect('list_marriage_license_records')
    else:
        form = MarriageLicenseForm()
    return render(request, 'create_marriage_license.html', {'form': form})

def list_marriage_license_records(request):
    records = MarriageLicense.objects.all()
    return render(request, 'list_marriage_records.html', {'records': records})

def view_marriage_license(request, pk):
    record = get_object_or_404(MarriageLicense, pk=pk)
    return render(request, 'view_marriage_license.html', {'record': record})


def update_marriage_license(request, pk):
    record = get_object_or_404(MarriageLicense, pk=pk)
    if request.method == 'POST':
        form = MarriageLicenseForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            return redirect('list_marriage_license_records')
    else:
        form = MarriageLicenseForm(instance=record)
    return render(request, 'update_marriage_license.html', {'form': form})

def delete_marriage_license(request, pk):
    record = get_object_or_404(MarriageLicense, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('list_marriage_license_records')
    return render(request, 'delete_marriage_license.html', {'record': record})

def create_property_deed(request):
    if request.method == 'POST':
        form = PropertyDeedForm(request.POST, request.FILES)
        if form.is_valid():
            property_deed = form.save(commit=False)
            property_deed.issued_by = request.user
            property_deed.save()
            return redirect('property_deeds')
    else:
        form = PropertyDeedForm()
    return render(request, 'create_property_deed.html', {'form': form})



def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Succesfful saved in the database')
            return redirect('list_people')
    else:
        form = PersonForm()
    return render(request, 'add_person.html', {'form': form})

def list_people(request):
    people = Person.objects.all()
    return render(request, 'list_people.html', {'people': people})


def view_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    return render(request, 'view_person.html', {'person': person})

#am not using this view instead am using the bellow one 
def update_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return redirect('list_people')
    else:
        form = PersonForm(instance=person)
    return render(request, 'update_person.html', {'form': form, 'person': person})



def create_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES ,instance=person)
        if form.is_valid():
            form.save()
            return redirect('list_people')  # Redirect to a list view or another page
    else:
        form = PersonForm(instance=person)
    
    
    return render(request, 'create_person.html', {'form': form ,'person': person})



def delete_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        person.delete()
        return redirect('list_people')
    return render(request, 'delete_person.html', {'person': person})


def search_person(request):
    form = PersonSearchForm()
    person = None
    if request.method == 'POST':
        form = PersonSearchForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data['id_number']
            try:
                person = get_object_or_404(Person, id_number=id_number)
            except ObjectDoesNotExist:
                messages.warning(request, 'No Record Found')
    return render(request, 'search_person.html', {'form': form, 'person': person})




def xprint_person_as_pdf(request, pk):
    person = get_object_or_404(Person, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="person_{person.id_number}.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Add content to PDF
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 100, f"ID Number: {person.id_number}")
    p.drawString(100, height - 130, f"Full Name: {person.full_name}")
    p.drawString(100, height - 160, f"Date of Birth: {person.date_of_birth.strftime('%Y-%m-%d')}")
    p.drawString(100, height - 190, f"Place of Birth: {person.place_of_birth}")
    p.drawString(100, height - 220, f"Gender: {person.gender}")
    p.drawString(100, height - 250, f"Date of Issue: {person.date_of_issue.strftime('%Y-%m-%d') if person.date_of_issue else 'N/A'}")
    p.drawString(100, height - 280, f"Expiry Date: {person.expiry_date.strftime('%Y-%m-%d') if person.expiry_date else 'N/A'}")
    p.drawString(100, height - 310, f"Nationality: {person.nationality}")
    p.drawString(100, height - 340, f"Parent/Guardian: {person.parent_or_guardian if person.parent_or_guardian else 'N/A'}")

    # Add profile picture
    if person.profile_picture:
        p.drawInlineImage(person.profile_picture.path, 400, height - 200, width=100, height=100)
    
    # Add thumbprint
    if person.thumbprint:
        p.drawInlineImage(person.thumbprint.path, 400, height - 300, width=100, height=100)
    
    p.showPage()
    p.save()
    return response


def print_person_as_pdf(request, pk):
    person = get_object_or_404(Person, pk=pk)

    # Get absolute URLs
    profile_picture_url = request.build_absolute_uri(person.profile_picture.url) if person.profile_picture else None
    thumbprint_url = request.build_absolute_uri(person.thumbprint.url) if person.thumbprint else None
    
    # Render the HTML template with the person data
    context = {
        'person': person,
        'profile_picture_url': profile_picture_url,
        'thumbprint_url': thumbprint_url,
    }
    html_string = render_to_string('person_template.html', context)
    
    # Convert HTML to PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
    
    # Check for errors
    if pdf.err:
        return HttpResponse('Error rendering PDF', status=500)
    
    # Return the PDF as a response
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="person_{person.id_number}.pdf"'
    return response




def pay_tax(request):
    if request.method == 'POST':
        form = TaxPaymentForm(request.POST)
        if form.is_valid():
            tax_payment = form.save(commit=False)
            tax_payment.user = request.user
            tax_payment.status = 'Pending'
            tax_payment.secret_code = generate_secret_code()  # Generate and set the secret code
            tax_payment.code_expiration = timezone.now() + timedelta(days=30)
            tax_payment.save()
            
            # Send email with secret code
            send_mail(
                'Kanjo Tax Payment Confirmation',
                f'Your secret code is {tax_payment.secret_code}. This code is valid until {tax_payment.code_expiration}.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            
            return redirect('payment_success')
    else:
        form = TaxPaymentForm()
    return render(request, 'pay_tax.html', {'form': form})

def verify_code(request):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            secret_code = form.cleaned_data['secret_code']
            try:
                payment = TaxPayment.objects.get(secret_code=secret_code)
                if not payment.is_code_expired():
                    payment.status = 'Completed'
                    payment.save()
                    return redirect('verification_success')
                else:
                    return render(request, 'verify_code.html', {'form': form, 'error': 'Code has expired.'})
            except TaxPayment.DoesNotExist:
                return render(request, 'verify_code.html', {'form': form, 'error': 'Invalid code.'})
    else:
        form = VerifyCodeForm()
    return render(request, 'verify_code.html', {'form': form})

def payment_success(request):
    return render(request, 'payment_success.html')

def verification_success(request):
    return render(request, 'verification_success.html')


def search_payment_by_code(request):
    form = SearchSecretCodeForm(request.POST or None)
    payment = None
    error_message = None

    if request.method == 'POST' and form.is_valid():
        secret_code = form.cleaned_data['secret_code']
        try:
            payment = TaxPayment.objects.get(secret_code=secret_code)
        except TaxPayment.DoesNotExist:
            error_message = 'No payment found with that secret code.'

    return render(request, 'search_payment.html', {
        'form': form,
        'payment': payment,
        'error_message': error_message
    })



def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, ' You have been logged in successfully.')
            return redirect('home')  # Replace 'dashboard' with your desired URL name
        else:
            # Return an 'invalid login' error message.
            messages.error(request, ' Username or Password did not match. Try again.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    


    
    
def custom_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            id_number = form.cleaned_data.get('id_number')
            password = form.cleaned_data.get('password1')

            # Get the CompanyStaff instance
            staff = Person.objects.get(username=username, id_number=id_number)

            # Create a new user
            if User.objects.filter(username=username):
                messages.warning(request,"The Username with that Identification No already exist!")
            else:
                user = User.objects.create_user(username=username, password=password)
                user.email = staff.email
                user.first_name = staff.first_name
                user.last_name = staff.last_name
                # Save other fields as needed

                user.save()
                login(request, user)
                messages.success(request, 'You account has been created successfully.')
                return redirect('home')
           
        
           
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})




def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('login'))


# User dashboard view
@login_required
def user_dashboard(request):
    user = Person.objects.filter(username=request.user.username).first()

    if not user:
        # Render the custom "Student Not Found" template
        return render(request, 'error_404.html', {'user': request.user})
    #user = get_object_or_404(Person, id_number=request.user.username)  # Assuming `username` is used for id_number
    payments = TaxPayment.objects.filter(user=request.user)
    context = {
        'user': user,
        'payments': payments
    }
    return render(request, 'user_dashboard.html', context)


# Update profile view
@login_required
def update_profile(request):
    user = get_object_or_404(Person, id_number=request.user.username)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = PersonForm(instance=user)
    return render(request, 'update_profile.html', {'form': form})


# Verify payment code view
@login_required
def verify_payment_code(request):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['secret_code']
            try:
                payment = TaxPayment.objects.get(secret_code=code)
                if payment.is_code_expired():
                    return render(request, 'verify_code.html', {'form': form, 'error': 'Code has expired'})
                return render(request, 'payment_details.html', {'payment': payment})
            except TaxPayment.DoesNotExist:
                return render(request, 'verify_code.html', {'form': form, 'error': 'Invalid code'})
    else:
        form = VerifyCodeForm()
    return render(request, 'verify_code.html', {'form': form})



###################### ---NHIF--- ############

def member_list(request):
    members = Member.objects.all()
    return render(request, 'nhif_app/member_list.html', {'members': members})

def member_detail(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    payments = member.payments.all()
    return render(request, 'nhif_app/member_detail.html', {'member': member, 'payments': payments})

def add_payment(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        month_name = request.POST.get('month')
        amount = request.POST.get('amount')

        # Ensure the month exists or create it
        month, created = Month.objects.get_or_create(name=month_name)

        MonthlyPayment.objects.create(member=member, month=month, amount=amount)
    return redirect('member_detail', member_id=member.id)



@login_required
def user_dashboardx(request):
    user = get_object_or_404(Person, username=request.user.username)
    payments = TaxPayment.objects.filter(user=user).order_by('-date')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            # Create a new payment record
            TaxPayment.objects.create(
                user=user,
                amount=amount,
                description=description,
                date=timezone.now()  # Set the payment date to now
            )
            return redirect('user_dashboard')  # Redirect to the dashboard after successful payment
    else:
        form = PaymentForm()

    context = {
        'user': user,
        'payments': payments,
        'form': form
    }
    return render(request, 'userx_dashboard.html', context)


def homepage(request):
    user = get_object_or_404(Person, username=request.user.username)

    # Retrieve user's payments
    payments = TaxPayment.objects.filter(user=user).order_by('-date')

    # Retrieve all payments for chart data
    all_payments = TaxPayment.objects.all()
    total_amount_paid = all_payments.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    total_users = Person.objects.count()

    # Prepare data for the chart
    payment_data = TaxPayment.objects.filter(user=user).order_by('date')
    months = [payment.date.strftime('%b %Y') for payment in payment_data]
    amounts = [payment.amount for payment in payment_data]

    # Get the 5 most recent transactions
    recent_transactions = payments[:5]

    context = {
        'user': user,
        'payments': payments,
        'months': json.dumps(months),
        'amounts': json.dumps(amounts),
        'total_amount_paid': total_amount_paid,
        'total_users': total_users,
        'recent_transactions': recent_transactions
    }
    return render(request, 'index.html', context)


def payment_status(request):
    # Get all users and months
    users = Person.objects.all()
    months = Month.objects.all().order_by('name')

    # Create a dictionary to hold payment status
    payment_status = {}

    # Initialize payment status for each user and month
    for user in users:
        payment_status[user.username] = {month.name: False for month in months}

    # Update the payment status based on actual payments
    payments = TaxPayment.objects.select_related('user', 'month').all()
    for payment in payments:
        payment_status[payment.user.username][payment.month.name] = True

    context = {
        'users': users,
        'months': months,
        'payment_status': payment_status
    }
    return render(request, 'payment_status.html', context)



def monthly_collections(request):
    # Retrieve all months
    months = Month.objects.all().order_by('name')

    # Aggregate payment amounts by month
    monthly_data = TaxPayment.objects.values('month').annotate(total_collected=Sum('amount')).order_by('month')

    # Create lists for months and amounts
    month_names = [month.name for month in months]
    amounts_collected = [0] * len(month_names)  # Initialize amounts collected list

    # Map aggregated data to the correct months
    for data in monthly_data:
        month_name = data['month']
        total_amount = data['total_collected']
        if month_name in month_names:
            index = month_names.index(month_name)
            amounts_collected[index] = total_amount

    context = {
        'month_names': month_names,
        'amounts_collected': amounts_collected,
    }
    return render(request, 'monthly_collections.html', context)



def search_user(request):
    form = UserSearchForm(request.GET or None)
    user = None
    payments = None

    if form.is_valid():
        username = form.cleaned_data['username']
        user = get_object_or_404(Person, username=username)
        payments = TaxPayment.objects.filter(user=user).order_by('date')

    context = {
        'form': form,
        'user': user,
        'payments': payments
    }
    return render(request, 'search_user.html', context)