#!/usr/bin/env python3
# unwrapurl: decodes short URLs and reveals 'hidden' details such as IP address, geolocation
# author: Carmelo C
# email: carmelo.califano@gmail.com
# history, date format ISO 8601:
#  2022-08-26: 1.0 initial version
# Adapted from: https://isc.sans.edu/diary/28980

# Import some modules
import argparse                    # Parser for command-line options, arguments and sub-commands
import ipinfo                      # IPinfo Python Client Library
import ipaddress                   # IPv4/IPv6 manipulation library
import json                        # JSON encoder and decoder
import requests                    # HTTP library for Python
import subprocess                  # Subprocess management
import sys                         # System-specific parameters and functions
from urllib.parse import urlparse  # Parse URLs into components

# Version number
__version__ = '1.0'
__build__ = '20220826'


def findLocation(url):
    """
    findLocation() sends a HEAD request to 'url', only headers are returned
    """
    o = requests.head(url)

    try:
        location = o.headers['Location']
        parsedURL = urlparse(location)
        if parsedURL.scheme[:4] == 'http':
            location = parsedURL.scheme + '://' + parsedURL.netloc
    except KeyError:
        print('[-] Location unavailable')
        sys.exit(20)  # ERROR: target location unavailable

    if ISVERBOSE == 1:
        print('[+] Target URL: "' + location + '"')
    elif ISVERBOSE > 1:
        print('[+] Scheme     : "' + parsedURL.scheme + '"')
        print('[+] Domain     : "' + parsedURL.netloc + '"')
        print('[+] Path       : "' + parsedURL.path + '"')
        print('[+] Params     : "' + parsedURL.params + '"')
        print('[+] Query      : "' + parsedURL.query + '"')
        print('[+] Fragment   : "' + parsedURL.fragment + '"')
    else:
        print(location)
        sys.exit(0)

    print('[+] Status code : "' + expandStatus(o.status_code) + '"', end = '\n\n')

    # a 2-tuple is returned, for instance: ('https://www.example.com', 'www.example.com')
    return (location, parsedURL.netloc)


def expandStatus(code):
    """
    expandStatus() displays a friendly text corresponding to the status code
    """
    if code == 302:
        return 'Found (302)'
    elif code == 307:
        return 'Temporary Redirect (307)'
    elif code == 308:
        return 'Permanent Redirect (308)'
    else:
        return str(code) 


def getIPfromURL(url):
    """
    getIPfromURL() does a DNS query to translate any URL(s) to an IP address
    Since CNAME are also possibly returned, some clean up is necessary
    """
    foundIPs = []
    process = subprocess.Popen(['dig', '+short', url],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
#    stdout, stderr
    outList = stdout.split()

    for listitem in outList:
       try:
           ipaddress.IPv4Address(listitem.decode('utf-8'))
           foundIPs.append(listitem.decode('utf-8'))
       except:
           pass

    length = len(foundIPs)
    if ISVERBOSE: print(f'[+] Found {length} IP address(es)', end = '\n\n')

    return foundIPs


def readConf():
    """ 
    readConf() reads the application's configuration from an external file.
    The file is JSON-formatted and contains:
    - the IPinfo access token
    Args:
    - none
    """
    try:
        with open('ipinfo_config.json', 'r') as config_in:
            config_json = json.load(config_in)
        if ISVERBOSE > 2: print('[+] Config file found')
        if config_json['TOKEN'] == '': 
            print('[-] IPinfo access token empty!')
            print('[-] Quitting!', end = '\n\n')
            sys.exit(30)  # ERROR: empty access token
        else:
            if ISVERBOSE > 2: print('[+] IPinfo access token found!')
    except FileNotFoundError:
        print('[-] Config file not found')
        print('[-] Quitting!', end = '\n\n')
        sys.exit(40)  # ERROR: config file not found

    return config_json['TOKEN']


def getIPdetails(ip, access_token):
    """ 
    getIPdetails() consumer the IPinfo API to harvest information about the 'ip' being passed on
    an access token is needed which is fetched from a JSON confind file by readConf()
    """
    handler = ipinfo.getHandler(access_token)
    return handler.getDetails(ip)


def main():
    parser = argparse.ArgumentParser(description='"Unwraps" short URLs showing all the hidden details, version ' + __version__ + ', build ' + __build__ + '.')
    parser.add_argument('-u', '--url', metavar = '<URL>', type = str, help = 'URL to be analyzed')
    parser.add_argument('-v', '--verbose', action = 'count', default = 0, help = 'Print extended information')
    parser.add_argument('-V', '--version', action = 'version', version = '%(prog)s ' + __version__)

    # In case of no arguments an help message is shown
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(10)  # ERROR: no arguments
    else:
        args = parser.parse_args() # parse command line

    # A global variable is instantiated in case of -v/--verbose argument
    global ISVERBOSE
    ISVERBOSE = args.verbose

    # Here the URL is "normalized", if a heading such as 'http://' is not present we add it
    # e.g.: example.com -> http://example.com
    url = args.url
    if url[:4] != 'http':
        url = 'http://' + url

    t_location = findLocation(url)
    ipList = getIPfromURL(t_location[1])
    access_token = readConf()
    for ip in ipList:
        details = getIPdetails(ip, access_token)
        print('[+] IP: ' + ip)
        try:
            print('[+] hostname: ' + details.hostname)
        except AttributeError:
            print('[+] hostname: not present')
            pass
        print('[+] org: ' + details.org, end = '\n\n')


if __name__ == '__main__':
    main()

