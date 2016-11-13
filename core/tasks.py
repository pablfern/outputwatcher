# -*- coding: utf-8 -*-
import json
from celery import Celery
from datetime import datetime
from core.models import Output, Transaction, FollowingOutputs

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task()
def process_tx_update(data):
    json_data = json.loads(data)
    if 'op' in json_data and json_data['op'] == "utx" and 'x' in json_data:
        scripts = []
        for _input in json_data['x']['inputs']:
            scripts.append(_input['prev_out']['script'])
        
        if FollowingOutputs.objects.filter(status='watching',
                                           output__script__in=scripts).exists():
            # TODO: We are only using livenet. Testnet should be added
            tx = Transaction.objects.get_or_create(transaction_id=json_data['x']['hash'], 
                                                   network='livenet')[0]
            spent_date = datetime.fromtimestamp(json_data['x']['time'])
            for follow in FollowingOutputs.objects.filter(status='watching',
                                                          output__script__in=scripts):
                follow.output.spent_transaction = tx
                follow.output.save()
                follow.status = 'notified'
                follow.save()
                send_email(follow.id)
                print 'Following output updated ' + follow.id
        else:
            print 'Discarding tx notification...'

@app.task()
def send_email():
    pass


@app.task()
def test_task():
    print 'WOlolo'