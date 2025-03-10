from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Optionels(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,verbose_name="Opsiyon İsmi")

    def __str__(self):
        return f"{self.name}"


class Option(models.Model):
    optionels = models.ForeignKey(Optionels,null=False,blank=False,verbose_name="Opsiyon Kategorisi",on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=False,blank=False,verbose_name="Opsiyon İsmi")

    def __str__(self):
        return f"{self.optionels} | {self.name}"


class Images(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False,verbose_name="İçecek İsmi")
    image = models.ImageField(upload_to="coffeimages/",verbose_name="İçecek Resimleri")

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,verbose_name="İçecek İsmi")
    description = models.TextField(null=False,blank=False,verbose_name="İçecek Açıklaması")
    image = models.ForeignKey(Images,null=False,blank=True,verbose_name="İçecek Resimleri",on_delete=models.CASCADE)
    optionels = models.ManyToManyField(Optionels,null=False,blank=False)
    price = models.FloatField(null=False,blank=True,verbose_name="Fiyat")
    slug = models.SlugField(null=False,blank=True,unique=True,db_index=True)
    numberofsales = models.IntegerField(null=False,blank=True,default=0)

    def save(self, *args, **kwargs): #This function adds slug by title
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.name}"
    

class OrderItem(models.Model):
    item = models.ForeignKey(Item,null=False,blank=False,on_delete=models.CASCADE)
    piece = models.IntegerField(null=False,blank=False,default=1)
    options = models.ManyToManyField(Option,null=True,blank=True,verbose_name="Opsiyonlar")
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        related_options = Option.objects.filter(optionels__in=self.item.optionels.all())  # Doğrudan tüm ilişkili Option'ları al
        self.options.set(related_options)


    def __str__(self):
        return f"{self.item} | {self.piece}"
    
    def totalprice(self):
        total = self.piece * self.item.price
        return total
    
    def numberofsalespiece(self):
        salespiece = self.piece + self.item.numberofsales
        return salespiece

    
class ShoppingCart(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,null=False,blank=False,on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(OrderItem,null=False,blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=False,blank=False)

    def __str__(self):
        return f"{self.date_created} | {self.complete}"
    
    def totalpricecart(self):
        return sum(order_item.totalprice() for order_item in self.orderitems.all())
    
    def totalnumberofsalespiece(self):
        return sum(order_item.numberofsalespiece() for order_item in self.orderitems.all())

