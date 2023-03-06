from calendar import TextCalendar
import cmd
import shlex

class CalendarCmd(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.calendar = TextCalendar()
        
    def do_prmonth(self, arg):
        """Print a month’s calendar in a multi-line string."""
        year, month, *_ = shlex.split(arg)
        self.calendar.prmonth(int(year), int(month))
    
    def do_pryear(self, arg):
        """Print the calendar for an entire year as a multi-line string."""
        year, *_ = shlex.split(arg)
        self.calendar.pryear(int(year))
        
CalendarCmd().cmdloop()