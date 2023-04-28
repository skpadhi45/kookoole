"""kookoole URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
 
from django.contrib import admin
from django.urls import path

#media setup
from django.conf import settings
from django.conf.urls.static import static

#import views
from kookoole import views
from kookooleShop.middlewares.auth import auth_middleware


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('',views.shopPage ,name='homePage'),
    path('sign-up/',views.signupPage , name='signupPage'),
    path('log-in/',views.loginPage),
    path('log-out/',views.Logout) ,
    path('cart-in/',views.Cart , name='cart') ,
     
    path('check-out/',auth_middleware(views.CheckOut)) ,
    path('orders-status/',views.OrdersStatus) ,
    path('manage-orders/',views.Cancelation) ,
    path('search-products/',views.Search) ,
    path('thanks/',views.Thanks) ,
    
    
]
#MEDIA SETUP
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
