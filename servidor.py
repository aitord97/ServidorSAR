#!/usr/bin/env python3
import socket, sys, os
import comandos.py
import Embalses.py
PORT = 6544
MAX_BUF = 1024

def enviarER(s, codigo):
    s.sendall( (ER-{}.format(codigo)).encode("ascii"))

def enviarOK(s, parm = ""):
    s.sendall ( (OK+{}.format(parm)).encode("ascii"))

def splitComd(mens):
    cmd = mens[:4]
    params = mens[5:]
    return cmd, params
def getEmbalse(idEmb):
    for i in Embalses.Embalses.listaEmbalses:
        if i[0] == idEmb:
            idEmbalse = i[0]
            nomEmbalse = i[1]
            lvlEmbalse = i[2]
            return idEmbalse, nomEmbalse, lvlEmbalse
    return "0", "", 0

def interpComando(comd, parm=""):
    if comd == comandos.Command.GATE:
        idEmb = param[:5]
        porNivel= param[6:]
        if len(porNivel)!= 3:
            enviarER(s, 4)
            return
        print(("Cambiado el nivel del embalse {} a {}").format(idEmb, porNivel))
        enviarOK(s)
        return
    if comd == comandos.Command.STAT:
        idEmb = param
        if len(idEmb)==0:
            enviarER(s, 3)
            return
        if len(idEmb)!=5:
            enviarER(s, 4)
            return
        idEmbalse, _, nivelEmbalse = getEmbalse(idEmb)
        if idEmbalse == "0":
            enviarER(s, 11)
            return
        enviarOK(s, nivelEmbalse)
        return



    if comd == comandos.Command.NAME:

        //TODO


    if comd == comandos.Command.LEVE:

        //TODO

    enviarER(s, 1)






if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", PORT))

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    while True:
        mens, dir_cli = s.recvfrom(MAX_BUF)
        if not os.fork():
            s.connect(dir_cli)
            cmd, params = splitComd(mens)
            interpComando(cmd, params)
            s.close()
            exit(0)



    s.close()
