#!/usr/bin/env python3
import socket, sys, os
import comandos.py
PORT = 6544

def enviarER(s, codigo):
    s.sendall( (ER-{}.format(codigo)).encode("ascii"))
def enviarOK(s, parm = ""):
    s.sendall ( (OK+{}.format(parm)).encode("ascii"))

def interpComando(comd, parm=""):
    if comd == comandos.GATE:
        idEmb = param[0:5]
        porNivel= param[6:]
        if len(porNivel)!= 3:
            enviarER(s, 4)
            return
        print(("Cambiado el nivel del embalse {} a {}").format(idEmb, porNivel))
        enviarOK(s)
        return




if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", PORT))
