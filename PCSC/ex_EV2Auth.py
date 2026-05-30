
from enum import Enum
from py_pcsc_reader.cmd_apdu import *
from py_pcsc_reader.resp_apdu import *
from py_pcsc_reader.pcsc_reader import *
from py_pcsc_reader.print_bytes_util import COLOR, printColor, printlnColor, printBytes
from py_pcsc_reader.crypto_util import *
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding, serialization, cmac



class EV2_Auth:
    def __init__(self, reader, aesKeyNo:int, aesKey):
        self._reader = reader
        self._aesKeyNo = aesKeyNo
        if type(aesKey) == bytes or type(aesKey) == bytearray:
            self._aesAuthKey = aesKey
        elif type(aesKey) == str:
            self._aesAuthKey = bytes.fromhex(aesKey)   

  

    def AuthEV2FirstPart1(self)-> bytes:
        authEV2FirstPart1CmdApdu = CmdApdu()
        authEV2FirstPart1CmdApdu.CLA = 0x90
        authEV2FirstPart1CmdApdu.INS = 0x71
        authEV2FirstPart1CmdApdu.P1 = 0x00
        authEV2FirstPart1CmdApdu.P2 = 0x00
        baData = bytearray()
        baData.append(self._aesKeyNo) # KeyNo
        baData.append(0) # LenCap = 0
        authEV2FirstPart1CmdApdu.Data = baData
        authEV2FirstPart1CmdApdu.Le = 0x00
                
        respApdu = self._reader.Exchange(authEV2FirstPart1CmdApdu, 
                                 expectedSW1SW2=0x91AF, 
                                 description='AuthEV2 First Part 1')
        self._encryptedRndB = respApdu.Data 
        return respApdu.Data


    def AuthEV2FirstPart2(self):
        authEV2FirstPart2CmdApdu = CmdApdu()
        authEV2FirstPart2CmdApdu.CLA = 0x90
        authEV2FirstPart2CmdApdu.INS = 0xAF
        authEV2FirstPart2CmdApdu.P1 = 0x00
        authEV2FirstPart2CmdApdu.P2 = 0x00
        authEV2FirstPart2CmdApdu.Le = 0x00
        
        rndA = os.urandom(16)
        printBytes('    rndA = 0x', rndA, color=COLOR.Gray)

        rndB = CryptoUtil.AES_CBC_Decrypt(self._aesAuthKey, self._encryptedRndB)
        printBytes('    rndB = 0x', rndB, color=COLOR.Gray)

        rndBDash = bytearray()
        rndBDash.extend(rndB[1:16]) # rotate rndB to calculate rndB'
        rndBDash.append(rndB[0])
        #printBytes('rndBDash = 0x', rndBDash)
        
        baDataPlain = bytearray()
        baDataPlain.extend(rndA)
        baDataPlain.extend(rndBDash)
        
        baDataEncrypted = CryptoUtil.AES_CBC_Encrypt(self._aesAuthKey, baDataPlain) 
        authEV2FirstPart2CmdApdu.Data = baDataEncrypted
 
        
        respApdu = self._reader.Exchange(authEV2FirstPart2CmdApdu, 
                                 expectedSW1SW2=0x9100, 
                                 description='AuthEV2 First Part 2')

   
        plainRespApduData = CryptoUtil.AES_CBC_Decrypt(self._aesAuthKey, respApdu.Data) 
        printBytes('    plainRespApduData = 0x', plainRespApduData, color=COLOR.Gray)

        transId = plainRespApduData[0:4] # 4 byte Transaction Identifier
        rndADash = plainRespApduData[4:20] # 16 byte rndA'

        rndARec = bytearray()
        rndARec.extend(rndADash[15:16])
        rndARec.extend(rndADash[0:15])
        
        printBytes('    Transaction Identifier = 0x', transId, color=COLOR.Gray)
        #printBytes('rndADash = 0x', rndADash, color=COLOR.Gray)
        printBytes('    rndARec = 0x', rndARec, color=COLOR.Gray)

if __name__ == '__main__':
    try:
        reader = PCSCReader()
        reader.connect()
        reader.activateCard()
        
        # Select application 
        selectAppCmdApdu = CmdApdu()
        selectAppCmdApdu.CLA = 0x00
        selectAppCmdApdu.INS = 0xA4
        selectAppCmdApdu.P1 = 0x04
        selectAppCmdApdu.P2 = 0x0C
        selectAppCmdApdu.Data = 'D2 76 00 00 85 01 01'
        selectAppCmdApdu.Le = 0

        respApdu = reader.Exchange(selectAppCmdApdu,
                                   expectedSW1SW2=0x9000, 
                                   description='Select Application')

        hostAesKey = '00' * 16
        authEV2_Host = EV2_Auth( reader, aesKeyNo = 0, aesKey = hostAesKey)
        authEV2_Host.AuthEV2FirstPart1()
        authEV2_Host.AuthEV2FirstPart2()

        reader.disconnect()


    except Exception as e:
        print(COLOR.RED.value + f'Exception: {e}')