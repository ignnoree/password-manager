from cs50 import SQL
import secrets
import string
from cryptography.fernet import Fernet
import os

key='g8V5b3R_j6Jm6htd2ZZzK4t1Oa6b_6fi6eA9M12J3m0='



def generate_password(length):
    
    alphabet = string.ascii_letters  
    digits = string.digits 
    special_chars = "!@_?"
    
   
    all_chars = alphabet + digits + special_chars
    
    password = [
        secrets.choice(string.ascii_uppercase),  
        secrets.choice(digits),                 
        secrets.choice(special_chars)           
    ]
    
    
    password += [secrets.choice(all_chars) for _ in range(length - 3)]
    
    
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)



def encrypt(text):

    fernet = Fernet(key)

    encMessage = fernet.encrypt(text.encode())
    print(encMessage)


    return encMessage

    





def decrypt(encMessage,key):
    
    fernet = Fernet(key)

    decMessage = fernet.decrypt(encMessage).decode()

    return (f"decrypted password : {decMessage}")





def savepass(service_name):
    db = SQL("sqlite:///passwords.db")
    password = generate_password(10)
    hashedpassword=encrypt(password)
    print(f'password = {password}')
    res=input("Do you want to save this password? (y/n): ")
    if res=="y":
        db.execute("INSERT INTO passwords (service_name, hashed_password) VALUES(?, ?)", service_name, hashedpassword)
        print("Password saved successfully")
    else:
        print("Password not saved")
    

def getpass(service_name):
    db = SQL("sqlite:///passwords.db")
    rows = db.execute("SELECT hashed_password FROM passwords WHERE service_name= ?", service_name)[0]
    hashedpassword=rows['hashed_password']
    plainpass=decrypt(hashedpassword,key)
    print(plainpass)
    


if not key:
    print('Key not found')

else:
    while True:
        input1=input("Do you want to save or get password? (s/g): ")
        if input1=="s":
            service_name=input("Enter service name: ")
            savepass(service_name)
        elif input1=="g":    
            service_name=input("Enter service name: ")
            getpass(service_name)







        

        