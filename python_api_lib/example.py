from xmlmc import XmlmcService
from xmlmc import XmlmcHelper

# Initiate XmlmcService instance
#
xmlmc = XmlmcService("<your instance name>")
#
# With API key (Recommended)
#
xmlmc.set_api_key("<your API key>")
#
# Alternatively, using user ID and password
#
#xmlmc.add_param("userId", "<your user ID>")
#xmlmc.add_param("password", "<your password>").encode("base64")
#json_string = xmlmc.invoke("session", "userLogon")
#if XmlmcHelper.is_call_success(json_string):
#    session_id = XmlmcHelper.get_param_value(json_string, "params/sessionId")
#xmlmc.invoke("session", "userLogoff")

#
# How to get the API Key
# Please note: you'll need to establish a session (with userID and password)
# before calling deviceAdd & deviceRegister
# session::deviceAdd -> (authCode) -> session::deviceRegister -> (API Key)
#
# Sample Code:
#xmlmc.add_param("description", "python example")
#json_string = xmlmc.invoke("session", "deviceAdd")
#if XmlmcHelper.is_call_success(json_string):
#  authCode = XmlmcHelper.get_param_value(json_string, "params/authCode")
#  xmlmc.add_param("userId", "<your user ID>")
#  xmlmc.add_param("authCode", authCode)
#  xmlmc.add_param("deviceInfo", "python example")
#  json_string = xmlmc.invoke("session", "deviceRegister")
#  if XmlmcHelper.is_call_success(json_string):
#      print("API Key: " + XmlmcHelper.get_param_value(json_string, "params/apiKey"))

#
# How to get session info
#
# Sample Code:
#json_string = xmlmc.invoke("session", "getSessionInfo")
#if XmlmcHelper.is_call_success(json_string):
#    user_id = XmlmcHelper.get_param_value(json_string, "params/userId")
#    time_zone = XmlmcHelper.get_param_value(json_string, "params/regionalSettings/timeZone")
#else:
#    print(XmlmcHelper.get_error_message(json_string))
#

#
# How to specify complex type
#
# <location> in activity::conversationPost is complex type
# <location>
#   <latitude>51.556943</latitude>
#   <longitude>-0.403499</longitude>
#   <elevation>0</elevation>
#   <placeName>Hornbill Limited</placeName>
# </location>
#
# Sample Code:
#param = xmlmc.add_param("conversationId", "<conversation ID>")
#xmlmc.add_param("content", "Test content")
#
# add_param returns parameter object, use it to add child elements
#
#locationParam = xmlmc.add_param("location")
#locationParam.add_child("latitude", "51.556943")
#locationParam.add_child("longitude", "-0.403499")
#locationParam.add_child("elevation", "0")
#locationParam.add_child("placeName", "Hornbill Limited")
#print(param)
#json_string = xmlmc.invoke("activity", "conversationPost")
#if XmlmcHelper.is_call_success(json_string):
#   print(XmlmcHelper.get_param_value(json_string, "params/messageId"))
#else:
#   print(XmlmcHelper.get_error_message(json_string))


