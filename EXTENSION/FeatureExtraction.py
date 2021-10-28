# -*- coding: utf-8 -*-
import pandas as pd
import re
#pip install tldextract
#pip install whois
#pip install dnspython
import dns.resolver
import tldextract
import socket
from urlparse import urlparse
from urlparse import urlsplit
from bs4 import BeautifulSoup
import requests
import json
import urllib
import dill as pkl
import whois
import sys


"""#FEATURE EXTRACTION"""

#length url
def url_length(url):
    return len(url)

#IP
def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)|'  # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
        '[0-9a-fA-F]{7}', url)  # Ipv6
    if match:
        return 1
    else:
        return 0

#nb_dot


def count_dots(url):

    parsed = urlsplit(url)
    hostname = parsed.netloc
    return hostname.count('.')

#nb_hyphen
def count_hyphens(url):
    return url.count('-')

#nb_at
def count_at(url):
     return url.count('@')

#nb_qm
def count_questionmark(url):
    return url.count('?')

#nb_and
def count_and(url):
     return url.count('&')

#nb_or
def count_or(url):
    return url.count('|')

#nb_eq
def count_equal(url):
    return url.count('=')

#nb_underscore
def count_underscore(url):
    return url.count('_')

#nb_tilde
def count_tilde(url):
    if url.count('~')>0:
        return 1
    return 0

#nb_percent
def count_percentage(url):
    return url.count('%')

#nb_slash
def count_slash(url):
    return url.count('/')

#nb_star
def count_star(url):
    return url.count('*')

#nb_colon
def count_colon(url):
    return url.count(':')

#nb_comma
def count_comma(url):
     return url.count(',')

#nb_semicolon
def count_semicolon(url):
     return url.count(';')

#nb_dollar
def count_dollar(url):
     return url.count('$')

#nb_space
def count_space(url):
     return url.count(' ')+url.count('%20')

def req(url):
    extracted_domain = tldextract.extract(url)
    domain = extracted_domain.domain+'.'+extracted_domain.suffix
    subdomain = extracted_domain.subdomain
    tmp = url[url.find(extracted_domain.suffix):len(url)]
    pth = tmp.partition("/")
    path = pth[1] + pth[2]
    words_raw, words_raw_host, words_raw_path= words_raw_extraction(extracted_domain.domain, subdomain, pth[2])
    return  words_raw

def words_raw_extraction(domain, subdomain, path):
        w_domain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", domain.lower())
        w_subdomain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", subdomain.lower())
        w_path = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", path.lower())
        raw_words = w_domain + w_path + w_subdomain
        w_host = w_domain + w_subdomain
        raw_words = list(filter(None,raw_words))
        return raw_words, list(filter(None,w_host)), list(filter(None,w_path))

#nb_www
def check_www(url):
        words_raw = req(url)
        count = 0
        for word in words_raw:
            if not word.find('www') == -1:
                count += 1
        return count

def check_com(url):
        words_raw = req(url)
        count = 0
        for word in words_raw:
            if not word.find('com') == -1:
                count += 1
        return count

def count_double_slash(url):
    list=[x.start(0) for x in re.finditer('//', url)]
    if list[len(list)-1]>6:
        return 1
    else:
        return 0
    return url.count('//')

def req_path(url):
    extracted_domain = tldextract.extract(url)
    domain = extracted_domain.domain+'.'+extracted_domain.suffix
    subdomain = extracted_domain.subdomain
    tmp = url[url.find(extracted_domain.suffix):len(url)]
    pth = tmp.partition("/")
    path = pth[1] + pth[2]
    return  path

def req_scheme(url):
  parsed = urlparse(url)
  scheme = parsed.scheme
  return scheme

#http_in_path
def count_http_token(url):
    url_path = req_path(url)
    return url_path.count('http')

#https_token
def https_token(url):
    scheme = req_scheme(url)
    if scheme == 'https':
        return 0
    return 1

