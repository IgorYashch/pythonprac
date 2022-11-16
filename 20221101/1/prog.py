class Omnibus:

    attributes_counts = {}

    def __setattr__(self, name, val):

        if '_' + name not in self.__dict__:            

            self.__dict__['_' + name] = None

            Omnibus.attributes_counts[name] = Omnibus.attributes_counts.get(name, 0) + 1


    def __getattr__(self, name):

        if '_' + name in self.__dict__:
            return Omnibus.attributes_counts[name]
            

    def __delattr__(self, name):

        if '_' + name in self.__dict__:
            del self.__dict__['_' + name]
            
            Omnibus.attributes_counts[name] -= 1
            if Omnibus.attributes_counts[name] == 0:
                del Omnibus.attributes_counts[name]


import sys
exec(sys.stdin.read())
