import argparse
import requests
import yaml
import time
from datetime import datetime

def load_endpoints(filepath):
    try:
        with open(filepath, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
    except PermissionError:
        print(f"Error: Permission denied accessing {filepath}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")
    return None

def check_health(endpoint):
    try:
        response = requests.request(
            method=endpoint.get('method', 'GET'),
            url=endpoint['url'],
            headers=endpoint.get('headers', {}),
            data=endpoint.get('body', ''),
            timeout=0.5,
        )
        return 200 <= response.status_code < 300 and \
               response.elapsed.total_seconds() < 0.5
    except requests.RequestException:
        return False

def main():
    parser = argparse.ArgumentParser(description="Health checker for HTTP endpoints.")
    parser.add_argument(
        'yaml_file', 
        type=str, 
        help="Path to the YAML file containing the endpoints.",
        default='endpoints.yml',
        nargs='?'
    )
    args = parser.parse_args()

    endpoints = load_endpoints(args.yaml_file)
    health_stats = {}

    try:
        while True:
            print(f"Checking health... {datetime.now()}")
            for endpoint in endpoints:
                domain = endpoint['url'].split('/')[2]
                health_stats.setdefault(domain, {'up': 0, 'total': 0})

                if check_health(endpoint):
                    health_stats[domain]['up'] += 1
                health_stats[domain]['total'] += 1
            
            for domain, stats in health_stats.items():
                availability = (stats['up'] / stats['total']) * 100
                #print(f"Debug: {domain} {stats['up']} {stats['total']}")
                print(f"{domain} has {availability:.0f}% availability percentage")
            
            time.sleep(15)
    
    except KeyboardInterrupt:
        print("Program interrupted by user")
    
if __name__ == "__main__":
    main()