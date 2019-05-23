#!/usr/bin/env python

'''Farmware: switch between USB and Raspberry Pi cameras.'''

import os
import json
import requests
import sys
from xml.dom.minidom import parse, parseString
from farmware_tools import device
from farmware_tools import get_config_value

#https://docs.python.org/3/library/xml.dom.minidom.html

'''
https://www.mkyong.com/python/python-read-xml-file-dom-example/
from xml.dom import minidom

doc = minidom.parse("staff.xml")

# doc.getElementsByTagName returns NodeList
name = doc.getElementsByTagName("name")[0]
print(name.firstChild.data)

staffs = doc.getElementsByTagName("staff")
for staff in staffs:
        sid = staff.getAttribute("id")
        nickname = staff.getElementsByTagName("nickname")[0]
        salary = staff.getElementsByTagName("salary")[0]
        print("id:%s, nickname:%s, salary:%s" %
              (sid, nickname.firstChild.data, salary.firstChild.data))
'''

xml_url = get_config_value(farmware_name='Weather watcher', config_name='forecast_url_setter', value_type=str)
period_to_check = get_config_value(farmware_name='Weather watcher', config_name='period_to_check_setter', value_type=int)
skip_watering_limit = get_config_value(farmware_name='Weather watcher', config_name='skip_watering_limit_setter', value_type=int)
watering_sequence = get_config_value(farmware_name='Weather watcher', config_name='watering_sequence_setter', value_type=str)

# validate xml_url if URL is from yr.no website, whether XML can be reached

# validate if period_to_check is in 6,12,18,24

if period_to_check not in (6, 12, 18, 24):
    message = "Wrong input for forecast period - you entered:  " + period_to_check + ". Values (6,12,18 or 24) shd be used"
    device.log(message, message_type='warn')

# validate if skip_watering_limit is positive or zero
if skip_watering_limit < 0:
    message = "Wrong input for precipitation watering limit -  should be integer 0 or positive"
    device.log(message, message_type='warn')

# validate if watering_sequence exists and get the ID of that sequence
#  prefix = self.farmwarename.lower().replace('-','_')
#  self.input_sequence_beforemove  = os.environ.get(prefix+"_sequence_beforemove", 'None').split(",")
# https://stackoverflow.com/questions/4906977/how-to-access-environment-variable-values


response=requests.get(xml_url)
try:
    with open('yrno_feed2.xml', 'w') as file:
        file.write(response.content)
except OSError as err:
    message = "OS error: {0}".format(err)
    device.log(message, message_type='info')

except ValueError:
    message = "value error."
    device.log(message, message_type='info')
except:
    message = "Unexpected error:", sys.exc_info()[0]
    device.log(message, message_type='info')
    raise

yrno_dom = parse("yrno_feed2.xml")


forecast = yrno_dom.getElementsByTagName("time")[0]


until_value = forecast.getAttribute("to")
temp = forecast.getElementsByTagName("symbol")[0]
fcst_text = temp.getAttribute("name")
temp2 = forecast.getElementsByTagName("precipitation")[0]
precip = temp2.getAttribute("value")
message = "Forecast until:"+until_value+" is:"+fcst_text+" with precipitation:"+precip+"mm"
device.log(message, message_type='info')
