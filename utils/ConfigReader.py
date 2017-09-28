import ConfigParser
import logging

class BaseConfig:

    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read('proxable.conf')

    def getSections(self):
        return self.config.sections()

    def getIsDebug(self):
        return bool(self.config.get('Proxable', 'debug'))

    def getLogDIR(self):
        return self.config.get('Proxable','logdir')

    def getLogLevel(self):
        if self.getIsDebug():
            return logging.DEBUG
        return logging.INFO

    def getInfluxDBHost(self):
        return self.config.get('Proxable', 'influxDB_Host')

    def getInfluxDBPort(self):
        return self.config.get('Proxable', 'influxDB_Port')

    def getInfluxDBUser(self):
        return self.config.get('Proxable', 'influxDB_Username')

    def getInfluxDBPassword(self):
        return self.config.get('Proxable', 'influxDB_Password')

    def getManagerEndpoint(self):
        return self.config.get('Proxable', 'manager_endpoint')

    def updateValue(self, section, config, value):
        try:
            if value is not None:
                self.config.set(section,config, value)
                with open('proxable.conf', 'wb') as configfile:
                    self.config.write(configfile)
                return True
            else:
                return False
        except:
            return False

class ServerConfig(BaseConfig):

    def getProxyHost(self):
        return self.config.get('ProxableServer', 'proxy_host')

    def getProxyPort(self):
        return int(self.config.get('ProxableServer', 'proxy_port'))

    def getUseFailsafe(self):
        return bool(self.config.get('ProxableServer', 'use_failsafe_proxy'))

class ManagerConfig(BaseConfig):

    def getAPIHost(self):
        return self.config.get('ProxableManager', 'api_host')

    def getAPIPort(self):
        return int(self.config.get('ProxableManager', 'api_port'))

    def getMemcachedHost(self):
        return self.config.get('ProxableManager', 'memcached_host')

    def getMemcachedPort(self):
        return int(self.config.get('ProxableManager', 'memcached_port'))

    def getDatabaseEngine(self):
        return self.config.get('ProxableManager', 'database_engine')

    def getDatabasePath(self):
        return self.config.get('ProxableManager', 'database_path')

    def getMemcachedEndpoint(self):
        return "{}:{}".format(self.getMemcachedHost(), self.getMemcachedPort())

    def getDBHost(self):
        return self.config.get('ProxableManager', 'database_host')

    def getDBUser(self):
        return self.config.get('ProxableManager', 'database_username')

    def getDBPassword(self):
        return self.config.get('ProxableManager', 'database_password')

    def getDBName(self):
        return self.config.get('ProxableManager', 'database_name')