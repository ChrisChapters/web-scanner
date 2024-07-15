# Web Scanner

## Overview
Web Scanner is a Python tool designed for detecting SQL injection vulnerabilities in web applications. It utilizes techniques to test both query parameters and form inputs for various SQL injection payloads.

## Features
- **SQL Injection Detection**: Checks for common SQL injection vulnerabilities using different types of payloads.
- **Query Parameter Testing**: Tests query parameters in URLs for potential vulnerabilities.
- **Form Input Testing**: Analyzes form inputs for susceptibility to SQL injection attacks.

## Requirements
- Python 3.x
- Requests library (`pip install requests`)
- BeautifulSoup library (`pip install beautifulsoup4`)

## Usage
1. Clone the repository:
   
2.   git clone https://github.com/ChrisChapters/web-scanner.git
   
3.   cd web-scanner

4.   python -m venv venv

5.   source venv\bin\activate\

6.   pip install .

7.   web-scanner "website url"  //eg:web-scanner http://testphp.vulnweb.com/

   
