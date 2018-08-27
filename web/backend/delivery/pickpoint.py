import requests
import json
import functools


class Client(object):
    
    API_URL = 'https://e-solution.pickpoint.ru/apitest'
    LOGIN_URL = API_URL + '/login'
    LOGOUT_URL = API_URL + '/logout'
    STATES_URL = API_URL + '/getstates'
    TRACK_URL = API_URL + '/tracksending'
    SENDING_INFO_URL = API_URL + '/sendinginfo'
    
    def __init__(self, login, password, session_id=None):
        self._login = login
        self._password = password
        self._session_id = session_id
            
    def _exec_request(self, url, payload, method='GET'):
        headers = {
                'Content-type': 'application/json',
                'Accept': 'text/plain',
                'Content-Encoding': 'utf-8'
        }
        if method == 'GET':
            response = requests.get(url, params=payload)
        elif method == 'POST':
            response = requests.post(url, data=json.dumps(payload), headers=headers)
        else:
            raise NotImplementedError('Unknown method "%s"' % method)
        return response
    
    def login(self):
        payload = {
            'Login': self._login,
            'Password': self._password
        }
        response = self._exec_request(self.LOGIN_URL, payload, method='POST')
        if response.status_code == 200:
            self._session_id = response.json()['SessionId']
        else:
            msg = 'Invalid login response'
            raise Exception(msg)
        return response
    
    def check_auth(self):
        if self._session_id is None:
            msg = 'Login required'
            raise Exception(msg)
    
    def get_states(self):
        payload = dict()
        response = self._exec_request(self.STATES_URL, payload)
        return response.json()
    
    def track_sending(self, order):
        self.check_auth()
        payload = {
            'SessionId': self._session_id,
            'SenderInvoiceNumber': order['id']
        }
        response = self._exec_request(self.TRACK_URL, payload, method='POST')
        return response
    
    def get_order_info(self, order):
        self.check_auth()
        payload = {
            'SessionId': self._session_id,
            'SenderInvoiceNumber': order['id'],
        }
        response = self._exec_request(self.SENDING_INFO_URL, payload, method='POST')
        return response
    
    def logout(self):
        self.check_auth()
        payload = {
            'SessionId': self._session_id
        }
        response = self._exec_request(self.LOGOUT_URL, payload, method='POST')
        if response.status_code != 200:
            msg = 'Invalid logout response'
            raise Exception(msg)
        return response
