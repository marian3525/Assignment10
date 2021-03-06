class CommandParser():
    def __init__(self):
        pass

    def readCommand(self):
        cmd = input(">>>")

        if cmd.find(" ")==-1:
            self.__command = cmd
            self.__params = []
            return

        command = cmd[:cmd.find(" ")]
        command.strip(" ")

        params = cmd[cmd.find(" ")+1:]
        params = params.split()

        for param in params:
            param.strip(" ")

        self.__command = command
        self.__params = params

    def getParams(self):
        return self.__params

    def getCommand(self):
        return self.__command