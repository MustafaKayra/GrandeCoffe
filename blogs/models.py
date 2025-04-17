from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Commentreply(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="Yorum Yanıt Yazarı")
    content = models.TextField(null=False,blank=False,verbose_name="Yorum Yanıt İçeriği")
    date = models.DateTimeField(auto_now_add=True,verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Yorum Yanıtı"
        verbose_name_plural = "Yorum Yanıtları"

    def __str__(self):
        return f"{self.content}"



class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False,blank=False,verbose_name="Yorum Yazarı")
    content = models.TextField(null=False,blank=False,verbose_name="Yorum İçeriği")
    date = models.DateTimeField(auto_now_add=True,verbose_name="Oluşturulma Tarihi")
    reply = models.ManyToManyField(Commentreply,null=True,blank=True,verbose_name="Yorum Yanıtları")

    class Meta:
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"

    def __str__(self):
        return f"{self.content}"
    


class Content(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True,verbose_name="Başlık(İsteğe Göre Yazılabilir)")
    content = models.TextField(null=False,blank=False,verbose_name="İçerik")

    class Meta:
        verbose_name = "İçerik"
        verbose_name_plural = "İçerikler"

    def __str__(self):
        return f"{self.name}"



class Blog(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,verbose_name="Blog İsmi")
    description = models.CharField(max_length=1000,null=False,blank=False,verbose_name="Açıklama")
    image = models.ImageField(upload_to="blogimages/",null=False,blank=False,verbose_name="Blog Kapak Resmi")
    content = models.ManyToManyField(Content,null=False,blank=False,verbose_name="İçerikler")
    date = models.DateTimeField(auto_now_add=True,verbose_name="Oluşturulma Tarihi")
    slug = models.SlugField(null=False,blank=True,unique=True,db_index=True,verbose_name="URL")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Yazar")
    comments = models.ManyToManyField(Comment,null=True,blank=True,verbose_name="Yorumlar")

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Bloglar"

    def save(self, *args, **kwargs): #This function adds slug by title
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.name}"
    


class Contact(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False,verbose_name="İsim")
    email = models.EmailField(null=False,blank=False,verbose_name="Email")
    subject = models.CharField(max_length=500,null=False,blank=False,verbose_name="Konu")
    message = models.TextField(null=False,blank=False,verbose_name="Mesaj")

    class Meta:
        verbose_name = "İletişim Formu"
        verbose_name_plural = "İletişim Formları"

    def __str__(self):
        return f"{self.name} | {self.subject}"