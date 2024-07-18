import itertools
import tempfile
import pyzipper
import rarfile


def extract_zipfile(file_path, password, output_path=None):
    try:
        with pyzipper.AESZipFile(file_path, compression=pyzipper.ZIP_LZMA) as zf:
            zf.setpassword(str(password).encode())
            zf.extractall(output_path)
        return True
    except RuntimeError:
        pass

    return False


def extract_rarfile(file_path, password, output_path=None):
    try:
        with rarfile.RarFile(file_path) as rf:
            rf.setpassword(str(password).encode())
            rf.extractall(output_path)
        return True
    except rarfile.BadRarFile:
        pass

    return False


def bruteforce_start(file_path, password_set, password_length, extract_method, output_path=None):
    for length in range(1, password_length+1):
        passwords = itertools.product(password_set, repeat=length)
        for password in passwords:
            password = "".join(password)
            if extract_method(
                    file_path, output_path=output_path, password=password):
                return password


def bruteforce(file_path, password_set, password_length, output_path=None):

    with tempfile.TemporaryDirectory() as output_folder:
        if not output_path:
            output_path = output_folder

        if file_path.endswith(".zip"):
            return bruteforce_start(file_path, password_set, password_length, extract_method=extract_zipfile, output_path=output_path)
        elif file_path.endswith(".rar"):
            return bruteforce_start(file_path, password_set, password_length, extract_method=extract_rarfile, output_path=output_path)


def dictionary_attack(file_path, password_file, output_path=None):

    with tempfile.TemporaryDirectory() as output_folder:
        if not output_path:
            output_path = output_folder
        print(file_path)

        if file_path.endswith(".zip"):
            return dictionary_attack_start(file_path, password_file, output_path, extract_zipfile)
        elif file_path.endswith(".rar"):
            return dictionary_attack_start(file_path, password_file, output_path, extract_rarfile)


def dictionary_attack_start(file_path, password_file, output_path, extract_method):

    with open(password_file, 'r') as file:
        passwords = file.readlines()

        for password in passwords:
            if extract_method(file_path, password=password.removesuffix("\n"), output_path=output_path):
                return password
