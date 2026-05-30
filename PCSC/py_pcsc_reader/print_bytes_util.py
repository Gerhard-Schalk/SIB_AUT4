'''
    Copyright (c) 2023-2026, Gerhard H. Schalk

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''
from enum import Enum

class COLOR(Enum):
    '''
    Enum class defining ANSI color codes for terminal output.

    Provides color constants for formatting console text output with different colors.
    Each color is represented by its corresponding ANSI escape sequence.
    '''
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[94m"
    Gray = "\033[90m"
    White = "\033[37m"
    RESET_COLOR = "\033[0m"


def printColor(value, color = COLOR.RESET_COLOR ):  
    '''
        Prints colored text to the console without a newline.
        
        Args:
            value: The text string to print
            color: The COLOR enum value to use for text formatting (default: RESET_COLOR)
        
        Uses ANSI escape sequences to colorize terminal output. Does not append a newline
        after printing, allowing subsequent output on the same line.
    '''
    print(color.value + value, end='')


def printlnColor(value, color = COLOR.RESET_COLOR ):
    '''
        Prints colored text to the console with a newline.
        
        Args:
            value: The text string to print
            color: The COLOR enum value to use for text formatting (default: RESET_COLOR)
        
        Uses ANSI escape sequences to colorize terminal output. Does not append a newline
        after printing, allowing subsequent output on the same line.
    '''
    print(color.value + value)


def printBytes(prefix_text, value:bytes, color=COLOR.White, printASCII=False, charPerLine=16, ):
    '''
        Prints byte data in hexadecimal format with optional ASCII representation.
        
        Args:
            prefix_text: Text to display at the beginning of the first line
            value: The bytes object to print in hexadecimal format
            color: The COLOR enum value to use for text formatting (default: White)
            printASCII: If True, displays ASCII representation alongside hex (default: False)
            charPerLine: Number of bytes to display per line (default: 16)
        
        Outputs bytes in a formatted hex dump style with proper indentation for multi-line
        output. When printASCII is enabled, displays printable ASCII characters (32-126) and
        dots for non-printable bytes. Resets color formatting after printing.
    '''
    prefix_len = len(prefix_text)
    indent = ' ' * prefix_len

    print(color.value + prefix_text, end='')

    line_hex = ''
    line_ascii = ''
    i = 0

    for b in value:
        # hex part
        line_hex += '{0:02X} '.format(b)

        if printASCII == True:           
            # ascii part
            if 32 <= b <= 126:
                line_ascii += chr(b)
            else:
                line_ascii += '.'

        i += 1

        # full line reached
        if i % charPerLine == 0:
            print(line_hex + ' ' + line_ascii)

            line_hex = ''
            line_ascii = ''

            # indent next line
            print(indent, end='')

    # remaining bytes
    if line_hex:
        # pad hex part so ASCII lines up
        remaining = charPerLine - (i % charPerLine)
        if remaining != charPerLine:
            line_hex += '   ' * remaining

        print(line_hex + ' ' + line_ascii)

    print(COLOR.RESET_COLOR.value,end='\r')

