# -*- coding: utf-8 -*-
import json
import urllib
import httplib2


def base_url(network):
    if network == 'testnet':
        return 'https://test-insight.bitpay.com/api/'
    if network == 'livenet':
        return 'https://insight.bitpay.com/api/'
    return None


def get_outputs(txid, network):
    url = base_url(network) + 'tx/' + txid
    h = httplib2.Http()
    resp, content = h.request(url, method="GET")
    if resp.status == 200:
        content = json.loads(content)
        if 'vout' in content:
            outputs = []
            for out in content['vout']:
                if not out['spentTxId']:
                    aux = { 'value': out['value'],
                            'address': out['scriptPubKey']['addresses'],
                            'index': out['n'],
                            }
                    outputs.append(aux)
            return outputs    
    return {}
