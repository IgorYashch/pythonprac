import cmd
class Ech(cmd.Cmd):

    def do_echo(self, arg):
        """echo [parameters] -- print parameters"""
        print(arg)

    def do_dump(self, arg):
        print(self.dump)
        
    def complete_echo(self, prefix, line, start, end):
        self.dump = prefix, line, start, end
        variants = ['qwe', 'qwa', 'qqsdfg', 'qwulop', 'nooo!']
        return [s for s  in variants if s.startswith(prefix)]
    
    def do_EOF(self, arg):
        print()
        return 1

Ech().cmdloop()