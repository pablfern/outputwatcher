# -*- coding: utf-8 -*-
import json
from core.insight_api import *
from django import forms
from django.contrib import auth


class SearchOutput(forms.Form):
    NETWORK = [('livenet', 'livenet'), ('testnet', 'testnet')]
    transaction = forms.CharField(label=u'ID de la transacción', max_length=100, required=True)
    network = forms.ChoiceField(label='Network', required=True, widget=forms.RadioSelect,
                                        choices=NETWORK)

    def process(self):
        return self.cleaned_data['transaction'], self.cleaned_data['network']


class SearchOutputByTxIndexForm(forms.Form):
    NETWORK = [('livenet', 'livenet'), ('testnet', 'testnet')]
    transaction = forms.CharField(label=u'ID de la transacción', max_length=100, required=True)
    index = forms.IntegerField(label=u'Indice', required=True)
    network = forms.ChoiceField(label='Network', required=True, widget=forms.RadioSelect,
                                choices=NETWORK)

    def clean_index(self):
        _index = self.cleaned_data['index']
        if not _index or _index < 0:
            raise forms.ValidationError(u'El índice ingresado debe ser mayor o igual a 0')
        return _index

    def process(self):
        index = self.cleaned_data['index']
        transaction = self.cleaned_data['transaction']
        network = self.cleaned_data['network']
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
            choices=[("{}_{}".format(o['index'], o['value']), 
                      "Indice: {}, Valor: {} BTCs".format(o['index'], o['value'])) for o in outputs], widget=forms.RadioSelect)

    def process(self):
        return self.cleaned_data['output'].split('_')


class LoginForm(forms.Form):

    error_messages = {
        'login_invalid': u"Usuario o contraseña inválidos",
    }

    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={
        'placeholder': 'Correo electrónico'}))
    password = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput(
            attrs={'placeholder': 'Contraseña'}))

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
