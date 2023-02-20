import sys
import cowsay

message = ' '.join(sys.argv[1:])
print(cowsay.cowsay(message))
