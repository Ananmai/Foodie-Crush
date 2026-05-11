from django.db import models
class Customer(models.Model):
    username = models.CharField(max_length=20); password = models.CharField(max_length=20); email = models.CharField(max_length=20); mobile = models.CharField(max_length=10); address = models.CharField(max_length=50)
class Restaurant(models.Model):
    name = models.CharField(max_length=20); picture = models.URLField(default='https://designshack.net/wp-content/uploads/Free-Simple-Restaurant-Logo-Template.jpg'); cuisine = models.CharField(max_length=200); rating = models.FloatField()
class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="items"); name = models.CharField(max_length=20); description = models.CharField(max_length=200); price = models.FloatField(); vegeterian = models.BooleanField(default=False)
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE); items = models.ManyToManyField("Item")
