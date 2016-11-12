# -*- coding: utf-8 -*-
from django import forms


class SearchOutput(forms.Form):
    NETWORK = [('livenet', 'livenet'), ('testnet', 'testnet')]
    transaction = forms.CharField(label=u'ID de la transacción', max_length=100, required=True)
    network = forms.ChoiceField(label='Network', required=True, widget=forms.RadioSelect,
                                        choices=NETWORK)

    def process(self):
        return self.cleaned_data['transaction'], self.cleaned_data['network']


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
            choices=[(o['n'], o) for o in outputs], widget=forms.RadioSelect)