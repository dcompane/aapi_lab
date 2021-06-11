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

Input: No input. ensure to modify the alertIDs you want to modify
Output: printed confirmation from the response

Change Log
Date (YMD)    Name                  What
--------      ------------------    ------------------------
20210323      Daniel Companeetz     Initial commit
"""

import json
from pprint import pprint
from sys import exit
#Control-M Python API can be found at https://github.com/dcompane/controlm_py
import controlm_py as ctm
from controlm_py.rest import ApiException
from aapi_conn import CtmConnection

host_name = 'vl-aus-ctm-em01.ctm.bmc.com'
host_port = '8443'
endpoint = r'/automation-api'
aapi_user = 'CTMAPI'
aapi_password = 'ctmtickets'
host_ssl = True          # server using https only
aapi_verify_ssl = False  # False if server using self-signed SSL certs



# Create connection to the AAPI server
aapi_client = CtmConnection(host=host_name,port=host_port, 
                            user=aapi_user,password=aapi_password,
                            ssl=host_ssl, verify_ssl=aapi_verify_ssl,
                            additional_login_header={'Accept': 'application/json'})

run_instance = ctm.api.run_api.RunApi(api_client=aapi_client.api_client)

#Modifies properties of the alert
run_alert = ctm.AlertParam(alert_ids=[211089], urgency="Normal", comment="INC987654")

try:
    # runs the update.
    api_response = run_instance.update_alert(body=run_alert)
except ApiException as e:
    print("Exception when submitting alert update request: %s\n" % e)
    exit(30)

print(api_response)


#Updates the status of the alert
run_alert_status = ctm.AlertStatusParam(alert_ids=[211089], status="New")

try:
    # Retrieves a report by name.
    api_response = run_instance.update_alert_status(body=run_alert_status)
except ApiException as e:
    print("Exception when submitting alert update request: %s\n" % e)
    exit(30)

print(api_response)


aapi_client.logout()