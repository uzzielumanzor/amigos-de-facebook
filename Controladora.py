#!/usr/bin/env
import networkx as nx
import matplotlib.pyplot as plt
from Persona import Persona
import operator
import time


def mVecino(G, nodo):
    nodos_ordenados = sorted(G.nodes())
    indice_nodo = nodos_ordenados.index(nodo)

    nodo_vecino = []

    for indice_nodo2, nodo2 in enumerate(nodos_ordenados):
        if indice_nodo2 > indice_nodo and nodo2 in G.neighbors(nodo):
            nodo_vecino.append(nodo2)

    return tuple(nodo_vecino)


def oUsuario(personas, miNombre):

    usuario = None
    for persona in personas:
        if persona.nombre == miNombre:
            usuario = persona

    return usuario


def pLista(personas):
    lista = []

    for persona in personas:
        temp = []
        persona = str(persona).split(";")
        temp.append(persona[1].split(","))
        temp.append(persona[0].split(","))
        # map(int, temp[0])
        lista.append(Persona(temp[1][0], temp[1][1], temp[0]))

    return lista


def getAmigos(personas, lista):
    temp = []

    for persona in personas:
        if persona.id in lista:
            temp.append(persona)

    return temp


def getNombres(lista):
    temp = []

    for x in lista:
        temp.append(x.nombre)

    return temp


def sacarEd(personas):
    lista = []
    for persona in personas:
        for amigo in persona.friends:
            if (persona.id, amigo) not in lista and tuple(
                    reversed((persona.id, amigo))) not in lista:
                lista.append((persona.id, amigo))

    return lista


def sacarEd2(personas, id, friends):
    lista = []

    # for x in friends:
     #   lista.append((id, x))

    for persona in personas:
        if persona.id in friends:
            for amigo in persona.friends:
                if amigo in friends:
                    if tuple(reversed((persona.id, amigo))) not in lista:
                        lista.append((persona.id, amigo))

    return lista


def diccionario(indices):
    dic = {}

    for i in indices:
        dic[i] = False

    return dic


def verificador(diccionario, lista):
    a = {}
    b = []
    for y in lista:
        a[y["sb"]] = 0
        if not diccionario[y["sb"]]:
                a[y["sb"]] = a[y["sb"]] + 1
        for x in y["cn"]:
            if not diccionario[x]:
                a[y["sb"]] = a[y["sb"]] + 1
    #b.append(a)

    return a


def setCover(G):
    n = 0
    temp = None
    cofre = []
    nodos_ordenados = sorted(G.nodes())
    set_sublistas = []
    index = diccionario(nodos_ordenados)

    for indice_nodo, nodo in enumerate(nodos_ordenados):
        set_sublista = {}

        set_sublista['sb'] = nodo
        set_sublista['cn'] = mVecino(G, nodo)
        set_sublistas.append(set_sublista)

    while sum(1 for condition in index.values() if condition) < len(nodos_ordenados):
        v = verificador(index, set_sublistas)
        v = max(v.iteritems(), key=operator.itemgetter(1))[0]

        for i in set_sublistas:

            if i["sb"] == v:
                index[i["sb"]] = True
                for x in i['cn']:
                    if x in index:
                        index[x] = True

        cofre.append(v)

    return cofre


def clique(G):
    cli = ()
    nodos_ordenados = sorted(G.nodes())
    clique_sublistas = []

    for indice_nodo, nodo in enumerate(nodos_ordenados):
        clique_sublista = {}

        clique_sublista['sb'] = (nodo, )
        clique_sublista['cn'] = mVecino(G, nodo)
        clique_sublistas.append(clique_sublista)

    while clique_sublistas:
        sublista = clique_sublistas.pop(0)
        for nodo_agregado in sublista['cn']:
            vecino_nodo = mVecino(G, nodo_agregado)
            lista_base = sublista['sb'] + (nodo_agregado, )
            lista_llave = tuple(
                sorted(set
                       (vecino_nodo).intersection(sublista['cn'])))

            for nodo2 in lista_llave:
                nueva_lista_base = lista_base + tuple(nodo2)
                nueva_lista_llave = tuple(
                    sorted(set(lista_llave).intersection(mVecino(G, nodo2))))

                if len(nueva_lista_llave + nueva_lista_base) > len(cli):
                    cli = nueva_lista_base + nueva_lista_llave
                    clique_sublistas.append({
                        'sb': nueva_lista_base, 'cn': nueva_lista_llave})

    return cli


def main():
    """Funcion controladora"""
    start_time = time.time()
    # personas con defectos , ;
    personas = open('grafo.txt', 'r').read().splitlines()
    # personas sin defectos
    personas = pLista(personas)
    # obtener usuario
    usuario = oUsuario(personas, "daniel")
    # obtener amigos del usuario
    amigos = getAmigos(personas, usuario.friends)
    tuplas = sacarEd(amigos)
    #tuplas2 = sacarEd2(amigos, usuario.id, usuario.friends)
    # print setCover(amigos)
    G = nx.Graph()
    G.add_edges_from(tuplas)
    #G2 = nx.Graph()
    # G2.add_edges_from(tuplas2)

    #nx.draw_circular(G, node_size=3000, node_color='r')
    #plt.show()
    #nx.draw_circular(G2, node_size=3000, node_color='r')
    # plt.show()

    cli = clique(G)

    print "Sublista Clique"
    print cli

    print "Sublista Set Cover"
    print setCover(G)

    tiempo = time.time() - start_time
    print "Tiempo de ejecucion: ", tiempo

if __name__ == '__main__':
    main()
