from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

#To add field in UserCreationForm
class RegisterUserForm(UserCreationForm):
    #widget are used to apply boostrap
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    #yang ni kita tambah sebab tiada pada field yang kita tambah.
    #yang ni object yang dah built in, jadi tinggal tambah widgetnya sahaja.
    def __init__(self, *args, **kwargs):
	    super(RegisterUserForm, self).__init__(*args, **kwargs)

	    self.fields['username'].widget.attrs['class'] = 'form-control'
	    self.fields['password1'].widget.attrs['class'] = 'form-control'
	    self.fields['password2'].widget.attrs['class'] = 'form-control'
