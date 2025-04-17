from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Optionels(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,verbose_name="Opsiyon İsmi")

    class Meta:
        verbose_name = "Opsiyon Kategorisi"
        verbose_name_plural = "Opsiyon Kategorileri"

    def __str__(self):
        return f"{self.name}"


class Option(models.Model):
    optionels = models.ForeignKey(Optionels,null=False,blank=False,verbose_name="Opsiyon Kategorisi",on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=False,blank=False,verbose_name="Opsiyon İsmi")

    class Meta:
        verbose_name = "Opsiyon"
        verbose_name_plural = "Opsiyonlar"

    def __str__(self):
        return f"{self.optionels} | {self.name}"


class Images(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False,verbose_name="İçecek İsmi")
    image = models.ImageField(upload_to="coffeimages/",verbose_name="İçecek Resimleri")

    class Meta:
        verbose_name = "İçecek Resmi"
        verbose_name_plural = "İçecek Resimleri"

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,verbose_name="İçecek İsmi")
    description = models.TextField(null=False,blank=False,verbose_name="İçecek Açıklaması")
    image = models.ForeignKey(Images,null=False,blank=True,verbose_name="İçecek Resimleri",on_delete=models.CASCADE)
    optionels = models.ManyToManyField(Optionels,null=False,blank=False)
    price = models.FloatField(null=False,blank=True,verbose_name="Fiyat")
    slug = models.SlugField(null=False,blank=True,unique=True,db_index=True,verbose_name="URL")
    numberofsales = models.IntegerField(null=False,blank=True,default=0,verbose_name="Satış Sayısı")

    class Meta:
        verbose_name = "İçecek"
        verbose_name_plural = "İçecekler"

    def save(self, *args, **kwargs): #This function adds slug by title
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.name}"
    

class OrderItem(models.Model):
    item = models.ForeignKey(Item,null=False,blank=False,on_delete=models.CASCADE,verbose_name="Sipariş Edilen İçecek")
    piece = models.IntegerField(null=False,blank=False,default=1,verbose_name="İçecek Sayısı")
    options = models.ManyToManyField(Option,null=True,blank=True,verbose_name="Opsiyonlar")
    date = models.DateTimeField(auto_now_add=True,verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Sipariş Edilen İçecek"
        verbose_name_plural = "Sipariş Edilen İçecekler"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def __str__(self):
        options_str = ", ".join(option.name for option in self.options.all())
        return f"{self.item} | {options_str} | {self.piece}"

    
    def totalprice(self):
        total = self.piece * self.item.price
        return total
    
    def numberofsalespiece(self):
        salespiece = self.piece + self.item.numberofsales
        return salespiece

    
class ShoppingCart(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,null=False,blank=False,on_delete=models.CASCADE,verbose_name="Müşteri")
    orderitems = models.ManyToManyField(OrderItem,null=False,blank=False,verbose_name="Sipariş Edilen İçecekler")
    date_created = models.DateTimeField(auto_now_add=True,verbose_name="Sepetin Oluşturulma Tarihi")
    ordered = models.BooleanField(default=False,blank=False,null=False,verbose_name="Sipariş Edilme Durumu")

    class Meta:
        verbose_name = "Sepet"
        verbose_name_plural = "Sepetler"

    def __str__(self):
        return f"{self.customer} Siparişi"
    
    def totalpricecart(self):
        return sum(order_item.totalprice() for order_item in self.orderitems.all())
    
    def totalnumberofsalespiece(self):
        return sum(order_item.numberofsalespiece() for order_item in self.orderitems.all())
    

class OrderedCard(models.Model):
    shoppingcart = models.ForeignKey(ShoppingCart,null=False,blank=False,on_delete=models.CASCADE,verbose_name="Sepet")
    date = models.DateTimeField(auto_now_add=True,verbose_name="Sipariş Edilme Tarihi")
    complete = models.BooleanField(default=False,blank=False,null=False,verbose_name="Tamamlanma Durumu")

    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"

    def __str__(self):
        return f"{self.shoppingcart} | {self.date}"

