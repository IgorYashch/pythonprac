import sys
import gettext
import os
from gettext import ngettext

popath = os.path.join(os.path.dirname(__file__), 'po')
translation = gettext.translation('counter', popath, fallback=True)
_, ngettext = translation.gettext, translation.ngettext
    

while s := sys.stdin.readline():
    print(ngettext('{} word entered', '{} words entered', len(s.split())).format(len(s.split())))
    
