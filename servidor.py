#!/usr/bin/env python3
import socket, sys, os, signal
import comandos

PORT = 6544
MAX_BUF = 1024
listaEmbalses=[["GI317", "Urkulu", 000, 400],["NA071", "Yesa", 000, 500],["HU119", "Mediana", 000, 600]]


""" Envia el mensaje de respuesta ER por el socket (s) con el codigo de error indicado (codigo) """

def enviarER(s, codigo):
    s.sendall( ("ER-{}".format(codigo)).encode())
    return

""" Envia el mensaje de respuesta OK por el socket (s) con los parametros necesarios (parm)
    En caso de no pasarle ningun parametro se envia en mensaje vacio """

def enviarOK(s, parm = ""):
    s.sendall ( ("OK+{}".format(parm)).encode())
    return

""" Dado un mensaje cliente devuelve el comando y los parametros """

def splitComd(mens):
    cmd = mens[:4]
    params = mens[4:]
    return cmd, params

""" Dado un embalse devuelve toda la informacion si se encuentra en la lista.
    Si no se encuentra en la lista devuelve 0 """

def getEmbalse(idEmb):
    for i in listaEmbalses:
        if i[0] == idEmb:
            idEmbalse = i[0]
            nomEmbalse = i[1]
            aperEmbalse = i[2]
            nivlEmbalse = i[3]

            return idEmbalse, nomEmbalse, aperEmbalse, nivlEmbalse
    return "0"


""" Devuelve la lista de los embalses lista para ser enviada """

def formatListaEmbalses():
    mens=""
    for i in listaEmbalses:
        mens +=i[0]
        mens +=i[1]
        mens +=":"
    mens = mens[:len(mens)-1]
    return mens

""" Interpreta el comando y parametros dados, por defecto
 se le pasa el mensaje vacio como parametro """

def interpComando(comd, param=""):

    """ Modifica el valor de apertura del embalse indicado sino
        se encuentra el embalse envia el codigo de error 11 """

    if comd == comandos.Command.GATE:
        esta = False
        if param =="":
            enviarER(s,3)
            return

        idEmb = param[:5]
        porNivel= param[5:]
        if len(porNivel)!= 3:
            enviarER(s, 4)
            return

        for i in listaEmbalses:
            if i[0]==idEmb:
                esta = True
                i[2]=porNivel
                break
        if not esta:
            enviarER(s,11)
            return
        enviarOK(s)
        return

    """ Devuelve el porcentaje de apertura del embalse indicado, sino
        se encuentra el embalse devuelve el error 12 """

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
            enviarER(s, 12)
            return
        enviarOK(s, str(nivelEmbalse))
        return

    """ Devuelve la lista de los embalses, sino existe la lista devuelve
        el error 13 """

    if comd == comandos.Command.NAME:
        if param != "":
            enviarER(s,2)
        if not listaEmbalses:
            enviarER(s,13)
            return
        lista = formatListaEmbalses()
        enviarOK(s, lista)
        return

    """ Devuelve el nivel de llenado del embalse indicado,
        sino se indica el embalse se envia una lista con todos los porcentajes,
        si surge algún problema envia el error 14 """

    if comd == comandos.Command.LEVE:
        mens=""
        if param == "":
            for i in listaEmbalses:
                mens += str(i[3])
            enviarOK(s, mens)
            return
        else:
            idEmb,_,_,mens = getEmbalse(param)
            if idEmb == "0":
                enviarER(s,14)
                return
            mens = str(mens)
            enviarOK(s, mens)
            return
    enviarER(s, 1)
    return



""" MAIN """


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
