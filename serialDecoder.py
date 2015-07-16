#!/usr/bin/python2.7


import signal
import sys
import time
import serial
import io
import getopt

interval = '0.1'
device = '/dev/cu.usbserial'


try:
  port=serial.Serial(port=device,
                     baudrate=2400,
                     bytesize=serial.EIGHTBITS,
                     stopbits=serial.STOPBITS_ONE,
                     parity=serial.PARITY_NONE,
                     timeout=None)

  if not port.isOpen():
    port.open()

except IOError,err:
  print '\nError:' + str(err) + '\n'
  sys.exit(1)


## Close open port gracefully
def closePort(signal, frame):
  sys.stderr.write('\n\nYou pressed Ctrl+C!\n\n')
  port.flushInput()
  port.close()
  sys.exit(0)

signal.signal(signal.SIGINT, closePort)


# Every packet is 14 bytes long.
def getPacket():
  i = 0
  substr = ''
  while i<14:
    byte = port.read(1)
    # converting every byte to binary format keeping the low nibble.
    substr += '{0:08b}'.format(ord(byte))[4:]
    i += 1
  return substr


def stream_decode(substr):

  ac       = int(substr[0:1])
  dc       = int(substr[1:2])
  auto     = int(substr[2:3])
  pclink   = substr[3:4]
  minus    = int(substr[4:5])

  digit1   = substr[5:12]
  dot1     = int(substr[12:13])
  digit2   = substr[13:20]
  dot2     = int(substr[20:21])
  digit3   = substr[21:28]
  dot3     = int(substr[28:29])
  digit4   = substr[29:36]

  micro    = int(substr[36:37])
  nano     = int(substr[37:38])
  kilo     = int(substr[38:39])
  diotst   = int(substr[39:40])
  mili     = int(substr[40:41])
  percent  = int(substr[41:42])
  mega     = int(substr[42:43])
  contst   = int(substr[43:44])
  cap      = int(substr[44:45])
  ohm      = int(substr[45:46])
  rel      = int(substr[46:47])
  hold     = int(substr[47:48])
  amp      = int(substr[48:49])
  volts    = int(substr[49:50])
  hertz    = int(substr[50:51])
  lowbat   = int(substr[51:52])
  minm     = int(substr[52:53])
  fahrenh  = substr[53:54]
  celcius  = int(substr[54:55])
  maxm     = int(substr[55:56])

  digit = {"1111101":"0",
           "0000101":"1",
           "1011011":"2",
           "0011111":"3",
           "0100111":"4",
           "0111110":"5",
           "1111110":"6",
           "0010101":"7",
           "1111111":"8",
           "0111111":"9",
           "0000000":"",
           "1101000":"L"}

  valueStr = ("-" if minus else " ") +\
          digit.get(digit1,"") + ("." if dot1 else "") +\
          digit.get(digit2,"") + ("." if dot2 else "") +\
          digit.get(digit3,"") + ("." if dot3 else "") +\
          digit.get(digit4,"")
  try:
    valueNum = float(valueStr)
  except ValueError:
    valueNum = None

  flags = ",".join(["AC"         if ac     else "",
                    "DC"         if dc     else "",
                    "Auto"       if auto   else "",
                    "Diode test" if diotst else "",
                    "Conti test" if contst else "",
                    "Capacity"   if cap    else "",
                    "Rel"        if rel    else "",
                    "Hold"       if hold   else "",
                    "Min"        if minm   else "",
                    "Max"        if maxm   else "",
                    "LowBat"     if lowbat else ""])

  if valueNum == None:
    pass
  elif nano:
    valueNum *= 10e-9
  elif micro:
    valueNum *= 10e-6
  elif mili:
    valueNum *= 10e-3
  elif kilo:
    valueNum *= 10e3
  elif mega:
    valueNum *= 10e6


  units = ("%"    if percent else "") +\
          ("Ohm"  if ohm     else "") +\
          ("Amp"  if amp     else "") +\
          ("Volt" if volts   else "") +\
          ("Hz"   if hertz   else "") +\
          ("C"    if celcius else "")

  return (valueNum, units, flags)


#while 1:
#  substr = getPacket()
#  data = stream_decode(substr)

#  print data
#  time.sleep(float(interval))
#  port.flushInput()

