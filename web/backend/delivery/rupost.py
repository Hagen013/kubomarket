from datetime import datetime

import zeep
from zeep import Settings


class Client(object):

    SERVICE_URL_SINGLE = 'https://tracking.russianpost.ru/rtm34'
    WSDL_URL_SINGLE = SERVICE_URL_SINGLE + '?wsdl'

    def __init__(self, login, password):
        self._login = login
        self._password = password
        self._client_settings = Settings(strict=False)
        self._client_single = zeep.Client(
            self.WSDL_URL_SINGLE,
            settings=self._client_settings
        )

    def get_operation_history(self, track):
        result = self._client_single.service.getOperationHistory(
            OperationHistoryRequest={'Barcode': track["tracking_code"], 'MessageType': 0},
            AuthorizationHeader={'login': self._login, 'password': self.password}
        )
        return result
