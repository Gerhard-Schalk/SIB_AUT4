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

SW_LENGTH = int(2)

class RespApdu:
    """
    This class represents a ISO7816-4 command APDU (C-APDU).
    Supports short and extended APDU format.
    """
    def __init__(self, respApdu:bytes):
        self.__baRespApdu = respApdu
        self._Data = None
        self._SW1 = 0x00
        self._SW2 = 0x00
        self._SW1SW2 = 0x0000
    
        if self.__baRespApdu == None:
            raise ValueError('respApdu is None!')
        
        if len(self.__baRespApdu) < SW_LENGTH:
            raise ValueError('Incorrect respApdu length!')
        
        self._Data = self.__baRespApdu[:-2]
        self._SW1 = self.__baRespApdu[-2]
        self._SW2 = self.__baRespApdu[-1]
        self._SW1SW2 = self._SW1 *256 + self._SW2

    @property
    def Data(self)-> bytes:
        '''
        Gets the response APDU data bytes.
        '''
        return self._Data

    @property
    def SW1(self)-> bytes:
        '''
        Gets the response APDU status byte SW1.
        '''
        return self._SW1
    
    @property
    def SW2(self)-> bytes:
        '''
        Gets the response APDU status byte SW2.
        '''
        return self._SW2
    
    @property
    def SW1SW2(self)-> int:
        '''
        Gets the response APDU status word SW1SW2.
        '''
        return self._SW1SW2
    
    def __str__(self):
        if self.Data != None:
            return 'Data = 0x' + ' '.join(f"{byte:02X}" for byte in self.Data ) + '\n\r' \
                   +'SW1SW2 = 0x' + f'{self.SW1SW2:04X}'