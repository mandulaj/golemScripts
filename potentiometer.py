from subprocess import call
import urllib
import xml.etree.ElementTree as ET
import time, math

TELNET = "telnet 192.168.2.241 10001"
time_delay = 0.3
time_step = 0.001


class DataGetter():
  """Abstract class used for getting the voltage from a device"""
  def __init__(self):
    pass
  def get(self):
    pass

class PotentiometerMover():
  """Abstract class used for moving the potentiometer"""
  def __init__(self):
    pass

  def move(self, direction, distance):
    pass


class AD_DataGetter(DataGetter):
  """Class using the AD4ETH A2D converter for measuring the voltage"""
  def __init__(self, url):
    self.url = url

  def get(self):
    data = urllib.urlopen(self.url).read()
    root = ET.fromstring(data)
    inputs = root[0]

    return float(inputs.attrib['val'])

class Relay_PotentiometerMover(PotentiometerMover):
  """Class using the Quido relay for moving the potentiometer head"""
  def __init__(self):
    pass

  def _sendCommand(self, relayId, high):
    if relayId > 16 or relayId < 1:
      raise ValueError("Value out of bounds")

    stateLetter = ""
    if high:
      stateLetter = "H"
    else:
      stateLetter = "L"

    stringToSend = "echo '*B10S" + str(relayId) + stateLetter + "' | " + TELNET
    call(stringToSend, shell=True)

  def move(self, val):

    for i in xrange(abs(val)):
      if val > 0:
        self._sendCommand(2, True)
        self._sendCommand(3, True)
      else:
        self._sendCommand(2, False)
        self._sendCommand(3, False)

      time.sleep(time_delay)
      self._sendCommand(1, True)
      time.sleep(time_step)
      self._sendCommand(1, False)
      time.sleep(time_step)



class Potentiometer():
  def __init__(self, voltageGetter, rang=0.2):
    self.voltageGetter = voltageGetter
    self.rang = rang





  def setValue(self, value):
    while True:
      currentVal = self.getValue()
      print "currentVal: " , currentVal
      offset = currentVal - value
      print offset
      if abs(offset) < self.rang: # we are in range of the value
        return

      self._move(int(math.ceil(offset*10)))  # move the head a little



  def getValue(self):
    return self.voltageGetter.get()


dataGetter = AD_DataGetter('http://192.168.2.242/data.xml')

va = Potentiometer(dataGetter)

#call(IVon, shell=True);call(VIIon, shell=True);call(VIIIon, shell=True)
#time.sleep(1)
#print va.getValue()
#va.setValue(2.8)
#call(IVoff, shell=True);call(VIIoff, shell=True);call(VIIIoff, shell=True)

po = Relay_PotentiometerMover()



print "done"