#nb_subdomain
def count_subdomain(url):
    if len(re.findall("\.", url)) == 1:
        return 1
    elif len(re.findall("\.", url)) == 2:
        return 2
    else:
        return 3

#prefix_suffix
def prefix_suffix(url):
    if re.findall(r"https?://[^\-]+-[^\-]+/", url):
        return 1
    else:
        return 0

#shortening_service
def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|''db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net', url)
    if match:
        return 1
    else:
        return 0

def is_URL_accessible(url):
    page = None
    try:
        page = requests.get(url, timeout=5)
    except:
        parsed = urlparse(url)
        url = parsed.scheme+'://'+parsed.netloc
        if not parsed.netloc.startswith('www'):
            url = parsed.scheme+'://www.'+parsed.netloc
            try:
                page = requests.get(url, timeout=5)
            except:
                page = None

    if page and page.status_code == 200 and page.content not in ["b''", "b' '"]:
            return page
    else:
            return None

def count_redirection(url):
    page = is_URL_accessible(url)
    if page == None:
      return 0
    return len(page.history)

def req_domain(url):
    extracted_domain = tldextract.extract(url)
    domain = extracted_domain.domain+'.'+extracted_domain.suffix
    return domain

#nb_external_redirection
def count_external_redirection(url):
    page = is_URL_accessible(url)
    domain = req_domain(url)
    count = 0
    if page == None:
        return 0
    if len(page.history) == 0:
        return 0
    else:
        for i, response in enumerate(page.history,1):
            if domain.lower() not in response.url.lower():
                count+=1
            return count

#statistical_report
def statistical_report(url):
    domain = req_domain(url)

    url_match=re.search('at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',url)
    try:
        ip_address=socket.gethostbyname(domain)
        ip_match=re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                           '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                           '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                           '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                           '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                           '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',ip_address)
        if url_match or ip_match:
            return 1
        else:
            return 0
    except:
        return 2


def req_iframe(url):
  page = is_URL_accessible(url)
  if page == None:
    return 1
  content = page.content
  soup = BeautifulSoup(content, 'html.parser', from_encoding='iso-8859-1')
  IFrame = {'visible':[], 'invisible':[], 'null':[]}
  for i_frame in soup.find_all('iframe', width=True, height=True, frameborder=True):
          if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['frameborder'] == "0":
              IFrame['invisible'].append(i_frame)
          else:
              IFrame['visible'].append(i_frame)
  for i_frame in soup.find_all('iframe', width=True, height=True, border=True):
          if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['border'] == "0":
              IFrame['invisible'].append(i_frame)
          else:
              IFrame['visible'].append(i_frame)
  for i_frame in soup.find_all('iframe', width=True, height=True, style=True):
          if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['style'] == "border:none;":
              IFrame['invisible'].append(i_frame)
          else:
              IFrame['visible'].append(i_frame)
  return IFrame

#iframe
def iframe(url):
    IFrame = req_iframe(url)
    if IFrame == 1:
      return 1
    if len(IFrame['invisible'])> 0:
        return 1
    return 0

#onmouseover
def onmouseover(url):
    page = is_URL_accessible(url)
    if page == None:
      return 1
    content = page.content
    if 'onmouseover="window.status=' in str(content).lower().replace(" ",""):
        return 1
    else:
        return 0

#right_clic
def right_clic(url):

    page = is_URL_accessible(url)
    if page == None:
      return 1
    content = page.content
    content = content.decode('ISO-8859-1')
    if re.findall(r"event.button ?== ?2", content):
        return 1
    else:
        return 0

#whois_registered_domain
def whois_registered_domain(url):
    domain = req_domain(url)
    try:
        hostname = whois.whois(domain).domain_name
        if type(hostname) == list:
            for host in hostname:
                if re.search(host.lower(), domain):
                    return 0
            return 1
        else:
            if re.search(hostname.lower(), domain):
                return 0
            else:
                return 1
    except:
        return 1

