import argparse
import requests
from urllib.parse import urlparse
from requests.exceptions import RequestException, SSLError, ConnectionError
import csv

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD', 'PATCH', 'TRACE', 'CONNECT']

def load_targets(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def test_http_verbs(targets, follow_redirects, user_agent, cookie):
    session = requests.Session()
    headers = {}
    if user_agent:
        headers['User-Agent'] = user_agent
    if cookie:
        headers['Cookie'] = cookie

    results = []
    total_requests = 0

    for target in targets:
        parsed = urlparse(target)
        if not parsed.scheme:
            urls_to_try = [f"https://{target}", f"http://{target}"]
        else:
            urls_to_try = [target]

        successful_base_url = None
        for base_url in urls_to_try:
            try:
                test_url = f"{base_url}/"
                resp = session.get(test_url, headers=headers, timeout=5, allow_redirects=follow_redirects)
                successful_base_url = base_url
                break
            except RequestException:
                continue

        if not successful_base_url:
            results.append({
                'Target': target,
                'Method': 'N/A',
                'URL': 'All attempts failed',
                'Status': 'Error',
                'Reason': 'Could not connect'
            })
            continue

        for method in HTTP_METHODS:
            try:
                req = requests.Request(method, successful_base_url, headers=headers)
                prepped = session.prepare_request(req)
                resp = session.send(prepped, timeout=5, allow_redirects=follow_redirects)
                results.append({
                    'Target': target,
                    'Method': method,
                    'URL': successful_base_url,
                    'Status': resp.status_code,
                    'Reason': resp.reason
                })
                total_requests += 1
            except (RequestException, SSLError, ConnectionError) as e:
                results.append({
                    'Target': target,
                    'Method': method,
                    'URL': successful_base_url,
                    'Status': 'Error',
                    'Reason': str(e)
                })
                total_requests += 1

    return results, total_requests

def write_results_to_file(results, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

def print_summary(results, total_requests):
    print("\n====== SUMMARY ======")
    print(f"Total Targets: {len(set(r['Target'] for r in results))}")
    print(f"Total Requests Sent: {total_requests}")
    print(f"Total Success Responses: {sum(1 for r in results if isinstance(r['Status'], int))}")
    print(f"Total Errors: {sum(1 for r in results if not isinstance(r['Status'], int))}")
    print("=====================")

    return input("Do you want to print the full results to screen? (yes/no): ").strip().lower() in ['yes', 'y']

def print_results(results):
    for r in results:
        print(f"{r['Target']:30} | {r['Method']:8} | {r['URL']:40} | {r['Status']:6} | {r['Reason']}")

def main():
    parser = argparse.ArgumentParser(description="HTTP Verb Tampering Tester")
    parser.add_argument('-L', '--list', required=True, help='Input file with target domains (one per line)')
    parser.add_argument('-O', '--output', required=True, help='Output file to write results (CSV format)')
    parser.add_argument('-f', '--follow', action='store_true', help='Follow redirects')
    parser.add_argument('--user-agent', help='Custom User-Agent string')
    parser.add_argument('--cookie', help='Cookie string for session/auth')
    args = parser.parse_args()

    targets = load_targets(args.list)
    results, total_requests = test_http_verbs(
        targets,
        follow_redirects=args.follow,
        user_agent=args.user_agent,
        cookie=args.cookie
    )

    write_results_to_file(results, args.output)
    if print_summary(results, total_requests):
        print_results(results)

if __name__ == '__main__':
    main()
