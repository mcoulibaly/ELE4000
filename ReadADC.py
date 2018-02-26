#!/usr/bin/python

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

def readChans(mcp,distLR_SR,nb=10,moyenne=False):
    """Lis xnb tous les canaux du ADC et retourne la moyenne"""
    strr = '|'+'%5d|'*8+'\n'
    #st = '|'+'%5s|'*8+'\n'
    #print(st % ('C0','C1','C2','C3','C4','C5','C6','C7'))
    #print('-'*57)
    
    adcData = [0.0]*8
    sum = [0]*8
    if moyenne == True:
        # Lire nb les 8 canaux en faisant la somme
        for j in range(nb):
            # Lire les valeurs du ADC
            for i in range(8):
                adcData[i] = mcp.read_adc(i)
                sum[i] += adcData[i]
                
        # Faire la moyenne
        for i in range(8):
            adcData[i] = sum[i]/nb
        
        # Calcul de la distance Longue distance
        if distLR_SR == 'LR':
            for i in range(8):
                adcData[i] = distLR(adcData[i])
        
        # Calcul de la distance de courte distance
        if distLR_SR == 'SR':
            for i in range(8):
                adcData[i] = distSR(adcData[i])
        
        #Afficher et retourner la valeur
        print(strr % (adcData[0],adcData[1],adcData[2],adcData[3],adcData[4],adcData[5],adcData[6],adcData[7]))
        return adcData
    
    else:
        # Lire les valeurs du ADC
        for i in range(8):
            adcData[i] = distLR(mcp.read_adc(i))
            
        #Afficher et retourner la valeur
        print(strr % (adcData[0],adcData[1],adcData[2],adcData[3],adcData[4],adcData[5],adcData[6],adcData[7]))
        return adcData

def readChan(mcp,chan,moyenne=False):    
    """Fais une moyenne des valeurs lues ou retour la valeur lue dans un canaux"""
    strr = 'Chan '+str(chan)+': %f\n'
    sum = 0
    adcData = 0
    # Moyennage
    if moyenne == True:
        for i in range(10):
            adcData += distLR(mcp.read_adc(chan))
            #sum += adcData
        adcData = adcData/10
        print(strr % adcData)
        return adcData
    # Sans moyennage
    else:
        adcData = distLR(mcp.read_adc(chan))
        print(strr % adcData)
        return adcData

def distLR(data):
    """Calcul de la distance a Longue Range"""
    Vref = 5.0;
    # Conversion en volts
    volt = (data*Vref)/1024
    # Approximation lineaire
    #a = (1/0.007)
    #b = 2.5 - a*0.01
    #freqSpatial = (volt-b)/a
    # Approximation polynomial
    freqSpatial = -0.0009*volt**4 + 0.0102*volt**3 - 0.0377*volt**2 + 0.0651*volt - 0.0395
    dist = 1/freqSpatial # en cm
        
    #print('Distance: %f cm\n' % dist)
    
    return dist

def distSR(data):
    """Cacul de la distance a Short Range"""
    Vref = 5.0
    # Conversion en volts
    volt = (data*Vref)/1024
    # Approximation polynomial
    dist = 11.468*volt**6-121.13*volt**5+521.21*volt**4-1184.1*x**3+1535.2*volt**2-1137.2*volt+439.21
    
    
if __name__ =='__main__':
    
    # Declaration
    CLK = 11
    MISO = 9
    MOSI = 10
    CS0 = 8
    CS1 = 7
    # ADC 1
    mcp1 = Adafruit_MCP3008.MCP3008(clk=CLK,cs=CS0,miso=MISO,mosi=MOSI)
    # ADC 2
    mcp2 = Adafruit_MCP3008.MCP3008(clk=CLK,cs=CS1,miso=MISO,mosi=MOSI)

    while True:
        # Lire les valeurs du ADC
        # start = time.time()
        # data = readAllChansm(mcp1)
        # end = time.time()
        # duration = end - start
        # print(duration)

        start = time.time()
        #print('ADC 1')
        dist = readChan(mcp1,0,True)
        end = time.time()
        duration = end - start
        #print('Duration: %f sec\n' % duration)

        time.sleep(0.1)

##        start = time.time()
##        print('ADC 2')
##        dist = readChan(mcp2,0,True)
##        end = time.time()
##        duration = end - start
##        print('Duration: %f sec\n' % duration)
##
##        time.sleep(2)
