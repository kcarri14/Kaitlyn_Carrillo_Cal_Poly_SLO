import os
import json 
import unittest


# Setup and File Exploration

def get_file_paths(directory):    #gets file path from my personal directory in order to use files
    filepaths = []               #creates a new list for the files to be stored in 
    for root,dirs, files, in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):    #looks for files that have an ending with .txt
                filepath = os.path.join(root,file) 
                filepaths.append(filepath)  # adds the file to filepaths list

    return filepaths
    


#Decryption Functions
def decrypt_file(file_path, key):  #decrypts the file
    decrypted_string = ''   #empty string to store the decrypted strings in the file
    with open(file_path,'r') as file:   # opens the the file in reading mode
        for char in file.read():
            ascii = ord(char)            #assigns ascii as ord(char) which gets the ASCII value of the char
            decrypted = (ascii - key) % 128  #takes the ascii char and subtracts the key which is in the range(128) and divides it by 128 since there are 127 ASCII values
            converted_to_char = chr(decrypted) #chr(value) gets the character for the given ASCII value
            decrypted_string += converted_to_char #and then it adds the characters in the empty string
    return decrypted_string

 # Data Parsing and Validation
def parse_decrypted_data(data):  
    new_data = json.loads(data)   #parses the data that we got from the files
    return new_data




# Security Analysis Functions
def is_password_strong(password):  #checks to see if the passwords are strong
    if len(password) < 8:  #checks if the length is less than 8
        return False        #if it is, it will return false
    if  password.isupper() == True or password.islower() == True: #checks if password is all upper case or all lower case
        return False                                              #if it is, it will return false
 #checks if the password has any special characters    
    special = 0 
    for char in password: 
        if not char.isalnum(): # if it doesn't it adds 1 to the counter
            special += 1
    if special == 0: #if the counter is equal to 0 then it returns false
        return False

    return True  #if it passes all the tests, then the password is good
        
 
# Re-Encryption 
def encrypt_data(data, encryption_key): 
    encrypt_key = 0
    for char in encryption_key:
        encrypt_key += ord(char)

    encrypted_string = ' '     #empty string to store the decrypted strings in the file
    for char in data:
        ascii = ord(char)     #assigns ascii as ord(char) which gets the ASCII value of the char
        encrypted = (ascii - encrypt_key) % 128  #takes the ascii char and subtracts the key which is in the range(128) and divides it by 128 since there are 127 ASCII values
        encrypted_data = ord(encrypted)  #ord(char) which gets the ASCII value of the char
        encrypted_string += encrypted_data #and then it adds the ASCII character in the empty string
    return encrypted_string

def write_encrypted_data(data, file_path):  #writes the encrypted data back into the files
    if os.path.isopen(file_path):  
        with open(file_path, 'w') as file:
            file.write(data)

# Statistical Analysis
def calculate_statistics(data):
    total_number_account = len(data)  #finds the total number of accounts
 #bad passwords   
    password_count = 0
    for account in data:                    #for accounts in the data set, it checks if there is a bad password
        password = account['Password']
        bad_password = is_password_strong(password)
        if bad_password == False:             #if there is a bad password, it will add 1 to the password counter
            password_count += 1
    percent = password_count / total_number_account   # takes the total number of bad passwords and divde it by the total number of accounts
    print(f"The total number of bad passwords are: {password_count}")
    print(f"The percentage of bad passwords are {percent}")
#missing data
    count = 0
    for account1 in data:                   #for accounts in the data set, it checks if there is a bad password
            if "N/A" in account1.values():  #if there is an empty value, it will add it to the counter
                count += 1

    missing_data_percent = count / total_number_account  #takes the total number of missing data and divides it by the total number of accounts
    print(f"The number of accounts with missing data is {count}")
    print(f"The percentage of accounts with missing data is {missing_data_percent}")

# Report Generation
def generate_report(statistics):   
    total_number_of_accounts = len(statistics)
    print("-------------------------------------------------------------")
    print("Final Report:")
    print(" ")
    print(f"The total number of accounts is: {total_number_of_accounts}")
    pass

# Main Function
def main():
    directory_path = '/Users/kaitlyncarrillo/Downloads/Project 4 Data'   #assigns the directory with the files needed
    file_paths = get_file_paths(directory_path)  #retrieves the files that are needed
    for file_path in file_paths:    #for each file, decrypted the content
        for key in range(128):
            decrypted_content = decrypt_file(file_path, key)
            if "Password" in decrypted_content:           #if data has been decrypted, parse the data
                parsed_data = parse_decrypted_data(decrypted_content)
                
    # Generate report
    generate_report(parsed_data)   
    calculate_statistics(parsed_data)

main()  

#TESTING
class TestProject(unittest.TestCase):

    def test_get_file_paths(self):
        test_dir = '/Users/kaitlyncarrillo/Downloads/Project 4 Data'
        expected_file_paths = [ '/Users/kaitlyncarrillo/Downloads/Project 4 Data/keywords.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/West Bank/748_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/West Bank/678_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/West Bank/519_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/West Bank/555_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/West Bank/797_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/West Bank/565_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/South Bank/848_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/South Bank/948_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/South Bank/909_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/South Bank/321_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/South Bank/893_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/East Bank/333_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/East Bank/354_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/East Bank/414_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/East Bank/491_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/East Bank/475_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/East Bank/456_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/North Bank/178_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/North Bank/135_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/North Bank/232_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/North Bank/288_encrypted.txt', 
                               '/Users/kaitlyncarrillo/Downloads/Project 4 Data/North Bank/222_encrypted.txt'

        ]
        self.assertEqual(get_file_paths(test_dir), expected_file_paths)

    def test_is_password_strong(self):
        strong_password = 'MyP@ss0rd'
        weak = 'password'
        self.assertTrue(is_password_strong(strong_password))
        self.assertFalse(is_password_strong(weak))


if __name__ == "__main__":
    unittest.main()
