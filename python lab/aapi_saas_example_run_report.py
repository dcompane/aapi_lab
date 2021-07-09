"""
(c) 2020 Daniel Companeetz
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice (including the next paragraph) shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
https://opensource.org/licenses/MIT

# SPDX-License-Identifier: MIT
For information on SDPX, https://spdx.org/licenses/MIT.html

Input: a file name
Output, a table with the names defined in the program, and the line numbers where they were used.

Change Log
Date (YMD)    Name                  What
--------      ------------------    ------------------------
20200620      Daniel Companeetz     Initial commit
"""

import json
from sys import exit
from time import sleep
from urllib3 import PoolManager
from urllib3 import disable_warnings
from urllib3.exceptions import NewConnectionError, MaxRetryError, InsecureRequestWarning
from shutil import copyfileobj

import controlm_py as ctm
from controlm_py.rest import ApiException
from aapi_conn import SaaSConnection


host_name = 'your_tenant.url.com'
host_port = '443'
endpoint = r'/automation-api'
aapi_token = 'ABCDEFGHIJKLMN=='
host_ssl = True          # server using https only
aapi_verify_ssl = False  # False if server using self-signed SSL certs

# Create connection to the AAPI server
aapi_client = SaaSConnection(host=host_name,port=host_port, endpoint=endpoint,
                            aapi_token=aapi_token, ssl=host_ssl, verify_ssl=aapi_verify_ssl,
                            additional_login_header={'Accept': 'application/json'})

rpt_instance = ctm.api.reporting_api.ReportingApi(api_client=aapi_client.api_client)

name = 'Workloads_1' # str | The report name.
format = 'csv' # str |  (optional)
file_path = r'c:\temp\Workloads_1.csv'
report_run = ctm.RunReport(name=name, format=format) # RunReport object parameters | The report generation parameters


try:
    # Retrieves a report by name.
    api_response = rpt_instance.run_report(report_run)
except ApiException as e:
    print("Exception when submitting report request: %s\n" % e)
    exit(30)


while api_response.status == 'PROCESSING':
    sleep (10) # sleeps 10 seconds
    try: 
        api_response = rpt_instance.get_report_status(report_id=api_response.report_id)
    except ApiException as e:
        print("Exception when submitting report request: %s\n" % e)
        exit(30)
file_url = api_response.url
file_path = r'c:\temp\activejobs1.csv'
http = PoolManager()
try: 
    headers ={'x-api-key': aapi_token}
    with http.request('GET', file_url, headers=headers, preload_content=False) as http_response, open(file_path, 'wb') as out_file:       
        copyfileobj(http_response, out_file)
except:
    print("Exception when retrieving report")


