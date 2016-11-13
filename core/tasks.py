# -*- coding: utf-8 -*-
import json
from celery import Celery
from datetime import datetime
from core.models import Output, Transaction, FollowingOutputs
from core.emails import output_in_tx_email, output_in_confirmed_tx_email


app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task()
def process_request(data):
    json_data = json.loads(data)
    if 'op' in json_data:
        if json_data['op'] == 'utx':
            process_tx_update(json_data)
        elif json_data['op']=='block':
            process_block(json_data)


@app.task()
def process_block(json_data):
    confirmed_date = datetime.fromtimestamp(json_data['x']['time'])
    for tx in Transaction.objects.filter(transaction_index__in=json_data['x']['txIndexes']):
        tx.confirmed_date = confirmed_date
        tx.save()
        for follow in FollowingOutputs.objects.filter(output__transaction=tx):
            follow.status = 'confirmed'
            output_in_confirmed_tx_email()
            send_output_in_confirmed_tx_email.delay(follow.id)


@app.task()
def process_tx_update(json_data):
    if json_data['op'] == "utx" and 'x' in json_data:
        scripts = []
        for _input in json_data['x']['inputs']:
            scripts.append(_input['prev_out']['script'])
        
        if FollowingOutputs.objects.filter(status__in=['watching', 'used'],
                                           output__script__in=scripts).exists():
            # TODO: We are only using livenet. Testnet should be added
            tx = Transaction.objects.get_or_create(transaction_id=json_data['x']['hash'], 
                                                   network='livenet')[0]
            spent_date = datetime.fromtimestamp(json_data['x']['time'])
            for follow in FollowingOutputs.objects.filter(status__in=['watching', 'used'],
                                                          output__script__in=scripts):
                follow.output.spent_transaction = tx
                follow.output.spent_date = spent_date
                # follow.output.spent_index = 
                follow.output.save()
                follow.status = 'used'
                follow.save()
                send_output_in_tx_email.delay(follow.id)
                print 'Following output updated ' + follow.id
        else:
            print 'Discarding tx notification...'


@app.task()
def send_output_in_tx_email(follow_id):
    follow = FollowingOutputs.objects.get(id=follow_id)
    # TODO: Put output data here
    output_in_tx_email("OUTPUT?", follow.output.index, follow.output.spent_transaction.transaction_id, [follow.user.email])


@app.task()
def send_output_in_confirmed_tx_email(follow_id):
    follow = FollowingOutputs.objects.get(id=follow_id)
    # TODO: Put output data here
    output_in_confirmed_tx_email("OUTPUT?", follow.output.index, follow.output.spent_transaction.transaction_id, [follow.user.email])


@app.task()
def test_task():
    print 'Test task'
