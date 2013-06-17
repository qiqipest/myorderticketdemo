from django import forms

class interRouteForm(forms.Form):
    Route_From = forms.CharField()
    Route_To = forms.CharField()
    
class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required=False)
    message = forms.CharField()