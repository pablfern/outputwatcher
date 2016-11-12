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
            aux = []
            for out in content['vout']:
                aux.append(out) if not out['spentTxId'] else None
            return content['vout']    
    return {}
