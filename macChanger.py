#!/bin/python3

import subprocess
import random
import os
import optparse

if os.geteuid() != 0:
    print ("¡EJECUTA COMO ROOT!".center(100, "="))
    exit()
else:
    pass

parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interfaz", help="Interfaz a configurar. Ejemplo: ./macChanger.py -i eth0 -m 00:11:22:33:44:55")
parser.add_option("-m", "--mac", dest="nueva_MAC", help="MAC a establecer. Ejemplo: ./macChanger.py -i eth0 -m 00:11:22:33:44:55")
parser.add_option("-r", "--random", dest="random_MAC", help="Se establece una MAC aleatoria ( true ). Ejemplo: ./macChange.py -i eth0 -r true")
(options, arguments) = parser.parse_args()

conjuntoCars = ["A", "B", "C", "D", "E", "F"]

try:

    if options.nueva_MAC:
        nuevaMac = options.nueva_MAC
        
        subprocess.call(["ifconfig", options.interfaz, "down"])
        subprocess.call(["ifconfig", options.interfaz, "hw", "ether", nuevaMac])
        subprocess.call(["ifconfig", options.interfaz, "up"])

        print ( "Interfaz: ", options.interfaz)
        subprocess.call(["ip", "--color", "link", "show", options.interfaz])
    
    elif options.random_MAC == "true":

        for i in range(0, 9):
            conjuntoCars.append( i )

        nuevaMac = ""
        contador = 0
        while contador < 6:

            if contador == 0:
                nuevaMac += str(random.choice(conjuntoCars)) + str(random.choice(range(0,9,2)))
            else:
                nuevaMac += str(random.choice(conjuntoCars)) + str(random.choice(conjuntoCars))
            
            contador += 1

            if contador < 6:
                nuevaMac += ":"
            else:
                continue
        print ( "\n[+] Estableciendo la MAC " + nuevaMac + " sobre " + options.interfaz)
        
        subprocess.call(["ifconfig", options.interfaz, "down"])
        subprocess.call(["ifconfig", options.interfaz, "hw", "ether", nuevaMac])
        subprocess.call(["ifconfig", options.interfaz, "up"])

        subprocess.call(["ip", "--color", "link", "show", options.interfaz])

    else:
        print ("Error de sintaxis. Revisa la ayuda y vuelve a ejecutar el script: ./macChanger.py -h".center(130, "="))

except KeyboardInterrupt:
    print ("Se ha interrumpido el script...")
    exit()
