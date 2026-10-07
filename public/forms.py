from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
    
    # Honeypot field for bot protection
    website_hp = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website_hp(self):
        hp_value = self.cleaned_data.get('website_hp')
        if hp_value:
            raise forms.ValidationError("Spam bot detected.")
        return hp_value