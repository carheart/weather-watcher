#!/usr/bin/env python

'''Farmware: switch between USB and Raspberry Pi cameras.'''

import os
import json

import requests
from xml.dom.minidom import parse, parseString

#https://docs.python.org/3/library/xml.dom.minidom.html

#from farmware_tools import device
#from farmware_tools import get_config_value
'''
"name": "forecast_url_setter",
"label": "Specify URL to XML file from YR.NO website for your farmbot location",
"value": "https://www.yr.no/place/Slovakia/Nitra/Radava/forecast.xml"
},
{
"name": "period_to_check_setter",
"label": "Specify how much hours of forecast to consider - (enter number 6,12,18 or 24)",
"value": 12
},
{
"name": "skip_watering_limit_setter",
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

switch_camera_to = switch_camera_to.strip()
switch_camera_to = switch_camera_to.upper()

if switch_camera_to not in ("RPI", "USB"):
    message = "Wrong input to switch camera provided:  " + switch_camera_to + ". Values USB or RPI shd be used"
    device.log(message, message_type='info')
else:
    camera = os.getenv('camera', 'USB')
    device.set_user_env('camera', json.dumps(switch_camera_to))
    message = "Camera was switched to " + switch_camera_to
    device.log(message, message_type='success')






