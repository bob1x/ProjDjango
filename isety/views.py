from itertools import chain
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import logout 
from django.shortcuts import redirect
from django.urls import reverse_lazy 
from .forms import CommentForm, ConversationForm, MessageForm, UserUpdateForm, LogementForm, PosteForm, RecommandationForm, StageForm, TransportForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Conversation, Message, Poste, Likes,User,Comment,Notification,FriendRequest
from django.db.models import Q

from .models import Logement, Poste, Recommandation, Stage ,Transport, Evenement,Intrested
from django.views.generic.edit import CreateView,UpdateView
from .forms import EventForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Count



# Create your views here.
POSTE_MODELS = {
    "recommandation": Recommandation,
    "transport": Transport,
    "logement": Logement,
    "stage": Stage,
}

def index(request):
    
    query = request.GET.get('q')
    if query:
        postes = Poste.objects.filter(
            Q(poste_field__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
        evenements = Evenement.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(place__icontains=query)
        )
    else:
        postes = Poste.objects.all()
        evenements = Evenement.objects.filter(date_enev__gte=timezone.now()).order_by('date_enev')

    # Get the user based on query parameter (email or first name)
    user_query = request.GET.get('user')
    if user_query:
        user = User.objects.filter(Q(email=user_query) | Q(first_name__icontains=user_query)).first()
        if user:
            postes = postes.filter(user=user)  # Filter postes by user
            evenements = evenements.filter(user=user)

    featured_postes = Poste.objects.order_by('-likes')[:6]
    featured_evenements = Evenement.objects.all()

    return render(request, "index.html", {
        "postes": postes,
        "evenements": evenements,
        "featured_postes": featured_postes,
        "featured_evenements": featured_evenements
    })

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST,request.FILES)
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
def profile_settings(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('poste_list')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'user/profile_settings.html', {'form': form})


@login_required
def send_friend_request(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not FriendRequest.objects.filter(from_user=request.user, to_user=user).exists():
        FriendRequest.objects.create(from_user=request.user, to_user=user)
        Notification.objects.create(
            sender=request.user,
            recipient=user,
            notification_type='friend_request',
            message=f'{request.user.first_name} {request.user.last_name} sent you a friend request.'
        )
    return redirect('profile', user_id=user_id)

@login_required
def accept_friend_request(request, friend_request_id):
    user_id = request.user.id
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id)
    if friend_request.to_user == request.user and not friend_request.is_accepted:
        friend_request.is_accepted = True
        friend_request.save()
        request.user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(request.user)
        Notification.objects.filter(sender=request.user, recipient=friend_request.from_user, notification_type='friend_request').delete()
        Notification.objects.create(
            sender=request.user,
            recipient=friend_request.from_user,
            notification_type='friend_request',
            message=f'{request.user.first_name} {request.user.last_name} accepted your friend request.'
        )
    return redirect('profile', user_id=user_id)

