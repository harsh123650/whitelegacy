from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Sum, DateField
from django.db.models.functions import Cast
from django.http import HttpResponse
from datetime import timedelta

from .models import MilkDelivery, MilkingLog, HealthLog, UserProfile
from .forms import UserCreateForm
from .models import ContactMessage, SubscriptionRequest
from .forms import UserCreateForm, ContactForm, SubscribeForm


# ----------------------------
# Home Page
# ----------------------------
def index(request):
    return render(request, 'dairyapp/index.html')

def about_view(request):
    return render(request, 'dairyapp/about.html')

def contact_view(request):
    return render(request, 'dairyapp/contact.html')

def suscribe_view(request):
    return render(request, 'dairyapp/suscribe.html')

def guide_view(request):
    return render(request, 'dairyapp/guide.html')


def suscription_select(request):
    return render(request, 'dairyapp/suscription_select.html')




def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')  # Optional: or show a success message
    else:
        form = ContactForm()
    return render(request, 'dairyapp/contact.html', {'form': form})

def suscribe_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')  # Or show a message
    else:
        form = SubscribeForm()
    return render(request, 'dairyapp/suscribe.html', {'form': form})


def thank_you(request):
    return render(request, 'dairyapp/thank_you.html')

# ----------------------------
# Login View
# ----------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Hardcoded admin
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

        # Regular login
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            group_names = [group.name.lower() for group in user.groups.all()]
            if 'admin' in group_names:
                return redirect('admin_dashboard')
            elif 'staff' in group_names:
                return redirect('staff_dashboard')
            elif 'worker' in group_names:
                return redirect('worker_dashboard')
            elif 'customer' in group_names:
                return redirect('customer_dashboard')

        return render(request, 'dairyapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'dairyapp/login.html')

# ----------------------------
# Logout
# ----------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# ----------------------------
# Admin Dashboard
# ----------------------------
@login_required
def admin_dashboard(request):
    try:
        today = timezone.now().date()
        start_date = today - timedelta(days=6)

        # 🔍 Get date filters from GET request
        milk_date = request.GET.get('milk_date')
        delivery_date = request.GET.get('delivery_date')

        # User groups
        staff_users = UserProfile.objects.filter(role='staff')
        worker_users = UserProfile.objects.filter(role='worker')
        customer_users = UserProfile.objects.filter(role='customer')

        # Milking logs (filtered by date if selected)
        if milk_date:
            today_milking = MilkingLog.objects.filter(date=milk_date)
        else:
            today_milking = MilkingLog.objects.filter(date=today)

        # Delivery logs (filtered by date if selected)
        if delivery_date:
            today_deliveries = MilkDelivery.objects.filter(date=delivery_date)
        else:
            today_deliveries = MilkDelivery.objects.filter(date=today)

        today_health = HealthLog.objects.filter(date=today)

        # Latest entries
        latest_delivery = MilkDelivery.objects.last()
        milking_data = MilkingLog.objects.last()
        health_data = HealthLog.objects.last()

        # Chart data (last 7 days)
        delivery_summary = (
            MilkDelivery.objects
            .filter(date__gte=start_date)
            .annotate(day=Cast('date', output_field=DateField()))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        milking_summary = (
            MilkingLog.objects
            .filter(date__gte=start_date)
            .annotate(day=Cast('date', output_field=DateField()))
            .values('day')
            .annotate(total=Sum('milk_quantity'))
            .order_by('day')
        )

        labels = [str(entry['day']) for entry in delivery_summary]
        delivery_data = [entry['count'] for entry in delivery_summary]
        milking_data_chart = [entry['total'] for entry in milking_summary]

        context = {
            'latest_delivery': latest_delivery,
            'milking_data': milking_data,
            'health_data': health_data,
            'staff_list': staff_users,
            'worker_list': worker_users,
            'customer_list': customer_users,
            'form': UserCreateForm(),
            'today': today,
            'today_deliveries': today_deliveries,
            'today_milking': today_milking,
            'today_health': today_health,
            'labels': labels,
            'delivery_data': delivery_data,
            'milking_data_chart': milking_data_chart,
            'contact_messages': ContactMessage.objects.order_by('-submitted_at'),
            'subscriptions': SubscriptionRequest.objects.order_by('-submitted_at'),
        }

        return render(request, 'dairyapp/admin.html', context)

    except Exception as e:
        return HttpResponse(f"<h1>Error Occurred:</h1><p>{e}</p>")


# ----------------------------
# Delete Views
# ----------------------------
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.username != 'Harshal123':
        user.delete()
    return redirect('admin_dashboard')

@login_required
def delete_delivery(request, delivery_id):
    entry = get_object_or_404(MilkDelivery, id=delivery_id)
    entry.delete()
    return redirect('admin_dashboard')

@login_required
def delete_milking(request, milking_id):
    entry = get_object_or_404(MilkingLog, id=milking_id)
    entry.delete()
    return redirect('admin_dashboard')

@login_required
def delete_health(request, health_id):
    entry = get_object_or_404(HealthLog, id=health_id)
    entry.delete()
    return redirect('admin_dashboard')
@login_required
def delete_contact(request, contact_id):
    message = get_object_or_404(ContactMessage, id=contact_id)
    message.delete()
    return redirect('admin_dashboard')

@login_required
def delete_subscription(request, subscription_id):
    subscription = get_object_or_404(SubscriptionRequest, id=subscription_id)
    subscription.delete()
    return redirect('admin_dashboard')


# ----------------------------
# Staff Dashboard
# ----------------------------
@login_required
def staff_dashboard(request):
    customers = UserProfile.objects.filter(role='customer')
    if request.method == 'POST':
        MilkDelivery.objects.create(
            customer_id=request.POST.get('customer_id'),
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            submitted_by=request.user
        )
    return render(request, 'dairyapp/staff.html', {'customers': customers})

# ----------------------------
# Worker Dashboard
# ----------------------------
@login_required
def worker_dashboard(request):
    return render(request, 'dairyapp/worker.html')

# ----------------------------
# Customer Dashboard
# ----------------------------
@login_required
def customer_dashboard(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    deliveries = MilkDelivery.objects.filter(customer_id=profile.custom_id).order_by('-date', '-time')
    return render(request, 'dairyapp/customer.html', {
        'latest_delivery': deliveries.first(),
        'all_deliveries': deliveries
    })

# ----------------------------
# Create New User
# ----------------------------
@csrf_exempt
@login_required
def create_user_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            group_name = role.capitalize()
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

            prefix = {'staff': 'S', 'worker': 'W', 'customer': 'C'}.get(role, 'U')
            last_profile = UserProfile.objects.filter(role=role).order_by('-custom_id').first()
            last_number = int(last_profile.custom_id[1:]) if last_profile else 0
            new_custom_id = f"{prefix}{last_number + 1:03d}"

            UserProfile.objects.create(user=user, role=role, custom_id=new_custom_id)
            return redirect('admin_dashboard')

    return redirect('admin_dashboard')

# ----------------------------
# Worker Data Submission
# ----------------------------
@login_required
def submit_worker_data(request):
    if request.method == 'POST':
        buffalo_number = request.POST.get('buffalo_number')
        date = request.POST.get('date') or timezone.now().date()
        milk_time = request.POST.get('milk_time')
        milk_quantity = request.POST.get('milk_quantity')
        health_notes = request.POST.get('health_notes')

        if buffalo_number and milk_time and milk_quantity:
            MilkingLog.objects.create(
                buffalo_number=buffalo_number,
                date=date,
                milk_time=milk_time,
                milk_quantity=milk_quantity,
                submitted_by=request.user
            )

        if buffalo_number and health_notes:
            HealthLog.objects.create(
                buffalo_number=buffalo_number,
                date=date,
                health_notes=health_notes,
                submitted_by=request.user
            )

    return redirect('worker_dashboard')

