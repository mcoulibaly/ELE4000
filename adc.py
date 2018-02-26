#!/usr/bin/python

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

def writeToFileCalibrate(strData):
  calibOutFile = open("CalibOut.txt","a")
  strr = str(strData)
  calibOutFile.writelines(strr)
  calibOutFile.close()
  

def readAChanSR(mcp,moyenne=False,nb=10):
  """
  Fais la moyenne en lisant nb fois les 8 canaux
  Lit les canaux une seul fois
  Retourne les distances SR pour les deux cas (SR: Short range)
  """
  strr = '|'+'%5d|'*8+'\n'
  #st = '|'+'%5s|'*8+'\n'
  #print(strr % ('C0','C1','C2','C3','C4','C5','C6','C7'))
  #print('-'*57)
  
  adcData = [0.0]*8
  
  if moyenne == True:
      # Lire nb les 8 canaux en faisant la somme
      for j in range(nb):
          # Lire les valeurs des 8 ADCs
          for i in range(8):
              adcData[i] += distLR(mcp.read_adc(i))
              
      # Faire la moyenne
      for i in range(8):
          adcData[i] = adcData[i]/nb
      
      # Afficher et retourner la valeur
      print(strr % (adcData[0],adcData[1],adcData[2],adcData[3],adcData[4],adcData[5],adcData[6],adcData[7]))
      return adcData
  
  else:
      # Lire les valeurs du ADC
      for i in range(8):
          adcData[i] = distLR(mcp.read_adc(i))
          
      # Afficher et retourner la valeur
      print(strr % (adcData[0],adcData[1],adcData[2],adcData[3],adcData[4],adcData[5],adcData[6],adcData[7]))
      return adcData
        
def readAChanLR(mcp,moyenne=False,nb=10):
  """
  Fais la moyenne en lisant nb fois les 8 canaux
  Lit les canaux une seul fois
  Retourne les distances LR pour les deux cas (LR: Long range)
  """
  strr = '|'+'%5d|'*8+'\n'
  #st = '|'+'%5s|'*8+'\n'
  #print('-'*49)
  #print(st % ('C0','C1','C2','C3','C4','C5','C6','C7'))
  
  adcData = [0.0]*8
  
  if moyenne == True:
      # Lire nb les 8 canaux en faisant la somme
      for j in range(nb):
          # Lire les valeurs des 8 ADCs
          for i in range(8):
              adcData[i] += distLR(mcp.read_adc(i))
              
      # Faire la moyenne
      for i in range(8):
          adcData[i] = adcData[i]/nb
      
      # Afficher et retourner la valeur
      print(strr % (adcData[0],adcData[1],adcData[2],adcData[3],adcData[4],adcData[5],adcData[6],adcData[7]))
      return adcData
  
  else:
      # Lire les valeurs du ADC
      for i in range(8):
          adcData[i] = distLR(mcp.read_adc(i))
          
      # Afficher et retourner la valeur
      print(strr % (adcData[0],adcData[1],adcData[2],adcData[3],adcData[4],adcData[5],adcData[6],adcData[7]))
      return adcData

def readChanSR(mcp,chan,moyenne=False):    
    """
    Lis et retourne la distance SR d'un canal en faisant la moyenne
    ou pas du canal chan
    """
    adcData = 0
    
    if moyenne == True: # Moyenne en lisant 10 valeurs
        for i in range(10):
            adcData += distSR(mcp.read_adc(chan))

        adcData = adcData/10
        print('DistSR CH'+str(chan)+': %d\n' % adcData)
        return adcData

    else: # Lis les valeurs du canal chan
        adcData = distSR(mcp.read_adc(chan))
        print('DistSR CH'+str(chan)+': %d\n' % adcData)
        return adcData

def readChanLR(mcp,chan,moyenne=False):    
    """
    Lis et retourne la distance LR d'un canal en faisant la moyenne
    ou pas du canal chan
    """
    adcData = 0
    
    if moyenne == True: # Moyenne en lisant 10 valeurs
        for i in range(10):
            adcData += distLR(mcp.read_adc(chan))
        adcData = adcData/10
        print('DistLR CH'+str(chan)+': %d\n' % adcData)
        return adcData
      
    else: # Lit les valeurs du canal
        adcData = distLR(mcp.read_adc(chan))

        print('DistLR CH'+str(chan)+': %d\n' % adcData)

        # Calibrate
        strr = str(dataToVolt(mcp.read_adc(chan)))+'  '+str(1/adcData)+'\n'
        
        writeToFileCalibrate(strr)
        
        return adcData

def dataToVolt(data):
    Vref = 3.3
    volt = (data*Vref)/1024
    return volt

def distLR(data):
    """Calcul de la distance Long Range"""
    # Conversion en volts
    volt = dataToVolt(data)
    
    # Approximation lineaire
    Vref = 3.3;
    a = (1/0.007)
    b = 2.5 - a*0.01
    
    freqSpatial = (volt-b)/a
    # Approximation polynomial
    #freqSpatial = -0.0009*volt**4 + 0.0102*volt**3 - 0.0377*volt**2 + 0.0651*volt - 0.0395
    dist = 1/freqSpatial # en cm

    if dist < 0: # Force to zero negative values
      dist = 0
      
    return dist

def distSR(data):
    """Cacul de la distance Short Range"""
    Vref = 3.3
    # Conversion en volts
    volt = (data*Vref)/1024
    # Approximation polynomial
    dist = 11.468*volt**6-121.13*volt**5+521.21*volt**4-1184.1*x**3+1535.2*volt**2-1137.2*volt+439.21

    if dist < 0: # Force to zero negative values
      dist = 0
    #print('Distance: %f\n' % dist)
    return dist
    
    
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
    # mcp2 = Adafruit_MCP3008.MCP3008(clk=CLK,cs=CS1,miso=MISO,mosi=MOSI)

    while True:
        # Lire les valeurs du ADC
        # start = time.time()
        # data = readAllChansm(mcp1)
        # end = time.time()
        # duration = end - start
        # print(duration)
        dist = readChanLR(mcp1,0)
        time.sleep(5)

        # Le temps de lectur est approximativement de 0.05s - 50ms
        # To Do: Tester short distance IR
        #        Tester Thread
        #        Trouver moyen de limiter lecture (100cm - 500cm et aussi pour short range)
        #        Intergrer avec rotation  moteur

  
