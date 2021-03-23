import argparse
import requests
import threading
import time
import http.client as httplib
import fileworks
import re

from queue import Queue


interesting_domains = []
to_discover = []
queue = Queue()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domains", dest="domains", help="Domains to walk through")    
    arguments = parser.parse_args()
    if not arguments.domains:
        parser.error("null target")
    return arguments

def threader():
    while True:
        domain = queue.get()
        run_domain(domain)
        queue.task_done()

def walk_through(domains):
    for x in range(24):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    f = open(domains, "r")
    for line in f:
        try:
            queue.put(line.strip())
        except:
            pass
    f.close()

    queue.join()

def run_domain(domain):        
    check_domain(domain)        

def check_domain(url):
    try:
        response = requests.get(url, timeout=2.5)
        location = re.search('(.*:\/\/.*?[.].*?)\/', response.url + '/').group(1)
        if response.status_code == 200 and len(response.content) > 200 and location not in interesting_domains:              
            interesting_domains.append(location)
            fileworks.write_line("interesting_domains.list", location)
            print("[+] {} looks interesting".format(location))
        elif response.status_code != 404 and location not in to_discover:
            to_discover.append(location)
            fileworks.write_line("to_discover.list", location)
    except Exception as e:
        pass

def print_results():
    print("Done\n")
    print("[Alive domains] {}".format(len(interesting_domains + to_discover)))
    print("[Interesting domains] {}".format(len(interesting_domains)))
    print("[To discover] {}".format(len(to_discover)))

def main():
    args = get_args()
    try:
        walk_through(args.domains)
        print_results()
    except KeyboardInterrupt:
        print("\nAborted\n")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

