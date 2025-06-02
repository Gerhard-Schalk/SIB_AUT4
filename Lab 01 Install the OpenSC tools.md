# OpenSC-tool
OpenSC provides a set of libraries and utilities to work with Smartcards. 
OpenSC implements the standard APIs to Smartcards e.g.
PKCS#11 API, Windows’ SmartCard Minidriver and macOS CryptoTokenKit.

- Download and Wiki: https://github.com/OpenSC/OpenSC/wiki
- Documentation: https://www.mankier.com/package/opensc
- Source Code Download: https://github.com/OpenSC/OpenSC
  
  **Note:** Add OpenSC Tool path to environment variables

  ![Add OpenSC Tool path to environment variables](/images/OpenSC_Install_Add_Env_Var.png)
 

### Basic examples
```
opensc-tool --list-readers
```
```
opensc-tool --reader 0 --list-algorithms
```
**Note**: Use the reader number returned by ```opensc-tool --list-readers```.
```
opensc-tool --reader 0 --atr -v
```
Use the following link to parse your ATR:  https://smartcard-atr.apdu.fr/ 
```
opensc-tool --reader 0 --name
```
