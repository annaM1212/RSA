import random
import math
import tkinter as tk
from tkinter import messagebox


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1


def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def generate_prime():
    while True:
        num = random.randint(100, 999) 
        if is_prime(num):
            return num


def generate_keys():
    p = generate_prime()
    q = generate_prime()

    while p == q:
        q = generate_prime()

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = random.randint(2, phi_n - 1)
    while gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)

    d = mod_inverse(e, phi_n)

    return ((e, n), (d, n))


def encrypt(text, public_key):
    e, n = public_key
    encrypted = [pow(ord(char), e, n) for char in text]
    return encrypted


def decrypt(encrypted, private_key):
    d, n = private_key
    decrypted = ''.join([chr(pow(char, d, n)) for char in encrypted])
    return decrypted


class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Шифрование и Расшифровка")

        self.public_key, self.private_key = generate_keys()

        self.label = tk.Label(root, text="Введите текст для шифрования:")
        self.label.pack()

        self.text_input = tk.Text(root, height=5, width=50)
        self.text_input.pack()

        self.encrypt_button = tk.Button(root, text="Зашифровать", command=self.encrypt_text)
        self.encrypt_button.pack()

        self.encrypted_label = tk.Label(root, text="Зашифрованный текст:")
        self.encrypted_label.pack()

        self.encrypted_output = tk.Label(root, text="")
        self.encrypted_output.pack()

        self.decrypt_button = tk.Button(root, text="Расшифровать", command=self.decrypt_text)
        self.decrypt_button.pack()

        self.decrypted_label = tk.Label(root, text="Расшифрованный текст:")
        self.decrypted_label.pack()

        self.decrypted_output = tk.Label(root, text="")
        self.decrypted_output.pack()

    def encrypt_text(self):
        text = self.text_input.get("1.0", "end-1c")
        if text.strip() == "":
            messagebox.showerror("Ошибка", "Введите текст для шифрования.")
            return
        encrypted = encrypt(text, self.public_key)
        self.encrypted_output.config(text=str(encrypted))

    def decrypt_text(self):
        encrypted_text = self.encrypted_output.cget("text")
        if not encrypted_text:
            messagebox.showerror("Ошибка", "Сначала зашифруйте текст.")
            return
        try:
            encrypted_list = list(map(int, encrypted_text.strip('[]').split(', ')))
            decrypted = decrypt(encrypted_list, self.private_key)
            self.decrypted_output.config(text=decrypted)
        except Exception as e:
            messagebox.showerror("Ошибка", "Ошибка при расшифровке текста.")
            print(e)


if __name__ == "__main__":
    root = tk.Tk()
    app = RSAApp(root)
    root.mainloop()
