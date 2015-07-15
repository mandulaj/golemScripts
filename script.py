from subprocess import call
import urllib
import xml.etree.ElementTree as ET
import time, math

TELNET = "telnet 192.168.2.241 10001"
time_delay = 0.3
time_step = 0.001

#res = Device("192.168.2.243:10001")
#print res.get_outputs_state("192.168.2.243:10001")

Ion = "echo '*B1OS1H'|" + TELNET
Ioff = "echo '*B1OS1L'|" + TELNET
IIon = "echo '*B1OS2H'|" + TELNET
IIoff = "echo '*B1OS2L'|" + TELNET
IIIon = "echo '*B1OS3H'|" + TELNET
IIIoff = "echo '*B1OS3L'|" + TELNET
IVon = "echo '*B1OS4H'|" + TELNET
IVoff = "echo '*B1OS4L'|" + TELNET
Von = "echo '*B1OS5H'|" + TELNET
Voff = "echo '*B1OS5L'|" + TELNET
VIon = "echo '*B1OS6H'|" + TELNET
VIoff = "echo '*B1OS6L'|" + TELNET
VIIon = "echo '*B1OS7H'|" + TELNET
VIIoff = "echo '*B1OS7L'|" + TELNET
VIIIon = "echo '*B1OS8H'|" + TELNET
VIIIoff = "echo '*B1OS8L'|" + TELNET


class DataGetter():
  def __init__(self):
    pass
  def get(self):
    pass

class AD_DataGetter(DataGetter):
  def __init__(self, url):
    self.url = url

  def get(self):
    data = urllib.urlopen(self.url).read()
    root = ET.fromstring(data)
    inputs = root[0]

    return float(inputs.attrib['val'])



class Varistor():
  def __init__(self, voltageGetter, rang=0.2):
    self.voltageGetter = voltageGetter
    self.rang = rang

  def _move(self, val):
    for i in xrange(abs(val)):
      if val > 0:
        call(IIon, shell=True)
        call(IIIon, shell=True)
      else:
        call(IIoff, shell=True)
        call(IIIoff, shell=True)

      time.sleep(time_delay)
            call(Ion, shell=True)
      time.sleep(time_step)
            call(Ioff, shell=True)
            time.sleep(time_step)



  def setValue(self, value):
    while True:
      currentVal = self.getValue()
      offset = currentVal - value
      print offset
      if abs(offset) < self.rang: # we are in range of the value
        return

      self._move(int(math.ceil(offset*10)))  # move the head a little



  def getValue(self):
    return self.voltageGetter.get()


dataGetter = AD_DataGetter('http://192.168.2.242/data.xml')

va = Varistor(dataGetter)

#call(IVon, shell=True);call(VIIon, shell=True);call(VIIIon, shell=True)
time.sleep(1)
print va.getValue()
#va.setValue(2.8)
#call(IVoff, shell=True);call(VIIoff, shell=True);call(VIIIoff, shell=True)
print "done"
