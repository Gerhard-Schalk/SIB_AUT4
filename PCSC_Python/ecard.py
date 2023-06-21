from smartcard.System import readers
from smartcard.util import toHexString, toASCIIString
from smartcard.util import toBytes
from smartcard.ATR import ATR


pcscReaderList = readers()

i = 0
for pcscReader in pcscReaderList:
    print(f'[{i:d}] {pcscReader}')
    i += 1

selectedPcscReader = int(input("Please select a reader (0..n): "))

connection = pcscReaderList[selectedPcscReader].createConnection()



connection.connect()

print("ATR = 0x", toHexString( connection.getATR() ))

#print "ATR Historical Bytes", toHexString( ATR(connection.getATR()).getHistoricalBytes())
print( ATR(connection.getATR()).dump() )


print("    Select Master File ...")
data, sw1, sw2 = connection.transmit( toBytes ("00 A4 00 0C 02 3F 00") )


print( "    Select eCard Application ...")
data, sw1, sw2 = connection.transmit( toBytes ("00 A4 04 0C 08 D0 40 00 00 17 01 01 01") )


print("    Read Binary ...")
data, sw1, sw2 = connection.transmit( toBytes ("00 B0 81 00 00") )
if sw1 == 0x90 and sw2 == 0x00:
    print( ": received = 0x", toHexString(data))
    print("\n\nASCII:", toASCIIString(data))
