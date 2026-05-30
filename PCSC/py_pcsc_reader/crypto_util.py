#
#  Copyright (c) 2022-2024, Gerhard H. Schalk
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from enum import Enum
from .print_bytes_util import printColor, printlnColor, printBytes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding, serialization, cmac
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
from cryptography.hazmat.primitives.ciphers.aead import AESCCM


class CryptoUtil:
    @staticmethod
    def AES_CBC_Encrypt(key: bytes, data: bytes, iv=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') -> bytes:
        """
        Encrypts data using AES in CBC mode.
        
        Args:
            key: The encryption key (must be 16, 24, or 32 bytes for AES-128, AES-192, or AES-256)
            data: The plaintext data to encrypt
            iv: The initialization vector (default: 16 zero bytes)
        
        Returns:
            The encrypted ciphertext as bytes
        """
        aesCipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        aesEncryptor = aesCipher.encryptor()
        cipherText = aesEncryptor.update(data) 
        return cipherText
    
    @staticmethod
    def AES_CBC_Decrypt(key: bytes, data: bytes, iv=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') -> bytes:
        """
        Decrypts data using AES in CBC mode.
        
        Args:
            key: The decryption key (must be 16, 24, or 32 bytes for AES-128, AES-192, or AES-256)
            data: The ciphertext data to decrypt
            iv: The initialization vector (default: 16 zero bytes)
        
        Returns:
            The decrypted plaintext as bytes
        """
        aesCipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        aesDecrypto = aesCipher.decryptor()
        plainText = aesDecrypto.update(data) 
        return plainText

    @staticmethod
    def AES_CMAC(key: bytes, data: bytes) -> bytes:
        """
        Generates an AES-CMAC (Cipher-based Message Authentication Code) for the given data.
        
        Args:
            key: The secret key for CMAC generation (must be 16, 24, or 32 bytes for AES-128, AES-192, or AES-256)
            data: The data to authenticate
        
        Returns:
            The CMAC tag as bytes
        """
        c = cmac.CMAC(algorithms.AES(key))
        c.update(bytes(data))
        return c.finalize()

    @staticmethod
    def AES_CCM_Encrypt(key: bytes, Nonce: bytes, data: bytes) -> bytes:
        """
        Encrypts data using AES in CCM mode (Counter with CBC-MAC).
        
        Args:
            key: The encryption key (must be 16, 24, or 32 bytes for AES-128, AES-192, or AES-256)
            Nonce: The nonce value for CCM mode
            data: The plaintext data to encrypt
        
        Returns:
            The encrypted ciphertext with authentication tag as bytes
        """
        aesccm = AESCCM(key, tag_length=8)
        cipherText = aesccm.encrypt(Nonce, data, None)
        return cipherText

    @staticmethod
    def AES_CCM_Decrypt( key: bytes, Nonce: bytes, data: bytes) -> bytes:
        """
        Decrypts data using AES in CCM mode (Counter with CBC-MAC).
            
        Args:
            key: The decryption key (must be 16, 24, or 32 bytes for AES-128, AES-192, or AES-256)
            Nonce: The nonce value for CCM mode
            data: The ciphertext data with authentication tag to decrypt
        
        Returns:
            The decrypted plaintext as bytes
        """
        aesccm = AESCCM(key, tag_length=8)
        plainText = aesccm.decrypt(Nonce, data, None)
        return plainText
    
    @staticmethod
    def SHA256(data:bytes) -> bytes:
        """
        Computes the SHA-256 hash of the given data.
        
        Args:
            data: The data to hash
        
        Returns:
            The SHA-256 hash digest as bytes
        """
        digest = hashes.Hash( hashes.SHA256() )
        digest.update(data)
        return digest.finalize()