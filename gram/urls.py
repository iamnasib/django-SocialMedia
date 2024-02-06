from django.urls import path,include,re_path
from . import views
from .views import SignupView,CustomLoginView,ResetPasswordView,ChangePasswordView,PostUpdateView,Home
from django.contrib.auth import views as auth_views
from .forms import LoginForm
import notifications.urls
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(Home.as_view()), name='home'),
    path('home', login_required(Home.as_view()), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='gram/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path("follow/",views.followToggle, name="follow"),
    path("follow-requests/",views.followRequestList, name="request-list"),
    path("accept-request/",views.acceptRequest, name="accept-request"),
    path("delete-request/",views.deleteRequest, name="delete-request"),
    path("remove-follower/",views.removeFollower, name="remove-follower"),
    path("remove-following/",views.removeFollowing, name="remove-following"),
    path("block-user/",views.blockUser, name="block-user"),
    path("blocked-users/",views.blockedUsersList, name="blocked-users"),
    
    #path("follow-request/<str:requested_by_user>/",views.followRequestToggle, name="follow-request"),
    path("upload-post/",views.UploadPost, name="upload-post"),
    path("tale/",views.upload_tales, name="tale"),
    path('edit-post/<int:pk>',PostUpdateView.as_view(), name='edit-post'),
    path("view-post/<int:id>/",views.view_post,name='view-post'),
    path("saved-posts/",views.savedPostsList,name='saved-post'),
    path("add-repository/",views.repositoryPost,name='add-repository'),
    path("repository/",views.repositoryList,name='repository'),
    path("search", views.search, name='search'),
    path("email-verification", views.email_verification, name='email-verification'),
    path("like/",views.likeToggle, name="like"),
    path("likes/<int:id>",views.likeList, name="likeList"),
    path("email-otp/<str:username>/<str:email>",views.email_otp,name='email-otp'),
    path("delete-user",views.delete_user,name='delete-user'),
    path("deactivate-user",views.deactivate_user,name='deactivate-user'),
    path("delete-post/<int:id>/",views.delete_post,name='delete-post'),
    path("save/",views.savePost, name="save"), 
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='gram/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view()),

    path('webpush/', include('webpush.urls')),
    #Notification
    path('notifications',views.notifications, name='notifications'),
    re_path(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    # add this new url entry to include the social auth's urls
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path('<str:username>/followers',views.followers,name='followers'),
    path('<str:username>/following',views.following,name='following'),
    path('<str:username>',views.profile,name='profile'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]