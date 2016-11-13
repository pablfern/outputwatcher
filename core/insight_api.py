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
        return 'https://blockchain.info/es/rawtx/$tx_hash'
    if network == 'livenet':
        return 'https://insight.bitpay.com/api/'
    return None


def get_outputs(txid, network):
    url = 'https://blockchain.info/es/rawtx/' + txid
    h = httplib2.Http()
    resp, content = h.request(url, method="GET")
    if resp.status == 200:
        content = json.loads(content)
        if 'out' in content:
            outputs = []
            for out in content['out']:
                if 'spent' not in out or not out['spent']:
                    aux = { 'value': out['value'],
                            'index': out['n'],
                            'script': out['script'],
                            'tx_index': out['tx_index'],
                            }
                    outputs.append(aux)
            return outputs
    raise InsightApiException()


def get_output_by_index(txid, index, network):
    url = 'https://blockchain.info/es/rawtx/' + txid
    h = httplib2.Http()
    resp, content = h.request(url, method="GET")
    if resp.status == 200:
        content = json.loads(content)
        if 'out' in content:
            for out in content['out']:
                if out['n'] == index:
                    if 'spent' not in out or not out['spent']:
                        return {'value': out['value'],
                                'index': out['n'],
                                'script': out['script'],
                                'tx_index': out['tx_index'],
                                }
                    else:
                        raise OutputAlreadySpentException()
            raise OutputNotFoundException()
    raise InsightApiException()
