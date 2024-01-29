from datetime import datetime
from tabnanny import check
from django import forms
from numpy import require
from lsmsApp import models

from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
import datetime

class SaveUser(UserCreationForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    password1 = forms.CharField(max_length=250)
    password2 = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name','password1', 'password2',)

class UpdateProfile(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdateUser(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
    class Meta:
        model = User
        fields = ('old_password','new_password1', 'new_password2')

class SavePrice(forms.ModelForm):
    laundry_type = forms.CharField(max_length=250)
    price = forms.CharField(max_length=250)
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Prices
        fields = ('laundry_type', 'price', 'status', )

    def clean_laundry_type(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        laundry_type = self.cleaned_data['laundry_type']
        try:
            if id > 0:
                price = models.Prices.objects.exclude(id = id).get(laundry_type = laundry_type, delete_flag = 0)
            else:
                price = models.Prices.objects.get(laundry_type = laundry_type, delete_flag = 0)
        except:
            return laundry_type
        raise forms.ValidationError("Laundry Type already exists.")

class SaveProducts(forms.ModelForm):
    name = forms.CharField(max_length=250)
    description = forms.CharField(max_length=250)
    price = forms.CharField(max_length=250)
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Products
        fields = ('name', 'description', 'price', 'status', )

    def clean_name(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            if id > 0:
                product = models.Products.objects.exclude(id = id).get(name = name, delete_flag = 0)
            else:
                product = models.Products.objects.get(name = name, delete_flag = 0)
        except:
            return name
        raise forms.ValidationError("Product Name already exists.")

class SaveStockIn(forms.ModelForm):
    product = forms.CharField(max_length=250)
    quantity = forms.CharField(max_length=250)

    class Meta:
        model = models.StockIn
        fields = ('product', 'quantity',)

    def clean_product(self):
        pid = self.cleaned_data['product']
        try:
            product = models.Products.objects.get(id = pid, delete_flag = 0)
            return product
        except:
            raise forms.ValidationError("Product is Invalid.")

class SaveLaundry(forms.ModelForm):
    code = forms.CharField(max_length=250)
    client = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250,required= False)
    status = forms.CharField(max_length=2)
    payment = forms.CharField(max_length=2)
    total_amount = forms.CharField(max_length=250)
    tendered = forms.CharField(max_length=250)
    

    class Meta:
        model = models.Laundry
        fields = ('code', 'client', 'contact', 'status', 'payment', 'total_amount', 'tendered',)

    def clean_code(self):
        code = self.cleaned_data['code']
       
        if code == 'generate':
            pref = datetime.datetime.now().strftime('%y%m%d')
            code = 1
            while True:
                try:
                    check = models.Laundry.objects.get(code = f"{pref}{code:05d}")
                    code = code + 1
                except:
                    return f"{pref}{code:05d}"
                    break
        else:
            return code
    
    def clean_payment(self):
        tendered = float(self.data['tendered'])
        if tendered > 0:
            return 1
        else:
            return 0

    def save(self):
        instance = self.instance
        Products = []
        Items = []
        # print(f"{self.data}")
        if 'price_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('price_id[]')):
                prices = models.Prices.objects.get(id= val)
                price = self.data.getlist('laundry_price[]')[k]
                weight = self.data.getlist('laundry_weight[]')[k]
                total = float(price) * float(weight)
                try:
                    Items.append(models.LaundryItems(laundry = instance, laundry_type = prices, price = price,weight = weight, total_amount = total))
                    print("LaundryItems..")
                except Exception as err:
                    print(err)
                    return False
        if 'product_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('product_id[]')):
                product = models.Products.objects.get(id= val)
                price = self.data.getlist('product_price[]')[k]
                qty = self.data.getlist('product_quantity[]')[k]
                total = float(price) * float(qty)
                try:
                    Products.append(models.LaundryProducts(laundry = instance, product = product, price = price, quantity = qty, total_amount = total))
                    print("LaundryProducts..")
                except Exception as err:
                    print(err)
                    return False
        try:
            instance.save()
            models.LaundryProducts.objects.filter(laundry = instance).delete()
            models.LaundryProducts.objects.bulk_create(Products)
            models.LaundryItems.objects.filter(laundry = instance).delete()
            models.LaundryItems.objects.bulk_create(Items)
        except Exception as err:
            print(err)
            return False
