# -*- coding: utf-8 -*-
from web.forms import SearchOutput, OutputForm
from core.insight_api import get_outputs

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'web/index.html', {})


def login(request):
    return render(request, 'web/account/login.html', {})


def register(request):
    return render(request, 'web/account/register.html', {})


def following_outputs(request):
    return render(request, 'web/following_outputs.html', {})


def search_output(request):
    search_form = SearchOutput(request.POST or None)
    if search_form.is_valid():
        txid, network = search_form.process()
        request.session['txid'] = txid
        request.session['network'] = network
        return redirect('add-output')
#        return HttpResponseRedirect(add_output, txid, network)

    return render(request, 
                  'web/outputs/search_output.html', 
                  {'search_form': search_form})


def add_output(request):
    txid = request.session['txid']
    network = request.session['network']
    content = get_outputs(txid, network)
    outputs = {'outputs': content}
    output_form = OutputForm(request.POST or None, 
                             initial={'transaction': txid, 
                                      'network': network, }, **outputs)
    if output_form.is_valid():
        pass

    return render(request, 
                  'web/outputs/add_output.html', 
                  { 'txid': txid,
                    'network': network,
                    'output_form': output_form,
                    'content': content })
