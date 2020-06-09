from email_finder import email_finder
from email_finder_gevent import email_finder_gevent
import time
import json


def main():
    with open('config', 'r') as config:
        content = json.load(config)
    print(content)
    start = time.time()
    if content["gevent"] == 1:
        email_finder("input.xml", 2)
    else:
        email_finder_gevent("input.xml", 2)
    print("Time wasted", time.time() - start)


if __name__ == '__main__':
    main()
