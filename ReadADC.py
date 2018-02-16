#!/usr/bin/python

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

def readAllChansm(mcp,nb=10,moyenne=False):
    """Lis xnb tous les canaux du ADC et retourne la moyenne"""
    strr = '|'+'%5d|'*8+'\n'
    #st = '|'+'%5s|'*8+'\n'
    #print(strr % ('C0','C1','C2','C3','C4','C5','C6','C7'))
    #print('-'*57)
    
    adcData = [0]*8
    if moyenne == True:
        sum = [0]*8
        for j in range(nb):
            # Lire les valeurs du ADC
            for i in range(8):
                adcData[i] = mcp.read_adc(i)
                sum[i] += adcData[i]
        for j in range(nb):
            adcData[i] = sum[i]/nb
            
        print(strr % (adcData[0],adcData[1],adcData[2],adcData[3],adcData[4],adcData[5],adcData[6],adcData[7]))
        return adcData
    else:
        # Lire les valeurs du ADC
        for i in range(8):
            adcData[i] = mcp.read_adc(i)
        print(strr % (adcData[0],adcData[1],adcData[2],adcData[3],adcData[4],adcData[5],adcData[6],adcData[7]))
        return adcData

def readChan(mcp,chan,moyenne=False):    
    """Fais une moyenne des valeurs lues ou retour la valeur lue"""
    strr = 'Chan '+str(chan)+': %d\n'
    sum = 0
    if moyenne == True:
        for i in range(10):
            adcData = mcp.read_adc(chan)
            sum += adcData
        adcData = sum/10
        print(strr % adcData)
        return adcData
    else:
        adcData = mcp.read_adc(chan)
        print(strr % adcData)
        return adcData
    
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
        data = readAllChansm(mcp1)
        # end = time.time()
        # duration = end - start
        # print(duration)
        time.sleep(0.2)
