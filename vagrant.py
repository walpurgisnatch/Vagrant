import argparse
import requests
import threading
import time
import http.client as httplib
import re

from queue import Queue


interesting_domains = []
to_discover = []
threads = 24
output = []
defaults = ["interesting_domains.list", "to_discover.list"]
queue = Queue()

def get_args():
    global threads
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domains", dest="domains", help="Domains to walk through")
    parser.add_argument("-o", "--output", dest="output", nargs='*', help="Send output to file")
    parser.add_argument("-b", "--both", dest="both", action="store_true", help="Creates two files in current directory with default names")
    parser.add_argument("-t", "--threads", type=int, dest="threads", help="Number of threads")
    arguments = parser.parse_args()
    if not arguments.domains:
        parser.error("null target")
    if arguments.threads:
        threads = arguments.threads
    return arguments

args = get_args()

def fine_url(url):
    try:
        response = requests.get(url, timeout=2.5)
    except:
        return set_url(url)
    return url

def set_url(url):
    try:
        test = httplib.HTTPSConnection(url)
        test.request("GET", "/")
        response = test.getresponse()
        if (response.status == 200) | (response.status == 302):
            url = "https://www." + str(url)
        else:
            url = "http://www." + str(url)
    except:
        url = "http://" + str(url)
    return url

def threader():
    while True:
        domain = queue.get()
        run_domain(domain)
        queue.task_done()

def walk_through(domains):
    for x in range(threads):
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
    check_domain(fine_url(domain))        

def check_domain(url):
    try:
        response = requests.get(url, timeout=2.5)
        location = re.search('^(.*:\/\/.*?)\/', response.url + '/').group(1)
        if response.status_code == 200 and len(response.content) > 200 and location not in interesting_domains:              
            interesting_domains.append(location)
            print("[+] {} looks interesting".format(location))
            write_line(to_file(0), location)
        elif output_exists[1] or args.both:
            if response.status_code != 404 and location not in to_discover:
                to_discover.append(location)            
                write_line(to_file(1), location)            
    except Exception as e:
        pass

def to_file(i):
    if output_exists(output, i):
        return output[i]
    elif args.both:
        if i == 0:
            return defaults[0]
        return defaults[1]

def output_exists(o, i):
    if len(o) > i and o[i]:
        return True
    return False

def print_results():
    print("Done\n")
    print("[Alive domains] {}".format(len(interesting_domains + to_discover)))
    print("[Interesting domains] {}".format(len(interesting_domains)))
    print("[To discover] {}".format(len(to_discover)))

def write_line(fname, data):
    with open(fname, 'a') as f:
        f.write(data + "\n")

def main():
    try:
        if args.output:
            if output_exists(args.output[0]):
                output.append(args.output[0])
            if output_exists(args.output[1]):
                output.append(args.output[1])
        walk_through(args.domains)
        print_results()
    except KeyboardInterrupt:
        print("\nAborted\n")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
