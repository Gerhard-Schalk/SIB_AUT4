from enum import Enum
from py_pcsc_reader.cmd_apdu import *
from py_pcsc_reader.resp_apdu import *
from py_pcsc_reader.pcsc_reader import *
import ndef
import webbrowser
from urllib.parse import unquote


if __name__ == '__main__':
    try:
        # Flag to control whether web links found in NDEF records should be automatically opened in a browser
        openWebLink = False

        reader = PCSCReader()
        reader.connect()
        reader.activateCard()
        
        # Select Application
        selectAppCmdApdu = CmdApdu()
        selectAppCmdApdu.CLA = 0x00
        selectAppCmdApdu.INS = 0xA4
        selectAppCmdApdu.P1 = 0x04
        selectAppCmdApdu.P2 = 0x00
        selectAppCmdApdu.Data = 'D2 76 00 00 85 01 01'
        selectAppCmdApdu.Le = 0
        
        respApdu = reader.Exchange(selectAppCmdApdu,
                                 description='\nSelect Application',
                                 expectedSW1SW2=0x9000)
      
        
        # Select File - Capability Container File
        respApdu = reader.Exchange("00 A4 00 0C 02 E1 03",
                                 description='\nSelect NDEF File: FID = E104',
                                 expectedSW1SW2=0x9000)

        # Read Binary - Capability Container File
        respApdu = reader.Exchange("00 B0 00 00 00",
                                 description='\nRead CC file',
                                 expectedSW1SW2=0x9000)

        # Select NDEF-File
        baData = bytearray()

        #get NDEF-file ID from CC-file
        baData.append(respApdu.Data[9])     
        baData.append(respApdu.Data[10])

        selectNdefFileCmdApdu = CmdApdu()
        selectNdefFileCmdApdu.CLA = 0x00
        selectNdefFileCmdApdu.INS = 0xA4
        selectNdefFileCmdApdu.P1 = 0x00
        selectNdefFileCmdApdu.P2 = 0x0C
        selectNdefFileCmdApdu.Data = baData
        selectNdefFileCmdApdu.Le = 0

  
        respApdu = reader.Exchange(selectNdefFileCmdApdu,
                            description='\nSelect NDEF-File',
                            expectedSW1SW2=0x9000)
        
        # Read NDEF size
        respApdu = reader.Exchange("00 B0 00 00 02",
                                 description='\nRead NDEF-file size',
                                 expectedSW1SW2=0x9000)

        ndefSize = bytearray(respApdu.Data)[1]
        print('Ndef Message Size = ' + str(ndefSize) )


        readNdefFileCmdApdu = CmdApdu()
        readNdefFileCmdApdu.CLA = 0x00
        readNdefFileCmdApdu.INS = 0xB0
        readNdefFileCmdApdu.P1 = 0x00
        readNdefFileCmdApdu.P2 = 0x02
        readNdefFileCmdApdu.Le = ndefSize

        respApdu = reader.Exchange(readNdefFileCmdApdu,
                            description='\nRead NDEF-File',
                            expectedSW1SW2=0x9000)
        
        reader.disconnect()

        
        print('\n\rParsed Ndef Message:\n\r' )
        for record in ndef.message_decoder(respApdu.Data): 
            print(record)
            if isinstance(record, ndef.UriRecord):
                # convert %3D to = and %26 to &
                parsed_url = unquote(record.uri)
                print(f'Parsed URL: {parsed_url}')
        reader.disconnect()

        if openWebLink and isinstance(record, ndef.UriRecord):
            # opent the web links found in NDEF records in a browser
            webbrowser.open(parsed_url)
         

    except Exception as e:
        print(COLOR.RED.value + f'Exception: {e}')