from django.urls import path
from main import views

urlpatterns = [
    path('',views.BaseView.as_view(),name='home' ),
    path('api/shop-list/<int:pin>', views.ShopView.as_view(), name='shops'),
    path('api/shop-slots/<str:gst_id>', views.list_slots_for_shop, name='slots'),
    path('api/book-slot/', views.book_slot, name='shops'),
    path('api/user-bookings', views.user_booked_slots, name='user-slots')
]