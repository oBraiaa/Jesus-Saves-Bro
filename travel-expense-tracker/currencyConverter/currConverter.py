# This is a new currency converter with a more limited selection of codes than the old one
# Code uses FreeCurrencyApi and is adapted from https://github.com/everapihq/freecurrencyapi-python

import freecurrencyapi

client = freecurrencyapi.Client('fca_live_dYpKygHdKc4ABOXLH1Gi3IOTN0The77WCKxEqdEV')

rates = client.latest()['data']

def convert(info):
    """
    Reads currency parameters and calculates the converted value
    #1. Original Currency
    #1. New currency
    #2. Amount to be converted (integers or floats only)
    """
    old_curr = info[0]
    new_curr = info[1]
    amount = float(info[2])

    old_to_usd = amount/float(rates[old_curr])
    result = float(rates[new_curr]) * old_to_usd
    return result
