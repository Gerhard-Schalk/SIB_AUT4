# OpenSC-tool
OpenSC provides a set of libraries and utilities to work with smart cards. 
OpenSC implements the standard APIs to smart cards e.g.
PKCS#11 API, Windows’ Smart Card Minidriver and macOS CryptoTokenKit.

- Wiki: https://github.com/OpenSC/OpenSC/wiki
- Download: https://github.com/OpenSC/OpenSC
  - **Note:** Add OpenSC Tool path to environment variables
- Documentation: https://www.mankier.com/package/opensc 

### Basic examples
```
opensc-tool --list-readers
```
```
opensc-tool --list-algorithms
```
**Note**: Use the reader number returned by ```opensc-tool --list-readers```.
```
opensc-tool --reader 0 --atr -v
```
Use the following link to parse your ATR:  https://smartcard-atr.apdu.fr/ 
```
opensc-tool --reader 0 --name
```
## YubiKey Manager
Use the YubiKey Manager to configure the PIV functionality on your YubiKey 5 NFC.
- Download: https://www.yubico.com/support/download/yubikey-manager/

Use the YubiKey Manager to generate a self-signed RSA2048 certificate in Slot9c (KEY_ID = 02).

![Yubikey Manager 1](/images/YubikeyManager_1.png)

![Yubikey Manager 2](/images/YubikeyManager_2.png)

![Yubikey key alias per slot and object type](/images/Yubikey_key_alias.png)

## Yubico PIV Tool
The YubiKey supports the Personal Identity Verification (PIV) card interface specified in NIST SP 800-73 document "Cryptographic Algorithms and Key Sizes for PIV". 

PIV enables you to perform RSA or ECC sign/decrypt operations using a private key stored on the smartcard, through common interfaces like PKCS#11.
 
This project contain the library, tools and PKCS#11 module to interact with the hardware functionality.

- Download: https://developers.yubico.com/yubico-piv-tool/Releases/
  - **Note:** Add Yubico PIV Tool path to environment variables
- Documenation: https://developers.yubico.com/yubico-piv-tool/Manuals/yubico-piv-tool.1.html 

Example: Displays the device’s meta data and the slots content
```
yubico-piv-tool -r "Yubico YubiKey OTP+FIDO+CCID 0" -a status
```
![Yubikey PIV Tool](/images/PivTool_Device_meta_data.png)

#  Windows 10 Certutil CLI Tool
The windows Certutil.exe is a command-line program that is installed as part of Certificate Services. Use the following command to display the Yubikey certificates. 

**Note:** 
- Default Yubikey PIN: `0123456`
- Default Yubikey PUK:: `12345678`

```
Certutil -SCInfo
```
![Cert Util](/images/CertUtil_1.png)

![Cert Util](/images/CertUtil_2.png)

# Windows Certification Manager
Insert the Yubikey and run the following command to start the Windows 10 certification manager:

```
Certmgr.msc
```
Try to find you Yubikey certificate.

![Windows Certification Manager](/images/Win_Certmgr.png)

# PKCS#15 and ISO/IEC 7816-15 File Structure
- Interoperability using Standardized and Dynamic file system.
- EF.DIR contains Applications on card indexed by their AID’s.
- Each Application contains predefined and mandatory information
  - EF (TokenInfo)
    - Generic information about the card such as card capabilities, Serial Number, Algorithms, etc.
  - EF (Object Directory File - ODF)
    - Contains pointers to other directory files of a particular PKCS#15 Class
