
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

Utility for manipulating PKCS #15 data structures on Smartcards and similar security token. 

- Documentation: https://www.mankier.com/1/pkcs15-tool


**Note**: Use the reader number returned by ```opensc-tool --list-readers```.

## Basic examples
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
