from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('public_records/new/', views.create_public_record, name='create_public_record'),
    path('public_records/', views.list_public_records, name='list_public_records'),
    
    
    path('marriage_licenses/new/', views.create_marriage_license, name='create_marriage_license'),
    path('marriage_licenses/', views.list_marriage_license_records, name='list_marriage_license_records'),
      path('marriage_licenses/<int:pk>/', views.view_marriage_license, name='view_marriage_license'),
     path('marriage_licenses/<int:pk>/update/', views.update_marriage_license, name='update_marriage_license'),
    path('marriage_licenses/<int:pk>/delete/', views.delete_marriage_license, name='delete_marriage_license'),


    path('property_deeds/new/', views.create_property_deed, name='create_property_deed'),

     path('vehicles/', views.list_vehicles, name='list_vehicles'),
    path('vehicles/new/', views.create_vehicle, name='create_vehicle'),
    path('vehicles/<int:pk>/', views.view_vehicle, name='view_vehicle'),
    path('vehicles/<int:pk>/edit/', views.update_vehicle, name='update_vehicle'),
    path('vehicles/<int:pk>/delete/', views.delete_vehicle, name='delete_vehicle'),
    path('vehicles/search/', views.search_vehicle, name='search_vehicle'),

    path('people/', views.list_people, name='list_people'),
    path('people/add/', views.add_person, name='add_person'),
    path('person/<int:pk>/', views.view_person, name='view_person'),


    #path('person/<int:pk>/edit/', views.update_person, name='update_person'),
    path('person/<int:pk>/edit/', views.create_person, name='update_person'),
     #path('create/<int:pk>/edit/', views.create_person, name='create_person'),


    path('person/<int:pk>/delete/', views.delete_person, name='delete_person'),
    path('search-person/', views.search_person, name='search_person'),
    path('print_person/<int:pk>/', views.print_person_as_pdf, name='print_person'),

    path('pay-tax/', views.pay_tax, name='pay_tax'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('verification-success/', views.verification_success, name='verification_success'),
    path('search-payment/', views.search_payment_by_code, name='search_payment_by_code'),

    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('register/', views.custom_register, name='register'),
    path('', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('verify-code/', views.verify_payment_code, name='verify_code'),
    #path('payment-details/', views.payment_details, name='payment_details'),

    ##############################################
    path('member_list', views.member_list, name='member_list'),
    path('member/<int:member_id>/', views.member_detail, name='member_detail'),
    path('member/<int:member_id>/add_payment/', views.add_payment, name='add_payment'),
    path('monthly_collections/', views.monthly_collections, name='monthly_collections'),
    path('search/', views.search_user, name='search_user'),
    path('payment_status', views.payment_status , name='payment_status'),
    path('homepage', views.homepage , name='homepage'),
    path('user_dashboardx', views.user_dashboardx , name='user_dashboardx'),
    path('add_payment', views.add_payment , name='add_payment'),
   
    
]
