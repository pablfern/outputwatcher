# -*- coding: utf-8 -*-
from datetime import datetime
from web.forms import SearchOutput, OutputForm, LoginForm, RegisterForm
from core.models import Transaction, Output, FollowingOutputs
from core.insight_api import get_outputs, get_output_by_index, OutputAlreadySpentException,\
                             OutputNotFoundException, InsightApiException
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError


def home(request):
    if request.user.is_authenticated():
        return redirect('following-outputs')
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
    following = FollowingOutputs.objects.filter(user=request.user, status='watching').order_by('-creation_date')
    following_spent = FollowingOutputs.objects.filter(user=request.user, status='used', user_status='pending').order_by('-creation_date')
    following_spent_confirmed = FollowingOutputs.objects.exclude(status='watching').filter(user=request.user, user_status='confirmed').order_by('-creation_date')
    return render(request, 
                  'web/outputs/following_outputs.html', 
                  {'following': following,
                   'following_spent': following_spent,
                   'following_spent_confirmed': following_spent_confirmed,})


@login_required
def search_output(request):
    search_form = SearchOutput(request.POST or None)

    if search_form.is_valid():
        txid, network, index = search_form.process()
        if not index == None:
            try:
                data = get_output_by_index(txid, index, network)
                transaction = Transaction.objects.get_or_create(transaction_id=txid, 
                                                                network=network,
                                                                transaction_index=data['tx_index'])[0]
                output = Output.objects.get_or_create(transaction=transaction, 
                                                      index=index, 
                                                      amount=data['value'],
                                                      script=data['script'])[0]
                FollowingOutputs.objects.create(user=request.user, output=output)
                return redirect(reverse('following-outputs')+ '?success=El output fue agregado a tu lista de seguimiento')
            except OutputAlreadySpentException as e:
                return redirect(reverse('search-output')+ '?msg=El output indicado ya fue gastado')
            except OutputNotFoundException as e:
                return redirect(reverse('search-output')+ '?msg=No se encontraron resultados')
            except InsightApiException as e:
                return redirect(reverse('search-output')+ '?msg=Ocurrio un error en el servidor')
            except IntegrityError as e:
                return redirect(reverse('following-outputs') + '?msg=Ya estas siguiendo el output indicado')

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
        return redirect(reverse('search-output')+ '?msg=El output indicado ya fue gastado')
    except OutputNotFoundException as e:
        return redirect(reverse('search-output')+ '?msg=No se encontraron resultados')
    except InsightApiException as e:
        return redirect(reverse('search-output')+ '?msg=Ocurrio un error en el servidor')
    except IntegrityError as e:
        return redirect(reverse('following-outputs') + '?msg=Ya estas siguiendo el output indicado')

    outputs = {'outputs': content}
    output_form = OutputForm(request.POST or None, 
                             initial={'transaction': txid, 
                                      'network': network, }, **outputs)
    if output_form.is_valid():
        index, amount, script, tx_index = output_form.process()
        transaction = Transaction.objects.get_or_create(transaction_id=txid, 
                                                        network=network, 
                                                        transaction_index=tx_index)[0]
        output = Output.objects.get_or_create(transaction=transaction, 
                                              index=index, 
                                              amount=amount,
                                              script=script)[0]
        try:
            FollowingOutputs.objects.create(user=request.user, output=output)
        except IntegrityError as e:
            return redirect(reverse('following-outputs') + '?msg=Ya estas siguiendo el output indicado')
    
        request.session.pop('txid', None)
        request.session.pop('network', None)
        return redirect(reverse('following-outputs')+ '?success=El output fue agregado a tu lista de seguimiento')

    return render(request, 
                  'web/outputs/add_output.html', 
                  { 'txid': txid,
                    'network': network,
                    'output_form': output_form,
                    'content': content })


@login_required
def cancel_output(request, following_id):
    try:
        following = FollowingOutputs.objects.get(user=request.user, id=following_id)
        following.delete()
        return redirect('following-outputs')
    except Exception:
        raise Http404


@login_required
def confirm_output(request, following_id):
    try:
        following = FollowingOutputs.objects.get(user=request.user, id=following_id)
        following.user_status = 'confirmed'
        following.save()
        return redirect('following-outputs')
    except Exception:
        raise Http404
