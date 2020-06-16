from django.urls import path

from . import views

app_name = 'shumeipai'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register/api/ajax/', views.register_ajax, name='register_ajax'),
    path('home/', views.home, name='home'),
    path('api/login/', views.login, name='login'),
    path('api/login_ajax/', views.login_ajax, name='login_ajax'),
    path('api/captcha/', views.captcha_, name='captcha'),
    path('api/insert_data/', views.insert_data, name='insert_data'),
    path('home/api/logout/', views.logout, name='logout'),
    path('home/api/search/', views.search, name='search'),
    path('home/api/limited/', views.limited, name='limited'),
    path('home/api/configure/', views.configure, name='configure'),
    path('home/api/configure/delete/', views.configure_delete, name='configure_delete'),
    path('home/api/configure/update/', views.configure_update, name='configure_update'),
    path('home/api/configure/insert/', views.configure_insert, name='configure_insert'),
    path('home/api/search/delete_update/', views.search_delete_update, name="delete_update"),
    path('home/api/get_excel_data/', views.get_excel_data, name='get_excel_data'),
    path('home/api/get_echarts_data/', views.get_echarts_data, name="get_echarts_data"),

]
