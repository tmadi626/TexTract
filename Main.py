import configparser
from my_module import my_program

if __name__ == "__main__":
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Pass the configuration to the main program
    my_program.run(config)