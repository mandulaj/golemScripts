PORT=telnet 192.168.2.241 10001
imeDelay=sleep 0.2s
TimeStep=0.001s
CountEnd=5

Ion=echo "*B1OS1H"|$(PORT)
Ioff=echo "*B1OS1L"|$(PORT)
IIon=echo "*B1OS2H"|$(PORT)
IIoff=echo "*B1OS2L"|$(PORT)
IIIon=echo '*B1OS3H'|$(PORT)
IIIoff=echo "*B1OS3L"|$(PORT)


getval:
	wget -o /dev/null -O - 'http://192.168.2.253/data.xml' | grep -Po '<input id="4".*bar="\K[ 0-9]*'|xargs

all:
	for i in `seq 1 $(CountEnd)`; do make -i GoUp TmInt=$(TimeStep) ;$(TimeDelay);done
	for i in `seq 1 $(CountEnd)`; do make -i GoDown TmInt=$(TimeStep) ;$(TimeDelay);done
		
GoUp:
	make -i TrimUp;
	$(TimeDelay);
	make -i DriveON;
	sleep $(TmInt)
	make -i DriveOFF;
	
GoDown:
	make -i TrimDown;
	$(TimeDelay);
	make -i DriveON;
	sleep $(TmInt)
	make -i DriveOFF;
	
	
TrimUp:
	$(IIoff);$(IIIoff)
	
TrimDown:
	$(IIon);$(IIIon)
	
DriveON:
	$(Ion)
	
DriveOFF:
	$(Ioff)
	
	
