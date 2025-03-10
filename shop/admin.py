from django.contrib import admin
from .models import Item, Images, Optionels, Option, OrderItem, ShoppingCart
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
    
admin.site.register(OrderItem, OrderItemAdmin)


admin.site.register(Item)
admin.site.register(ShoppingCart)
admin.site.register(Images)
admin.site.register(Option)
admin.site.register(Optionels)


