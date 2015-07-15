from subprocess import call
import urllib
import xml.etree.ElementTree as ET
import time, math

TELNET = "telnet 192.168.2.243 10001"
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



class Varistor():
	def __init__(self, addr, rang=0.2):
		self.url = addr
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
		data = urllib.urlopen(self.url).read()
		root = ET.fromstring(data)
		inputs = root[0]
		return float(inputs.attrib['val'])

va = Varistor('http://192.168.2.253/data.xml')

print va.getValue()
va.setValue(3)
print "done"
