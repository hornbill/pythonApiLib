from xmlmc import XmlmcService
from xmlmc import XmlmcHelper

#
# Initiate XmlmcService instance
#
xmlmc = XmlmcService("<your instance name>")
#
# With API key (Recommended)
#
xmlmc.set_api_key("<your API key>")
#
# Or, regular login with user ID and password
#
# xmlmc.add_param("userId", "<your user id>")
# xmlmc.add_param("password", "<your password>").encode("base64")
# json_string = xmlmc.invoke("session", "userLogon")
# if XmlmcHelper.is_call_success(json_string):
#    session_id = XmlmcHelper.get_param_value(json_string, "params/sessionId")
# xmlmc.invoke("session", "userLogoff")

# Get session info
json_string = xmlmc.invoke("session", "getSessionInfo")
if XmlmcHelper.is_call_success(json_string):
    user_id = XmlmcHelper.get_param_value(json_string, "params/userId")
    time_zone = XmlmcHelper.get_param_value(json_string, "params/regionalSettings/timeZone")
else:
    print(XmlmcHelper.get_error_message(json_string))

