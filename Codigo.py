import serial
import time
import string
import pynmea2
import os

def gps():
    port="/dev/ttyAMA0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    i = 1;
    file = open('datos25.txt','a')
    try:
        while i<=1:
            dataout = pynmea2.NMEAStreamReader()
            newdata=ser.readline().decode('ISO-8859-1')
                
            if newdata[0:6] == "$GPRMC":
                i+=1
                newmsg=pynmea2.parse(newdata)
                lat=newmsg.latitude
                lng=newmsg.longitude
                gps = "Latitud = " + str(lat) + " y Longitud = " + str(lng)
                print(gps)
                file.write("\n")
                file.write(gps)
    except Exception as error:
        
        print("-------------------------------")
        print("Volviendo a sensar...")
        print("-------------------------------")
        
        file.write("-------------------------------")
        file.write("\n Volviendo a sensar \n")
        file.write("-------------------------------")

    finally:
        ser.close()


def red():
    os.system('sudo iwlist wlan0 scan | grep -e Quality -e ESSID > scan.dat')
    f = open('scan.dat', 'r')
    file = open('datos25.txt','a')
    lines = f.readlines()
    contador = 0;
    for n in range(0, len(lines), 2):
        lines[n] = lines[n].replace(' ', '')
        quality, quality_data, signal_data = lines[n].split('=')
        quality_data = quality_data[:5]
        signal_data = signal_data[:3]

        lines[n+1] = lines[n+1].replace(' ', '')
        essid = lines[n+1].replace('ESSID:', '')
        essid = essid[:-1]
        if essid == '"RodriguezHOME"':
            contador+=1
            datos = '%d, %s \tCALIDAD: %s \tSEÑAL: %s' % (contador,essid, quality_data, signal_data)
            print (datos)
            file.write("\n")
            file.write(datos)
        
def main():
    n = 0;
    file = open('datos25.txt','w')
    while True:
        n+=1
        print("Datos sensado %s" %(n))
        gps()
        red()
        print("----------------------------------")
        file.close() 
        time.sleep(2)
   
if __name__=="__main__":
    main()
