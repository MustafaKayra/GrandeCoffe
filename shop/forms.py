from django import forms
from .models import Item, OrderItem, Option


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['piece', 'options']

    def __init__(self, *args, **kwargs):
        item = kwargs.pop('item', None)  # item nesnesini al
        super().__init__(*args, **kwargs)
        if item:
            self.fields['options'].queryset = Option.objects.filter(optionels__in=item.optionels.all())  # Seçenekleri filtrele
        else:
            self.fields['options'].queryset = Option.objects.none()

