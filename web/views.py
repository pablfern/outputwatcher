# -*- coding: utf-8 -*-
from datetime import datetime
from web.forms import SearchOutput, OutputForm, LoginForm, RegisterForm
from core.models import Transaction, Output, FollowingOutputs
from core.insight_api import get_outputs, get_output_by_index, OutputAlreadySpentException,\
                             OutputNotFoundException, InsightApiException
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError

def home(request):
    return render(request, 'web/index.html', {})


def login(request):
    if request.user.is_authenticated():
        return redirect('following-outputs')

    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        login_form.process(request)
        return redirect('following-outputs')
    return render(request, 'web/account/login.html', { 'login_form': login_form})


def register(request):
    if request.user.is_authenticated():
        return redirect('following-outputs')
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
        register_form.process(request)
        return redirect('following-outputs')
    return render(request, 'web/account/register.html', {'register_form': register_form})


@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required
def following_outputs(request):
    request.session.pop('txid', None)
    request.session.pop('network', None)
    following_outputs = FollowingOutputs.objects.filter(user=request.user).order_by('-creation_date')
    return render(request, 'web/outputs/following_outputs.html', {'following_outputs': following_outputs,})


@login_required
def search_output(request):
    search_form = SearchOutput(request.POST or None)

    if search_form.is_valid():
        txid, network, index = search_form.process()
        if index:
            try:
                data = get_output_by_index(txid, index, network)
                transaction = Transaction.objects.get_or_create(transaction_id=txid, network=network)[0]
                output = Output.objects.get_or_create(transaction=transaction, index=index, amount=data['value'])[0]
                FollowingOutputs.objects.create(user=request.user, output=output, creation_date=datetime.now())
                return redirect('following-outputs')
            except OutputAlreadySpentException as e:
                # TODO ADD Alert with messages
                return redirect('search-output')
            except OutputNotFoundException as e:
                # TODO ADD Alert with messages
                return redirect('search-output')
            except InsightApiException as e:
                # TODO ADD Alert with messages
                return redirect('search-output')
            except IntegrityError as e:
                return redirect('following-outputs')

        request.session['txid'] = txid
        request.session['network'] = network
        return redirect('add-output')
    
    return render(request, 
                  'web/outputs/search_output.html', 
                  {'search_form': search_form})


@login_required
def add_output(request):
    txid = request.session['txid']
    network = request.session['network']
    try:
        content = get_outputs(txid, network)
    except OutputAlreadySpentException as e:
        # TODO ADD Alert with messages
        return redirect('search-output')
    except OutputNotFoundException as e:
        # TODO ADD Alert with messages
        return redirect('search-output')
    except InsightApiException as e:
        # TODO ADD Alert with messages
        return redirect('search-output')
    except IntegrityError as e:
        return redirect('following-outputs')

    outputs = {'outputs': content}
    output_form = OutputForm(request.POST or None, 
                             initial={'transaction': txid, 
                                      'network': network, }, **outputs)
    if output_form.is_valid():
        index, amount = output_form.process()
        transaction = Transaction.objects.get_or_create(transaction_id=txid, network=network)[0]
        output = Output.objects.get_or_create(transaction=transaction, index=index, amount=amount)[0]
        FollowingOutputs.objects.create(user=request.user, output=output, creation_date=datetime.now())
        request.session.pop('txid', None)
        request.session.pop('network', None)
        return redirect('following-outputs')

    return render(request, 
                  'web/outputs/add_output.html', 
                  { 'txid': txid,
                    'network': network,
                    'output_form': output_form,
                    'content': content })
