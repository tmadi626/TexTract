import configparser
from my_module import my_program

if __name__ == "__main__":
    config = configparser.ConfigParser()
    # Read the configuration file
    config.read("config.ini")

    # Pass the configuration to the main program
    # innitiate the program
    my_program = my_program.MyProgram(config)
