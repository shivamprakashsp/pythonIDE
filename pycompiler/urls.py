
from django.urls import path, include
from django.contrib import admin

# import views

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),

     # Auth
    
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('saved/', views.savedcodes, name='savedcodes'),
    path('ide/', views.index, name="indexpage"),
    path('code/<int:code_pk>', views.viewcode, name='viewcode'),

    # path('runcode', views.runcode, name="run"),
]