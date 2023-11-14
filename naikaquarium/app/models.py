from django.db import models
from django.contrib.auth.models import User

# Create your models here.

OFFER_CAT = (
    ("fishfood", "fishfood"),
    ("catfood", "catfood"),
    ("dogfood", "dogfood"),
    ("petfish", "petfish"),
    ("assc", "assc"),
)

class Offer(models.Model):
    heading = models.CharField(max_length=50)
    text = models.CharField(max_length=200)
    category = models.CharField(choices=OFFER_CAT, max_length=20)

    def __str__(self):
        heading = str(self.heading)
        text = str(self.text)

        return(f"{heading}: {text}")

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    house_number = models.CharField(max_length=50)
    locality = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    city = models.CharField(max_length=100)

    def __str__(self):
        name = str(self.name)
        phone_number = str(self.phone_number)
        house_number = str(self.house_number)
        locality = str(self.locality)
        id = str(self.id)
        return (f"({id}) {name}/{phone_number}, Add: {house_number}{locality}")
    

CATEGORY = (
    ("F", "Fish Food"),
    ("C", "Cat Food"),
    ("D", "Dog Food"),
    ("P", "Pet Fish"),
    ("A", "Accessories"),
)



class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    original_price = models.FloatField()
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY, max_length=2)
    product_img = models.ImageField(upload_to="product_imgs")
    is_active = models.BooleanField(default=True)


    def __str__(self):
        title = str(self.title)
        price = str(self.price)
        id = str(self.id)
        return(f"ID: {id} - {title} - Rs{price}")
    


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.price
    

STATUS = (
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On The Way", "On The Way"),
    ("Delivered", "Delivered"),
    ("Canceled", "Canceled"),    
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=STATUS, default="Pending", max_length=50)


    @property
    def total_cost(self):
        return self.quantity * self.product.price