# OpenSC-tool
OpenSC provides a set of libraries and utilities to work with smart cards. 
OpenSC implements the standard APIs to smart cards e.g.
PKCS#11 API, Windows’ Smart Card Minidriver and macOS CryptoTokenKit.

Download and Wiki: https://github.com/OpenSC/OpenSC/wiki

Documentation: https://www.mankier.com/package/opensc 

### Basic examples
```
opensc-tool --list-readers
opensc-tool --reader 0 -atr -v
opensc-tool --reader 0 --name
```

# OpenSC – pkcs15-tool
Utility for manipulating PKCS #15 data structures on smart cards and similar security token.

Documentation: https://www.mankier.com/1/pkcs15-tool

### Basic examples
```
pkcs15-tool --reader 0 --dump
pkcs15-tool --reader 0 --list-keys
pkcs15-tool --reader 0 --list-public-keys
pkcs15-tool --reader 0 --read-public-key 02
pkcs15-tool --reader 0 --read-certificate 02
```

#  Windows 10 Certutil CLI Tool
The windows Certutil.exe is a command-line program that is installed as part of Certificate Services.

```
Certutil -SCInfo
```

# Windows 10 Certification Manager
Insert the Yubikey and run the following command to start the Windows 10 certification manager:

```
Certmgr.msc
```

# pkcs11-tool
Utility for managing and using PKCS #11 security tokens (e.g. Yubikey).

Documentation: https://www.mankier.com/1/pkcs11-tool

### Basic examples
```
pkcs11-tool --module "C:\Program Files\Yubico\Yubico PIV Tool\bin\libykcs11.dll" --list-slots

pkcs11-tool --module "C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll" --list-slots
pkcs11-tool --list-slots
pkcs11-tool --list-mechanisms
pkcs11-tool --list-objects
```

# Yubikey Example:
# Signing data with pkcs11-tool and verifying the signature with OpenSSL
Generate some data to be signed ...
```
echo "Hallo World" > data.txt
```

Signing data with pkcs11-tool using Yubikey KEY_ID 02 (Slot 9c)

Default Yubikey 5 NFC **PIN: 123456**

```
pkcs11-tool --sign -m RSA-SHA256 --id 2 -i data.txt -o data.sig
```


**Note:** If required specify the path to the PKCS11 DLL using --module in all relevant examples:

Example: ```--module "C:\Program Files\Yubico\Yubico PIV Tool\bin\libykcs11.dll"```



Read the certificate with KEY_ID 02 (Slot 9c) in DER format from the Yubikey 
```
pkcs11-tool --read-object --id 02 --type cert --output-file Yubikey5_DigSign_Cert_Slot_9c.crt
```	


To convert the certificate in DER format to PEM format, use OpenSSL tools:
```
openssl x509 -inform DER -in Yubikey5_DigSign_PubKey_Slot_9c.der -outform PEM > Yubikey5_DigSign_PubKey_Slot_9c.pem
```


Read the public key wiht KEY_ID 02 (Slot 9c) in DER format from the Yubikey
```
pkcs11-tool --read-object --id 02 --type pubkey --output-file Yubikey5_DigSign_PubKey_Slot_9c.der
```


To convert the public key in DER format to PEM format, use OpenSSL tools: (does not work)
```
openssl rsa -inform der -in Yubikey5_DigSign_PubKey_Slot_9c.der -outform pem -out Yubikey5_DigSign_PubKey_Slot_9c.pem
```


To verify the signature with openssl, the public key needs to be extracted from the certificate.
```
openssl x509 -in Yubikey5_DigSign_Cert_Slot_9c.pem -pubkey -noout > Yubikey5_DigSign_PubKey_Slot_9c.pem
```


Verifying the signature with OpenSSL
```
openssl dgst -sha256 -verify Yubikey5_DigSign_PubKey_Slot_9c.pem -signature data.sig data.txt
```