#domain_age
def domain_age(url):
    domain = req_domain(url)
    url1 = domain.split("//")[-1].split("/")[0].split('?')[0]
    show = "https://input.payapi.io/v1/api/fraud/domain/age/" + url1
    r = requests.get(show)

    if r.status_code == 200:
        data = r.text
        jsonToPython = json.loads(data)
        result = jsonToPython['result']
        if result == None:
            return -2
        else:
            return result
    else:
        return -1

#web_traffic
def web_traffic(url):
        try:
            rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
        except:
            return 0
        return int(rank)

#dns_record
def dns_record(url):
    domain = req_domain(url)
    try:
        nameservers = dns.resolver.resolve(domain,'NS')
        if len(nameservers)>0:
            return 0
        else:
            return 1
    except:
        return 1

def featureExtraction(url):

  features = []
  features.append(url_length(url))
  features.append(having_ip_address(url))
  features.append(count_dots(url))
  features.append(count_hyphens(url))
  features.append(count_at(url))
  features.append(count_questionmark(url))
  features.append(count_and(url))
  features.append(count_or(url))
  features.append(count_equal(url))
  features.append(count_underscore(url))
  features.append(count_tilde(url))
  features.append(count_percentage(url))
  features.append(count_slash(url))
  features.append(count_star(url))
  features.append(count_colon(url))
  features.append(count_comma(url))
  features.append(count_semicolon(url))
  features.append(count_dollar(url))
  features.append(count_space(url))
  features.append(check_www(url))
  features.append(check_com(url))
  features.append(count_double_slash(url))
  features.append(count_http_token(url))
  features.append(https_token(url))
  features.append(count_subdomain(url))
  features.append(prefix_suffix(url))
  features.append(shortening_service(url))
  features.append(count_redirection(url))
  features.append(count_external_redirection(url))
  features.append(statistical_report(url))
  features.append(iframe(url))
  features.append(onmouseover(url))
  features.append(right_clic(url))
  features.append(whois_registered_domain(url))
  features.append(domain_age(url))
  features.append(web_traffic(url))
  features.append(dns_record(url))


  return features

feature_names = ['length_url','ip','nb_dots','nb_hyphens','nb_at','nb_qm','nb_and','nb_or','nb_eq','nb_underscore',
            'nb_tilde','nb_percent','nb_slash','nb_star','nb_colon','nb_comma','nb_semicolumn','nb_dollar','nb_space',
            'nb_www','nb_com','nb_dslash','http_in_path','https_token','nb_subdomains','prefix_suffix','shortening_service',
            'nb_redirection','nb_external_redirection','statistical_report','iframe','onmouseover','right_clic','whois_registered_domain',
            'domain_age','web_traffic','dns_record']

def predict(url):

  phish_features = []
  phish_features.append(featureExtraction(url))
  feature_names = ['length_url','ip','nb_dots','nb_hyphens','nb_at','nb_qm','nb_and','nb_or','nb_eq','nb_underscore',
              'nb_tilde','nb_percent','nb_slash','nb_star','nb_colon','nb_comma','nb_semicolumn','nb_dollar','nb_space',
              'nb_www','nb_com','nb_dslash','http_in_path','https_token','nb_subdomains','prefix_suffix','shortening_service',
              'nb_redirection','nb_external_redirection','statistical_report','iframe','onmouseover','right_clic','whois_registered_domain',
              'domain_age','web_traffic','dns_record']
  myfeatures = pd.DataFrame(phish_features, columns= feature_names)
  import pickle
  print(myfeatures)
  model = pickle.load(open('Final_Model_Extension.pkl','r'))

  status = model.predict(myfeatures)
  return status

def main():
    url = sys.argv[1]
    print(url)
    result = predict(url)
    if result == 0:
        print("SAFE")
    elif result == 1:
        print("PHISHING")

        # print 'Error -', features_test
if __name__ == "__main__":
    main()
