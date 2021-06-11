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
20210503      Daniel Companeetz     Initial commit
"""



import json
from sys import exit
#Control-M Python API can be found at https://github.com/dcompane/controlm_py
import controlm_py as ctm
from controlm_py.rest import ApiException
from aapi_conn import SaaSConnection

host_name = 'se-pre-prod-aapi.us1.preprod.ctmsaas.com'
host_port = '443'
endpoint = r'/automation-api'
aapi_token = 'UFBSR0JYOmVlOTkxODY5LWQ1MmMtNDQ2Zi05ODJlLWZiYWUzMjY0NGFjOTpRZEJ1TzlzZkc3TEc4UmFRQlZWL29GdW92MllhakNOYkM2eExwT0dNcmtRPQ=='
host_ssl = True          # server using https only
aapi_verify_ssl = False  # False if server using self-signed SSL certs

# Create connection to the AAPI server
aapi_client = SaaSConnection(host=host_name,port=host_port, endpoint=endpoint,
                            aapi_token=aapi_token, ssl=host_ssl, verify_ssl=aapi_verify_ssl,
                            additional_login_header={'Accept': 'application/json'})

deploy_instance = ctm.api.deploy_api.DeployApi(api_client=aapi_client.api_client)

format = 'json' # str | Output format (json or xml) (optional) (default to json)
#format = 'xml:folder' # str | Output format (json or xml) (optional) (default to json)
#format = 'xml:job' # str | Output format (json or xml) (optional) (default to json)

folder = 'dco-alicorp' # str |  (optional)
#folder = 'DCO_IBP-Test' # str |  (optional) This fails because of the AI jobs

ctm = 'IN01' # str |  (optional) 

result={}
try:
    # Get deployed jobs that match the search criteria.
    api_response = deploy_instance.get_deployed_folders_new(format=format, folder=folder, ctm=ctm)
    print(api_response.replace("'",'"'))
    result = json.loads(api_response.replace("'",'"'))
except ApiException as e:
    print("Exception when calling DeployApi->get_deployed_folders_new: %s\n" % e)
except NameError as e:
    print("Exception: The API returned an error when calling DeployApi->get_deployed_folders_new: %s\n" % e)


# aapi_client.logout()

exit(0)
