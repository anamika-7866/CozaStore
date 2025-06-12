from django.urls import path
from.views import *
urlpatterns = [
    path('',index,name='index'),
    path('blog/',blog),
    path('productdetail/<int:id>/',productdetail,name='detailpage'),
    path('shop/',product),
    path('contact/',contact),
    path('about/',about),
    path('login/',login1,name="login"),
    path('register/',register),
    path('userlog/',userlog),
    path('logout/',userlogout),
    path('usersignup/',createcustomer),
    path('addtocart',addtocart),
    path('cart/',cartview),
    path('wishlist/',viewwishlist),
    path('remove/<int:id>',removeitem),
    path('try',fetch_data),
    path('checkout/',checkout),
    path('confirm/',orderconfirm),
    path('addtowishlist',addtowishlist),
    path('remove-wishlist-item/<int:id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('search',search,name='search'),
    path("product/search/",productsearch),
    path('header/<int:id>',header),
    path("remove_from_wishlist_after_cart",remove_from_wishlist_after_cart, name="remove_from_wishlist_after_cart"),
    path('ordertrack',ordertrack)

]

