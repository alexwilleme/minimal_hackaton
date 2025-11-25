"""AwsManager"""
from threading import Lock

import boto3

from app.config import ConfigManager


# pylint: disable=too-many-public-methods
class Aws:
    """Aws implementing Singleton for the connection to Amazon Web Services - only instantiates what is used."""
    _instance = None
    _lock = Lock()  # To make the singleton thread-safe
    _config = None
    _session = None

    __ec2 = None
    __s3 = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Aws, cls).__new__(cls)
                    cls._instance._config = ConfigManager().get_config()
                    if cls._instance._config.CLOUD_ID == "local":
                        cls._instance._session = boto3.session.Session(region_name=cls._instance._config.AWS_REGION)
                        # cls._instance._session = boto3.session.Session(region_name=cls._instance._config.AWS_REGION,
                        #                                               profile_name=cls._instance._config.AWS_PROFILE_NAME)
                    else:
                        cls._instance._session = boto3.session.Session(region_name=cls._instance._config.AWS_REGION)
        return cls._instance

    # region properties

    @property
    def s3(self):
        if self.__s3 is None:
            self.__s3 = self._session.client(service_name="s3")
        return self.__s3

    @property
    def ec2(self):
        if self.__ec2 is None:
            self.__ec2 = self._session.client(service_name="ec2")
        return self.__ec2

    # endregion
