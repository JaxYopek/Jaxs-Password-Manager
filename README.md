# Jax's Password Manager

## Overview
Jax's Password Manager is a simple password management application built with Python, SQLite, PyQt, and the cryptography library. It allows you to securely store, delete, and retrieve passwords for different websites. 

## Getting Started
### Prerequisites
- Python 3.x
- PyQt5
- cryptography library
  
### Installation
1. **Clone the repository**
```
git clone https://github.com/JaxYopek/Jaxs-Password-Manager
cd Jaxs-Password-Manager
```
2. **Install the required packages**
```
pip install PyQt5 cryptography
```

### Usage

1. **Run the application:**
```
python main.py
```

2. **Set Master Password:**
   - The first time you run the application, you will be prompted to set a master password. This password will be used to protect your stored passwords.
  
3. **Add a Password:**
   - Enter the wesbite, username, and password you want to store.
   - Click the "Add Password" button to save the password.

4. **Retrieve a Password:**
   - Enter the website and username for which you want to retreive the password
   - Click on the "Get Password" button to display the password

5. **Delete a Password:**
   - Enter the website and username of the password you want to delete.
   - Click on the trash can to delete the password.
  
## Contributing
Feel free to submit issues or pull requests to improve the application. Any feedback is appreciated.

## License
Distributed under the MIT License. See LICENSE.md for more information.

## Acknowledgments 
[The Python Code: How to Build a Password Manager in Python](https://thepythoncode.com/article/build-a-password-manager-in-python)