![PKCS#15](/images/PKCS15.png)

# OpenSC – pkcs15-tool

Utility for manipulating PKCS #15 data structures on smart cards and similar security token. 

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

# pkcs11-tool
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

# Yubikey - Signing data with pkcs11-tool and verifying the signature with OpenSSL
## Signing
**Step 1:** Generate some data to be signed ...
```
echo "Hallo World" > data.txt
```
   
**Step 2:** Signing data with pkcs11-tool using Yubikey KEY_ID 02 (Slot 9c)
- **Note:**  Default Yubikey PIN: `0123456`

```
pkcs11-tool --sign -m RSA-SHA256 --id 2 -i data.txt -o data.sig
```

## Verifying 
**Step 1:** Read the certificate with KEY_ID 02 (Slot 9c) in DER format from the Yubikey 
```
pkcs11-tool --read-object --id 02 --type cert --output-file Yubikey5_DigSign_Cert_Slot_9c.crt
```	


**Step 2:** To convert the certificate in DER format to PEM format, use OpenSSL tools:
```
openssl x509 -inform DER -in Yubikey5_DigSign_Cert_Slot_9c.crt -outform PEM > Yubikey5_DigSign_Cert_Slot_9c.pem
```

Print the certificate in text form with OpenSSL

```
openssl x509 -in Yubikey5_DigSign_Cert_Slot_9c.pem -text -noout
```

**Step 3:** To verify the signature with openssl, the public key needs to be extracted from the certificate.
```
openssl x509 -in Yubikey5_DigSign_Cert_Slot_9c.pem -pubkey -noout > Yubikey5_DigSign_PubKey_Slot_9c.pem
```

**Step 4:** Verifying the signature with OpenSSL
```
openssl dgst -sha256 -verify Yubikey5_DigSign_PubKey_Slot_9c.pem -signature data.sig data.txt
```


# Yubikey - Using PIV for SSH through PKCS #11

This is a step-by-step guide on setting up a YubiKey with PIV to work
for public-key authentication with OpenSSH through PKCS#11.

![SSH](/images/SSH.png)

![SSH through PKCS #11](/images/SSH_Console.png)

For more details see https://developers.yubico.com/PIV/Guides/SSH_with_PIV_and_PKCS11.html

![Yubikey key alias per slot and object type](/images/Yubikey_key_alias_ssh.png)

**Note:** Use option ```-r "Yubico YubiKey OTP+FIDO+CCID 0"``` to define a PC/SC reader. 


**Step 1:** Generate a RSA key pair in slot 9
```
yubico-piv-tool -s 9a -a generate -o Yubikey5_SSH_PubKey_Slot_9a.pem
```
**Step 2:** Create a new self-signed certificate for that public key.
The only use for the X.509 certificate is to satisfy PIV/PKCS #11 lib. It needs to be able to extract the public-key from the smartcard, and to do that through the X.509 certificate.
```
yubico-piv-tool -a verify-pin -a selfsign-certificate -s 9a -S "/CN=Yubikey5_SSH_Slot9a/" -i Yubikey5_SSH_PubKey_Slot_9a.pem -o Yubikey5_SSH_Cert.pem
```

**Step 3:** Import self signed certificate
```
yubico-piv-tool -a import-certificate -s 9a -i Yubikey5_SSH_Cert.pem
```

**Step 4:** Export the public key from the PIV Smart Card in the correct format for SSH.
```
ssh-keygen -D "C:\Program Files\Yubico\Yubico PIV Tool\bin\libykcs11.dll" -e > yubico_ssh_key.pub
```

**Step 5:** Copy your public key to your target system (e.g. Raspberry Pi)

**Note:** At the moment, Windows 10’s implementation of the OpenSSH client does not have the ```ssh-copy-id``` command available.
- Linux: ```ssh-copy-id <"USERNAME">@<"IP-ADDRESS">```
- Windows: see below:
```
type yubico_ssh_key.pub | ssh pi@10.0.0.1 -p 22 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

Authenticate to the target system using the Yubikey through PKCS11#:
```
ssh -I "C:\Program Files\Yubico\Yubico PIV Tool\bin\libykcs11.dll" pi@10.0.0.1 -p 22
```
# Digitally Sign a Microsoft Word Document using a Smart Card
Please see:  https://playbooks.idmanagement.gov/playbooks/signword/ 