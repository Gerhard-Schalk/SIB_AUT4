#  Explore the Yubikey card certificates
##  Windows 10 Certutil CLI Tool
The windows Certutil.exe is a command-line program that is installed as part of Certificate Services. Use the following command to display the Yubikey certificates. 

**Note:** 
- Default Yubikey PIN: `0123456`
- Default Yubikey PUK:: `12345678`

```
Certutil -SCInfo
```
![Cert Util](/images/CertUtil_1.png)

![Cert Util](/images/CertUtil_2.png)

## Windows Certification Manager
Insert the Yubikey and run the following command to start the Windows 10 certification manager:

```
Certmgr.msc
```
Try to find you Yubikey certificate.

![Windows Certification Manager](/images/Win_Certmgr.png)

Download the certificate. Print the certificate content using certutil.
```
certutil -dump <cert_name.crt>
```

Certutil also contains an ASN.1 parser:
```
certutil -asn <cert_name.crt>
```



## PKCS#15 and ISO/IEC 7816-15 File Structure
- Interoperability using Standardized and Dynamic file system.
- EF.DIR contains Applications on card indexed by their AID’s.
- Each Application contains predefined and mandatory information
  - EF (TokenInfo)
    - Generic information about the card such as card capabilities, Serial Number, Algorithms, etc.
  - EF (Object Directory File - ODF)
    - Contains pointers to other directory files of a particular PKCS#15 Class
![PKCS#15](/images/PKCS15.png)

## OpenSC – pkcs15-tool

Utility for manipulating PKCS #15 data structures on Smartcards and similar security token. 

- Documentation: https://www.mankier.com/1/pkcs15-tool


**Note**: Use the reader number returned by ```opensc-tool --list-readers```.

### Basic examples
**Note**: Use the reader number returned by ```opensc-tool --list-readers```.
```
pkcs15-tool --reader 0 --dump
```
```
pkcs15-tool --reader 0 --list-keys
```
```
pkcs15-tool --reader 0 --list-public-keys
```
```
pkcs15-tool --reader 0 --read-public-key 02
```
```
pkcs15-tool --reader 0 --read-certificate 02
```

## pkcs11-tool
Utility for managing and using PKCS #11 security tokens (e.g. Yubikey).

- pkcs11-tool is a command line tool to test functions and perform crypto operations using a PKCS#11. 
- It always requires a local available working PKCS11 module. 
  - .DLL in Windows
  - .so in Linux
 - pkcs11-tool suppots various cryptographic action. 


- Documentation: https://www.mankier.com/1/pkcs11-tool

### PKCS#11 - Cryptoki System Architecture
![PKCS#11](/images/PKCS11_Architecture.png)

### Basic examples
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