#
#  Copyright (c) 2022-2024, Gerhard H. Schalk
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

class CmdApdu:
    """
    This class represents a ISO7816-4 command APDU (C-APDU).
    Supports short and extended APDU format.
    """
    LE_SHORT_MAX = 256
    LE_EXTENDED_MAX = 65536
    def __init__(self):
        self._CLA = 0x00
        self._INS = 0x00
        self._P1 = 0x00
        self._P2 = 0x00
        self._Lc = None
        self._Data = None
        self._Le = None
    
    @property
    def CLA(self)-> int:
        '''
        The the class byte.
        '''
        return self._CLA
    
    @CLA.setter
    def CLA(self, value:int):
        if value < 0 or value > 255:
            raise ValueError('CLA out of range')
        self._CLA = value
    
    @property
    def INS(self)-> int:
        '''
        The the instruction byte.
        '''
        return self._INS
    
    @INS.setter
    def INS(self, value:int):
        if value < 0 or value > 255:
            raise ValueError('INS out of range')
        self._INS = value

    @property
    def P1(self)-> int:
        '''
        The the parameter byte P1 .
        '''
        return self._P1
    
    @P1.setter
    def P1(self, value:int):
        if value < 0 or value > 255:
            raise ValueError('P1 out of range')
        self._P1 = value

    
    @property
    def P2(self)-> int:
        '''
        The the parameter byte P2 .
        '''
        return self._P2
    
    @P2.setter
    def P2(self, value:int):
        if value < 0 or value > 255:
            raise ValueError('P2 out of range')
        self._P2 = value


    @property
    def Lc(self)-> int:
        '''
        Length command byte:
        Codes the number of data bytes to send to the card, 'None' if none data is send.
        Short APDU: 1..255
        Extended APDU: 1..65535.
        '''
        return self._Lc
    
    @Lc.setter
    def Lc(self, value:int):
        if value == 0:
            self._Lc = None
        else:
            self._Lc = value

    @property
    def Le(self)-> int:
        '''
        Length expected:
        Codes the number of data bytes (1..256) expected form the card, 'None' if none data is expected.
        Short APDU: 0 means the maximum of 256 bytes.
        Extended APDU: 0 means the maximum of 65536 bytes.
        '''
        return self._Le
    
    @Le.setter
    def Le(self, value:int):
        self._Le = value

    @property
    def Data(self)-> bytes:
        '''
        Get the command apdu data bytes.
        '''
        return self._Data
    
    @Data.setter
    def Data(self, value):
        '''
        Set the command apdu data bytes.
        '''
        if type(value) == bytes or type(value) == bytearray:
            self._Data = value
        elif type(value) == str:
            self._Data = value = bytes.fromhex(value) 
        if self._Data != None:
            self._Lc = len(self._Data)
    

    
    def getBytes(self) -> bytes:
        '''
        Gets the command APDU bytes.
        
        Constructs the byte representation of the command APDU according to ISO/IEC 7816-4 specification.
        Supports both short and extended APDU formats:
        - Case 1: CLA INS P1 P2
        - Case 2S: CLA INS P1 P2 Le (short)
        - Case 2E: CLA INS P1 P2 0x00 Le1 Le2 (extended)
        - Case 3S: CLA INS P1 P2 Lc DATA (short)
        - Case 3E: CLA INS P1 P2 0x00 Lc1 Lc2 DATA (extended)
        - Case 4S: CLA INS P1 P2 Lc DATA Le (short)
        - Case 4E: CLA INS P1 P2 0x00 Lc1 Lc2 DATA Le1 Le2 (extended)
        
        Returns:
            bytes: The complete command APDU as a byte array.
        '''
        '''
        Gets the command Apdu bytes.
        '''
        self._lcIsExtLength = False

        self._baCmdApdu = bytearray()
        self._baCmdApdu.append(self._CLA)
        self._baCmdApdu.append(self._INS)
        self._baCmdApdu.append(self._P1)
        self._baCmdApdu.append(self._P2)

        if self._Lc != None:
            if  self._Lc <= 255 and ( self._Le == None or self._Le <= 256)  :
                # The short Lc field constists of one byte and encodes the number
                # of data bytes from 1 to 255.
                
                # Case 3S and 4S
                self._baCmdApdu.append( self._Lc & 0xFF )
            else:
                # The extended Lc field consitsts of tree bytes. The first byte (offset = 5)
                # always set to 0x00. The two bytes (offset = 6 and 7) are endcoding the 
                # number of data bytes from 1 to 65535
                
                # Case 3E and 4E
                self._lcIsExtLength = True

                self._baCmdApdu.append(0x00);
                self._baCmdApdu.append( (self._Lc & 0xFF00) >> 8) 
                self._baCmdApdu.append(self._Lc & 0xFF)

            # Add Data
            self._baCmdApdu.extend(self._Data)

        if self._Le != None:

            if  (self._lcIsExtLength == False) and (self._Le <= 256):
                # The Le field consists of one byte, encodes the number of bytes form 1 to 256 
                # (0x00 means the maximum, 256) expected form the card.
                # Case 2S and 4S
                if self._Le == 256:
                    self._baCmdApdu.append( 0x00 )
                else:
                    self._baCmdApdu.append( self._Le & 0xFF )
            else:

                # The Le field consists of two byte, encodes the number of bytes form 1 to 65536 
                # (0x0000 means the maximum, 65536) expected form the card.
                if self._Le == 65536:
                    if self._lcIsExtLength == False:
                        # Case 2E
                        self._baCmdApdu.append(0x00)
                        self._baCmdApdu.append(0x00)
                        self._baCmdApdu.append(0x00)
                    else:
                        # Case 4E
                        self._baCmdApdu.append(0x00)
                        self._baCmdApdu.append(0x00)
                else:
                    if self._lcIsExtLength == False:
                        # Case 2E
                        self._baCmdApdu.append(0x00)
                        self._baCmdApdu.append( (self._Le & 0xFF00) >> 8) 
                        self._baCmdApdu.append(self._Le & 0xFF)
                    else:
                        # Case 4E
                        self._baCmdApdu.append( (self._Le & 0xFF00) >> 8) 
                        self._baCmdApdu.append(self._Le & 0xFF)
        return self._baCmdApdu

    def setBytes( self, cmdApdu: bytes ):
        """
        Parse a byte array or hex string into APDU command components.
        
        This method parses the provided APDU command and sets the CLA, INS, P1, P2,
        Lc, Data, and Le fields according to ISO/IEC 7816-4 APDU format.
        
        Supports all APDU cases:
        - Case 1: CLA INS P1 P2
        - Case 2S: CLA INS P1 P2 Le (short)
        - Case 3S: CLA INS P1 P2 Lc DATA (short)
        - Case 4S: CLA INS P1 P2 Lc DATA Le (short)
        - Case 2E: CLA INS P1 P2 {00 Le Le} (extended)
        - Case 3E: CLA INS P1 P2 {00 Lc Lc} DATA (extended)
        - Case 4E: CLA INS P1 P2 {00 Lc Lc} DATA {Le Le} (extended)
        
        Args:
            cmdApdu: The APDU command as bytes, bytearray, or hex string
            
        Raises:
            ValueError: If the APDU format is invalid or length is less than 4 bytes
        """
        cmdApduBuffer = None
        if type(cmdApdu) == bytes or type(cmdApdu) == bytearray:
            cmdApduBuffer = cmdApdu
        elif type(cmdApdu) == str:
            cmdApduBuffer = cmdApdu = bytes.fromhex(cmdApdu) 

        if (len(cmdApduBuffer) < 4):
            raise ValueError('The minimum APDU length is 4 bytes!')

        self.CLA = cmdApduBuffer[0]
        self.INS = cmdApduBuffer[1]
        self.P1 = cmdApduBuffer[2]
        self.P2 = cmdApduBuffer[3]
        self.Lc = None
        self.Data = None
        self.Le = None

        if (len(cmdApduBuffer) == 4):   
            # Case 1: CLA INS P1 P2
            pass
    
        elif (len(cmdApduBuffer) == 5):
            # Case 2S: CLA INS P1 P2 Le
            if (cmdApduBuffer[4] == 0):
                self.Le = 256
            else:
                self.Le = cmdApduBuffer[4]

        elif ((len(cmdApduBuffer) > 5) and (cmdApduBuffer[4] != 0)):

            self.Lc = cmdApduBuffer[4]
            if (self.Lc == 0):
                raise ValueError('APDU format error!')
            
            if (len(cmdApduBuffer) == (5 + self.Lc)):
                # CASE 3S: CLA INS P1	P2	Lc	DATA ..	DATA 
                baData = bytearray()
                for i in range(0, self.Lc):              
                    baData.append(cmdApduBuffer[5 + i])
                self.Data = baData

            elif (len(cmdApduBuffer) == (6 + self.Lc)):
                # CASE 4S: CLA INS P1	P2 Lc DATA .. DATA Le
                if (cmdApduBuffer[len(cmdApduBuffer) - 1] == 0):
                    self.Le = 256
                else:
                    self.Le = cmdApduBuffer[len(cmdApduBuffer) - 1]

                baData = bytearray()
                for i in range(0, self.Lc):              
                    baData.append(cmdApduBuffer[5 + i])
                self.Data = baData
            else:
                raise ValueError('APDU format error!')

        elif ((len(cmdApduBuffer) == 7) and (cmdApduBuffer[4] == 0)):
            # CASE 2E: CLA INS P1 P2 {00 Le Le}
            if ((cmdApduBuffer[5] == 0) and (cmdApduBuffer[6] == 0)):
                self.Le = 65536
            else:
                self.Le = (cmdApduBuffer[5] * 256) + cmdApduBuffer[6]

        elif ((len(cmdApduBuffer) > 7) and (cmdApduBuffer[4] == 0)):
            self.Lc = (cmdApduBuffer[5] * 256) + cmdApduBuffer[6]
            
            if (self.Lc == 0):
                raise ValueError('APDU format error!')

            if (len(cmdApduBuffer) == (7 + self.Lc)):
                # CASE 3E: CLA INS P1 P2 {00 Lc Lc} DATA ..	DATA
                baData = bytearray()    
                for i in range(0, self.Lc):              
                    baData.append(cmdApduBuffer[7 + i])
                self.Data = baData                    

            elif (len(cmdApduBuffer) and (9 + self.Lc)):
                # CASE 4E: CLA INS P1	P2 {00 Lc Lc} DATA .. DATA {Le Le}
                if ((cmdApduBuffer[len(cmdApduBuffer) - 2] == 0) and (cmdApduBuffer[len(cmdApduBuffer) - 1] == 0)):
                    self.Le = 65536
                else:
                    self.Le = (cmdApduBuffer[len(cmdApduBuffer) - 2] * 256) + cmdApduBuffer[len(cmdApduBuffer) - 1]

                baData = bytearray()    
                for i in range(0, self.Lc):              
                    baData.append(cmdApduBuffer[7 + i])
                self.Data = baData 

            else:
                raise ValueError('APDU format error!')
        else:
            raise ValueError('APDU format error!')

    def __str__(self):
        baCmdApdu = self.getBytes()
        return '0x' + ' '.join(f"{byte:02X}" for byte in self._baCmdApdu )

      

if __name__ == '__main__':
        #import sys
        #import os
        #sys.path.append(os.path.join(os.path.dirname(__file__), '..'))        

        import util.print_bytes_util

        baData = bytearray()
        for i in range(0,75):
            baData.append(i & 0xFF)

        selectAppCmdApdu = CmdApdu()
        selectAppCmdApdu.CLA = 0x00
        selectAppCmdApdu.INS = 0xA4
        selectAppCmdApdu.P1 = 0x04
        selectAppCmdApdu.P2 = 0x0C
        selectAppCmdApdu.Data = baData
        #selectAppCmdApdu.Le = CmdApdu.LE_EXTENDED_MAX


        tstCmd = CmdApdu()

        baSelect = selectAppCmdApdu.getBytes()
        util.print_bytes_util.printBytes('baSelect ', baSelect)


        tstCmd.setBytes(baSelect)

        baTst = tstCmd.getBytes()
        
        util.print_bytes_util.printBytes('baTst    ', baTst )
        print(tstCmd.Lc)
        util.print_bytes_util.printBytes('baTst Data ', tstCmd.Data )
