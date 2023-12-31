#!/usr/bin/python3

import argparse
from concurrent.futures import ThreadPoolExecutor
import dns.resolver
import time
import socket
import json

def dns_query(resolver, fqdn, record_type='A', nameserver=None):
    if nameserver:
        resolver.nameservers = [nameserver]
    start_time = time.time()
    answer = resolver.resolve(fqdn, record_type)
    resolution_time = (time.time() - start_time) * 1000
    epoch_timestamp_millis = int(time.time() * 1000)
    responses = [str(r) for r in answer.rrset]
    return {
        "fqdn": fqdn,
        "record_type": record_type,
        "resolution_time": resolution_time,
        "responses": responses,
        "epoch_timestamp_millis": epoch_timestamp_millis
    }

def load_test(fqdn, record_type, num_requests, concurrency, nameserver=None):
    resolver = dns.resolver.Resolver()
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        results = list(executor.map(lambda _: dns_query(resolver, fqdn, record_type, nameserver), range(num_requests)))

    total_time = sum(res["resolution_time"] for res in results)
    avg_time = total_time / len(results)
    return avg_time, results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNS Load Tester")
    parser.add_argument("--dns_server", required=True, help="DNS server IP address")
    parser.add_argument("--fqdn", required=True, help="Fully Qualified Domain Name")
    parser.add_argument("--num_requests", required=True, type=int, help="Number of DNS requests to make")
    parser.add_argument("--concurrency", required=True, type=int, help="Number of concurrent requests")

    args = parser.parse_args()

    dns_server = args.dns_server
    fqdn = args.fqdn
    num_requests = args.num_requests
    concurrency = args.concurrency
    record_type = 'A'  # Kept as a constant for this example

    start_time = time.time()
    avg_response_time, responses = load_test(fqdn, record_type, num_requests, concurrency, dns_server)
    end_time = time.time()
    total_duration = (end_time - start_time) * 1000

    hostname = socket.gethostname()
    filename = f"{int((num_requests / total_duration) * 1000)}-rps_{int(avg_response_time)}-art_{num_requests}-rqusts_{concurrency}-thrds_{fqdn}_{hostname}.json"

    with open(filename, "w") as f:
        output_data = {
            "dns_server": dns_server,
            "threads": concurrency,
            "num_requests": num_requests,
            "test_duration_msecs": total_duration,
            "responses_per_sec": (num_requests / total_duration) * 1000,
            "average_response_msecs": avg_response_time,
            "responses": responses
        }
        json.dump(output_data, f, indent=4)
