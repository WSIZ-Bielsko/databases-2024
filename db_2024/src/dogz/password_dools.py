from argon2 import PasswordHasher

if __name__ == '__main__':
    ph = PasswordHasher()
    my_password = '1234'
    my_hash = ph.hash(my_password)

    checked_password = '1234__'

    ph.verify(my_hash, checked_password)  # raises argon2.exceptions.VerifyMismatchError on error
