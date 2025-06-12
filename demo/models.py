from django.db import models
from django.contrib.auth.models import User

class Mainframe(models.Model):
    heading=models.CharField(max_length=200)
    short_description=models.CharField(max_length=200)
    image=models.ImageField(upload_to='media/')
    def __str__(self):
        return  self.heading

class Category(models.Model):
    category_name=models.CharField(max_length=200)
    category_img=models.ImageField(upload_to='media/')
    def __str__(self):
        return  self.category_name

class Product(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    price=models.IntegerField()
    def __str__(self):
        return  self.name



class ProductImage(models.Model):
    product=models.ForeignKey(Product,related_name='product_images',on_delete=models.CASCADE)
    image=models.ImageField(upload_to='media/')
    def __str__(self):
        return  self.image.name

class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    total=models.IntegerField(default=0)
    def __str__(self):
        return  f" cart for {self.user}"


class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name='product_id',on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    size=models.CharField(max_length=200,default='')
    color=models.CharField(max_length=200,default='')
    description=models.TextField(default='')
    def __str__(self):
        return  f" cart for  Item {self.product}"

class Wishlist(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def _str_(self):
        return  f" wishlist for {self.user}"
    
class WishlistItem(models.Model):
    wishlist=models.ForeignKey(Wishlist,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name='wishlist_id',on_delete=models.CASCADE)

class confirmorders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    delieverytype=models.CharField(max_length=500)
    firstname=models.CharField(max_length=500,default='')
    lastname=models.CharField(max_length=500,default='')
    state=models.CharField(max_length=500,default='')
    zip=models.CharField(max_length=500,default='')
    country=models.CharField(max_length=500,default='')
    city=models.CharField(max_length=500)
    address=models.CharField(max_length=500)
    CartItems=models.ManyToManyField(CartItem,related_name='orders')

class Contact(models.Model):
    email=models.CharField(max_length=200)
    msg=models.TextField()
    def __str__(self):
        return self.email

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user=models.ForeignKey(User,on_delete=models.CASCADE) # You can link this to a user model if you have one
    rating = models.IntegerField()  # Store rating from 1 to 5
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user}"
