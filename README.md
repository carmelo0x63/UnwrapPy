# UnWrapPy
Python script decoding shortened URLs and displaying such "hidden" info as the source IP address: Un-wrap-Application-Python -> UnWrapPy

The script is based on [Requests](https://requests.readthedocs.io/) and the [IPinfo Python Client Library](https://github.com/ipinfo/python).
The two libraries are used to safely decode short URLs and gather additional info such as the source IP address, location and more.

----

Inspired by [Taking Apart URL Shorteners](https://isc.sans.edu/diary/28980), I decided to implement the same in Python while adding a few additional features.</br>
[I know](https://en.wikipedia.org/wiki/KISS_principle) this shouldn't be done but boredom on a rainy weekend, you know...</br>

### Initialize
```
$ python3 -m venv venv

$ source venv/bin/activate

(venv) $ python3 -m pip install --upgrade pip setuptools wheel

(venv) $ python3 -m pip install requests ipinfo
```

----

An example manual process will help explain what the script does and how it can help speed up the discovery process.</br>
"https[://]bit.ly[/]3ABvcy5" is a short address pointing to "https://isc.sans.edu/". The URL is safe but how can we get more details.</br>
bitly offers a method to do so, by adding a "+" ("plus sign") to the URL the user's browser will be pointed to a bit.ly page showing the decoded URL.</br>
What if we'd want to do the same in a programmatic and CLI-based way?</br>

1. use a program, such as `curl`, to fetch the headers from the URL shortener service:
```
$ URL="https://bit.ly/3ABvcy5"; curl -s -k -v -I $URL 2>&1 | awk -F" " 'tolower($1) ~ /^location:/ {print $2}'
https://isc.sans.edu/
```
**NOTE**:
- `-s`: disable the progress meter
- `-k`: insecure, that is no TLS, for testing purpose only
- `-v`: verbose
- `-I`: fetch HTTP headers only
The latter option is important, by using it we won't fetch the whole HTML!</br>

2. next, we resolve the name into one of more IP addresses:
```
$ dig +short isc.sans.ed 
45.60.103.34
45.60.31.34
```

3. finally, we use an online service, such as `ipinfo.io`, to gather more information on the literal IP addresses we've resolved the original URL to:
```
$  curl -H "Authorization: Bearer $TOKEN" -H "Accept: application/json" ipinfo.io/45.60.103.34 
{
  "ip": "45.60.103.34",
  "city": "Redwood City",
  "region": "California",
  "country": "US",
  "loc": "37.5331,-122.2486",
  "org": "AS19551 Incapsula Inc",
  "postal": "94065",
  "timezone": "America/Los_Angeles"
}%
```

----

### Python process
The same process but in Python this time:
```
>>> import requests, subprocess, ipinfo

>>> url = 'https://bit.ly/3ABvcy5'
>>> o = requests.head(url)
>>> o.headers
{'Server': 'nginx', 'Date': 'Sat, 27 Aug 2022 19:10:18 GMT', 'Content-Type': 'text/html; charset=utf-8', 'Content-Length': '108', 'Cache-Control': 'private, max-age=90', 'Location': 'https://isc.sans.edu/', 'Via': '1.1 google', 'Alt-Svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000'}
>>> o.status_code
301

>>> url = 'isc.sans.edu'
>>> subprocess.check_output(['dig', '+short', url])
b'45.60.103.34\n45.60.31.34\n'

>>> access_token = '***'
>>> handler = ipinfo.getHandler(access_token)
>>> result = handler.getDetails('45.60.103.34')
>>> result.details
{'ip': '45.60.103.34', 'city': 'Redwood City', 'region': 'California', 'country': 'US', 'loc': '37.5331,-122.2486', 'org': 'AS19551 Incapsula Inc', 'postal': '94065', 'timezone': 'America/Los_Angeles', 'country_name': 'United States', 'isEU': False, 'latitude': '37.5331', 'longitude': '-122.2486'}
```

----

### A few test URLs

https://bit.ly/3ABvcy5 -> 'https://isc.sans.edu/'

https://4vnx.short.gy/BuB4TW -> 'https://isc.sans.edu/'

https://tinyurl.com/bdhf48p4 -> 'http://isc.sans.edu/'

https://rb.gy/rickpn -> 'https://isc.sans.edu/'

https://tinyurl.com/3tuudmuv -> 'mailto:rob@coherentsecurity.com'

https://tinyurl.com/4zkd52jt -> 'tel://2725035'

https://t.co/0BACDYaBmU -> 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

https://f00.it/p9523 -> https://fxhomeonline.com/cb/?t=sms8&num=3351222469&name=Carmelo&surname=Califano&email=&privacy=https%3A%2F%2Fbit.ly%2Fe7_privacy


for URL in bit.ly/3ABvcy5 4vnx.short.gy/BuB4TW tinyurl.com/bdhf48p4 rb.gy/rickpn tinyurl.com/3tuudmuv tinyurl.com/4zkd52jt t.co/0BACDYaBmU f00.it/p9523; do echo $URL": "; ./unwrapurl.py -v -u $URL; done 







