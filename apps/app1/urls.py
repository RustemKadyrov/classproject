from unicodedata import name
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

# from .views import index, index_2, index_3, admin_page, show
from app1.views import IndexView, LoginView

urlpatterns = [
    path('',                    IndexView.as_view(),  name='page_main'),
    path('show/<int:user_id>/', views.show,   name='page_show'),
    path('delete/',             views.delete, name='page_delete'),
    # path('about/',              views.about,  name='page_about'),
    # path('primitive/'           views.primitive, name='page_primitive'),
    
    path('register/', views.register, name='page_register'),
    path('login/',    LoginView.as_view(),    name='page_login'),
    path('logout/',   views.logout,   name='page_logout'),
]

# urlpatterns = [
#     path('',index),
#     path('main/',index_2),
#     path('second/',index_3),
#     path('admin/',admin_page),
#     path('show/',show),
#     path('__debug__/', include('debug_toolbar.urls')),
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

