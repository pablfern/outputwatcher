# -*- coding: utf-8 -*-
import json
import urllib
import httplib2


class OutputAlreadySpentException(Exception):
    pass


class OutputNotFoundException(Exception):
    pass


class InsightApiException(Exception):
    pass


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
                            #'address': out['scriptPubKey']['addresses'],
                            'index': out['n'],
                            }
                    outputs.append(aux)
            return outputs
    raise InsightApiException()


def get_output_by_index(txid, index, network):
    url = base_url(network) + 'tx/' + txid
    h = httplib2.Http()
    resp, content = h.request(url, method="GET")
    if resp.status == 200:
        content = json.loads(content)
        if 'vout' in content:
            for out in content['vout']:
                if out['n'] == index:
                    if not out['spentTxId']:
                        return {'value': out['value'],
                                'index': index}
                    else:
                        raise OutputAlreadySpentException()
            raise OutputNotFoundException()
    raise InsightApiException()
