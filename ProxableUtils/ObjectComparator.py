from ProxableUtils import Logging
import logging

# Compares two proxy json objects to make sure that aside from their status property they're identical.
def compare_proxy_objects(json_a, json_b):
    try:
        json_a["status"] = ""
        json_b["status"] = ""
        if json_a == json_b:
            return True
        else:
            return False
    except:
        return False