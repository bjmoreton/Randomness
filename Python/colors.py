"""
Color Utilities Module
Author: Richard Moreton
Description:
    Provides a set of ANSI color codes for terminal text and background styling,
    including standard colors, bright variants, 256-color support, and basic blink effect.
    Includes functions to parse custom color codes in strings and replace them with ANSI sequences.

Usage:
    from colors import Colors, parse_colors

    # Example
    print(parse_colors("&rThis is bright red text&~"))
    print(f"{Colors.color256(196)}This is color 196 in 256-color mode{Colors.reset}")
"""

import re


class Colors:
    """
    ANSI color codes for terminal output.
    Includes:
        - Standard text colors
        - Bright text colors
        - Background colors
        - Bright background colors
        - Blinking text
        - 256-color support
    """

    # Reset ANSI formatting
    reset = "\033[0m"

    # Standard text colors
    black = "\033[30m"
    darkGrey = "\033[1;30m"
    red = "\033[0;31m"
    green = "\033[32m"
    yellow = "\033[33m"
    orange = "\033[0;33m"
    blue = "\033[34m"
    magenta = "\033[35m"
    cyan = "\033[36m"
    lightBlue = "\033[1;36m"
    white = "\033[37m"
    grey = "\033[0;37m"

    # Bright text colors
    brightBlack = "\033[30;1m"
    brightRed = "\033[31;1m"
    brightGreen = "\033[32;1m"
    brightYellow = "\033[33;1m"
    brightOrange = "\033[38;5;214;1m"
    brightBlue = "\033[34;1m"
    brightMagenta = "\033[35;1m"
    brightCyan = "\033[36;1m"
    brightWhite = "\033[37;1m"

    # Standard background colors
    bgBlack = "\033[40m"
    bgRed = "\033[41m"
    bgGreen = "\033[42m"
    bgYellow = "\033[43m"
    bgOrange = "\033[48;5;208m"
    bgBlue = "\033[44m"
    bgMagenta = "\033[45m"
    bgCyan = "\033[46m"
    bgWhite = "\033[47m"

    # Bright background colors
    bgBrightBlack = "\033[40;1m"
    bgBrightRed = "\033[41;1m"
    bgBrightGreen = "\033[42;1m"
    bgBrightYellow = "\033[43;1m"
    bgBrightOrange = "\033[48;5;214;1m"
    bgBrightBlue = "\033[44;1m"
    bgBrightMagenta = "\033[45;1m"
    bgBrightCyan = "\033[46;1m"
    bgBrightWhite = "\033[47;1m"

    # Blink text effect
    blink = "\033[5m"

    # 256-color support (text)
    @staticmethod
    def color256(color: int) -> str:
        """
        Returns the ANSI escape code for a 256-color foreground.

        :param color: Integer between 0-255 representing the 256-color code
        :return: ANSI escape sequence as a string
        """
        return f"\033[38;5;{color}m"

    # 256-color support (background)
    @staticmethod
    def bgColor256(color: int) -> str:
        """
        Returns the ANSI escape code for a 256-color background.

        :param color: Integer between 0-255 representing the 256-color code
        :return: ANSI escape sequence as a string
        """
        return f"\033[48;5;{color}m"


def replace_with_color_code(input_str: str) -> str:
    """
    Replace placeholders of the form '}<number>' in a string with
    the corresponding 256-color ANSI escape codes.

    Example:
        "This is }196 red text" -> "This is <ANSI code for color 196> red text"

    :param input_str: Input string containing placeholders
    :return: String with 256-color placeholders replaced by ANSI codes
    """
    return re.sub(
        r"}(\d+)", lambda match: Colors.color256(int(match.group(1))), input_str
    )


def parse_colors(string_to_parse: str) -> str:
    """
    Parse a string and replace custom color codes with ANSI escape sequences.

    Supports codes like:
        &x  -> black
        &B  -> blue
        &c  -> cyan
        &b  -> bright blue
        &g  -> bright green
        &r  -> bright red
        &~  -> reset
    And more (see replacements dictionary).

    Also supports '}<number>' for 256-color codes.

    :param string_to_parse: The input string containing color placeholders
    :return: The string with ANSI escape codes applied
    """
    ret_string = string_to_parse

    # Dictionary mapping custom codes to Colors class attributes
    replacements = {
        "&x": Colors.black,
        "&B": Colors.blue,
        "&c": Colors.cyan,
        "&b": Colors.brightBlue,
        "&g": Colors.brightGreen,
        "&z": Colors.brightBlack,
        "&r": Colors.brightRed,
        "&G": Colors.green,
        "&w": Colors.brightWhite,
        "&C": Colors.lightBlue,
        "&O": Colors.orange,
        "&P": Colors.brightMagenta,
        "&p": Colors.magenta,
        "&R": Colors.red,
        "&W": Colors.white,
        "&y": Colors.yellow,
        "&Y": Colors.brightYellow,
        "&~": Colors.reset,
    }

    # Replace all custom codes with ANSI codes
    for key, value in replacements.items():
        ret_string = ret_string.replace(key, value)

    # Replace any 256-color placeholders
    ret_string = replace_with_color_code(ret_string)

    # Ensure the string ends with a reset to avoid bleeding colors
    return f"{ret_string}{Colors.reset}"


def print_color(output: str):
    """
    Print a string to the terminal with color parsing.

    :param output: The string containing color codes
    """
    print(parse_colors(output))
