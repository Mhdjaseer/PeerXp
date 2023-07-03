from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect, render
from .forms import DepartmentForm,NewUserCreation,NewTicketForm
from .models import Department,Ticket
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import logout


class home(TemplateView):
    template_name = "users/home.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AdminDashboard(UserPassesTestMixin,TemplateView):
    template_name = "Admin/dashbord.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = NewUserCreation()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NewUserCreation(request.POST)
        if form.is_valid():
            print("the form is valid")
            user = form.save(commit=False)
            user.created_by = self.request.user
            user.save()
            return redirect('admin')  # Replace 'admin_dashboard' with your actual URL name for the dashboard page
        return render(request, self.template_name, {'form': form})
    

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin') 
            else:
                return redirect('home')  
        else:
            error_message = 'Invalid login credentials'
            return render(request, self.template_name, {'error_message': error_message})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'Admin/department_list.html', {'departments': departments})




@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.created_by = request.user  # Assuming the logged-in user is the creator/admin
            department.save()
            return redirect('department_list')  # Redirect to the department list view
    else:
        form = DepartmentForm()
    
    return render(request, 'Admin/create_department.html', {'form': form})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')  # Redirect to the department list view
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'Admin/update_department.html', {'form': form, 'department': department})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    if department.customuser_set.exists():
        messages.error(request, 'Cannot delete the department because it is associated with one or more users.')
        return redirect('department_list')

    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully.')
        return redirect('department_list')

    return render(request, 'Admin/delete_department.html', {'department': department})



# tickets
from .ticket import post_ticket_to_zendesk

def create_ticket(request):
    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.contact_email = request.user.email
            ticket.contact_phone = request.user.phone_number
            ticket.save()

            response = post_ticket_to_zendesk(ticket,ticket.contact_phone,ticket.contact_email)
            if response.status_code == 201:
                messages.success(request, 'Ticket created successfully.')
                return redirect('new_ticket')
            else:
                messages.error(request, 'Failed to create ticket. Please try again later.')

    else:
        form = NewTicketForm(initial={
            'contact_email': request.user.email,
            'contact_phone': request.user.phone_number
        })

    return render(request, 'new_ticket.html', {'form': form})


def ticket_list(request):
    if request.user.is_superuser:
        # Super admin sees all tickets
        tickets = Ticket.objects.all()
    else:
        # Regular user sees tickets assigned to their department
        department = request.user.department
        tickets = Ticket.objects.filter(department=department)
    
    context = {'tickets': tickets}
    return render(request, 'ticket_list.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')