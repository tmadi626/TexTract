import configparser
from my_module import my_program

if __name__ == "__main__":
    config = configparser.ConfigParser()
    # Read the configuration file
    config.read("config.ini")

    # Innitiate the program
    # & pass the configuration to the main program
    my_program = my_program.MyProgram(config)
