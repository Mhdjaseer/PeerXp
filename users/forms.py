from django import forms
from .models import Department,CustomUser,Ticket



class NewUserCreation(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['name','email','password','phone_number','department','role',]





class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']


class NewTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'body', 'priority','department']