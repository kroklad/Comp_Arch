import sys
import os.path
import re
import urllib.request
import gevent
from gevent import socket


def find_emails(uri, output, nesting, max_nesting):
    output.write("<url>\n")
    output.write(uri+"\n")
    output.write("</url>\n")
    page = urllib.request.urlopen(uri)
    page_text = page.read().decode("utf8")
    # find a@a-a.a a(at)a-a.a
    p = r'([a-zA-Z0-9_.+-]+(?:@|\(at\))(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z0-9]+)'
    result = re.findall(p, page_text, re.MULTILINE | re.IGNORECASE)
    # print(uri)
    for email in result:
        # print(email)
        output.write('<email>\n')
        output.write(email)
        output.write('\n</email>\n')
    if nesting == max_nesting:
        return
    p = r'(?:href=\")([a-zA-Z0-9-_./:]+)(?:")'
    result = re.findall(p, page_text, re.MULTILINE | re.IGNORECASE)
    threads = []
    for href in result:
        threads.append(gevent.spawn(find_emails,
                                    href, output, nesting+1, max_nesting))
    gevent.joinall(threads)


def email_finder_gevent(input_, max_nesting):
    with open(input_, 'r') as input:
        content = input.read()
    p = r'(?:<url>)([a-zA-Z0-9:/._-]+)(?:</url>)'
    result = re.findall(p, content, re.MULTILINE | re.IGNORECASE)
    with open('output.xml', 'w') as output:
        threads = []
        for url in result:
            threads.append(gevent.spawn(find_emails,
                                        url, output, 0, max_nesting))
        gevent.joinall(threads)
