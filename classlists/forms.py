from django import forms

class School_StaffForm(forms.Form):
    first_name=forms.CharField(label='First Name',max_length=25,)
    last_name=forms.CharField(label='Last Name',max_length=25,)
    teacher_name=forms.CharField(label='Teacher Name',max_length=25,)
    email=forms.EmailField(label='Email',)
    password1=forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password again", widget=forms.PasswordInput)
    allow_contact=forms.BooleanField(label="Allow Email Contact", initial=True, required=False,)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2
