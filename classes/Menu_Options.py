import os
from classes.Encrypt_Decrypt import CaesarCipher, CaesarCipherMessage, CaesarCipherFiles
from classes.Letter_Dist import LetterFrequencyDistribution
from classes.Infer_Cipher import breakCaesarCipher


class MenuOptions:
    def __init__(self):

        # dictionary storing options from 1 - 8
        self.menu_options = {
            1: 'Encrypt/Decrypt Message',
            2: 'Encrypt/Decrypt File',
            3: 'Analyze letter frequency distribution',
            4: 'Infer Caesar cipher key from file',
            5: 'Analyze and sort encrypted files',
            6: 'Extra Option One',
            7: 'Extra Option Two',
            8: 'Exit'
        }
    # prevents users from just pressing "Enter" for certain inputs

    def get_non_empty_input(self, prompt):
        user_input = input(prompt)
        while not user_input.strip():  # Check if the input is empty or contains only whitespace
            print("Input cannot be empty. Please try again.")
            user_input = input(prompt)
        return user_input

    def start(self):
        # print essential introduction
        print('\n***********************************************************************')
        print('* ST1507 DSAA: Welcome To:                                            *')
        print('*                                                                     *')
        print('*  ~ Caesar Cipher Encrypted Message Analyzer ~                       *')
        print('*---------------------------------------------------------------------*')
        print('*                                                                     *')
        print('*  - Done By: Wilfred Djumin (2237503)                                *')
        print('*  - Class DAAA/FT/2B/05                                              *')
        print('*********************************************************************** \n')
        # Prompt user to press "Enter" key
        starting_input = input("Press Enter to continue...")
        # Prompt user to press "Enter" key

    def print_menu(self):
        print("\nPlease select your choice: (1,2,3,4,5,6,7,8)")
        # Looping through dictionary to list options to user
        for choice, description in self.menu_options.items():
            print(f"\t {choice}. {description}")

    def get_choice(self):

        # reference: https://python-course.eu/python-tutorial/errors-and-exception-handling.php

        while True:

            try:

                # Prompt user for choice
                choice = int(input("Enter your choice: "))

                # Check if the choice exist in the menu_options dictionary
                if choice in self.menu_options:

                    # Ask user for confirmation
                    confirm_choice = input(
                        f'You chose option {choice}: {self.menu_options.get(choice)}. Confirm? (y/n): ').lower()

                    if confirm_choice == 'y':
                        # Return the inputted choice if confirmed
                        return choice
                    elif confirm_choice == 'n':
                        print('Operation canceled. Please choose again.\n')
                    else:
                        print(
                            'Invalid confirmation. Please enter "y" for yes or "n" for no.\n')

                # If not, prompt user to re-enter a number between 1 and 8
                else:
                    print("Invalid choice. Please enter a number between 1 and 8.\n")

            # raise ValueError if user does not input a number/integer
            except ValueError:
                print("Invalid input. Please enter a valid number.\n")

    # method/function that filters what function(s) to run based on user input
    def handle_choice(self, choice):
        if choice == 1:
            self.handle_encryption_decryption('message')
        elif choice == 2:
            self.handle_encryption_decryption('file')
        elif choice == 3:
            self.analyze_letter_frequency()
        elif choice == 4:
            self.break_caesar_cipher()
        elif choice == 5:
            self.analyze_encrypted_files()
        elif choice == 6:
            self.extra_option_one()
        elif choice == 7:
            self.extra_option_two()
        elif choice == 8:
            # Execute a clean exit if user presses 8
            print(
                "Bye, thanks for using ST1507 DSAA: Caesar Cipher Encrypted Message Analyzer")
            exit(0)

    # Methods related to Caesar Cipher For Messages and Files options 1 and 2 as well as other classes
    ##
    def get_valid_cipherkey(self):
        while True:
            try:
                cipherkey = int(input("\nEnter the cipher key: "))
                return cipherkey
            except ValueError:
                print("Please enter a valid number.")

    def get_action_input(self):
        action = ''
        while action != "e" and action != 'd':
            action = input(
                '\nEnter "E" for Encrypt or "D" for Decrypt: ').lower()
            if action != "e" and action != 'd':
                print("Only enter either 'E' or 'D'")
        return action

    def get_file_path(self, file_name):
        file_path = os.path.join(os.path.dirname(__file__), "..", "Dataset")

        # Get the list of files in the directory
        files_in_directory = [f for f in os.listdir(file_path)]

        # Check if the exact file name is in the list
        if file_name in files_in_directory:
            return os.path.join(file_path, file_name)
        else:
            print(f"File {file_name} not found.")
            return None

    def create_output_file(self, output_filename):
        # Ensure the "Dataset" directory exists
        dataset_dir = os.path.join(os.path.dirname(__file__), "..", "Dataset")
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)

        # Normalize the output filename to handle invalid characters
        normalized_output_filename = os.path.normpath(output_filename)

        # Split the normalized output_filename into directory and file name components
        output_dir, output_file = os.path.split(normalized_output_filename)

        # Create the full path for the output file in the "Dataset" directory
        return os.path.join(dataset_dir, output_file)

    def get_cipher_instance(self, cipherkey):
        return CaesarCipherMessage(cipherkey)

    def encrypt_file(self, cipherkey, input_path, output_file):
        cipher = CaesarCipherFiles(cipherkey, input_path)
        output_file_path = self.create_output_file(output_file)
        cipher.encrypt(input_path, output_file_path)

    def decrypt_file(self, cipherkey, input_path, output_file):
        cipher = CaesarCipherFiles(cipherkey, input_path)
        output_file_path = self.create_output_file(output_file)
        cipher.decrypt(input_path, output_file_path)

    # Main Handle Encryption Function when user select 1 and 2 option
    def handle_encryption_decryption(self, input_type):  # 1 & 2

        while True:
            action = self.get_action_input()

            if action == "e":
                plaintext = self.get_non_empty_input(
                    f"\nPlease type {input_type} you want to encrypt: ")

                if input_type == 'file':
                    input_path = self.get_file_path(plaintext)
                    if input_path == None:
                        break

                    else:
                        cipherkey = self.get_valid_cipherkey()
                        output_file = self.get_non_empty_input(
                            "\nPlease enter an output file: ")
                        self.encrypt_file(cipherkey, input_path, output_file)
                else:
                    cipherkey = self.get_valid_cipherkey()
                    cipher = self.get_cipher_instance(cipherkey)
                    print(cipher.encrypt(plaintext))
                break

            elif action == 'd':
                ciphertext = self.get_non_empty_input(
                    f"\nPlease type {input_type} you want to decrypt: ")

                if input_type == 'file':
                    input_path = self.get_file_path(ciphertext)
                    if input_path == None:
                        break
                    else:
                        cipherkey = self.get_valid_cipherkey()
                        output_file = self.get_non_empty_input(
                            "\nPlease enter an output file: ")
                        self.decrypt_file(cipherkey, input_path, output_file)
                else:
                    cipherkey = self.get_valid_cipherkey()
                    cipher = self.get_cipher_instance(cipherkey)
                    print(cipher.decrypt(ciphertext))
                break

    def analyze_letter_frequency(self):  # 3
        while True:
            # Instantiate the LetterFrequencyDistribution class and prompt user for file
            letter_dist_input = input(
                "Please enter the file you want to analyze: ")

            # Check file path if it exists
            file_path = self.get_file_path(letter_dist_input)
            # Return to menu options if file dont exist
            if file_path == None:
                break
            # Continue with analyzing
            else:
                letter_dist = LetterFrequencyDistribution(file_path)
                # Call the analyze_file method here if needed
                letter_dist.analyze_file()
                # Call other methods or operations as needed
                input("\nPress enter key, to continue.....")

            break

    def break_caesar_cipher(self):  # 4

        while True:

            # Input file handling
            input_file_analyze = input(
                "\nPlease enter the file you want to analyze: ")

            input_file_path = self.get_file_path(input_file_analyze)

            if input_file_path == None:
                break

            cipher_breaker = breakCaesarCipher(input_file_path)

            input_reference_file = input(
                "\nPlease enter the reference frequencies file: ")

            file_path_ref = self.get_file_path(input_reference_file)

            if file_path_ref == None:
                break

            cipher_breaker.reference_file_analysis(file_path_ref)

            # Calculate Cipher Key

            cipher_key = cipher_breaker.calculate_cipher_key()

            print(f"The inferred caesar cipher key is: {cipher_key}")

            # Prompt whether user wants to decrypt
            prompt_for_decryption = input(
                "\nWould you want to decrypt this file using the key? y/n: ")

            # Return user to menu options if selected 'n'
            if prompt_for_decryption.lower() != 'y' and prompt_for_decryption.lower() == 'n':
                print(
                    f"Selected '{prompt_for_decryption}', back to menu options...")
                break
            else:
                cipherkey = cipher_key
                output_file = self.get_non_empty_input(
                    "\nPlease enter an output file: ")
                self.decrypt_file(cipherkey, input_file_path, output_file)
            break
