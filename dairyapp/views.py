# Standard Library
from datetime import date, timedelta
import calendar

# Django Core Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.template.loader import get_template
from django.utils import timezone
from django.conf import settings

# Django Auth & Decorators
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Django ORM / DB functions
from django.db.models import Count, Sum, DateField
from django.db.models.functions import Cast

# Third-Party Libraries
import razorpay
from xhtml2pdf import pisa

# Local App Models and Forms
from .models import (
    MilkDelivery, MilkingLog, HealthLog, UserProfile,
    ContactMessage, SubscriptionRequest, Subscription, Payment
)

from .forms import (
    UserCreateForm, ContactForm, SubscribeForm
)


# ----------------------------------
# Decorators
# ----------------------------------
def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if hasattr(request.user, 'userprofile'):
                role = request.user.userprofile.role
                if role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("⛔ Access Denied: You are not authorized.")
        return wrapper
    return decorator


# ----------------------------------
# Home & Static Pages
# ----------------------------------

def index(request):
    return render(request, 'dairyapp/index.html')


def about_view(request):
    return render(request, 'dairyapp/about.html')


def guide_view(request):
    return render(request, 'dairyapp/guide.html')


def thank_you(request):
    return render(request, 'dairyapp/thank_you.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = ContactForm()
    return render(request, 'dairyapp/contact.html', {'form': form})


def suscribe_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = SubscribeForm()
    return render(request, 'dairyapp/suscribe.html', {'form': form})


# ----------------------------------
# Authentication Views
# ----------------------------------

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Hardcoded Admin Login
        if username == "Harshal123" and password == "Harshal@123":
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                group, _ = Group.objects.get_or_create(name='Admin')
                user.groups.add(group)
                UserProfile.objects.create(user=user, role='admin', custom_id='A001')
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user, role='admin', custom_id='A001')

            login(request, user)
            return redirect('admin_dashboard')

        # Normal Login (Staff/Worker/Customer)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            role = user.groups.first().name.lower()
            return redirect(f'{role}_dashboard')

        return render(request, 'dairyapp/login.html', {
            'error': 'Invalid credentials'
        })

    return render(request, 'dairyapp/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def forgot_password_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return render(request, 'dairyapp/forgot_password.html', {
                'message': 'Password reset successful!'
            })
        except User.DoesNotExist:
            return render(request, 'dairyapp/forgot_password.html', {
                'error': 'User not found!'
            })

    return render(request, 'dairyapp/forgot_password.html')


# ----------------------------------
# Subscription and Payment
# ----------------------------------

@login_required
def subscription_select(request):
    if request.method == "POST":
        username = request.user.username
        plan = request.POST.get('plan')

        # Plan Pricing
        plan_prices = {
            'monthly': 3000,
            'quarterly': 18000,
            'yearly': 36000,
        }
        amount = plan_prices.get(plan)

        if not amount:
            messages.error(request, "Please select a valid subscription plan.")
            return redirect('subscription_select')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Invalid username.")
            return redirect('subscription_select')

        # Check if already subscribed
        active_subscription = Subscription.objects.filter(
            customer=user,
            end_date__gte=date.today()
        ).first()

        if active_subscription:
            msg = f"You already have an active subscription until {active_subscription.end_date}."
            messages.error(request, msg)
            return redirect('subscription_select')

        # Save data to session for Razorpay page
        request.session['subscription_data'] = {
            'username': username,
            'plan': plan,
            'amount': amount
        }

        return redirect('payment_page')

    return render(request, 'dairyapp/subscription_select.html', {
        'username': request.user.username
    })


