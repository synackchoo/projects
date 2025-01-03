import os
import time

def is_palindrome(word: str) -> bool:
    normalized_word = ''.join(word.lower().split())
    return normalized_word == normalized_word[::-1]

def main() -> bool:
    os.system('cls' if os.name == 'nt' else 'clear')
    word = input("Enter a word to check if it's a palindrome: ")
    if is_palindrome(word):
        print(f"'{word}' is a palindrome.")
    else:
        print(f"'{word}' is not a palindrome.")

    input("Press Enter to continue...")

    another = input("Would you like to check another word? (yes/no): ")
    if another == 'no':
        print("Goodbye!")
        time.sleep(2) #Sleep for 2 seconds
    return another == 'yes'
   

if __name__ == '__main__':
    while main():
        pass