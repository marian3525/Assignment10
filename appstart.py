from Controller.GameController import GameController
from UserInterface.CommandParser import CommandParser
from UserInterface.cli import CLI
from Validator.Validator import Validator

gameController = GameController()
parser = CommandParser()
validator = Validator()
cli = CLI(gameController, parser, validator)
cli.mainLoop()