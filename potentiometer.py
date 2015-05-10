#from pydcpf.appliances.quido import Device as QuidoDevice
#from pydcpf.appliances.ad4xxx_drak4 import Device as AD4Device
#from pydcpf.appliances.evr116 import Device as EVRDevice
#from pydcpf.appliances.AC250Kxxx import Device as AC250KDevice

TELNET = "telnet 192.168.2.243 10001"
time_delay = 0.2
time_step = 0.001


Ion = "*B1OS1H"
Ioff = "*B1OS1L"
IIon = "*B1OS2H"
IIoff = "*B1OS2L"
IIIon = "*B1OS3H"
IIIoff = "*B1OS3L"

def getValue():
    return exec("wget -o /dev/null -O - 'http://192.168.2.253/data.xml' | grep -Po '<input id='1'.*val='\K[ 0-9]*'|xargs")

print getValue()

