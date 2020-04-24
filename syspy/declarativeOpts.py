import sys, getopt, inspect

def parseOptions(arguments, shortOpts, longOpts):
    try:
        options, remainder = getopt.getopt(
            arguments,
            shortOpts,
            longOpts
        )
        command = None
        try:
            command = remainder[0]
            remainder = remainder[1:]
        except:
            remainder = None
        return options, command, remainder
    except getopt.GetoptError as err: raise(err)

class DeclarativeOptions:
    def __init__(self):
        self.__opts__ = [a for a in dir(self) if not a.startswith('__')]
        self.__instructions_map__ = {}
        self.__short_opts__ = []
        self.__long_opts__ = []
        for opt in self.__opts__:
            variations = opt.split('_')
            particular_instruction = getattr(self, opt).instructions
            has_arg = self.__has_arguments__(particular_instruction)
            long_opt = variations[0]
            self.__instructions_map__['--' + long_opt] = particular_instruction
            self.__long_opts__.append(long_opt + '=' if has_arg else long_opt)
            if len(variations) > 1:
                short_opt = variations[1]
                self.__instructions_map__['-' + short_opt] = particular_instruction
                self.__short_opts__.append(short_opt + ':' if has_arg else short_opt)
        self.__short_opts__ = ''.join(self.__short_opts__)

    @staticmethod
    def __has_arguments__(fun):
        try: # python3
            return len(inspect.getfullargspec(fun).args) > 0
        except: # python 2
            return len(inspect.getargspec(fun)[0]) > 0

    def __parse_options__(self, argv):
        return parseOptions(argv, self.__short_opts__, self.__long_opts__)

    def __handle_options__(self, options):
        for opt, arg in options:
            instructions_method = self.__instructions_map__[opt]
            if arg: instructions_method(arg)
            else: instructions_method()

    def __documentation__(self):
        for opt in self.__opts__:
            line = []
            variations = opt.split('_')
            attr = getattr(self, opt)
            has_arg = self.__has_arguments__(attr.instructions)
            long_opt = ['--', variations[0], '=<arg>'] if has_arg else ['--', variations[0]]
            if len(variations) > 1:
                short_opt = [', -', variations[1], ' <arg>'] if has_arg else [', -', variations[1]]
            else: short_opt = []
            description = [': ', attr.description]
            line += long_opt + short_opt + description
            print(''.join(line))

class DeclarativeCommands:
    def __list__(self):
        return [a for a in dir(self) if not a.startswith('__')]

    def __documentation__(self):
        for cmd in self.__list__():
            command_class = getattr(self, cmd)
            print(''.join([command_class.__name__, ': ', command_class.description]))


    def __run_command__(self, command, remainder):
        if (command):
            if command in self.__list__():
                instructions = getattr(self, command).instructions
                instructions(remainder)
            else: self.__default_unspecified_command__(command, remainder)
        else: self.__default_no_args__()

class DeclarativeCLI:
    def run(self, arguments):
        self.opts = self.Options()
        options, command, remainder = self.opts.__parse_options__(arguments)
        self.cmds = self.Commands()
        self.opts.__handle_options__(options)
        self.cmds.__run_command__(command, remainder)

def header(msg):
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color
    print('{}_____________________________________________________________________________{}'.format(CYAN, NC))
    print('{}{}{}'.format(CYAN, msg, NC))

def document(particular_doc):
    if hasattr(particular_doc, 'header'):
        header(particular_doc.header)
    else: header(particular_doc.__name__)
    particular_doc.body()

