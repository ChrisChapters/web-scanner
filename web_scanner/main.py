import argparse
from web_scanner import scanner

def main():
    parser = argparse.ArgumentParser(description='Web Vulnerability Scanner')
    parser.add_argument('url', help='URL of the website to check')
    args = parser.parse_args()

    scanner.check_vulnerabilities(args.url)

if __name__ == '__main__':
    main()
