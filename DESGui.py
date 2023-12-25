import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from DESEngine import DES

class DESApplication:
    def __init__(self, root):
        self.root = root
        root.title("DES Encryption/Decryption")

        self.mode_label = tk.Label(root, text="Select Mode:")
        self.mode_label.grid(row=0, column=0, columnspan=2)
        self.mode_var = tk.StringVar()
        self.mode_dropdown = ttk.Combobox(root, textvariable=self.mode_var, state='readonly')
        self.mode_dropdown['values'] = ('BIN', 'HEX', 'TEXT')
        self.mode_dropdown.current(0)
        self.mode_dropdown.grid(row=1, column=0, columnspan=2)

        self.message_label_text = tk.StringVar(root, value="Message:")
        self.message_label = tk.Label(root, textvariable=self.message_label_text)
        self.message_label.grid(row=2, column=0, sticky="w")
        self.message_text = tk.Text(root, height=8, width=40)
        self.message_text.grid(row=3, column=0)
        self.message_text.bind("<Key>", self.on_message_change)

        self.result_label_text = tk.StringVar(root, value="")
        self.result_label = tk.Label(root, textvariable=self.result_label_text)
        self.result_label.grid(row=2, column=1, sticky="w")
        self.result_text = tk.Text(root, height=8, width=40)
        self.result_text.grid(row=3, column=1)

        self.key_label = tk.Label(root, text="Key (64-bit): Enter 16 '0x' characters")
        self.key_label.grid(row=4, column=0, columnspan=2)
        self.key_entry = tk.Entry(root, width=35)
        self.key_entry.grid(row=5, column=0, columnspan=2, padx=10, pady=4)

        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=6, column=0, columnspan=2, pady=4)

        self.encrypt_button = tk.Button(self.button_frame, text="Encrypt", command=self.encrypt_message)
        self.encrypt_button.pack(side=tk.LEFT, padx=10)

        self.decrypt_button = tk.Button(self.button_frame, text="Decrypt", command=self.decrypt_message)
        self.decrypt_button.pack(side=tk.LEFT, padx=10)

    def on_message_change(self, event):
        if not self.message_text.edit_modified():
            return
        self.message_label_text.set("Message:")
        self.result_label_text.set("")
        self.message_text.edit_modified(False)

    def encrypt_message(self):
        try:
            self.message_label_text.set("Plain Text")
            self.result_label_text.set("Cipher Text")
            mode = self.mode_var.get()
            self.des = DES(mode)
            message = self.message_text.get("1.0", "end-1c")
            key = self.key_entry.get()
            encrypted_message = self.des.encryptMsg(message, key)
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", encrypted_message)
        except Exception as e:
            messagebox.showerror("Encryption Error", f"Error occurred during encryption: {e}")

    def decrypt_message(self):
        try:
            self.message_label_text.set("Cipher Text")
            self.result_label_text.set("Plain Text")
            mode = self.mode_var.get()
            self.des = DES(mode)
            message = self.message_text.get("1.0", "end-1c")
            key = self.key_entry.get()
            decrypted_message = self.des.decryptMsg(message, key)
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", decrypted_message)
        except Exception as e:
            messagebox.showerror("Decryption Error", f"Error occurred during decryption: {e}")

root = tk.Tk()
app = DESApplication(root)
root.mainloop()