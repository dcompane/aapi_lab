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
20200826      Daniel Companeetz     Initial commit
"""

import json
from sys import exit
from urllib3 import disable_warnings
from urllib3.exceptions import NewConnectionError, MaxRetryError, InsecureRequestWarning

import controlm_py as ctm
from controlm_py.rest import ApiException
from aapi_conn import CtmConnection

from pprint import pprint


def run_folder(api_cli, ctm_server='ctm_server', ctm_folder=''):
    """
    Simple function that uses the ConfigApi service retrieve the agents list.

    :param api_cli: property from CTMConnection object
    :param ctm_server: logical name of the ctm server
    :param ctm_folder: name of the folder to order
    :return: list of named tuple: [{'key': 'value'}] access as list[0].key
    """

    # Instantiate the service
    run_api = ctm.api.run_api.RunApi(api_client=api_cli)
    data = ctm.OrderFolderParameters(ctm=ctm_server, folder=ctm_folder) # OrderFolderParameters | parameters to select the jobs to run (optional)

    #Call the service
    try:
        # Execute requested jobs in certain folder
        api_response = run_api.order_jobs_in_folder(data=data)
        # pprint(api_response)
    except ctm.rest.ApiException as e:
        print("Exception when calling RunApi->order_jobs_in_folder: %s\n" % e)

    return api_response

if __name__ == '__main__':

    host_name = 'vl-aus-ctm-em01.ctm.bmc.com'
    host_port = '8443'
    host_ssl = True          # server using https only
    aapi_user = 'CTMAPI'
    aapi_password = 'ctmtickets'
    aapi_verify_ssl = False  # server using self-signed SSL certs

    # Create connection to the AAPI server
    aapi_session = CtmConnection(host=host_name,port=host_port, ssl=host_ssl, verify_ssl=aapi_verify_ssl,
                                user=aapi_user,password=aapi_password,
                                additional_login_header={'accept': 'application/json'})
    aapi_client = aapi_session.api_client
    

    ret = run_folder(aapi_client, ctm_server='psctm', ctm_folder='DCO_WeatherTest')
    # print(ret.__dict__)
    print(ret)
    print('\n')
    # print(dir(ret))
    print(ret.run_id)
    print(ret.status_uri)


    # Log out
    # if you prefer, you can call the destructor
    # Closing the program without logging out explicitly will cause an exception
    #   The cause is that the network subsystem is shutdown prior to the execution of the destructor code that logs out.
    #   Explicitly deleting the instance (or logging out) will avoid the exception.
    # del aapi_client           # This deletes the instance of the CtmConnection object
    aapi_session.logout()        # This logs out and causes the destructor to do nothing.
    exit(0)
