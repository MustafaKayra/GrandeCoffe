from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from .models import Item,ShoppingCart
from users.models import CustomUser
from blogs.models import Blog
from .forms import OrderItemForm
from blogs.forms import Contactform
import iyzipay
import json
from django.contrib import messages
from django.core.mail import send_mail

def index(request):
    toprated = Item.objects.order_by('-numberofsales')[:3]
    lastblogs = Blog.objects.order_by('-date')[:1]
    footercoffes = Item.objects.order_by('-numberofsales')[:4]
    if request.method == "POST":
        form = Contactform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"İletişim Formu Başarıyla Gönderildi")
            return redirect('index')
        else:
            messages.warning(request,form.errors)
    else:
        form = Contactform()
    context = {
        "toprated":toprated,
        "lastblogs":lastblogs,
        "form":form,
        "footercoffes":footercoffes
    }
    return render(request,"index.html",context)

def order(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Sitemize Giriş Yapmadan Kahve Sipariş Edemezsiniz!")
        return redirect('login')
    footercoffes = Item.objects.order_by('-numberofsales')[:4]
    cart = ShoppingCart.objects.filter(customer=request.user).first()
    if not cart:
        return render(request,"shoppingcartdetail.html",{"footercoffes":footercoffes})

    totalprice = cart.totalpricecart()
    customer = request.user
    salesofpiece = cart.totalnumberofsalespiece()

    if request.method == "POST":
        if "deleteallcoffeincart" in request.POST:
            cart.delete()
            messages.warning(request,"Sepet Başarıyla Silindi")
            return redirect('order')
        options = {
            'api_key': 'sandbox-LC3nNJCVAqA1QZYlFSreYK5VO3nYIDlE',
            'secret_key': 'sandbox-kOflXwc5MbTldBKuogFADjFlrQlKsMfS',
            'base_url': 'sandbox-api.iyzipay.com',
        }

        name = request.POST.get("name")
        surname = request.POST.get("surname")
        adres = request.POST.get("adres")
        city = request.POST.get("city")
        country = request.POST.get("country")
        zipcode = request.POST.get("zipcode")
        gsmnumber = request.POST.get("gsmnumber")
        email = request.POST.get("email")
        cardNumber = request.POST.get("cartnumber")
        expire = request.POST.get("expiretime")
        cvc = request.POST.get("cvc")

        payment_card = {
            'cardHolderName': customer.first_name +" "+ customer.last_name, #Kart Sahibinin Adı
            'cardNumber': customer.cardnumber, #Kart Numarası
            'expireMonth': customer.expire.split("/")[0].strip(), #Kartın Son Kullanma Ayı
            'expireYear': customer.expire.split("/")[1].strip(), #Kartın Son Kullanma Yılı
            'cvc': customer.cvc, #Kartın Güvenlik Numarası
            'registeredCart': '1' #Kartı Kaydedip Kaydetmeme Durumu '0' Kaydetmez '1' Kaydeder
        }

        buyer = {
            'id': str(customer.id), #Alıcının ID'si
            'name': customer.first_name, #Alıcının Adı
            'surname': customer.last_name, #Alıcının Soyadı
            'gsmNumber': customer.gsmnumber, #Alıcının Telefon Numarası
            'email': customer.email, #Alıcının Emaili
            'identityNumber': '74300864791', #Alıcının Kimlik Numarası
            'lastLoginDate': '2015-10-05 12:43:35', #Alıcının Son Giriş Yaptığı Tarih
            'registrationDate': '2013-04-21 15:12:09', #Alıcının Kayıt Olduğu Tarih
            'registrationAddress': customer.address, #Alıcının Kayıtlı Olduğu Adresi
            'ip': request.META.get('REMOTE_ADDR'), #Alıcının IP Adresi
            'city': customer.city, #Alıcının Yaşadığı Şehir
            'country': customer.country, #Alıcının Yaşadığı Ülke
            'zipCode': customer.zipcode, #Alıcının Posta Kodu
        }

        address = {
            'contactName': customer.first_name +" "+ customer.last_name, #Adresle İlgili Kişinin Adı
            'city': customer.city, #Şehir
            'country': customer.country, #Ülke
            'address': customer.address, #Adres Detayları
            'zipCode': customer.zipcode #Posta Kodu
        }

        basket_items = [
            
        ]

        total_price_calculated = 0

        for items in cart.orderitems.all():
            item_total_price = items.item.price * items.piece

            basket_item = {
                "id": str(items.item.id),
                "name": items.item.name,
                "category1": str([option.optionels.name for option in items.options.all()]),
                "category2": str([option.name for option in items.options.all()]),
                "itemType": 'PHYSICAL',
                "price": str(item_total_price),
                "quantity": str(items.piece) 
            }
            print(f"Ürün Sayısı: {items.piece}")
            total_price_calculated += item_total_price  # Toplam tutarı hesapla
            basket_items.append(basket_item)
        
        if total_price_calculated != totalprice:
            raise ValueError(f"Gönderilen toplam fiyat ({totalprice}) ile hesaplanan toplam fiyat ({total_price_calculated}) uyuşmuyor!")


        payment_request = {
            'locale': 'tr', #Dil ve yerel ayar
            'conversationId': '123456789', #İsteğin Konuşma Id'si
            'price': str(totalprice), #Toplam Tutar(Vergiler Hariç)
            'paidPrice': str(totalprice), #Ödenen Toplam Tutar(Vergiler Dahil)
            'currency': 'TRY', #Para Birimi
            'installment': '1', #Taksit Sayısı
            'basketId': str(cart.id), #Sepet ID'si
            'paymentChannel': 'WEB', #Ödeme Kanalı
            'paymentGroup': 'PRODUCT', #Ödeme Grubu('PRODUCT' ürün ödemesi için)
            'paymentCard': payment_card, #Ödeme Kartı Bilgileri
            'buyer': buyer, #Alıcı Bilgileri,
            'shippingAddress': address, #Teslimat Adresi
            'billingAddress': address, #Fatura Adresi
            'basketItems': basket_items #Sepet Öğeleri
        }

        payment = iyzipay.Payment().create(payment_request, options)
        payment_result = json.loads(payment.read().decode('utf-8'))
        print(payment_card.get("expireMonth"))
        if payment_result.get("status") == "success":
            messages.success(request,"Ödeme Başarıyla Gerçekleşti Siparişiniz Hazırlanıyor")
            for items in cart.orderitems.all():
                items.item.numberofsales += items.piece
                items.item.save()
                print(items.item.numberofsales)
            admin_emails = list(CustomUser.objects.filter(is_staff=True).values_list("email", flat=True))

            subject = f"Yeni Sipariş Alındı 🚀 ID:{cart.id}"
            message = f"""
            Yeni Bir Sipraiş Alındı!

            Müşteri: {customer.first_name} {customer.last_name}
            
            

            """

            cart.delete()
        elif payment_result.get("status") == "failure":
            messages.warning(request,"Ödeme Başarısız Oldu. Kart Ve Adres Bilgilerinizi Kontrol Ediniz")
            print(payment_result)
            return redirect('updateuser')
        return redirect('order')
    

    context = {
        "cart":cart,
        "customer":customer,
        "totalprice":totalprice,
        "salesofpiece":salesofpiece,
        "footercoffes":footercoffes
    }
    return render(request,"shoppingcartdetail.html",context)

def coffes(request):
    coffe = Item.objects.all()
    footercoffes = Item.objects.order_by('-numberofsales')[:4]
    context = {
        "coffe":coffe,
        "footercoffes":footercoffes
    }
    return render(request,"gallery.html",context)
    
def coffesdetail(request,slug):
    footercoffes = Item.objects.order_by('-numberofsales')[:4]
    coffe = get_object_or_404(Item,slug=slug)
    form = OrderItemForm(item=coffe)
    customer = request.user
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request,"Sitemize Giriş Yapmadan Kahve Sipariş Edemezsin!")
            return redirect('login')
        form = OrderItemForm(request.POST, item=coffe)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.item = coffe
            order_item.save()
            shopping_cart, created = ShoppingCart.objects.get_or_create(customer=customer)

            if not created:
                shopping_cart.orderitems.add(order_item)
            else:
                shopping_cart.orderitems.set([order_item])
            
            form.save_m2m()
            messages.success(request,"Form Başarıyla Kaydedildi")
            return redirect('order')
        else:
            print("Form Başarısız")
            messages.warning(form.errors)
    context = {
        "coffe":coffe,
        "form":form,
        "footercoffes":footercoffes
    }
    return render(request,"about.html",context)

def deletecoffeincart(request,id):
    cart = get_object_or_404(ShoppingCart,customer=request.user)
    deletedcoffe = cart.orderitems.filter(id=id)
    deletedcoffe.delete()
    messages.warning(request,"Kahve Başarıyla Sepetten Silindi")
    return redirect('order')