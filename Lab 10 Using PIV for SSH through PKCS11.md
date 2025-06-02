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

Print the certificate in text form with OpenSSL

```
openssl x509 -in Yubikey5_SSH_Cert.pem -text -noout
```


**Step 3:** Import self signed certificate
```
yubico-piv-tool -a import-certificate -s 9a -i Yubikey5_SSH_Cert.pem
```

**Step 4:** Export the public key from the PIV Smartcard in the correct format for SSH.
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