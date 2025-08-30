from django.urls import path
from.views import UserSignupView,AdminSignupView,LoginView,RefreshTokenView,Logoutview,Forgetpassword,Resetpassword

urlpatterns = [
    path('signup/',UserSignupView.as_view(),name='user-create'),
    path('create-admin',AdminSignupView.as_view(),name='admin-create'),

    # Auth with tokens
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', Logoutview.as_view(), name='logout'),

    #otp & forgot password
    path('forgot-password',Forgetpassword.as_view(), name='password-forget'),

    #reset newpassword
    path('reset-password',Resetpassword.as_view(), name='password-reset')

]
