import requests

def log_handler_request(handler, request_type):
    handler.logger.info("Client: {} | {} Request. Target: {}".format(handler.client_address, request_type, handler.path))
    handler.logger.info("Client: {} | {} Headers: {}".format(handler.client_address, request_type, handler.headers))
    handler.logger.info("Client: {} | {} Cookies: {}".format(handler.client_address, request_type, handler.headers.get('Cookie')))
    if request_type == "POST":
        handler.logger.info("Client: {} | {} Reading data of lendth {}".format(handler.client_address, "POST",int(handler.headers['Content-Length'])))

def get_session_proxy(handler, Is_CONNECT=False):

    proxy_protocol = None
    proxy_address = None
    proxy_port = None

    # If we return None then we will bypass the secondary proxies.
    if "Proxy_Bypass" in handler.headers:
        return None

    # Either get the proxy from the cookies, or try get one from the Proxy Manager and create the cookies.
    if "x-proxy_address" in handler.headers:
        proxy_protocol = handler.headers['x-proxy_protocol']
        proxy_address = handler.headers['x-proxy_address']
        proxy_port = handler.headers['x-proxy_port']
    else:
        response = requests.get("http://127.0.0.1:5000/proxy/consume").json()
        proxy_protocol = response['protocol']
        proxy_address = response['address']
        proxy_port = response['port']

    # At this point if any of these values are still None then something failed.
    if (proxy_protocol is None) or (proxy_address is None) or (proxy_port is None):
        raise Exception("Failed to find or request a proxy.")

    # If this is from the do_CONNECT method then we need to format the proxy info differently.
    if Is_CONNECT == True:
        return (proxy_address, int(proxy_port))

    handler.send_header("x-proxy_id", response['id'])
    handler.send_header("x-proxy_address", response['address'])
    handler.send_header("x-proxy_port", response['port'])
    handler.send_header("x-proxy_protocol", response['protocol'])
    # Return the proxy connection details in the urllib2 format.
    return {proxy_protocol: "{}:{}".format(proxy_address,proxy_port)}