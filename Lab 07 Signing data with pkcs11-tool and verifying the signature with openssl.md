# Yubikey - Signing data with pkcs11-tool and verifying the signature with OpenSSL
## Signing
**Step 1:** Generate some data to be signed ...
```
echo "Hallo World" > data.txt
```
   
**Step 2:** Signing data with pkcs11-tool using Yubikey KEY_ID 02 (Slot 9c)
- **Note:**  Default Yubikey PIN: `123456`

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


