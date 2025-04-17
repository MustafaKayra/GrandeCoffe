from django import forms
from .models import Item, OrderItem, Option

class DynamicOptionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        item = kwargs.pop('item')  # Ürün bilgisini alıyoruz
        super().__init__(*args, **kwargs)

        for optionel in item.optionels.all():
            self.fields[f'optionel_{optionel.id}'] = forms.ModelChoiceField(
                queryset=Option.objects.filter(optionels=optionel),
                label=optionel.name,
                required=True
            )


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

