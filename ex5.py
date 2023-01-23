import os
import json

def get_encrypted_charachter(letter, shift):
    letters_abc = ord('z') - ord('a') + 1
    if letter.isalpha():
        if letter.islower():
            return chr(((ord(letter) - ord('a') + shift) % letters_abc) + ord('a'))
        else:
            return chr(((ord(letter) - ord('A') + shift) % letters_abc) + ord('A'))

    else:
        return letter


class CaeserCipher:
    def __init__(self, k):
        self.key = k

    def encrypt(self, str1):
        tmp_str = ""
        for letter in str1:
            tmp_str += get_encrypted_charachter(letter, self.key)
        return tmp_str

    def decrypt(self, str1):
        tmp_str = ""
        for letter in str1:
            tmp_str += get_encrypted_charachter(letter, -self.key)
        return tmp_str


class VigenereCipher:
    def __init__(self, list1):
        self.shift_list = list1

    def encrypt(self, str1):
        letter_counter = 0
        new_str = ""
        for letter in str1:
            if letter.isalpha():
                new_str += get_encrypted_charachter(letter, letter_counter % self.shift_list.size())
                letter_counter += 1
            else:
                new_str += letter
        return new_str

    def decrypt(self, str1):
        letter_counter = 0
        new_str = ""
        for letter in str1:
            if letter.isalpha():
                new_str += get_encrypted_charachter(letter, -(letter_counter % self.shift_list.size()))
                letter_counter += 1
            else:
                new_str += letter
        return new_str


def getNumberToList(letter):
    if letter.islower():
        return ord(letter)-ord('a')
    else:
        return ord(letter)-ord('A')+26


def getVigenereFromStr(str1):
    list1 = [getNumberToList(letter) for letter in str1 if letter.isalpha()]
    return VigenereCipher(list1)


def processDirectory(dir_path):
    json_file = os.path.join(dir_path ,"config.json")
    if os.path.isfile(json_file):
        with open(json_file, 'r') as f:
            loaded_dict = json.load(f)
    if loaded_dict['type'] == 'Caesar':
        caeser_cipher = CaeserCipher(loaded_dict['key'])
        if loaded_dict['mode'] == 'encrypted':
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                output_file_path = os.path.splitext(file_path)[0]+'.enc'
                if file_path.endswith(".txt"):
                    with open(file_path, 'r') as f:
                        input_str = f.read()
                        with open(output_file_path, 'w') as g:
                            g.write(caeser_cipher.encrypt(input_str))
                            g.close()
        else:
            for file in os.listdir(dir_path):
                if os.path.splitext(file)[1] == '.enc':
                    with open(file, 'r') as f:
                        input_str = f.read()
                        output_file = open(os.path.splitext(f)[0]+'.txt', 'w')
                        output_file.write(caeser_cipher.decrypt(input_str))
                        output_file.close()
    else:
        if isinstance((loaded_dict['key'])[0], int):
            vigenere_cipher = VigenereCipher(loaded_dict['key'])
        else:
            vigenere_cipher = getVigenereFromStr(loaded_dict['key'])
        if loaded_dict['mode'] == 'encrypted':
            for file in os.listdir(dir_path):
                if os.path.splitext(file)[1] == '.txt':
                    with open(file, 'r') as f:
                        input_str = f.read()
                        output_file = open(os.path.splitext(f)[0]+'.enc', 'w')
                        output_file.write(vigenere_cipher.encrypt(input_str))
                        output_file.close()
        else:
            for file in os.listdir(dir_path):
                if os.path.splitext(file)[1] == '.enc':
                    with open(file, 'r') as f:
                        input_str = f.read()
                        output_file = open(os.path.splitext(f)[0]+'.txt', 'w')
                        output_file.write(vigenere_cipher.decrypt(input_str))
                        output_file.close()