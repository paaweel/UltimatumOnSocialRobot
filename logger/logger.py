from logger_config import LoggerConfig
import logging


def log_sound(function):

    def sound_function_wrapper():
        output = function()

        print ("output")
        return output

    return sound_function_wrapper


if __name__ == "__main__":
    
    @log_sound
    def f():
        print("st")
        return "st"

    f()