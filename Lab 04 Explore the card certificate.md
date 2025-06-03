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
