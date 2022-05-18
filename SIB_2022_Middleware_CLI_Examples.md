# opensc-tool
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

# pkcs11-tool / Open SSL
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


