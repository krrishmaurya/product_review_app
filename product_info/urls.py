from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProductInfo.as_view(),name = 'ProductInfo'),
    path('new_product/',views.NewProduct.as_view(),name = 'NewProduct'),
    path('new_review',views.NewReview.as_view(),name = 'NewReview')
]