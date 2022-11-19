def objcount(cls):
    class cls_wrapper(cls):
        counter = 0
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__class__.counter += 1

        def __del__(self):
            if '__del__' in cls.__dict__:
                super().__del__()
            self.__class__.counter -= 1

    return cls_wrapper

import sys
exec(sys.stdin.read())