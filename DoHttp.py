'''
dohttp version 0.7
'''
import requests
from requests.auth import HTTPDigestAuth
import json
import logging

def dohttp(hostname='', sdk_url='/manage/v2/requests', restapi_username='', restapi_password='', payload=False, protocol='http://', method='GET', port='8002',
           http_timeout=10, debug=False):
    '''
    :The goal is easy object function to conect to marklogic host.
    :param hostname: the marklogic hostname of a cluster
    :param sdk_url:  the request rest-api connection basic request is /manage/v2/requests for checking if hosts is alive.
    :param protocol: http or https
    :param method: get, post or put
    :param port: default is 8002 but for application can that be differed
    :return: result
    '''
    # dict of methodes to use on the request module.
    debug = str(debug)
    logging_levels = {
        'False': logging.CRITICAL,
        'True': logging.DEBUG
    }
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT,
                        level=logging_levels[debug])
    logger = logging.getLogger('dohttp')
    requestTypes = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'DELETE': requests.delete,
        'HEAD': requests.head,
        'OPTIONS': requests.options
    }
    # Set headers for
    headers = {'content-type': 'application/json', 'accept': 'application/json'}
    # Create request sdk_url
    url = protocol + hostname + ':' + port + sdk_url
    try:
        payload = json.dumps(payload)
    except:
        pass
    try:
        do_requests = requestTypes[method](url,
                                           auth=HTTPDigestAuth(restapi_username, restapi_password),
                                           headers=headers, data=payload, timeout=http_timeout)
        do_requests.raise_for_status()
    # Checking if http request is valid by error, connection errors or timeout.
    except requests.exceptions.HTTPError as errh:
        logger.debug('Debug: %s', "Http Error:" + str(errh))
        return False
    except requests.exceptions.ConnectionError as errc:
        logger.debug('Debug: %s', "Error Connecting:" + str(errc))
        return False
    except requests.exceptions.Timeout as errt:
        logger.debug('Debug: %s', "Error Timeout:" + str(errt))
        return False
    else:
        logger.debug('Debug: %s', "HTTP status code:" + str(do_requests.status_code))
        try:
            return json.loads(do_requests.text)
        except:
            return True