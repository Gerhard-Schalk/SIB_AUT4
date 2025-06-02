# OpenSC - pkcs11-tool
Utility for managing and using PKCS #11 security tokens (e.g. Yubikey).

- pkcs11-tool is a command line tool to test functions and perform crypto operations using a PKCS#11. 
- It always requires a local available working PKCS11 module. 
  - .DLL in Windows
  - .so in Linux
 - pkcs11-tool suppots various cryptographic action. 


- Documentation: https://www.mankier.com/1/pkcs11-tool

## PKCS#11 - Cryptoki System Architecture
![PKCS#11](/images/PKCS11_Architecture.png)

## Basic examples
```
pkcs11-tool --list-slots
```
```
pkcs11-tool --list-mechanisms
```
```
pkcs11-tool --list-objects
```
**Note:** If required specify a PKCS#11 module (or library) to load:
```
pkcs11-tool --module "C:\Program Files\Yubico\Yubico PIV Tool\bin\libykcs11.dll" --list-slots
```