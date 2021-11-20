from django import forms


choices = [('1', '1'), ('2', '2'),('3','3'),('4','4'),('5','5')]

class NewProductForm(forms.Form):
    product_name = forms.CharField(max_length=20)
    price = forms.IntegerField()
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 20}))


# class ProductReviewForm(forms.Form):

#     rating = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
#     feedback = forms.CharField(
#         widget=forms.Textarea(attrs={'rows': 5, 'cols': 20}))
