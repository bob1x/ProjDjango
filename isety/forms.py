from django import forms
from .models import Conversation, Poste, Recommandation, Transport, Logement, Stage ,Message
from django.forms import ModelForm

from django.contrib.auth.forms import AuthenticationForm

# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=150, label="username")
#     password = forms.CharField(widget=forms.PasswordInput, label="Password")
    

from django.contrib.auth.forms import AuthenticationForm
from .models import User,Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User , Evenement


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)


class EmailLoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
        return email

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'mt-2 p-2 border border-gray-300 focus:outline-none focus:ring-0 focus:border-gray-300 rounded text-sm text-gray-900'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'mt-2 p-2 border border-gray-300 focus:outline-none focus:ring-0 focus:border-gray-300 rounded text-sm text-gray-900'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'mt-2 p-2 border border-gray-300 focus:outline-none focus:ring-0 focus:border-gray-300 rounded text-sm text-gray-900', 'placeholder': 'Enter your email'})
    )
    telnum = forms.CharField(
        max_length=15, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'mt-2 p-2 border border-gray-300 focus:outline-none focus:ring-0 focus:border-gray-300 rounded text-sm text-gray-900', 'placeholder': 'Enter your telephone number'})
    )
    photo = forms.ImageField(
        required=False, 
        widget=forms.ClearableFileInput(attrs={'class': 'mt-2 p-2 border border-gray-300 focus:outline-none focus:ring-0 focus:border-gray-300 rounded text-sm text-gray-900'})
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'telnum', 'photo', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'mt-2 p-2 border border-gray-300 focus:outline-none focus:ring-0 focus:border-gray-300 rounded text-sm text-gray-900'


class UserUpdateForm(forms.ModelForm):
    
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'mb-2 w-full rounded-md border bg-white px-2 py-2 outline-none ring-blue-600 sm:mr-4 sm:mb-0 focus:ring-1'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'w-full rounded-md border bg-white px-2 py-2 outline-none ring-blue-600 focus:ring-1'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'your.email@domain.com" class="w-full rounded-md border bg-white px-2 py-2 outline-none ring-blue-600 focus:ring-1', 'placeholder': 'Enter your email'})
    )
    telnum = forms.CharField(
        max_length=15, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'w-full rounded-md border bg-white px-2 py-2 outline-none ring-blue-600 focus:ring-1', 'placeholder': 'Enter your telephone number'})
    )
   
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full rounded-md border bg-white px-2 py-2 outline-none ring-blue-600 focus:ring-1', 'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full rounded-md border bg-white px-2 py-2 outline-none ring-blue-600 focus:ring-1', 'placeholder': 'Confirm your password'})
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'max-w-full rounded-lg px-2 font-medium text-blue-600 outline-none ring-blue-600 focus:ring-1'})
    )
    
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'telnum','password1', 'password2','photo')
        
class PosteForm(ModelForm):
    class Meta:
        model = Poste
        # Specify fields from the Poste model and its subclasses
        fields = "__all__"

class RecommandationForm(forms.ModelForm):
    class Meta:
        model = Recommandation
        fields = ["texte", "poste_type", "image"]
        widgets = {
            'texte': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'poste_type': forms.Select(attrs={'class': 'form-select mt-1 block w-full'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input mt-1 block w-full'}),
        }


class TransportForm(ModelForm):
    class Meta:
        model = Transport
        fields = ["image","poste_type","depart", "destination", "heure_dep", "nbre_sieges", "contact_Trans"]
        widgets = {
            'poste_type': forms.Select(attrs={'class': 'form-select mt-1 block w-full'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'depart': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'destination': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'heure_dep': forms.TimeInput(attrs={
                'class': 'bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'min': '04:00',
                'max': '23:00',
                'value': '00:00',
                'required': True
            }),
            'nbre_sieges': forms.NumberInput(attrs={'class': 'form-input mt-1 block w-full'}), 
            'contact_Trans': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
        } 
            
        
        


class LogementForm(ModelForm):
    class Meta:
        model = Logement    
        fields = ["image","poste_type","localisation", "description", "logment_contact"]
        widgets = {
            'poste_type': forms.Select(attrs={'class': 'form-select mt-1 block w-full '}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input mt-1 block w-full rounded-lg'}),
            'localisation': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'form-input mt-1 block w-full rounded-lg'}),
            'logment_contact': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-lg'}),
        }


class StageForm(ModelForm):
    class Meta:
        model = Stage
        fields = ["image","poste_type","typeStg", "societe", "duree", "sujet", "contact_Stage","specialite"]
        widgets = {
            'poste_type': forms.Select(attrs={'class': 'form-select mt-1 block w-full rounded-lg'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input mt-1 block w-full '}),
            'typeStg': forms.Select(attrs={'class': 'form-select mt-1 block w-full rounded-lg'}),
            'societe': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-lg'}),
            'duree': forms.NumberInput(attrs={'class': 'form-input mt-1 block w-full rounded-lg'}),
            'sujet': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-lg'}),
            'contact_Stage': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-lg'}),
            'specialite': forms.Select(attrs={'class': 'form-input mt-1 block w-full rounded-lg'}),
            
        }
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...','class':'px-0 w-full text-sm text-gray-900 border-0 focus:ring-0 focus:outline-none dark:text-white dark:placeholder-gray-400 dark:bg-gray-800'}),
        }



class EventForm(ModelForm):
    class Meta:
        model = Evenement
        fields = ["title", "description","place", "date_enev","heure_deb","heure_fin", "place_dispo", "img", "contact_Event"]
        widgets = {

            'title': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'description': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'date_enev': forms.DateInput(attrs={'type': 'date', 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
            
            'heure_deb': forms.TimeInput(attrs={
                'class': 'bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'min': '04:00',
                'max': '23:00',
                'value': '00:00',
                'required': True
            }),
            'heure_fin': forms.TimeInput(attrs={
                'class': 'bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'min': '04:00',
                'max': '23:00',
                'value': '00:00',
                'required': True
            }),
            'place_dispo': forms.NumberInput(attrs={'class': 'form-input mt-1 block w-full'}), 
            'contact_Event': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
        }
        
    
class MessageForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}))

    class Meta:
        model = Message
        fields = ['content']
        

class  ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = []