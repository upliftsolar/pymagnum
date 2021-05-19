# SPDX-License-Identifier:    BSD-3-Clause
#
# This code is provided as an example of a simple program to display
# IN LINE PROTOCOL
# every 60 seconds.
# run the program with --help for details of options.

import argparse
import json
import time
import pdb

from magnum import magnum 
#from pymagnum package. 
# This import statement implies example file is being run
# from inside the magnum folder

def line_protocol(_name,_tags,_fields,_t):
    prefix = _name
    for k,v in _tags.items():
        prefix += (','+k+'=\"'+str(v)+'\"')
    f = []
    for k,v in _fields.items():
        f.append(k+'='+str(v))
    return prefix +' '+','.join(f)+' ' + str(round(time.time_ns()))


parser = argparse.ArgumentParser(description="Magnum Data Extractor Example for Line Protcol (i.e., Telegraf)")
#parser.add_help()
parser.add_argument("-d", "--device", default="/dev/ttyUSB0",
                    help="Serial device name (default: %(default)s)")
parser.add_argument("-i", "--interval", default=60, type=int, dest='interval',
                    help="Interval, in seconds between logging (default: %(default)s)")
parser.add_argument("-t", "--table", default="magnum",
                    help="InfluxDb table name (default: %(default)s)")
parser.add_argument("-l", "--tags", default="%model_text%",
                    help="line protocol fields. As string, comma separated, and with %FOO% interpolation from keys. (as opposed to values) (default: %(default)s)")
parser.add_argument("-p", "--prefix", default="magnum_",
                    help="prefix, used by some db like influx to disambiguate or filter (default: %(default)s)")

parser.add_argument("-e", "--dummy_data", default=False,
                    help="uses fake data instead of real data")


class MockStruct:
    def __init__(self,_dict):
        self._dict = _dict

    def getDevices(self):
        return self._dict
        

def dummy_data():
  return [
  {
    "device": "INVERTER",
    "data": {
      "revision": "6.1",
      "mode": 128,
      "mode_text": "SEARCH",
      "fault": 8,
      "fault_text": "LOW BAT",
      "vdc": 46.0,
      "adc": 0,
      "VACout": 16,
      "VACin": 0,
      "invled": 0,
      "invled_text": "Off",
      "chgled": 0,
      "chgled_text": "Off",
      "bat": 27,
      "tfmr": 31,
      "fet": 30,
      "model": 115,
      "model_text": "MS4448PAE",
      "stackmode": 0,
      "stackmode_text": "Stand Alone",
      "AACin": 0,
      "AACout": 0,
      "Hz": 0.0
    }
    }
    ]

args = parser.parse_args()

if args.dummy_data != None:
    reader = None
else:
    reader = magnum.Magnum(device=args.device)

while True: 
    start = time.time()
    if args.dummy_data:
        devices = dummy_data()
    else:
        devices = reader.getDevices()
    #print(json.dumps(devices, indent=2))
    _t = time.time()
    for d in devices:
        _tags = {}
        for tag in args.tags.split(','):
            if('%' in tag):
                key = tag
                #key = key.format('%*%',s)
                key = key.replace('%','')
                _tags[key] = d['data'][key]
        _fields = {}
        for p in d['data']:
            val = d['data'][p]
            if(type(val) in [float,int]):
                key = (args.prefix + d['device']+'_' + p).lower()
                _fields[key] = val
            
        print(line_protocol(args.table,_tags,_fields,_t))
    duration = _t - start
    delay = args.interval - duration
    if delay > 0:
        time.sleep(delay)
