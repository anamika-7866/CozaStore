from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    mainframe=Mainframe.objects.all()
    categories=Category.objects.all()
    relatedproducts=Product.objects.all()[:4]
    Trandingproducts=Product.objects.all().order_by('-id')[:4]      
    return render(request,'index.html',{'categories':categories,'mainframe':mainframe,'relatedproducts':relatedproducts,'Trandingproducts':Trandingproducts})



def product(request):
    categories=Category.objects.all()
    if request.method == 'POST':
        Categoryid = request.POST.get('categoryid')
        print("------------------------------",Categoryid)
        products = Product.objects.filter(category=Categoryid)
        print("-------------------------",products)
        return render(request,'product.html',{'products':products})
    products=Product.objects.all()
    return render(request,'product.html',{'products': products,'categories':categories})

def product(request):
    categories=Category.objects.all()
    if request.method == 'POST':
        Categoryid = request.POST.get('categoryid')
        print("------------------------------",Categoryid)
        products = Product.objects.filter(category=Categoryid)
        print("-------------------------",products)

        
        return render(request,'product.html',{'products':products})
    products=Product.objects.all()
    
    return render(request,'product.html',{'products': products,'categories':categories})



def productsearch(request):
    Categoryid = request.GET.get('categoryid')
    price_range = request.GET.get('price')
    products = Product.objects.all()
    if Categoryid:
        products = products.filter(category__id=Categoryid)
    if price_range:
        if price_range == '100-500':
            products = products.filter(price__gte=100, price__lte=500)
        elif price_range == '500-1000':
            products = products.filter(price__gte=500, price__lte=1000)
        elif price_range == '1000-1500':
            products = products.filter(price__gte=1000, price__lte=1500)
        elif price_range == '1500-2000':
            products = products.filter(price__gte=1500, price__lte=2000)
    categories = Category.objects.all()
    
    return render(request, 'product.html', {'products': products, 'categories': categories})





    


def contact(request):
    if request.method=="POST":
        email=request.POST.get('email')
        msg=request.POST.get('msg')
        contact=Contact.objects.create(email=email,msg=msg)
        contact.save()
        print("_______",email,msg)
    return render(request,'contact.html')

def wishlist(request):
    return render(request,'wishlist.html')

def about(request):
    return render(request,'about.html')


def blogdetail(request):
    return render(request,'blog-detail.html')

def blog(request):
    relatedproducts=Product.objects.all()[:4]  
    return render(request,'blog.html',{'relatedproducts':relatedproducts})

