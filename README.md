
Hornbill Python API Lib
========

Integration
===
Various Hornbill Integration methods are documeted here: https://wiki.hornbill.com/index.php/Integration

Dependancys
===
This library requires the python library lxml (http://lxml.de/)

Pip can be used to install this library

```pip get lxml```


Using API Keys 
===

The best way for calling Hornbill API's is to use the API Key. These are associated to users in the Administration Tool and are passed with every API Call removing the need to login.
```
//-- Initiate XmlmcService instance
xmlmc = XmlmcService("<your instance name>")

//-- Set API Key
xmlmc.set_api_key("<your API key>")

//-- Invoke session::getSessionInfo
json_string = xmlmc.invoke("session", "getSessionInfo")
```

Using user ID and password
===

Using Hornbill API's required an authenticated session the first way to create a session it to call session::userlogon
```
//-- Initiate XmlmcService instance
xmlmc = XmlmcService("<your instance name>")

// Username
xmlmc.add_param("userId", "<your user id>")
//-- Password must be base64 encoded
xmlmc.add_param("password", "<your password>").encode("base64")

//-- Invoke session::userLogon
json_string = xmlmc.Invoke("session", "userLogon");

//-- Get SessionId from the API Response
if XmlmcHelper.is_call_success(json_string):
	session_id = XmlmcHelper.get_param_value(json_string, "params/sessionId")
```

Example
===

An example has been provided here:
https://github.com/hornbill/pythonApiLib/tree/master/python_api_lib

The following file needs to be updated to include your instance details:

https://github.com/hornbill/pythonApiLib/blob/master/python_api_lib/example.py


These strings need to be updated:
```
xmlmc = XmlmcService("<your instance name>")
xmlmc.set_api_key("<your API key>")
```



