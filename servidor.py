#!/usr/bin/env python3
import socket, sys, os, signal
import comandos
from multiprocessing import Process, Queue

PORT = 6544
MAX_BUF = 1024
listaEmbalses=[["GI317", "Urkulu", 000],["NA071", "Yesa", 000],["HU119", "Mediana", 000]]


def enviarER(s, codigo):
    s.sendall( ("ER-{}".format(codigo)).encode("ascii"))
    return

def enviarOK(s, parm = ""):
    s.sendall ( ("OK+{}".format(parm)).encode("ascii"))
    return

def splitComd(mens):
    cmd = mens[:4]
    params = mens[5:]
    return cmd, params

def getEmbalse(idEmb):
    for i in listaEmbalses:
        if i[0] == idEmb:
            idEmbalse = i[0]
            nomEmbalse = i[1]
            lvlEmbalse = i[2]
            return idEmbalse, nomEmbalse, lvlEmbalse
    return "0", "", 0

def formatListaEmbalses():
    mens=""
    for i in listaEmbalses:
        mens +=i[0]
        mens +=i[1]
        mens +=":"
    mens = mens[:len(mens)-1]
    return mens

def interpComando(comd, parm=""):

    if comd == comandos.Command.GATE:
        idEmb = param[:5]
        porNivel= param[6:]
        if len(porNivel)!= 3:
            enviarER(s, 4)
            return
        for i in listaEmbalses:
            if i[0]==idEmb:
                i[2]=porNivel
                break
        print(("Cambiado la apertura del embalse {} a {}").format(idEmb, porNivel))
        pipe_in.write(listaEmbalses)
        pipe_in.close()
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
        lista = formatListaEmbalses()
        enviarOK(s, lista)
        return


    if comd == comandos.Command.LEVE:
        mens=""
        for i in listaEmbalses:
            mens += i[2]
        enviarOK(s, mens)
        return
    enviarER(s, 1)
    return






if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", PORT))

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    pipe_in, pipe_out = os.pipe()

    while True:
        mens, dir_cli = s.recvfrom(MAX_BUF)
        s.connect(dir_cli)
        cmd, params = splitComd(mens.decode("ascii"))
        interpComando(cmd, params)





    s.close()
