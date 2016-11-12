# -*- coding: utf-8 -*-
from django import forms


class SearchOutput(forms.Form):
	NETWORK = [('livenet', 'livenet'), ('testnet', 'testnet')]
	transaction = forms.CharField(label=u'ID de la transacción', max_length=100, required=True)
	network = forms.ChoiceField(label='Network', required=True, widget=forms.RadioSelect,
                                        choices=NETWORK)

	def process(self):
		return transaction

