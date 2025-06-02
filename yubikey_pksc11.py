#!/usr/bin/env python3

# ----------------------------------------------
#               SIB_AUT4 Lab example
# ----------------------------------------------
# This example uses the Yubikey PKCS#11 library to sign "Hello World".
# The signature is verified using OpenSSL.

# Install required python library: pip install pykcs11

# Useful links:
# https://pypi.org/project/PyKCS11/
# https://github.com/LudovicRousseau/PyKCS11
# https://ludovicrousseau.blogspot.com/2023/04/verify-with-openssl-signature-computed.html
import binascii
from PyKCS11 import *

pkcs11 = PyKCS11Lib()
pkcs11.load(pkcs11dll_filename=r'C:\Program Files\Yubico\Yubico PIV Tool\bin\libykcs11.dll')  # adapt the path to libykcs11.dll
#pkcs11.load(pkcs11dll_filename='C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll')  


libraryInfo = pkcs11.getInfo()
print('----------------------------------------------------')
print('       PKSC#11 libary info')
print('----------------------------------------------------')
print(libraryInfo) # print libray info

print('\n')
print('----------------------------------------------------')
print('     Yubikey - RSA PKSC#11 Signature example ')
print('----------------------------------------------------')

slot = pkcs11.getSlotList(tokenPresent=True)[0]

session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)
session.login("123456") # Default Yubiky Pin


messageToSign = "Hello World!" # message to sign
mechanism = Mechanism(CKM_SHA256_RSA_PKCS, None)

# find first private key and compute signature
privKey = session.findObjects([(CKA_CLASS, CKO_PRIVATE_KEY)])[0]

signature = session.sign(privKey, messageToSign, mechanism)

#print(f"\nsignature: {binascii.hexlify(bytearray(signature))}")

print('Signature = 0x' + bytearray(signature).hex(' ').upper() )

# save the messageToSign text in a file
with open("messageToSign.txt", "w") as f:
    f.write(messageToSign)

# save to a signature in a file
with open("sig_sha256.bin", "bw") as f:
    f.write(bytearray(signature))

# Logout
session.logout()
session.closeSession()

print('\n')
print('----------------------------------------------------')
print('       The signature is verified using OpenSSL      ')
print('----------------------------------------------------')
# Read the certificate with KEY_ID 01 (Slot 9a) in DER format from the Yubikey
os.system('pkcs11-tool --read-object --id 01 --type cert --output-file Yubikey5_Cert_Slot_9a.crt')

# To convert the certificate in DER format to PEM format, use OpenSSL tools:
os.system('openssl x509 -inform DER -in Yubikey5_Cert_Slot_9a.crt -outform PEM > Yubikey5_Cert_Slot_9a.pem')


# To verify the signature with openssl, the public key needs to be extracted from the certificate.
os.system('openssl x509 -in Yubikey5_Cert_Slot_9a.pem -pubkey -noout > Yubikey5_PubKey_Slot_9a.pem')

# Verifying the signature with OpenSSL
os.system('openssl dgst -sha256 -verify Yubikey5_PubKey_Slot_9a.pem -signature sig_sha256.bin messageToSign.txt')