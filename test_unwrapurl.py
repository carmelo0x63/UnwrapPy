import unwrapurl

def test_bit_ly():
    assert unwrapurl.findLocation('https://bit.ly/3ABvcy5')[0] == 'https://isc.sans.edu/'

def test_short_gy():
    assert unwrapurl.findLocation('https://4vnx.short.gy/BuB4TW')[0] == 'https://isc.sans.edu/'

def test_tinyurl_com():
    assert unwrapurl.findLocation('https://tinyurl.com/bdhf48p4')[0] == 'http://isc.sans.edu/'

def test_rb_gy():
    assert unwrapurl.findLocation('https://rb.gy/rickpn')[0] == 'https://isc.sans.edu/'

def test_mailto():
    assert unwrapurl.findLocation('https://tinyurl.com/3tuudmuv')[0] == 'mailto:rob@coherentsecurity.com'

def test_tel():
    assert unwrapurl.findLocation('https://tinyurl.com/4zkd52jt')[0] == 'tel://2725035'

def test_t_co():
    assert unwrapurl.findLocation('https://t.co/0BACDYaBmU')[0] == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