def login1(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def header(request):
    categories=Category.objects.all()

    return render(request,'header.html',{"categories":categories})




def userlog(request):
    if request.method=='POST':
        email=request.POST['customeremail']
        paswd=request.POST['customerpassword']
        user=authenticate(request,username=email,password=paswd)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAA",email,paswd)
        if user is not None:
            login(request,user)
            print(user)
            return redirect('index')
    return redirect("login")        

def userlogout(request):
    logout(request)
    return redirect('index')

def createcustomer(request):
    if request.method=='POST':
        firstname=request.POST['customerfirst_name']
        lastname=request.POST['customerlast_name']
        email=request.POST['customeremail']
        paswd=request.POST['customerpassword']
        print(email,paswd)
        user=User.objects.create_user(username=email,email=email,password=paswd)
        user.first_name=firstname
        user.last_name=lastname
        user.save()
        
    return render(request,'login.html')

def search(request):
    query=request.GET['search-product']
    product_filtered=Product.objects.filter(name__icontains=query)
    return render(request,'product.html',{'products': product_filtered})



def searchAJAX(request):
    query=request.GET['search-product']
    print(query)
    product_filtered=Product.objects.filter(name__icontains=query).values()
    print(product_filtered)
    return JsonResponse({'product':list(product_filtered)})


@login_required
def addtocart(request):
    if request.method=='POST':
        data=json.loads(request.body)
        pid=int(data['pid'])
        quantity=int(data['quantity'])
        size = data.get('size', '')
        color = data.get('color', '') 
        product=get_object_or_404(Product,id=pid)
        cart,created=Cart.objects.get_or_create(user=request.user)
        cartitem,created=CartItem.objects.get_or_create(cart=cart,product=product)
        if not created:
            cartitem.quantity+=quantity
            cartitem.size = size  # Save the size selected by the user
            cartitem.color = color
            cartitem.save()
            cart.total+=quantity*product.price
            cart.save()
        if created:
            cartitem.quantity=quantity
            cartitem.size = size  # Save the size selected by the user
            cartitem.color = color
            cartitem.save()
            cart.total+=quantity*product.price
            cart.save()
        return JsonResponse({'key':'value'})



@login_required
def cartview(request):
    cart=Cart.objects.get(user=request.user)
    cartitems=CartItem.objects.filter(cart=cart)
    product_data=[]
    for i in cartitems:
        product=Product.objects.get(id=i.product_id)
        images=product.product_images.all()
        product_data.append({
            'product':product,
            'image':images[0].image.url if len(images) > 0 else '',
            'Quantity':i.quantity,
            'total':i.quantity*product.price
               
        })   
    return render(request,'shoping-cart.html',{'product_data':product_data})

def checkout(request):
    cart=Cart.objects.get(user=request.user)
    cartitems=CartItem.objects.filter(cart=cart)
    product_data=[]
    for i in cartitems:
        print("                                    ",i.product_id)

        product=Product.objects.get(id=i.product_id)
        images=product.product_images.all()
        product_data.append({
            'product':product,
            'image':images[0].image.url if len(images) > 0 else '',
            'Quantity':i.quantity,
            'total':i.quantity*product.price
               
        })   
    print("                                ",product_data)
    return render(request,'checkout.html',{'product_data':product_data,'total':cart.total})

def removeitem(request, id):
    try:
        cart = Cart.objects.get(user=request.user)
        cartitem = CartItem.objects.get(product_id=id, cart=cart)
        cartitem.delete()
        cartitems = CartItem.objects.filter(cart=cart)
        new_total = 0
        for item in cartitems:
            product = item.product
            new_total += item.quantity * product.price
        cart.total = new_total
        cart.save()
        product_data = []
        for item in cartitems:
            product = item.product
            images = product.product_images.all()
            product_data.append({
                'product': product,
                'image': images[0].image.url if len(images) > 0 else '',
                'Quantity': item.quantity,
                'total': item.quantity * product.price
            })
        return render(request, 'shoping-cart.html', {'product_data': product_data, 'cart_total': cart.total})

    except Cart.DoesNotExist:
        return render(request, 'shoping-cart.html', {'error': 'Cart not found'})

    except CartItem.DoesNotExist:
        return render(request, 'shoping-cart.html', {'error': 'Item not found in your cart'})


def fetch_data(request):
     if request.method=='POST':
        data=json.loads(request.body)
        quantity=data['quantity']
        total=data['total']
        pid=data['id']
        cart=Cart.objects.get(user=request.user)
        cartitems=CartItem.objects.get(product=pid,cart=cart)
        cartitems.quantity=quantity
        cartitems.save()
        cart.total=total
        cart.save()
        return JsonResponse({'key':'value'})

def orderconfirm(request):
    if request.method=='POST':
        countrycode=request.POST.get('countryCode')
        delieverytype=request.POST.get('delivery_strategies')
        firstname=request.POST.get('firstName')
        lastname=request.POST.get('lastName')
        address=request.POST.get('address1')
        city=request.POST.get('city')
        state=request.POST.get('zone')
        zip=request.POST.get('postalCode')
        cart=Cart.objects.get(user=request.user)
        cartItem=CartItem.objects.filter(cart=cart)
        confirm=confirmorders.objects.create(user=request.user,delieverytype=delieverytype,firstname=firstname,lastname=lastname,city=city,state=state,zip=zip,country=countrycode,address=address)
        confirm.CartItems.set(cartItem)
        confirm.save()
        return render(request,'checkout.html')

def productdetail(request,id):
    print("adsfghjkldfgfhvjklmlkjhgfdsdfghjk",id)
    data=Product.objects.get(id=id)
    images=data.product_images.all()
    print(images)
    return render(request,'product-detail.html',{'details':data,'images':images})

@login_required
def addtowishlist(request):
    if request.method=='POST':
        data=json.loads(request.body)
        pid=int(data['pid'])
        product=get_object_or_404(Product,id=pid)
        wishlist,created=Wishlist.objects.get_or_create(user=request.user)
        wishlistItem,created=WishlistItem.objects.get_or_create(wishlist=wishlist,product=product)
        print(created)
        return JsonResponse({'key':'value'})

@login_required
def viewwishlist(request):
    wishlist=Wishlist.objects.get(user=request.user)
    wishlistitem=WishlistItem.objects.filter(wishlist=wishlist)
    product_data=[]
    for i in wishlistitem:
        product=Product.objects.get(id=i.product_id)
        images=product.product_images.all()
        product_data.append(
            {
            'product':product,
            'image1':images[0].image.url if len(images) > 0 else '',
            'image2':images[0].image.url if len(images) > 0 else ''
                  })   
    return render(request,'wishlist.html',{'product_data':product_data})

@login_required
def remove_from_wishlist(request, id):
    if request.method == "POST":
        wishlist_item = get_object_or_404(
            WishlistItem,
            product_id=id,
            wishlist__user=request.user
        )
        wishlist_item.delete()
        return JsonResponse({"success": True, "message": "Item removed from wishlist."})
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

def productdetail(request,id):
    product = get_object_or_404(Product, id=id)
    images=product.product_images.all()

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        user = request.user
        review = Review(product=product, user=user, rating=rating, review_text=review_text)
        review.save()
        return redirect('detailpage',id=id)
    reviews = product.reviews.all()
    review=[]
    for i in reviews:
        
        review.append({
            'review':i,
            'rating_list':list(range(i.rating))
        })

    context = {
        'product': product,
        'images':  images,
        'review':review
    }

    return render(request, 'product-detail.html', context,)


@login_required
@csrf_exempt
def remove_from_wishlist_after_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")

        wishlist_item = WishlistItem.objects.filter(
            product_id=product_id,
            wishlist__user=request.user
        ).first()

        if wishlist_item:
            wishlist_item.delete()
            return JsonResponse({"success": True, "message": "Removed from wishlist after adding to cart."})
        return JsonResponse({"success": False, "message": "Item not in wishlist."})
    
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)


def ordertrack(request):
    return render(request,"ordertrack.html")

