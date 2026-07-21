from django import forms
from .models import Item


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=99, initial=1)

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_desc', 'item_price', 'item_image']