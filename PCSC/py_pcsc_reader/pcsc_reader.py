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
import os
from enum import Enum
from smartcard.System import readers
from smartcard.util import toHexString, toASCIIString
from smartcard.util import toBytes
from smartcard.ATR import ATR
from .cmd_apdu import CmdApdu
from .resp_apdu import RespApdu
from .print_bytes_util import COLOR, printColor, printlnColor, printBytes
from colorama import init
class PCSC_Reader_Exception(IOError):
    "PCSC_Reader_Exception Base class for VCOM_TPCSCReader related exceptions."

class ApduException(IOError):
    "ApduException Base class"

class PCSCReader:
    """
    PCSCReader class provides an interface to communicate with PC/SC smart card readers.
    
    This class handles connection management, card activation, and APDU exchange with smart cards
    through PC/SC compatible readers. It supports reader selection by name or interactive selection,
    and provides colored console output for debugging APDU communication.
    
    Methods:
        connect(pcsc_reader_name): Establishes connection to a PC/SC reader by name or interactive selection
        activateCard(): Activates the smart card and displays its ATR
        disconnect(): Disconnects from the reader and releases resources
        Exchange(cmdApdu, expectedSW1SW2, description): Sends command APDU and receives response APDU
    
    Raises:
        Exception: When reader is not found or no readers are available
        ApduException: When APDU exchange fails or response doesn't match expected SW1SW2
    """
    def __init__(self):
        if os.name != "posix":
            init() #enables ANSI codes in Windows.
        self.connection = None
        self.reader = None

    def connect(self, pcsc_reader_name=''):
        """
        Establishes a connection to a PC/SC smart card reader.
        
        This method searches for and connects to a PC/SC reader either by name or through
        interactive selection. If a reader name is provided, it searches for an exact or
        partial match. If no name is provided, it displays all available readers and prompts
        the user to select one.
        
        Args:
            pcsc_reader_name (str, optional): Name or partial name of the PC/SC reader to connect to.
                                              If empty, prompts for interactive selection. Defaults to ''.
        
        Returns:
            None
        
        Raises:
            Exception: If the specified reader is not found or no readers are available.
        """
        pcscReaderList = readers()

        # Find the pcsc reader by name
        if pcsc_reader_name:
            # Search for exact match or partial match
            for pcscReader in pcscReaderList:
                if pcsc_reader_name in str(pcscReader):
                    self.reader = pcscReader
                    break
            
            if not self.reader:
                raise Exception(f"Reader '{pcsc_reader_name}' not found")
        else:
            # Use first reader if no name specified
            if len(pcscReaderList) > 0:
                for i, pcscReader in enumerate(pcscReaderList):
                    print(f'[{i:d}] {pcscReader}')
                selected_reader_index = int(input("Please select a reader (0..n): "))
                self.reader = pcscReaderList[selected_reader_index]
            else:
                raise Exception("No readers available")
        
        # Create connection with the selected reader
        self.connection = self.reader.createConnection()
        print(f"Connected to: {self.reader}")
        return None

    def activateCard(self):
        """
        Activates the smart card and establishes communication.
        
        This method connects to the smart card in the reader and retrieves the Answer To Reset (ATR)
        which contains information about the card's capabilities and characteristics.
        
        Returns:
            bytes: The ATR (Answer To Reset) data from the smart card.
        
        Raises:
            Exception: If the card connection fails or no card is present in the reader.
        """
        self.connection.connect()
        atr = self.connection.getATR()
        print('ATR = 0x', toHexString( atr ) )
        return atr

    def disconnect(self):
        """
        Disconnects from the smart card and releases the connection.
        
        This method terminates the connection to the smart card and releases any resources
        associated with the connection to the reader.
        
        Returns:
            None
        """
        self.connection.disconnect()
        self.connection.release()
        return None
    
    def Exchange(self, cmdApdu, expectedSW1SW2=None, description='')->RespApdu:
        """
        Sends a command APDU to the smart card and receives the response.
        
        This method transmits a command APDU to the smart card and returns the response APDU.
        It supports multiple input formats for the command APDU and can optionally validate
        the response status word against an expected value.
        
        Args:
            cmdApdu: The command APDU to send. Can be bytes, bytearray, str (hex string), or CmdApdu object.
            expectedSW1SW2: Optional expected status word (SW1SW2) to validate the response against.
            description: Optional description of the command for logging purposes.
        
        Returns:
            RespApdu: The response APDU object containing the response data and status word.
        
        Raises:
            ApduException: If the command APDU type is invalid or if the response SW1SW2 
                            does not match the expected value.
        """
        if type(cmdApdu) == bytes or type(cmdApdu) == bytearray:
            self._cmdApdu = cmdApdu
        elif type(cmdApdu) == str:
            self._cmdApdu = bytes.fromhex(cmdApdu)      
        elif type(cmdApdu) == CmdApdu:
            self._cmdApdu = cmdApdu.getBytes()
        else:
            raise ApduException(f"Invalid command APDU type: cmdApdu must be type of bytes, bytearray or CmdApdu")
        
        print('    \n' + description)
        printBytes('--> C-Apdu 0x', self._cmdApdu, color=COLOR.BLUE, printASCII=True) 

        response, sw1, sw2 = self.connection.transmit(list(self._cmdApdu))
        baRespApdu = bytes(response + [sw1, sw2])
        printBytes('<-- R-Apdu 0x', baRespApdu, color=COLOR.GREEN, printASCII=True)
        
        respApdu = RespApdu(baRespApdu)
        if expectedSW1SW2 != None:
            if expectedSW1SW2 != respApdu.SW1SW2:
                raise ApduException(f'Error: Response SW1SW2 did not match the expected value!')

        return respApdu