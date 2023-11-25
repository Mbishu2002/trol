
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    register,
    login,
    verify_user,
    get_user,
    update_user,
    send_password_reset_email,
    set_new_password,
    logout,
    follow_user,
    get_followers,
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('verify/<str:uidb64>/<str:token>/', verify_user, name='verify_user'),
    path('get_user/', get_user, name='get_user'),
    path('update_user/<str:user_id>/', update_user, name='update_user'),
    path('reset_password/', send_password_reset_email, name='send_password_reset_email'),
    path('set_new_password/', set_new_password, name='set_new_password'),
    path('logout/', logout, name='logout'),
    path('follow_user/', follow_user, name='follow_user'),
    path('get_followers/<str:user_id>/', get_followers, name='get_followers'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)