import os, socket, logging
from influxdb import InfluxDBClient

class influxlogger(object):
    def __init__(self, config):
        
        self.config = config
        db_host = config.getInfluxDBHost()
        db_port = config.getInfluxDBPort()
        db_username = config.getInfluxDBUser()
        db_password = config.getInfluxDBPassword()
        self.client_logs = InfluxDBClient(db_host, db_port, db_username, db_password, 'proxy_logs')
        self.client_logs.create_database('proxy_logs')

    def log_info(self, host, caller, http_destination, assigned_proxy, status_code, status_message, handler_runtime):
        self._write_proxy_handler_log("info", host, caller, http_destination, assigned_proxy, status_code, status_message, handler_runtime)

    def log_warn(self, host, caller, http_destination, assigned_proxy, status_code, status_message, handler_runtime):
        self._write_proxy_handler_log("warn", host, caller, http_destination, assigned_proxy, status_code, status_message, handler_runtime)

    def log_error(self, host, caller, http_destination, assigned_proxy, status_code, status_message, handler_runtime):
        self._write_proxy_handler_log("error", host, caller, http_destination, assigned_proxy, status_code, status_message, handler_runtime)

    def _write_proxy_handler_log(self, severity, host, caller, http_destination, assigned_proxy, status_code, status_message, handler_runtime):

        proxy_address = "None"
        proxy_ip = "None"

        if assigned_proxy is not None:
            proxy_address = assigned_proxy[0]
            proxy_ip = assigned_proxy[1]

        new_handler_log = [
            {
                "measurement": "proxy_handler_log",
                "tags": {
                    "severity": severity,
                    "host": host,
                    "http_destination": http_destination,
                    "session": "{}:{}".format(caller[0], caller[1])
                },
                "fields": {
                    "caller": str(caller[0]),
                    "http_destination": http_destination,
                    "proxy_address": proxy_address,
                    "proxy_port": proxy_ip,
                    "status_code":status_code,
                    "status_message":status_message,
                    "connection_time":handler_runtime
                }
            }
        ]
        self.client_logs.write_points(new_handler_log)


    def log_connection_trace(self, host, caller, http_destination, assigned_proxy, connection_runtime, data_sent, data_received):
        if self.config.getIsDebug() == True:
            proxy_address = "None"
            proxy_port = "None"

            if assigned_proxy is not None:
                proxy_address = assigned_proxy[0]
                proxy_port = assigned_proxy[1]

            new_handler_log = [
                {
                    "measurement": "proxy_handler_connection_trace",
                    "tags": {
                        "severity": "trace",
                        "host": host,
                        "http_destination": http_destination,
                        "session": "{}:{}".format(caller[0], caller[1])
                    },
                    "fields": {
                        "caller_ip": str(caller[0]),
                        "caller_port": str(caller[1]),
                        "http_destination": http_destination,
                        "proxy_address": proxy_address,
                        "proxy_port": proxy_port,
                        "connection_time": connection_runtime,
                        "data_send": data_sent,
                        "data_received": data_received
                    }
                }
            ]
            self.client_logs.write_points(new_handler_log)

def get_logger(module_name, config):

    log_format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"

    if not os.path.exists(config.getLogDIR()):
        os.makedirs(config.getLogDIR())

    if os.path.exists(config.getLogDIR()):
        # create logger with the module name
        logger = logging.getLogger(module_name)
        logger.setLevel(config.getLogLevel())

        # create file handler which logs even debug messages
        file_handler = logging.FileHandler("{}/{}.log".format(config.getLogDIR(), module_name))
        file_handler.setLevel(config.getLogLevel())

        # create console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.getLogLevel())

        # Set the formatter for the logs.
        console_handler.setFormatter(logging.Formatter(log_format))
        file_handler.setFormatter(logging.Formatter(log_format))

        # add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # return the logger.
        return logger

    # path didn't exist and we couldn't create it. Return None.
    return None