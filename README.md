# AES256 Cipher and Decipher Script only using Bitarray Library

Welcome to our AES256 Cipher and Decipher Python project! 🚀

## Overview

This project aims to provide a slick and efficient implementation of the Advanced Encryption Standard (AES) with a key size of 256 bits. The encryption and decryption processes are achieved using the powerful Bitarray library, making the code not only secure but also fast.

## Features

- **AES256 Encryption:** Protect your string data with state-of-the-art encryption technology.
- **Bitarray Library:** Leverage the Bitarray library for efficient bitwise operations.
- **Supports any length:** Cypher from one character to the limit of python arrays.
- **Cool Factor:** It's not cool as hell, but, well, we have the spirit at least.

## Requirements

Make sure you have the Bitarray library installed. If not, you can install it using:

```bash
pip install bitarray
```

It is made with Poetry manager, so you can also use:

```bash
# Installs all dependencies added to the project
poetry install
```
## Usage

### 1. Clone the Repository

```bash
git clone https://github.com/andrwgm/AES-Protocolos.git
cd AES-Protocolos
```

### 2. Run the Script

Use the following commands to run the script and access to the CLI menu:

#### Execution

```bash
python aes256.py
```

Follow the prompts to enter the plain text you want to encrypt and the encryption key or the hex text to be decrypted with an encryption key.

(Yep, we know, the menu is in Spanish, idk, take Duolingo lessons and try to understand it)

## Example

>Key: 000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
>
>Message: Hello world! I'm using this cypher!

---
MsgEncrypted: 

> Hex: 6ba67a86317f67ae1d3fc31f34a43ab0a78221d723de03c364a9544fdbf04f107fa2f116e74fb46e4165585b1433d6ab

---
MsgDecrypted:

>Ascii:  Hello world! I'm using this cypher!



## Contribution

If you find a bug or have a suggestion, feel free to open an issue or create a pull request. Contributions are always welcome!



## Acknowledgments

Enjoy securing your data with this AES256 Cipher and Decipher script! 🔐✨