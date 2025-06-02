## Yubico PIV Tool
The YubiKey supports the Personal Identity Verification (PIV) card interface specified in NIST SP 800-73 document "Cryptographic Algorithms and Key Sizes for PIV". 

PIV enables you to perform RSA or ECC sign/decrypt operations using a private key stored on the smartcard, through common interfaces like PKCS#11.
 
This project contain the library, tools and PKCS#11 module to interact with the hardware functionality.

- Download: https://developers.yubico.com/yubico-piv-tool/Releases/
- Documenation: https://developers.yubico.com/yubico-piv-tool/Manuals/yubico-piv-tool.1.html 

  **Note:** Add Yubico PIV Tool path to environment variables


  ![Add Yubico PIV Tool path to environment variables](/images/YubicoPivTool_Install_Add_Env_Var.png)

Example: Displays the device’s meta data and the slots content
```
yubico-piv-tool -r "Yubico YubiKey OTP+FIDO+CCID 0" -a status
```
![Yubikey PIV Tool](/images/PivTool_Device_meta_data.png)

