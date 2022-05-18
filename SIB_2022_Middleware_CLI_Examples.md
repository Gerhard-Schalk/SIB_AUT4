#	opensc-tool

Documentation: https://www.mankier.com/package/opensc 
##Basic examples
```
opensc-tool --list-readers
opensc-tool --reader 0 -atr -v
opensc-tool --reader 0 --name
pkcs15-tool --reader 0 --dump
pkcs15-tool --reader 0 --list-keys
pkcs15-tool --reader 0 --list-public-keys
pkcs15-tool --reader 0 --read-public-key 02
pkcs15-tool --reader 0 --read-certificate 02
```

#  Windows 10 Certutil CLI Tool
##Certutil Example
```
Certutil -SCInfo
```

##Windows 10 Certification Manager
Insert the Yubikey and run the Windows 10 certification manager

```
Certmgr.msc
```

# pkcs11-tool / Open SSL
Docu: https://www.mankier.com/1/pkcs11-tool
##Basic examples
```
pkcs11-tool --module "C:\Program Files\Yubico\Yubico PIV Tool\bin\libykcs11.dll" --list-slots

pkcs11-tool --module "C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll" --list-slots
pkcs11-tool --list-slots
pkcs11-tool --list-mechanisms
pkcs11-tool --list-objects
```
##Examples
SET PKCS11_DLL = C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll
echo "Hallo World" > data.txt
pkcs11-tool --module "C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll" --sign -m RSA-SHA256 --id 2 -i data.txt -o data.sig


pkcs11-tool --module "C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll" --sign -m RSA-SHA256 --id 4 -i jcop_data.txt -o jcop_data.sig

pkcs11-tool --module "C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll" --sign -m RSA-SHA256 --id 4 -i jcop_data.txt -o jcop_data.sig
pkcs11-tool --module "C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll" --sign -m RSA-SHA256 --id 4 --pin "123456" -i jcop_data.txt -o jcop_data.sig
openssl dgst -sha256 -verify pubkey-9e.pem -signature jcop_data.sig jcop_data.txt

========================
	yubico-piv-tool
========================
set pcsc_reader=Identive CLOUD 4700 F Contactless Reader 1
yubico-piv-tool -r "%pcsc_reader%" -a generate -s 9e > pubkey-9e.pem
yubico-piv-tool -r %pcsc_reader% -a selfsign-certificate -s 9e -S "/CN=JC PIV Applet Demo" < pubkey-9e.pem > cert-9e.pem
yubico-piv-tool -r %pcsc_reader% -a import-certificate -s 9e < cert-9e.pem
yubico-piv-tool -r %pcsc_reader% -a status


========================
   SSH Example
========================
opensc-tool --list-readers
yubico-piv-tool -r "Identive CLOUD 4700 F Contact Reader 0" -s 9a -a generate -o public.pem
yubico-piv-tool -r "Identive CLOUD 4700 F Contact Reader 0" -a verify-pin -a selfsign-certificate -s 9a -S "/CN=SSH key/" -i public.pem -o cert.pem
yubico-piv-tool -r "Identive CLOUD 4700 F Contact Reader 0" -a import-certificate -s 9a -i cert.pem
ssh-keygen -D "C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll" -e > ssh_key.pub
type ssh_key.pub | ssh pi@xx.xx.xx.xx -p xxxx "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
ssh -I "C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll" pi@xx.xx.xx.xx -p xxxx

