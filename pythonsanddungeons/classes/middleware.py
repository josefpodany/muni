""" Module handling I/O operations with the user """
import re


class Middleware:
    """ Class handling I/O operations, filesystem operations """
    @staticmethod
    def string(prompt, regex_pattern="", warning=""):
        """
        asks user for string input until condition is fulfilled
        :param prompt: what to prompt to user
        :param regex_pattern: regular expression used to check the
        :param warning: what user sees after incorrect input
        :returns: string input
        """
        while True:
            user_input = input(prompt)
            if user_input.rstrip() != "" and re.search(regex_pattern, user_input):
                return user_input.lower()
            elif user_input.rstrip() != "":
                return user_input
            if warning:
                print(warning)

    @staticmethod
    def number(prompt, start, end):
        """
        asks user for numerical input until condition is fulfilled
        :param prompt: prompt for user to see
        :param start: start of the interval including the number
        :param stop: end of the interval including the number
        :returns: numerical input
        """
        while True:
            user_input = input(prompt)
            if user_input.isnumeric() and start <= int(user_input) <= end:
                return int(user_input)
            else:
                print("You must choose between {} and {}!".format(start, end))

    @staticmethod
    def indexed_items(items, indexing=True, start=1):
        """
        generic printing of items with or without indexes
        :param items: array of what to print
        :param indexing: whether to index the lines or not
        :param start: starting index
        :returns: string of items
        """
        index = start
        string = ""
        for item in items:
            if indexing:
                string += "({}) {}\n".format(index, item)
                index += 1
            else:
                string += item
        return string.rstrip()

    @staticmethod
    def load_csv(filepath):
        """
        loads csv and breaks it up
        :param filepath: path to a csv file
        """
        with open(filepath, "r") as f:
            data = []
            for line in f.readlines():
                temp = [x.rstrip() for x in line.split(";")]
                data.append(temp)
        return data
