from enum import Enum
from smartcard.ATR import ATR
from py_pcsc_reader.cmd_apdu import *
from py_pcsc_reader.resp_apdu import *
from py_pcsc_reader.pcsc_reader import *
from py_pcsc_reader.print_bytes_util import COLOR, printColor, printlnColor, printBytes


if __name__ == '__main__':
    try:
        reader = PCSCReader()
        reader.connect()
        atr = reader.activateCard()
       
        # parse ATR (Answer To Reset) and print details
        print( ATR(atr).dump() )

        reader.disconnect()


    except Exception as e:
        print(COLOR.RED.value + f'Exception: {e}')