from django.contrib import admin
from .models import Item, Images, Optionels, Option, OrderItem, ShoppingCart, OrderedCard
from django import forms

class OrderItemAdminForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'  # Tüm alanları dahil et

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'item' in self.data:  # Eğer admin panelinde Item seçildiyse
            try:
                item_id = int(self.data.get('item'))
                item = OrderItem._meta.model.objects.get(pk=item_id)
                self.fields['options'].queryset = Option.objects.filter(optionels__in=item.optionels.all())
            except (ValueError, OrderItem.DoesNotExist):
                pass
        elif self.instance.pk:  # Eğer düzenleme modundaysa
            self.fields['options'].queryset = Option.objects.filter(optionels__in=self.instance.item.optionels.all())
        else:  # Varsayılan olarak tüm seçenekleri gösterme
            self.fields['options'].queryset = Option.objects.none()

class OrderItemAdmin(admin.ModelAdmin):
    form = OrderItemAdminForm  # Özel formu kullan

    def has_module_permission(self, request):
        return False
admin.site.register(OrderItem, OrderItemAdmin)


class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('numberofsales',)
    fields = ('name','description','image','optionels','price','numberofsales')
admin.site.register(Item, ItemAdmin)


class ShoppingCartAdmin(admin.ModelAdmin):
    fields = ('customer', 'orderitems')
    readonly_fields = ('ordered','customer')

    def has_module_permission(self, request):
        return False
admin.site.register(ShoppingCart, ShoppingCartAdmin)


admin.site.register(Images)
admin.site.register(Option)
admin.site.register(Optionels)


class OrderedCardAdmin(admin.ModelAdmin):
    fields = ('shoppingcart','complete')
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.complete:
            shoppingcart = obj.shoppingcart
            for orderitem in shoppingcart.orderitems.all():
                orderitem.delete()
            obj.delete()
            shoppingcart.delete()
admin.site.register(OrderedCard, OrderedCardAdmin)


