import random
import string
import sys
import argparse
from enum import Enum
from typing import List, Optional
class PasswordStrength(Enum):
    VERY_WEAK = 0
    WEAK = 1
    MEDIUM = 2
    STRONG = 3
    VERY_STRONG = 4
class PasswordGenerator:
    def __init__(self):
        self.length = 12
        self.include_uppercase = True
        self.include_lowercase = True
        self.include_numbers = True
        self.include_symbols = True
        self.min_length = 6
        self.max_length = 32
    def generate_password(self) -> str:
        """Generate a random password based on current settings"""
        charset = ''
        if self.include_uppercase:
            charset += string.ascii_uppercase
        if self.include_lowercase:
            charset += string.ascii_lowercase
        if self.include_numbers:
            charset += string.digits
        if self.include_symbols:
            charset += string.punctuation
        if not charset:
            raise ValueError("At least one character type must be selected")
        return ''.join(random.SystemRandom().choice(charset) for _ in range(self.length))
    def assess_strength(self, password: str) -> PasswordStrength:
        """Assess the strength of a generated password"""
        strength = 0
        if len(password) >= 12:
            strength += 1
        if len(password) >= 16:
            strength += 1
        if any(c.isupper() for c in password):
            strength += 1
        if any(c.islower() for c in password):
            strength += 1
        if any(c.isdigit() for c in password):
            strength += 1
        if any(c in string.punctuation for c in password):
            strength += 1
        return PasswordStrength(min(strength, 4))
    def print_strength_meter(self, strength: PasswordStrength) -> None:
        """Display a visual strength meter"""
        colors = {
            0: '\033[91m',  
            1: '\033[93m',  
            2: '\033[33m',  
            3: '\033[92m',  
            4: '\033[92m',  
        }
        strength_text = {
            0: "Very Weak",
            1: "Weak",
            2: "Medium",
            3: "Strong",
            4: "Very Strong"
        }
        print("\nPassword Strength:")
        meter = "[" + "█" * (strength.value + 1) + " " * (4 - strength.value) + "]"
        print(f"{colors[strength.value]}{meter} {strength_text[strength.value]}\033[0m")
    def display_help(self) -> None:
        """Display usage instructions"""
        print("\nSecurePass - Professional Password Generator")
        print("=" * 45)
        print("\nUsage:")
        print("  securepass [options]")
        print("\nOptions:")
        print("  -l, --length LENGTH    Password length (6-32, default: 12)")
        print("  --no-upper             Exclude uppercase letters")
        print("  --no-lower             Exclude lowercase letters")
        print("  --no-numbers           Exclude numbers")
        print("  --no-symbols           Exclude symbols")
        print("  -h, --help             Show this help message")
        print("\nExample:")
        print("  securepass -l 16 --no-symbols")
    def run(self, args: Optional[List[str]] = None) -> None:
        """Run the password generator with command line arguments"""
        parser = argparse.ArgumentParser(description='Generate secure passwords', add_help=False)
        parser.add_argument('-l', '--length', type=int, default=12, 
                          help='Password length (6-32)')
        parser.add_argument('--no-upper', action='store_false', dest='include_uppercase',
                          help='Exclude uppercase letters')
        parser.add_argument('--no-lower', action='store_false', dest='include_lowercase',
                          help='Exclude lowercase letters')
        parser.add_argument('--no-numbers', action='store_false', dest='include_numbers',
                          help='Exclude numbers')
        parser.add_argument('--no-symbols', action='store_false', dest='include_symbols',
                          help='Exclude symbols')
        parser.add_argument('-h', '--help', action='store_true', 
                          help='Show help message')
        try:
            args = parser.parse_args(args)
            if args.help:
                self.display_help()
                return
            if not (self.min_length <= args.length <= self.max_length):
                print(f"Error: Password length must be between {self.min_length} and {self.max_length}")
                sys.exit(1)
            self.length = args.length
            self.include_uppercase = args.include_uppercase
            self.include_lowercase = args.include_lowercase
            self.include_numbers = args.include_numbers
            self.include_symbols = args.include_symbols
            password = self.generate_password()
            strength = self.assess_strength(password)
            print("\n\033[1mGenerated Password:\033[0m")
            print(f"\033[36m{password}\033[0m")  
            self.print_strength_meter(strength)
            print("\nSettings used:")
            print(f"  Length: {self.length}")
            print(f"  Character types: {'Uppercase' if self.include_uppercase else ''} "
                  f"{'Lowercase' if self.include_lowercase else ''} "
                  f"{'Numbers' if self.include_numbers else ''} "
                  f"{'Symbols' if self.include_symbols else ''}".strip())
            print("\nTip: For maximum security, use passwords with at least 12 characters including all character types.")
        except Exception as e:
            print(f"\nError: {str(e)}")
            self.display_help()
            sys.exit(1)
if __name__ == "__main__":
    generator = PasswordGenerator()
    generator.run()
