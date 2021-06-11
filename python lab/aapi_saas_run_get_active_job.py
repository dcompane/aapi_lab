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
from aapi_conn import SaaSConnection

host_name = 'se-pre-prod-aapi.us1.preprod.ctmsaas.com'
host_port = '443'
endpoint = r'/automation-api'
aapi_token = 'UFBSR0JYOmVlOTkxODY5LWQ1MmMtNDQ2Zi05ODJlLWZiYWUzMjY0NGFjOTpRZEJ1TzlzZkc3TEc4UmFRQlZWL29GdW92MllhakNOYkM2eExwT0dNcmtRPQ=='
host_ssl = True          # server using https only
aapi_verify_ssl = False  # False if server using self-signed SSL certs


# Create connection to the AAPI server
# Create connection to the AAPI server
aapi_client = SaaSConnection(host=host_name,port=host_port, endpoint=endpoint,
                            aapi_token=aapi_token, ssl=host_ssl, verify_ssl=aapi_verify_ssl,
                            additional_login_header={'Accept': 'application/json'})


run_instance = ctm.api.run_api.RunApi(api_client=aapi_client.api_client)

jobid = 'IN01:0097g' # str |  (optional)
api_response = run_instance.get_active_job(job_id=jobid)
pprint(api_response)

result = {}
print(api_response.replace("'",'"'))
result = json.loads(api_response.replace("'",'"').replace("True",'"True"'))
print ("")
# {"dco-ai-ibp": {"Type": "Job:ApplicationIntegrator:AI DCOSAPIBP", "ConnectionProfile": "DCO-ALICORP", "AI-Job Text": "CPI-DS - External Scheduler Integration", "AI-Job User": "ROSTUNI", "AI-Timeout in minutes": "60", "AI-Job Template": "CPI-DS - External Scheduler Integration", "SubApplication": "DCO_Alicorp", "Priority": 
# "Very Low", "RunAs": "DCO-ALICORP", "Application": "DCO", "Variables": [{"UCM-IBP_JOB_NAME": "ZAALD5F5V5APNVIMCPDLLLDZDHM"}, {"UCM-RUNNO": "00001"}, {"RUN-UCM-IBP_CSRF_TOK": "m--tzN7daGR5mkk8EtXm9A=="}, {"UCM-IBP_CSRF_TOK": "m--tzN7daGR5mkk8EtXm9A=="}, {"RUN-UCM-IBP_JOB_NAME": "ZAALD5F5V5APNVIMCPDLLLDZDHM"}, {"RUN-UCM-IBP_COOKIE": "SAP_SESSIONID_ZZO_100=WTnd8x4nAIMoq4bboNZPZbSWrWe0ShHrqTr6Fj7zfAQ%3d; path=/; secure; HttpOnly; sap-usercontext=sap-client=100; path=/;"}, {"UCM-IBP_COOKIE": "SAP_SESSIONID_ZZO_100=WTnd8x4nAIMoq4bboNZPZbSWrWe0ShHrqTr6Fj7zfAQ%3d; path=/; secure; HttpOnly; sap-usercontext=sap-client=100; path=/;"}, {"UCM-ACTIVE_AE_FAILED_JOB": "N"}], "IfBase:Folder:CompletionStatus_8": {"Type": "If:CompletionStatus", "CompletionStatus": "ANY", "DoNotify_0": {"Type": "Action:Notify", "Message": "Value is %%UCM-IBP_CSRF_TOK"}, "DoNotify_1": {"Type": "Action:Notify", "Destination": "JobLog", "Message": "Value is %%UCM-IBP_CSRF_TOK"}, "Mail_2": {"Type": "Action:Mail", "Subject": "message from saas pre-prod", "To": "daniel_companeetz@bmc.com", "Message": "Value is %%UCM-IBP_CSRF_TOK\\n", "AttachOutput": True}}, "IfBase:Folder:CompletionStatus_9": {"Type": "If:CompletionStatus", "CompletionStatus": "ANY", "DoNotify_0": {"Type": "Action:Notify", "Destination": "JobLog", "Message": "Value is %%RUN-UCM-IBP_CSRF_TOK"}, "DoNotify_1": {"Type": "Action:Notify", "Message": "Value is %%RUN-UCM-IBP_CSRF_TOK"}, "Mail_2": {"Type": "Action:Mail", "To": "dcompane@bmc.com", "Message": "Value is %%RUN-UCM-IBP_CSRF_TOK\\n", "AttachOutput": True}}}}
print(result[list(result.keys())[0]]["Variables"])
# [{'UCM-IBP_JOB_NAME': 'ZAALD5F5V5APNVIMCPDLLLDZDHM'}, {'UCM-RUNNO': '00001'}, {'RUN-UCM-IBP_CSRF_TOK': 'm--tzN7daGR5mkk8EtXm9A=='}, {'UCM-IBP_CSRF_TOK': 'm--tzN7daGR5mkk8EtXm9A=='}, {'RUN-UCM-IBP_JOB_NAME': 'ZAALD5F5V5APNVIMCPDLLLDZDHM'}, {'RUN-UCM-IBP_COOKIE': 'SAP_SESSIONID_ZZO_100=WTnd8x4nAIMoq4bboNZPZbSWrWe0ShHrqTr6Fj7zfAQ%3d; path=/; secure; HttpOnly; sap-usercontext=sap-client=100; path=/;'}, {'UCM-IBP_COOKIE': 'SAP_SESSIONID_ZZO_100=WTnd8x4nAIMoq4bboNZPZbSWrWe0ShHrqTr6Fj7zfAQ%3d; path=/; secure; HttpOnly; sap-usercontext=sap-client=100; path=/;'}, {'UCM-ACTIVE_AE_FAILED_JOB': 'N'}]
print(result[list(result.keys())[0]]["Variables"][2]["RUN-UCM-IBP_CSRF_TOK"])
# m--tzN7daGR5mkk8EtXm9A==




