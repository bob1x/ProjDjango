from itertools import chain
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import logout 
from django.shortcuts import redirect
from django.urls import reverse_lazy 
from .forms import LogementForm, PosteForm, RecommandationForm, StageForm, TransportForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required


from django.views.generic.edit import CreateView


from .models import Logement, Poste, Recommandation, Stage ,Transport

# Create your views here.

def index(request):
    recommandations = Recommandation.objects.all()
    transports = Transport.objects.all() 
    logements = Logement.objects.all()
    stages = Stage.objects.all()

    # Combine all types of postes into a single list
    postes = list(chain(recommandations, transports, logements, stages))

    return render(request, "index.html", {"postes": postes})



def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'authentication/signup.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")





@login_required

def poste_list(request):
    recommandations = Recommandation.objects.all()
    transports = Transport.objects.all() 
    logements = Logement.objects.all()
    stages = Stage.objects.all()

    postes = list(chain(recommandations, transports, logements, stages))
    
    return render(request, "poste/poste_list.html", {"postes": postes})

@login_required

def poste_create(request, post_type):
    
    switch = {
        'recommandation': RecommandationForm,
        'transport': TransportForm,
        'logement': LogementForm,
        'stage': StageForm,
       
    }
    form_class = switch.get(post_type, PosteForm)
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            form.save()
            return redirect('poste_list')
    else:
        form = form_class()
    
    return render(request, 'poste/poste_create.html', {'form': form})

@login_required

def poste_edit(request, id):
    poste_instance = None

    # Switch-like structure to determine the type of the Poste instance
    if Recommandation.objects.filter(id=id).exists():
        poste_instance = Recommandation.objects.get(id=id)
    elif Transport.objects.filter(id=id).exists():
        poste_instance = Transport.objects.get(id=id)
    elif Logement.objects.filter(id=id).exists():
        poste_instance = Logement.objects.get(id=id)
    elif Stage.objects.filter(id=id).exists():
        poste_instance = Stage.objects.get(id=id)

    if request.method == 'POST':
        form = PosteForm(request.POST,request.FILES, instance=poste_instance)
        if form.is_valid():
            form.save()
            return redirect('poste_list')
    else:
        form = PosteForm(instance=poste_instance)
    
    return render(request, 'poste/poste_edit.html', {'form': form})



@login_required

def poste_delete(request, id):
    # Determine the type of the Poste instance based on its child model
    poste_instance = None

    # Switch-like structure to determine the type of the Poste instance
    if Recommandation.objects.filter(id=id).exists():
        poste_instance = Recommandation.objects.get(id=id)
    elif Transport.objects.filter(id=id).exists():
        poste_instance = Transport.objects.get(id=id)
    elif Logement.objects.filter(id=id).exists():
        poste_instance = Logement.objects.get(id=id)
    elif Stage.objects.filter(id=id).exists():
        poste_instance = Stage.objects.get(id=id)

    if poste_instance:
        # If the instance exists, delete it
        poste_instance.delete()

    return redirect("poste_list")



def poste_details(request, id):
    # Determine the type of the Poste instance based on its child model
    poste_instance = None
    poste_type = None

    # Attempt to retrieve the Poste instance by ID
    try:
        # Try to get the Poste instance by ID from each child model
        poste_instance = Recommandation.objects.get(pk=id)
        poste_type = 'recommandation'
    except Recommandation.DoesNotExist:
        try:
            poste_instance = Transport.objects.get(pk=id)
            poste_type = 'transport'
        except Transport.DoesNotExist:
            try:
                poste_instance = Logement.objects.get(pk=id)
                poste_type = 'logement'
            except Logement.DoesNotExist:
                try:
                    poste_instance = Stage.objects.get(pk=id)
                    poste_type = 'stage'
                except Stage.DoesNotExist:
                    
                 return render(request, "poste/poste_detail.html", {"error": "Poste not found"})
    
    # Render the template with the appropriate data based on the Poste type
    return render(request, "poste/poste_detail.html", {"poste_instance": poste_instance, "poste_type": poste_type})