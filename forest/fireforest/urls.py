

from django.urls import path
from . import views
urlpatterns = [path("",views.index,name="index"),
            path("loginview",views.loginview,name="loginview"),
            path("signup",views.signup,name="signup"),
            path("processimg",views.processimg,name="processimg"),
            path("processredirect",views.processredirect,name="processredirect"),
             path("logoutview",views.logoutview,name="logoutview"),
           
            
    
]