@login_required
def download_invoice(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    template = get_template('dairyapp/payment_invoice.html')
    html = template.render({'payment': payment})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{payment.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('PDF generation failed')
    
    return response


# -----------------------------
# Admin Dashboard
# -----------------------------
@login_required
@role_required(['admin'])
def admin_dashboard(request):
    try:
        # Today's and 7-day range
        today = timezone.now().date()
        start_date = today - timedelta(days=6)

        # Filters from GET
        milk_date = request.GET.get('milk_date') or str(today)
        delivery_date = request.GET.get('delivery_date') or str(today)
        payment_month = request.GET.get('payment_month')

        # User lists by role
        staff_users = UserProfile.objects.filter(role='staff')
        worker_users = UserProfile.objects.filter(role='worker')
        customer_users = UserProfile.objects.filter(role='customer')

        # Today's records
        today_milking = MilkingLog.objects.filter(date=milk_date)
        today_deliveries = MilkDelivery.objects.filter(date=delivery_date)
        today_health = HealthLog.objects.filter(date=today)

        # Latest single records
        latest_delivery = MilkDelivery.objects.last()
        milking_data = MilkingLog.objects.last()
        health_data = HealthLog.objects.last()

        # Charts data (last 7 days)
        delivery_summary = MilkDelivery.objects.filter(date__gte=start_date)\
            .annotate(day=Cast('date', output_field=DateField()))\
            .values('day')\
            .annotate(count=Count('id'))\
            .order_by('day')

        milking_summary = MilkingLog.objects.filter(date__gte=start_date)\
            .annotate(day=Cast('date', output_field=DateField()))\
            .values('day')\
            .annotate(total=Sum('milk_quantity'))\
            .order_by('day')

        labels = [str(entry['day']) for entry in delivery_summary]
        delivery_data = [entry['count'] for entry in delivery_summary]
        milking_data_chart = [entry['total'] for entry in milking_summary]

        # Payments
        months = [(i, calendar.month_name[i]) for i in range(1, 13)]
        if payment_month and payment_month.isdigit():
            payment_data = Payment.objects.filter(date__month=int(payment_month)).order_by('-date')
        else:
            payment_data = Payment.objects.all().order_by('-date')

        # Final context for template
        context = {
            'form': UserCreateForm(),
            'today': today,
            'latest_delivery': latest_delivery,
            'milking_data': milking_data,
            'health_data': health_data,
            'staff_list': staff_users,
            'worker_list': worker_users,
            'customer_list': customer_users,
            'today_deliveries': today_deliveries,
            'today_milking': today_milking,
            'today_health': today_health,
            'labels': labels,
            'delivery_data': delivery_data,
            'milking_data_chart': milking_data_chart,
            'contact_messages': ContactMessage.objects.order_by('-submitted_at'),
            'subscriptions': SubscriptionRequest.objects.order_by('-submitted_at'),
            'months': months,
            'payment_data': payment_data,
            'selected_milk_date': milk_date,
            'selected_delivery_date': delivery_date,
            'selected_payment_month': payment_month,
        }

        return render(request, 'dairyapp/admin.html', context)

    except Exception as e:
        return HttpResponse(f"<h1>Error Occurred:</h1><p>{e}</p>")


# --------------------------------------
# Staff Dashboard
# --------------------------------------
@login_required
@role_required(['staff'])
def staff_dashboard(request):
    # Get all customers and current staff profile
    customers = UserProfile.objects.filter(role='customer')
    profile = UserProfile.objects.get(user=request.user)

    # Handle milk delivery submission by staff
    if request.method == 'POST':
        delivery = MilkDelivery.objects.create(
            customer_id=request.POST.get('customer_id'),
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            submitted_by=request.user
        )
        print("Delivery Created: ", delivery)

    return render(request, 'dairyapp/staff.html', {
        'customers': customers,
        'profile': profile
    })


# --------------------------------------
# Worker Dashboard
# --------------------------------------
@login_required
@role_required(['worker'])
def worker_dashboard(request):
    return render(request, 'dairyapp/worker.html')


# --------------------------------------
# Customer Dashboard
# --------------------------------------
@login_required
@role_required(['customer'])
def customer_dashboard(request):
    customer = request.user
    profile = UserProfile.objects.get(user=customer)

    # Get all deliveries for the customer
    all_deliveries = MilkDelivery.objects.filter(customer_id=customer).order_by('-date')

    # Get subscription and payment info
    subscription = Subscription.objects.filter(customer=customer).first()
    payment_data = Payment.objects.filter(user=customer).order_by('-date')

    return render(request, 'dairyapp/customer.html', {
        'all_deliveries': all_deliveries,
        'subscription': subscription,
        'payment_data': payment_data,
        'profile': profile,
    })


# --------------------------------------
# Create New User (Admin Only)
# --------------------------------------
@csrf_exempt
@login_required
def create_user_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            # Create user without saving to DB yet
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            password = form.cleaned_data['password']

            # Set password and save user
            user.set_password(password)
            user.save()

            # Add user to appropriate group
            group, _ = Group.objects.get_or_create(name=role.capitalize())
            user.groups.add(group)

            # Generate unique custom ID like C001, S001, etc.
            prefix = {'staff': 'S', 'worker': 'W', 'customer': 'C'}.get(role, 'U')
            last_profile = UserProfile.objects.filter(role=role).order_by('-custom_id').first()
            last_number = int(last_profile.custom_id[1:]) if last_profile else 0
            new_custom_id = f"{prefix}{last_number + 1:03d}"

            # Create UserProfile with role and ID
            UserProfile.objects.create(user=user, role=role, custom_id=new_custom_id)

            return redirect('admin_dashboard')

    return redirect('admin_dashboard')


# --------------------------------------
# Worker Submits Milking + Health Data
# --------------------------------------
@login_required
def submit_worker_data(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        buffalo_number = request.POST.get('buffalo_number')
        date = request.POST.get('date') or timezone.now().date()
        milk_time = request.POST.get('milk_time')
        milk_quantity = request.POST.get('milk_quantity')
        health_notes = request.POST.get('health_notes')

        # Save milking log if fields filled
        if buffalo_number and milk_time and milk_quantity:
            MilkingLog.objects.create(
                buffalo_number=buffalo_number,
                date=date,
                milk_time=milk_time,
                milk_quantity=milk_quantity,
                submitted_by=request.user
            )

        # Save health log if notes provided
        if buffalo_number and health_notes:
            HealthLog.objects.create(
                buffalo_number=buffalo_number,
                date=date,
                health_notes=health_notes,
                submitted_by=request.user
            )

        return redirect('worker_dashboard')

    return render(request, 'dairyapp/worker.html', {
        'profile': profile
    })


# --------------------------------------
# DELETE USER (Prevent deleting Admin Harshal123)
# --------------------------------------
@login_required
@csrf_exempt
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.username != 'Harshal123':  # Prevent deleting main admin
        user.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'User deleted'})
    return redirect('admin_dashboard')


# --------------------------------------
# DELETE MILK DELIVERY RECORD
# --------------------------------------
@login_required
@csrf_exempt
def delete_delivery(request, delivery_id):
    get_object_or_404(MilkDelivery, id=delivery_id).delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Delivery deleted'})
    return redirect('admin_dashboard')


# --------------------------------------
# DELETE MILKING LOG RECORD
# --------------------------------------
@login_required
@csrf_exempt
def delete_milking(request, milking_id):
    get_object_or_404(MilkingLog, id=milking_id).delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Milking record deleted'})
    return redirect('admin_dashboard')


# --------------------------------------
# DELETE HEALTH LOG RECORD
# --------------------------------------
@login_required
@csrf_exempt
def delete_health(request, health_id):
    get_object_or_404(HealthLog, id=health_id).delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Health record deleted'})
    return redirect('admin_dashboard')


# --------------------------------------
# DELETE CONTACT MESSAGE
# --------------------------------------
@login_required
@csrf_exempt
def delete_contact(request, contact_id):
    get_object_or_404(ContactMessage, id=contact_id).delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Contact message deleted'})
    return redirect('admin_dashboard')


# --------------------------------------
# DELETE SUBSCRIPTION REQUEST
# --------------------------------------
@login_required
@csrf_exempt
def delete_subscription(request, subscription_id):
    get_object_or_404(SubscriptionRequest, id=subscription_id).delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Subscription request deleted'})
    return redirect('admin_dashboard')

# --------------------------------------
# DELETE INVOICE RECORD
# --------------------------------------
@login_required
@csrf_exempt
def delete_invoice(request, pk):
    invoice = get_object_or_404(Payment, id=pk)
    invoice.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Invoice deleted'})
    return redirect('admin_dashboard')

# --------------------------------------
# RAZORPAY PAYMENT PAGE VIEW
# --------------------------------------
@login_required
def payment_page(request):
    subscription_data = request.session.get('subscription_data')
    if not subscription_data:
        return redirect('subscription_select')

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    amount = subscription_data['amount'] * 100  # Convert to paisa

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        'key_id': settings.RAZORPAY_KEY_ID,
        'order_id': payment['id'],
        'amount': amount,
        'subscription': subscription_data
    }

    return render(request, 'dairyapp/payment.html', context)
# --------------------------------------
# AFTER PAYMENT SUCCESS (store subscription and payment)
# --------------------------------------
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.session.get('subscription_data')
        if not data:
            return JsonResponse({'error': 'Session expired'}, status=400)

        username = data['username']
        plan = data['plan']
        amount = data['amount']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=400)

        start_date = date.today()
        if plan == 'monthly':
            end_date = start_date + timedelta(days=30)
        elif plan == 'quarterly':
            end_date = start_date + timedelta(days=90)
        else:
            end_date = start_date + timedelta(days=365)

        # Save subscription & payment
        Subscription.objects.create(
            customer=user,
            plan=plan,
            amount=amount,
            start_date=start_date,
            end_date=end_date
        )

        Payment.objects.create(
            user=user,
            plan=plan,
            amount=amount
        )

        return JsonResponse({'message': 'Payment and subscription recorded successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)
