#!/usr/bin/env


class Persona(object):

    """docstring for Persona"""

    def __init__(self, id, nombre, friends):
        super(Persona, self).__init__()
        self.id = id
        self.nombre = nombre
        self.friends = friends
