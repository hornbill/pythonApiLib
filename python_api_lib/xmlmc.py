from lxml import etree
from typing import List
import base64
import requests
import exception
import warnings

from posixpath import join as urljoin

try:
    import urlparse
    from urllib import urlencode
except:  # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode


class XmlmcHelper(object):
    @staticmethod
    def is_call_success(json_string):
        if json_string:
            if "@status" in json_string:
                return json_string["@status"] is True
        return False

    @staticmethod
    def get_param_value(json_string, path_of_param):
        if not path_of_param or path_of_param.isspace():
            raise exception.IllegalArgumentError("The path of parameter cannot be empty.")

        keys = path_of_param.strip().split("/")
        val = json_string
        for key in keys:
            key = key.strip()
            if not isinstance(val, dict) or key not in val:
                return None
            val = val[key]
        return val

    @staticmethod
    def get_error_message(json_string):
        if json_string:
            if "state" in json_string:
                state = json_string["state"];
                if "error" in state:
                    return state["error"]
        return "Unknown error"


class XmlmcService(object):

    _server_endpoint_ = ""
    _gateway_ = "xmlmc"
    _instance_name_ = ""
    _session_ = requests.session()
    _api_key_ = ""

    def __init__(self, instance_name, gateway="xmlmc"):
        self.params = list()
        self.req = None
        self._instance_name_ = instance_name
        self._gateway_ = gateway

    def set_server_endpoint(self, endpoint):
        self._server_endpoint_ = endpoint

    def set_instance_name(self, name):
        self._instance_name_ = name

    def get_instance_name(self):
        return self._instance_name_

    def get_server_endpoint(self):
        return self._server_endpoint_

    def set_api_key(self, api_key):
        self._api_key_ = api_key

    def get_api_key(self):
        return self._api_key_

    def set_gateway(self, gateway):
        self._gateway_ = gateway

    def get_gateway(self):
        return self._gateway_

    @staticmethod
    def resolve_instance_name(instance_name):
        if not instance_name or instance_name.isspace():
            raise exception.IllegalArgumentError("The instance name cannot be empty.")

        name = instance_name.lower()
        if name.startswith("http://") or name.startswith("https://"):
            return name

        r = requests.get("https://files.hornbill.com/instances/{0}/zoneinfo".format(instance_name))
        if not r:
            return None
        json_string = r.json()
        if not json_string:
            return None
        if "zoneinfo" not in json_string:
            return None

        zone_info = json_string["zoneinfo"]
        if "apiEndpoint" in zone_info:
            return zone_info["apiEndpoint"]
        if "endpoint" in zone_info:
            return zone_info["endpoint"]
        if "name" not in zone_info or "zone" not in zone_info:
            return None
        return "https://{0}api.hornbill.com/{1}".format(zone_info["zone"].replace("", "_"), zone_info["name"])

    def add_param(self, key, value=''):
        """
        :param key: name of the parameter
        :param value:  value of the parameters
        :return: return XmlmcParam object
        """
        if not key or key.isspace():
            return None
        param = XmlmcParam(str(key), str(value))
        self.params.append(param)
        return param

    def clear_params(self):
        self.params = list()

    def print_params(self):
        print('\n'.join(str(p) for p in self.params))

    def invoke(self, service, method):
        def addParamElements(p):
            elem = etree.Element(str(p.key))
            elem.text = p.value
            for c in p.childs():
                elem.append(addParamElements(c))
            return elem

        if not self._server_endpoint_ or self._server_endpoint_.isspace():
            if not self._instance_name_ or self._instance_name_.isspace():
                raise exception.IllegalArgumentError("You must specify either the server URL or instance name.")
            else:
                server_endpoint = XmlmcService.resolve_instance_name(self._instance_name_)
                if not server_endpoint or server_endpoint.isspace():
                    raise exception.IllegalArgumentError("Invalid instance name.")
                self.set_server_endpoint(server_endpoint)
        if not service or service.isspace():
            raise exception.IllegalArgumentError("Service name cannot be empty.")
        if not method or method.isspace():
            raise exception.IllegalArgumentError("Method name cannot be empty.")
        root_elem = etree.Element("methodCall")
        root_elem.set("service", service)
        root_elem.set("method", method)
        if self.params and len(self.params) > 0:
            param_elem = etree.Element("params")
            root_elem.append(param_elem)
            for param in self.params:
                elem = addParamElements(param)
                param_elem.append(elem)

        xml_body = str(etree.tostring(root_elem, encoding='utf8', method='xml'))
        self.clear_params()

        url = urljoin(self.get_server_endpoint(), self.get_gateway(), service) + "/"
        headers = {"Accept": "text/json", "Content-Type": "text/xmlmc; charset=utf-8"}
        api_key = self.get_api_key()
        if api_key and not api_key.isspace():
            headers["Authorization"] = "ESP-APIKEY " + self.get_api_key()
        self.req = self._session_.post(url, data=xml_body, headers=headers)
        return self.req.json()


class XmlmcParam(object):
    _childs = None

    def __init__(self):
        self.key = None
        self.value = None

    def __init__(self, k, v):
        self.key = k
        self.value = v

    def __str__(self):
        c = ''
        if self._childs is not None and len(self._childs) > 0:
            c = ''.join('\n{0}'.format(str(p)) for p in self._childs)
        return '<{0}>{1}{2}{3}</{0}>'.format(self.key, self.value, c, '\n' if len(c) else '')

    def add_child(self, k, v=''):
        if not k or k.isspace():
            return None
        _childs = self.childs()
        param = XmlmcParam(str(k), str(v))
        _childs.append(param)
        return param

    def encode(self, val):
        if not self.value and self.value.isspace():
            return
        if val == "base64":
            self.value = base64.b64encode(bytes(self.value, 'utf-8'))
            return
        warnings.warn("\'" + val + " \'encoding is not implemented.")

    def childs(self):
        """ return list of XmlmcParam objects """
        if self._childs is None:
            self._childs = list()
        return self._childs

    def clear_childs(self):
        self._childs = list()


