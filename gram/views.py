import datetime
from distutils.log import log
from itertools import chain
import json
import math
from multiprocessing import context
import random
from turtle import pos
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, DeleteView
from django.db.models import Q
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from notifications.signals import notify
from django.urls import resolve
from notifications.models import Notification
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.db.models.functions import Now
from datetime import timedelta
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification

from . models import MyUser, Posts, Like, Comments,Tales,IsSaved
from .forms import SignupForm, LoginForm, UpdateUserForm, UploadPostForm, EditPostForm, NewCommentForm,TalesForm

# Create your views here.


class SignupView(View):
    form_class = SignupForm
    initial = {'key': 'value'}
    template_name = 'gram/signup.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(SignupView, self).dispatch(request)

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_deactivated = True
            obj.save()

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(
                request, 'Account created successfully, verify your email to continue')
            return redirect('email-otp', username, email)
        return render(request, self.template_name, {'form': form})

# Class based view that extends from the built in login view to add a remember me functionality


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        username = form.cleaned_data.get('username')
        user = MyUser.objects.get(username=username)
        email = user.email
        if user.is_deactivated:
            #form.add_error('Verify your email to reactivate your account')
            messages.success(
                self.request, 'Verify your email to reactivate your account')
            return redirect('email-otp', username, email)
        else:
            if not remember_me:
                # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
                self.request.session.set_expiry(0)

                # Set session as modified to force data updates/cookie to be saved.
                self.request.session.modified = True

            # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
            return super(CustomLoginView, self).form_valid(form)


class Home(ListView, LoginRequiredMixin):
    model = Posts
    template_name = 'gram/home.html'
    context_object_name = 'posts'
    paginate_by = 15
    Tales.objects.filter(uploaded_on__lt=Now()-timedelta(days=1)).delete()
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        
        stories=[]
        
        userobj = MyUser.objects.get(username=self.request.user.username)
        following = userobj.followers.all()
        user_list=list(following)
        user_list.append(userobj)
        for user in user_list:
            if user.tales.all():
                items=[]
                for tale in user.tales.all():
                    items.append({
                        "id": tale.id, 
                        "type": "",
                        "length": 3,
                        "src": f'/media/{tale.file}',
                        "time":datetime.datetime.timestamp(tale.uploaded_on)*1000 ,
                        
                    })
                stories.append({
                    "id": user.id, 
                    "photo": f'/media/{user.DP}',
                    "items": items,
                    "name": user.username,  
                })
        
        posts_obj = Posts.objects.filter(
            user__in=user_list,in_repository=False).order_by('-uploaded_on')
        if self.request.user.is_authenticated:
            liked = [i for i in posts_obj if Like.objects.filter(
                user=self.request.user, post=i)]
            saved = [j for j in posts_obj if IsSaved.objects.filter(
                user=self.request.user, post=j)]
            context['liked_post'] = liked
            context['posts'] = posts_obj
            context['saved'] = saved
            context['stories']=json.dumps(stories)
        return context

@login_required
def upload_tales(request):
    tale_form = TalesForm()
    if request.method == 'POST':
        tale_form = TalesForm(request.POST or None, request.FILES or None)
        if tale_form.is_valid():
            obj = tale_form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(to='home')
    else:
        tale_form = TalesForm()
    return render(request, 'gram/upload_tale.html', context={'tale_form': tale_form})

