from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns =[
     path('', views.home,name='home'),
     path('signup/', views.signup,name='signup'),
     path('signin/', views.signin,name='signin'),
     path('signout/', views.signout,name='signin'),
     path('email-login/', views.emailLogin,name='home'),
     path('create-blog/', views.createblog,name='create-blog'),
     path('publish-blog/', views.publish_blog,name='publish-blog'),
     path('get-blogs/', views.get_blogs,name='get-blogs'),
     path('showblog/<int:id>', views.showblog,name='get-blogs'),
     path('view-blog-list', views.myBlogs,name='get-blogs'),
]
