# python 3.10 и новее

import inspect
import types

class check(type):
    def __new__(metacls, name, parents, namespace):
        cls = super().__new__(metacls, name, parents, namespace)

        # Пишем новый метод для создаваемого класса (не метокласса)
        # На входе объект этого класса
        def checker(self):
            annootation_dict = inspect.get_annotations(self.__class__)
            
            for name in annootation_dict:
                # проверим, что поле заполнено (а)
                try:
                    val = getattr(self, name)
                except Exception:
                    return False

                # проверим, что там лежит верный тип
                attr_type = annootation_dict[name]
                if isinstance(attr_type, types.GenericAlias):
                    attr_type = attr_type.__origin__

                if not isinstance(val, attr_type):
                    return False

            return True

        setattr(cls, 'check_annotations', checker)
        return cls

import sys
exec(sys.stdin.read())