@login_required
def reject_friend_request(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
    return redirect('home')

@login_required
def remove_friend(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Remove user from current user's friends
    request.user.friends.remove(user)
    
    # Remove current user from user's friends
    user.friends.remove(request.user)
    
    # Delete any existing friend requests between the users
    FriendRequest.objects.filter(from_user=request.user, to_user=user).delete()
    FriendRequest.objects.filter(from_user=user, to_user=request.user).delete()
    
    return redirect('profile', user_id=user_id)

    
    



@login_required
def poste_list(request):
    user = request.user
    
    today = timezone.now()
    
    user_posts_count = Poste.objects.filter(user=user).count()
    user_events_count = Evenement.objects.filter(user=user).count()
    
    # Retrieve the list of friends for the current user
    friends = user.friends.all()
    
    # Retrieve all postes
    postes = []
    events =[]
    conversations = Conversation.objects.all()

    if request.GET.get("filter") == "my_posts":
        postes = list(chain(*[model.objects.filter(user=request.user) for model in POSTE_MODELS.values()]))
    elif request.GET.get("filter") == "my_events":
        events = Evenement.objects.filter(user=request.user)
    else:
        postes = list(chain(*[model.objects.filter(user=request.user) for model in POSTE_MODELS.values()]))
    
    return render(request, "poste/poste_list.html", {"postes": postes, "friends": friends ,"events": events , "today": today,
                                                     "user_posts_count": user_posts_count, "user_events_count": user_events_count,'conversations': conversations})

@login_required
def poste_create(request, type_p, id=None):
    switch = {
        'recommandation': RecommandationForm,
        'transport': TransportForm,
        'logement': LogementForm,
        'stage': StageForm,
    }

    form_class = switch.get(type_p, PosteForm)

    # If an ID is provided, fetch the existing poste instance
    if id:
        poste_instance = get_object_or_404(Poste, pk=id)
        # Determine the actual subclass instance
        if isinstance(poste_instance, Recommandation):
            form_class = RecommandationForm
        elif isinstance(poste_instance, Transport):
            form_class = TransportForm
        elif isinstance(poste_instance, Logement):
            form_class = LogementForm
        elif isinstance(poste_instance, Stage):
            form_class = StageForm
        else:
            form_class = PosteForm
    else:
        poste_instance = None

    if request.method == 'POST':
        if poste_instance:
            form = form_class(request.POST, request.FILES, instance=poste_instance)
        else:
            form = form_class(request.POST, request.FILES)
        if form.is_valid():
            poste = form.save(commit=False)
            poste.user = request.user
            poste.poste_field = type_p
            poste.save()
            return redirect('poste_list')
    else:
        if poste_instance:
            form = form_class(instance=poste_instance)
        else:
            form = form_class()

    return render(request, 'poste/poste_create.html', {'form': form, 'type_p': type_p, 'poste_instance': poste_instance})

@login_required
@csrf_exempt
@require_POST
def poste_edit(request, id):
    poste_instance = get_object_or_404(Poste, id=id)

    # Determine the type of Poste instance and initialize the corresponding form
    if isinstance(poste_instance, Recommandation):
        form = RecommandationForm(request.POST or None, request.FILES or None, instance=poste_instance)
    elif isinstance(poste_instance, Transport):
        form = TransportForm(request.POST or None, request.FILES or None, instance=poste_instance)
    elif isinstance(poste_instance, Logement):
        form = LogementForm(request.POST or None, request.FILES or None, instance=poste_instance)
    elif isinstance(poste_instance, Stage):
        form = StageForm(request.POST or None, request.FILES or None, instance=poste_instance)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid Poste instance'})

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


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
        poste_instance.delete()

    return redirect("poste_list")




def poste_details(request, id):
    # Attempt to retrieve the Poste instance by ID
    poste_instance = get_object_or_404(Poste, pk=id)
    type_p = None
    new_comment = None

    if isinstance(poste_instance, Recommandation):
        type_p = 'recommandation'
    elif isinstance(poste_instance, Transport):
        type_p = 'transport'
    elif isinstance(poste_instance, Logement):
        type_p = 'logement'
    elif isinstance(poste_instance, Stage):
        type_p = 'stage'
    else:
        type_p = None

    # Fetch comments associated with the poste_instance
    comments = Comment.objects.filter(poste=poste_instance)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.poste = poste_instance
            new_comment.user = request.user
            new_comment.save()
            
            # Trigger notification if the comment author is not the post owner
            if poste_instance.user != request.user:
                Notification.objects.create(
                    sender=request.user,
                    recipient=poste_instance.user,
                    notification_type='comment',
                    message=f"{request.user.first_name} has commented on your post."
                )
        
        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            if comment.user == request.user or request.user.is_staff:
                comment.delete()
                # Delete the associated notification
                Notification.objects.filter(
                    sender=request.user,
                    recipient=poste_instance.user,
                    notification_type='comment',
                    message=f"{request.user.first_name} has commented on your post."
                ).delete()
                return redirect('poste_detail', id=poste_instance.pk)
            else:
                return HttpResponseForbidden("You are not allowed to delete this comment.")
    else:
        comment_form = CommentForm()
    
    # Check if the user has liked the post
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = poste_instance.user_has_liked(request.user)
    
    post_user = poste_instance.user
     
    return render(request, "poste/poste_detail.html", {
        "poste_instance": poste_instance,
        "type_p": type_p,
        "user_has_liked": user_has_liked,
        "post_user": post_user,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'comments': comments,  # Pass comments to the template
    })

@login_required
def like(request, post_id):
    user = request.user
    poste = get_object_or_404(Poste, id=post_id)
    current_likes = poste.likes
    liked = Likes.objects.filter(user=user, poste=poste).count()

    if not liked:
        Likes.objects.create(user=user, poste=poste)
        current_likes += 1
    else:
        Likes.objects.filter(user=user, poste=poste).delete()
        current_likes -= 1
    
    # Trigger notification if the liker is not the post owner
    if not liked and poste.user != request.user:
        Notification.objects.create(
            sender=request.user,
            recipient=poste.user,
            notification_type='like',
            message=f"{request.user.first_name} liked your post."
        )
    
    poste.likes = current_likes
    poste.save()
    
    return HttpResponseRedirect(reverse('poste_detail', args=[post_id]))

def profile_user(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    user_posts_count = Poste.objects.filter(user=profile_user).count()
    user_events_count = Evenement.objects.filter(user=profile_user).count()
    user_posts = []
    user_events =[]
    
    if request.GET.get("filter") == "hes_posts":
        user_posts = Poste.objects.filter(user=profile_user)  # Assuming your Poste model has a ForeignKey to User
    elif  request.GET.get("filter") == "hes_events":
        user_events = Evenement.objects.filter(user=profile_user)
    else: 
        user_posts = Poste.objects.filter(user=profile_user)  # Assuming your Poste model has a ForeignKey to User


    context = {
        'profile_user': profile_user,
        'user_posts': user_posts,
        'user_events': user_events,
        'user_events_count': user_events_count,
        'user_posts_count': user_posts_count,
    }
    return render(request, 'user/profile_user.html', context)



@login_required
def clear_notifications(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect('home')


class EvenementCreateView(CreateView):
    model = Evenement
    form_class = EventForm
    template_name = 'event/event_create.html'
    success_url = reverse_lazy('poste_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def event_delete(request, id):
    event = get_object_or_404(Evenement, id=id)
    event.delete()
    return redirect('poste_list')

def my_events(request):
    user = request.user
    today = timezone.now()
    
    # Retrieve the list of friends for the current user
    friends = user.friends.all()
    
    # Retrieve events the user is interested in
    interested_events = Intrested.objects.filter(user=user).select_related('event')

    return render(request, "event/my_events.html", {
        "interested_events": interested_events,
        "friends": friends,
        "today": today
    })

def event_list(request):
      # Filter events that have a date greater than or equal to the current time
    events = Evenement.objects.filter(date_enev__gte=timezone.now())
    
    # Delete events that have already passed
    past_events = Evenement.objects.filter(date_enev__lt=timezone.now())
    past_events.delete()
    
   
    most_liked_event = Evenement.objects.annotate(
        num_interests=Count('event_intrest')
    ).order_by('-num_interests').first()
    
    return render(request, 'event/event_list.html', {
        'events': events,
        'most_liked_event': most_liked_event
        # 'most_liked': most_liked
    })

def event_detail(request, id):


    event = get_object_or_404(Evenement, pk=id)
    interested_users = Intrested.objects.filter(event=event).select_related('user')

    interested_count = event.interest  # Assuming interested is the related name
    return render(request, 'event/event_details.html', {'event': event, 'interested_count': interested_count,
                                                        'interested_users': interested_users})

@require_POST
@login_required

def interested(request, event_id):
    event = get_object_or_404(Evenement, id=event_id)
    user_interest = Intrested.objects.filter(user=request.user, event=event)

    if user_interest.exists():
        # User is already interested, so remove the interest
        user_interest.delete()
        event.place_dispo += 1
        event.save()

        return JsonResponse({'status': 'ok', 'action': 'removed', 'place_dispo': event.place_dispo})
    else:
        # User is not interested, so add the interest
        Intrested.objects.create(user=request.user, event=event)
        if event.place_dispo > 0:
            event.place_dispo -= 1
            event.save()

            # Create a notification if the event user is not the same as the interested user
            if event.user != request.user:
                Notification.objects.create(
                    sender=request.user,
                    recipient=event.user,
                    notification_type='interested',
                    message=f"{request.user.first_name} is interested in your event {event.title}."
                )

            return JsonResponse({'status': 'ok', 'action': 'added', 'place_dispo': event.place_dispo})
    
    return JsonResponse({'status': 'error', 'message': 'An error occurred.'})





@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.all()

    # If the current user is not part of the conversation participants, redirect
    if request.user not in conversation.participants.all():
        return redirect('poste_list')  # Redirect to wherever you want
        
    # Handle message submission
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            sender = request.user
            content = form.cleaned_data['content']
            Message.objects.create(conversation=conversation, sender=sender, content=content)
            return redirect('conversation_detail', conversation_id=conversation_id)
    else:
        form = MessageForm()

    return render(request, 'conversation.html', {'conversation': conversation, 'messages': messages, 'form': form})


def create_message(request, conversation_id):
    conversation = Conversation.objects.get(id=conversation_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            sender = request.user
            
            # Create and save the new message
            message = Message.objects.create(conversation=conversation, sender=sender, content=content)
            
            # Redirect to the conversation detail page
            return redirect('conversation_detail', conversation_id=conversation_id)
    else:
        form = MessageForm()
    
    return render(request, 'conversation/create_message.html', {'form': form})


@login_required
def create_conversation(request,user_id):
    if request.method == 'POST':
        # Get the participant IDs from the form data
        participant_ids = [request.user.id, user_id]

        # Create a new conversation object
        conversation = Conversation.objects.create()

        # Add participants to the conversation
        conversation.participants.add(*participant_ids)

        # Redirect to the conversation detail page 
        return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        # Handle GET request
        return render(request, 'create_conversation.html')



def help(request):
    return render(request, 'help.html')