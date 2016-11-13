# -*- coding: utf-8 -*-
import json
from core.insight_api import *
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class SearchOutput(forms.Form):
    # NETWORK = [('livenet', 'livenet'), ('testnet', 'testnet')]
    transaction = forms.CharField(label=u'ID de la transacción', widget=forms.TextInput(attrs={
        'placeholder': 'Id de transacción', 'id': 'sr_bx'}), max_length=100, required=True)
    # network = forms.ChoiceField(label='Network', required=True, widget=forms.RadioSelect,
    #                                     choices=NETWORK)
    index = forms.IntegerField(label=u'Indice', widget=forms.TextInput(attrs={
        'placeholder': 'Indice output', 'id': 'sr_bx'}),required=False)

    def clean_index(self):
        _index = self.cleaned_data['index']
        if _index and _index < 0:
            raise forms.ValidationError(u'El índice ingresado debe ser mayor o igual a 0')
        return _index

    def process(self):
        index = self.cleaned_data['index']
        transaction = self.cleaned_data['transaction']
        # network = self.cleaned_data['network']
        network = 'livenet'
        return transaction, network, index


class OutputForm(forms.Form):
    transaction = forms.CharField(label=u'ID de la transacción', max_length=100, required=True)
    network = forms.CharField(max_length=20, required=True)

    output = forms.ChoiceField(label='Output', required=True, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        outputs = kwargs.pop('outputs', [])
        super(OutputForm, self).__init__(*args, **kwargs)
        self.fields['transaction'].widget = forms.HiddenInput()
        self.fields['network'].widget = forms.HiddenInput()
        self.fields['output'] = forms.ChoiceField(label='Output', required=True,
            choices=[("{}_{}_{}".format(o['index'], o['value'], o['script']), 
                      "Indice: {}, Valor: {} BTCs".format(o['index'], o['value'])) for o in outputs], widget=forms.RadioSelect)

    def process(self):
        return self.cleaned_data['output'].split('_')


class LoginForm(forms.Form):

    error_messages = {
        'login_invalid': u"Usuario o contraseña inválidos",
    }

    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={
        'placeholder': 'Correo electrónico', 'class': 'form-control'}))
    password = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput(
            attrs={'placeholder': 'Contraseña', 'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if username and password:
            user = auth.authenticate(
                username=username.lower(), password=password
            )
            if not user:
                raise forms.ValidationError(
                    self.error_messages['login_invalid'])
        return self.cleaned_data

    def process(self, request):
        username = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username.lower(), password=password)

        auth.login(request, user)
#        request.session['user_id'] = user.email
        return user


class RegisterForm(forms.Form):

    error_messages = {
        'register_invalid': u"Usuario o contraseña inválidos",
    }

    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={
        'placeholder': 'Correo electrónico', 'class': 'form-control'}), required=True)
    password = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput(
            attrs={'placeholder': 'Contraseña', 'class': 'form-control'}), required=True)
    repassword = forms.CharField(
        label="Repeti Contraseña", widget=forms.PasswordInput(
            attrs={'placeholder': 'Repetir Contraseña', 'class': 'form-control'}), required=True)

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')
        if User.objects.filter(email=username).exists():
            raise forms.ValidationError('Ya existe un usuario registrado con ese email')

    def process(self, request):
        username = self.cleaned_data['email'].lower()
        password = self.cleaned_data['password']
        repassword = self.cleaned_data.get('repassword')
        User.objects.create_user(username, username, password)
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        return user
