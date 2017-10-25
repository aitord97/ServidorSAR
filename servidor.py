#!/usr/bin/env python3
import socket, sys, os, signal
import comandos
from multiprocessing import Process, Queue

PORT = 6544
MAX_BUF = 1024
listaEmbalses=[["GI317", "Urkulu", 000, 400],["NA071", "Yesa", 000, 500],["HU119", "Mediana", 000, 600]]


def enviarER(s, codigo):
    s.sendall( ("ER-{}".format(codigo)).encode())
    return

def enviarOK(s, parm = ""):
    s.sendall ( ("OK+{}".format(parm)).encode())
    return

def splitComd(mens):
    cmd = mens[:4]
    params = mens[4:]
    return cmd, params

def getEmbalse(idEmb):
    for i in listaEmbalses:
        if i[0] == idEmb:
            idEmbalse = i[0]
            nomEmbalse = i[1]
            aperEmbalse = i[2]
            nivlEmbalse = i[3]

            return idEmbalse, nomEmbalse, aperEmbalse, nivlEmbalse
    return "0", "", 0

def formatListaEmbalses():
    mens=""
    for i in listaEmbalses:
        mens +=i[0]
        mens +=i[1]
        mens +=":"
    mens = mens[:len(mens)-1]
    return mens

def interpComando(comd, param=""):

    if comd == comandos.Command.GATE:
        idEmb = param[:5]
        porNivel= param[5:]
        if len(porNivel)!= 3:
            enviarER(s, 4)
            return
        for i in listaEmbalses:
            if i[0]==idEmb:
                i[2]=porNivel
                break
        print(("Cambiado la apertura del embalse {} a {}").format(idEmb, porNivel))
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
        idEmbalse, _, nivelEmbalse, _ = getEmbalse(idEmb)
        if idEmbalse == "0":
            enviarER(s, 11)
            return
        enviarOK(s, str(nivelEmbalse))
        return

    if comd == comandos.Command.NAME:
        lista = formatListaEmbalses()
        enviarOK(s, lista)
        return


    if comd == comandos.Command.LEVE:
        mens=""
        if param == "":
            for i in listaEmbalses:
                mens += str(i[3])
            enviarOK(s, mens)
            return
        else:
            _,_,_,mens = getEmbalse(param)
            mens = str(mens)
            enviarOK(s, mens)
            return
        enviarER(s, 1)
    return






if __name__ == "__main__":




    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", PORT))
        mens, dir_cli = s.recvfrom(MAX_BUF)
        s.connect(dir_cli)
        print("Conectado con " , dir_cli)
        cmd, params = splitComd(mens.decode())
        print("Comando: ",cmd)
        print("Parametros: ",params)
        interpComando(cmd, params)
        s.close()





    s.close()