@login_required
def likeToggle(request):
    post_id = request.GET.get("likeId", "")
    user = request.user
    post = Posts.objects.get(pk=post_id)
    user_id = post.user.id
    img = post.post_image.url
    caption = post.caption
    receiver = MyUser.objects.get(id=user_id)
    liked = False
    like = Like.objects.filter(user=user, post=post)
    likes = Like.objects.filter(post=post)
    loveCount = likes.count()
    if like:
        like.delete()
        notify.send(user, recipient=receiver, verb='unloved your post',
                    description=img, pid=post_id, caption=caption, category="love")
        if Notification.objects.filter(actor_object_id=user.id,recipient=receiver, verb='loved your post',
                    description=img, ).exists():
                    Notification.objects.filter(actor_object_id=user.id,recipient=receiver, verb='loved your post',
                    description=img, ).delete()
                    print("he")
        
    else:
        liked = True
        Like.objects.create(user=user, post=post)
        if loveCount >= 1:
            
            if Notification.objects.filter(actor_object_id=user.id,recipient=receiver, verb='unloved your post',
                        description=img, ).exists():
                        Notification.objects.filter(actor_object_id=user.id,recipient=receiver, verb='unloved your post',
                        description=img, ).delete()
            dict={"pid": post_id, "caption": caption,
                                    "category": "love","concatenation": True}
                                    
            Notification.objects.filter(recipient=receiver,
                        description=img, data=dict).delete() 
            n_verb=f'and {loveCount} others loved your post'
            notify.send(user, recipient=receiver, verb=n_verb,
                    description=img, pid=post_id, caption=caption, category="love",concatenation=True)
        else:
            notify.send(user, recipient=receiver, verb='loved your post',
                        description=img, pid=post_id, caption=caption, category="love")
            if Notification.objects.filter(actor_object_id=user.id,recipient=receiver, verb='unloved your post',
                        description=img, ).exists():
                        Notification.objects.filter(actor_object_id=user.id,recipient=receiver, verb='unloved your post',
                        description=img, ).delete()
                        

    resp = {
        'liked': liked,
        'loveCount': loveCount
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")

@login_required
def likeList(request,id):
    if Posts.objects.filter(pk=id).exists():
        post = Posts.objects.get(pk=id)
        if request.user in post.user.followers.all() or post.user.is_private==False or request.user==post.user:
            likes = Like.objects.filter(post=post)
            context={'likes':likes}
            return render(request,'gram/likes_list.html',context)
        else:
            return HttpResponse("not your post")
    else:
        return HttpResponse("not your post")
def profile(request, username):
    if MyUser.objects.filter(username=username).exists():
        userobj = MyUser.objects.get(username=username)

        following = userobj.followers.all()
        follower = userobj.following.all()
        # userobj.requested_by.remove(17)
        context = {}
        posts = userobj.posts_set.filter(in_repository=False).order_by('-id')
        disabled = True
        hits = 0
        if request.user.is_authenticated:
            current_user = MyUser.objects.get(username=request.user.username)
            if userobj in current_user.blocked_user.all() or userobj in current_user.blocked_by.all():
                return HttpResponse("blocked")
            else:
                # hitcount logic
                hit_count = get_hitcount_model().objects.get_for_object(userobj)
                hits = hit_count.hits
                if request.user.username != username:
                    
                    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
                    hit_count_response = HitCountMixin.hit_count(
                        request, hit_count)
                    if hit_count_response.hit_counted:
                        hits = hits + 1
                        hitcontext['hit_counted'] = hit_count_response.hit_counted
                        hitcontext['hit_message'] = hit_count_response.hit_message
                        hitcontext['total_hits'] = hits
                        
                if username != current_user.username:
                    if current_user in follower:
                        disabled = False
                elif username == current_user.username:
                    disabled = False
            liked = [i for i in posts if Like.objects.filter(
                user=request.user, post=i)]
            saved = [j for j in posts if IsSaved.objects.filter(
                user=request.user, post=j)]
       
        context = {"userobj": userobj, "following": following, "posts": posts,
                   "follower": follower, "disabled": disabled, "total_hits": hits,
                   "liked_post":liked,"saved":saved}
        return render(request, 'gram/profile.html', context)
    else:
        return HttpResponse("not found")


@login_required
def blockUser(request):
    blockUser = request.GET.get("user", "")
    user_profile = MyUser.objects.get(id=blockUser)
    current_user = MyUser.objects.get(username=request.user.username)
    blocked = True
    if user_profile in current_user.blocked_user.all():
        current_user.blocked_user.remove(user_profile.id)
        blocked = False
    else:
        user_profile.following.remove(current_user.id)
        user_profile.followers.remove(current_user.id)
        user_profile.requested_by.remove(current_user.id)
        user_profile.requested_to.remove(current_user.id)
        current_user.blocked_user.add(user_profile.id)
    resp = {
        'blocked': blocked,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")


@login_required
def blockedUsersList(request):
    current_user = MyUser.objects.get(username=request.user.username)
    blocked_users = current_user.blocked_user.all()
    context = {'blocked_users': blocked_users}
    return render(request, 'gram/blocked_users.html', context=context)


@login_required
def UploadPost(request):
    post_form = UploadPostForm()
    if request.method == 'POST':
        post_form = UploadPostForm(request.POST or None, request.FILES or None)
        if post_form.is_valid():
            obj = post_form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(to='home')
    else:
        post_form = UploadPostForm()
    return render(request, 'gram/upload_post.html', context={'post_form': post_form})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    
    fields = ['caption', 'post_image','comments_disabled']
    template_name = 'gram/edit_post.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return redirect('home')
        return False


@login_required
def view_post(request, id):
    if Posts.objects.filter(id=id,in_repository=False).exists():
        user = MyUser.objects.get(username=request.user)
        post = Posts.objects.get(id=id,in_repository=False)
        is_liked = Like.objects.filter(user=user, post=post)
        post_user = post.user
        follower = post_user.following.all()
        img = post.post_image.url
        caption = post.caption
        saved =IsSaved.objects.filter(user=request.user, post=post)
        if post_user in user.blocked_user.all() or post_user in user.blocked_by.all():
            return HttpResponse("not found")
        else:
            if user in follower or user == post_user or post_user.is_private == False:
                if request.method == 'POST':
                    form = NewCommentForm(request.POST)
                    if form.is_valid():
                        comment = form.cleaned_data.get('comment')
                        data = form.save(commit=False)
                        data.post = post
                        data.user = user
                        data.save()
                        if post_user == request.user:
                            return redirect('view-post', id=id)
                        else:
                            notify.send(user, recipient=post_user, verb='commented on your post', description=img,
                                        pid=id, category="comment", comment=comment)
                            return redirect('view-post', id=id)
                else:
                    form = NewCommentForm()
                context={'post': post, 'is_liked': is_liked, 'form': form,'saved':saved}
                return render(request, 'gram/post_single.html', context)
            #current_url = resolve(request.path_info).url_name
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse("error")

@login_required
def savePost(request):
    post = request.GET.get("post", "")
    user_post = Posts.objects.get(id=post)
    isSaved=IsSaved.objects.filter(user=request.user,post=user_post)
    saved = False
    if isSaved:
        isSaved.delete()
    else:
        IsSaved.objects.create(user=request.user,post=user_post)
        saved = True
    resp = {
        'saved': saved,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")

@login_required
def savedPostsList(request):
    isSaved=IsSaved.objects.filter(user=request.user).order_by('-id')
    # posts_obj=Posts.objects.filter(user=isSaved.post.user)
    liked = [i for i in isSaved if Like.objects.filter(
                user=request.user, post=i.post)]
    
    context={"isSaved":isSaved,"liked_post":liked}
    return render(request,"gram/saved_posts_list.html",context)

@login_required
def repositoryPost(request):
    post = request.GET.get("post", "")
    user_post = Posts.objects.get(id=post)
    isSaved=IsSaved.objects.filter(user=request.user,post=user_post)
    repository = False
    if user_post.in_repository==False:
        if isSaved:
            isSaved.delete()
            user_post.in_repository=True
            user_post.save()
            repository=True
        else:
            user_post.in_repository=True
            user_post.save()
            repository = True
    else:
        user_post.in_repository=False
        user_post.save()
    resp = {
        'repository': repository,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")

@login_required
def repositoryList(request):
   posts_obj = Posts.objects.filter(user=request.user,in_repository=True).order_by('-id')
   liked = [i for i in posts_obj if Like.objects.filter(
                user=request.user, post=i)]
   context={"posts":posts_obj,"liked_post":liked}
   return render(request,"gram/repository_list.html",context)

@login_required
def followToggle(request):
    followUser = request.GET.get("by_user", "")
    user_profile = MyUser.objects.get(id=followUser)
    current_user = MyUser.objects.get(username=request.user.username)
    followers = user_profile.following.all()
    requested_by = user_profile.requested_by.all()
    requested_to = user_profile.requested_to.all()
    dp = current_user.DP.url
    action = "follow"
    if user_profile.username != current_user.username:
        if current_user in followers:
            user_profile.following.remove(current_user.id)
            Notification.objects.filter(actor_object_id=current_user.id,recipient=user_profile,
                     verb='started following you').delete()
        else:
            if user_profile.is_private:
                if current_user in requested_by:
                    user_profile.requested_by.remove(current_user.id)
                else:
                    action = "requested"
                    user_profile.requested_by.add(current_user.id)
                    if Notification.objects.filter(actor_object_id=current_user.id,recipient=user_profile,
                                verb='started following you').exists():
                        Notification.objects.filter(actor_object_id=current_user.id,recipient=user_profile,
                                    verb='started following you').delete()
                    Notification.objects.filter(actor_object_id=current_user.id,recipient=user_profile,
                     verb='requested to follow you').delete()
                    notify.send(current_user, recipient=user_profile, verb='requested to follow you', description=dp,
                                    category="followRequest")
            else:
                if current_user in requested_to:
                    user_profile.requested_to.remove(current_user.id)
                    user_profile.followers.add(current_user.id)
                else:
                    action = "unfollow"
                    user_profile.following.add(current_user.id)
                    if Notification.objects.filter(actor_object_id=current_user.id,recipient=user_profile,
                     verb='requested to follow you').exists():
                        Notification.objects.filter(actor_object_id=current_user.id,recipient=user_profile,
                     verb='requested to follow you').delete()
                    Notification.objects.filter(actor_object_id=current_user.id,recipient=user_profile,
                     verb='started following you').delete()
                    notify.send(current_user, recipient=user_profile, verb='started following you', description=dp,
                                    category="followRequest")
    resp = {
        'action': action,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")
    # return HttpResponseRedirect(reverse(profile, args=[user_profile.username]))

@login_required
def acceptRequest(request):
    requestedByUser = request.GET.get("by_user", "")
    user_profile = MyUser.objects.get(id=requestedByUser)
    current_user = MyUser.objects.get(username=request.user.username)
    followers = user_profile.following.all()
    requested_by = user_profile.requested_by.all()
    requested_to = user_profile.requested_to.all()
    dp = current_user.DP.url
    action = "follow"
    if current_user in requested_to:
        user_profile.requested_to.remove(current_user.id)
        user_profile.followers.add(current_user.id)
        if current_user in followers:
            action = "unfollow"
        elif current_user in requested_by:
            action= "requested"
    elif current_user in followers:
        user_profile.following.remove(current_user.id)
    elif current_user in requested_by:
        user_profile.requested_by.remove(current_user.id)
    else:
        if user_profile.is_private:
            action = "requested"
            user_profile.requested_by.add(current_user.id)
            notify.send(current_user, recipient=user_profile, verb='requested to follow you', description=dp,
                                    category="followRequest")
            if Notification.objects.filter(actor_object_id=current_user.id,recipient=user_profile,
                     verb='started following you').exists():
                        Notification.objects.filter(actor_object_id=current_user.id,recipient=user_profile,
                     verb='started following you').delete()
        else:
            user_profile.followers.add(current_user.id)
            action = "unfollow"
            notify.send(current_user, recipient=user_profile, verb='started following you', description=dp,
                                    category="followRequest")
            if Notification.objects.filter(actor_object_id=current_user.id,recipient=user_profile,
                     verb='requested to follow you').exists():
                        Notification.objects.filter(actor_object_id=current_user.id,recipient=user_profile,
                     verb='requested to follow you').delete()
                
    resp = {
        'action': action,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")

@login_required
def deleteRequest(request):
    requestedByUser = request.GET.get("by_user", "")
    user_profile = MyUser.objects.get(id=requestedByUser)
    current_user = MyUser.objects.get(username=request.user.username)
    requested_to = user_profile.requested_to.all()
    deleted=False
    if current_user in requested_to:
        user_profile.requested_to.remove(current_user.id)
        deleted = True
    resp = {
        'deleted': deleted,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")

@login_required
def followRequestList(request):
    if request.user.is_private:
        return render(request,'gram/follow_request_list.html')
    else:
        return HttpResponse("not private")

@login_required
def removeFollower(request):
    removeFollower = request.GET.get("to_remove_user", "")
    user_profile = MyUser.objects.get(id=removeFollower)
    current_user = MyUser.objects.get(username=request.user.username)
    removed = True
    following=True
    if user_profile in current_user.following.all():
        current_user.following.remove(removeFollower)
    else:
        current_user.following.add(removeFollower)
        removed = False
    resp = {
        'removed': removed,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")
@login_required
def removeFollowing(request):
    removeFollowing = request.GET.get("to_remove_user", "")
    user_profile = MyUser.objects.get(id=removeFollowing)
    current_user = MyUser.objects.get(username=request.user.username)
    removed = True
    following=True
    if user_profile in current_user.followers.all():
        current_user.followers.remove(removeFollowing)
    else:
        current_user.followers.add(removeFollowing)
        removed = False
    resp = {
        'removed': removed,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(
            request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was updated successfully')
            return redirect(to='edit-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
    return render(request, 'gram/edit_profile.html', {'user_form': user_form})


@login_required
def followers(request, username):
    if MyUser.objects.filter(username=username).exists():
        user_profile = MyUser.objects.get(username=username)
        current_user = MyUser.objects.get(username=request.user.username)
        followers = user_profile.following.all()
        if current_user in followers:
            context = {"user_profile": user_profile, "followers": followers}
            return render(request, 'gram/followers.html', context)
        elif current_user == user_profile:
            context = {"user_profile": user_profile, "followers": followers}
            return render(request, 'gram/followers.html', context)
        else:
            return redirect('profile', username=user_profile.username)

    else:
        return HttpResponse("not found")


@login_required
def following(request, username):
    if MyUser.objects.filter(username=username).exists():
        user_profile = MyUser.objects.get(username=username)
        following = user_profile.followers.all()
        current_user = MyUser.objects.get(username=request.user.username)
        followers = user_profile.following.all()
        if current_user in followers:
            context = {"user_profile": user_profile, "following": following}
            return render(request, 'gram/following.html', context)
        elif current_user == user_profile:
            context = {"user_profile": user_profile, "following": following}
            return render(request, 'gram/following.html', context)
        else:
            return redirect('profile', username=user_profile.username)

    else:
        return HttpResponse("not found")


@login_required
def search(request):
    ctx = {}
    users = ()
    url_parameter = request.GET.get("q")

    if url_parameter:
        users = MyUser.objects.filter(Q(full_name__icontains=url_parameter) | Q(
            username__icontains=url_parameter)).exclude(blocked_by=request.user)
        ctx["users"] = users

    does_req_accept_json = request.accepts("application/json")
    is_ajax_request = request.headers.get(
        "x-requested-with") == "XMLHttpRequest" and does_req_accept_json

    if is_ajax_request:
        html = render_to_string(
            template_name="gram/users-results-partial.html",
            context={"users": users}
        )
        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, "gram/search.html", context=ctx)


def email_otp(request, username, email):
    subject, from_email, to = 'OTP', settings.EMAIL_HOST_USER, email
    text_content = ''
    otp_new = generateOTP()
    html_con1 = render_to_string('gram/email_temp.html')
    html_con2 = html_con1.replace("no-opt-is-here", otp_new)
    html_con3 = html_con2.replace("username-is-here", username)
    html_content = html_con3
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    request.session['otp_new'] = otp_new
    request.session['username'] = username
    return redirect(to='email-verification')


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def email_verification(request):
    username = request.session.get('username')
    if MyUser.objects.filter(username=username).exists():
        if request.method == 'POST':
            otp_new = request.session.get('otp_new')
            user = MyUser.objects.get(username=username)
            otp = request.POST.get('otp')
            if otp_new == otp:
                user.is_deactivated = False
                user.save()
                messages.success(
                    request, 'Email verified successfully, Login to continue')
                request.session['otp_new'] = ""
                request.session['username'] = ""
                return redirect(to='login')
            else:
                messages.error(request, 'Incorrect OTP')
        return render(request, "gram/email_verification.html")
    else:
        return HttpResponse("not")


@login_required
def notifications(request):
    user = MyUser.objects.get(username=request.user.username)
    blocked_user = user.blocked_user.all()
    blocked_by = user.blocked_by.all()
    user.notifications.mark_all_as_read()
    notifications = Notification.objects.filter(
        recipient=user).exclude(actor_object_id__in=blocked_user)
    context = {"notifications": notifications}
    return render(request, "gram/notifications.html", context=context)


@login_required
def delete_user(request):
    user = MyUser.objects.get(username=request.user.username)
    user.delete()
    messages.success(request, "Account deleted successfully")

    return redirect('login')


@login_required
def delete_post(request, id):
    post = Posts.objects.get(id=id)
    post.delete()

    return redirect('profile', username=request.user.username)


@login_required
def deactivate_user(request):
    user = MyUser.objects.get(username=request.user.username)
    user.is_deactivated = True
    user.save()
    logout(request)
    messages.success(
        request, "Account has been deactivated, Login to reactivate your account")

    return redirect('login')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'gram/password_reset.html'
    email_template_name = 'gram/password_reset_email.html'
    subject_template_name = 'gram/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'gram/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')
