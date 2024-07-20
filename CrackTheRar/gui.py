import string
import os
import rarfile
from threading import Thread
from pathlib import Path

from customtkinter import *
from CTkMessagebox import CTkMessagebox

from .crack import bruteforce, dictionary_attack

set_appearance_mode("system")
set_default_color_theme("blue")

DEFAULT_LARGE_BUTTON_FONT = ("Inter", 24, "bold")
DEFAULT_CHECKBOX_FONT = ("Inter", 16)
DEFAULT_BUTTON_FONT = ("Inter", 16)


class CrackTheRar(CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Crack The Rar")
        self.geometry("700x500")
        self.resizable(False, False)

        # Configuring Icon for the app
        icon = Path(__file__).parent / "icons/icon-512.ico"
        self.iconbitmap(icon)

        # Configuring Grid for Main App
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Creating Tabview
        self.tabview = CTkTabview(self)
        self.tabview._segmented_button.configure(
            font=DEFAULT_LARGE_BUTTON_FONT, height=45)
        self.tabview.grid(row=0, column=0, columnspan=2,
                          sticky=NSEW,  padx=10, pady=10)

        self.bruteforce_tab = self.tabview.add("Bruteforce")
        self.dictionary_tab = self.tabview.add("Dictionary")

        self.create_bruteforce_tab()
        self.create_dictionary_tab()
        self.create_file_selection()
        self.create_start_button()

    def password_length_slider_method(self, value):

        self.password_length.set(value)
        self.password_length_label.configure(
            text=f"Password Length: {self.password_length.get()}")

    def create_bruteforce_tab(self):
        self.bruteforce_tab.grid_columnconfigure((0, 1), weight=1)

        # Making variables for checboxes and slider
        self.uppercase_letters = BooleanVar(master=self.bruteforce_tab)
        self.lowercase_letters = BooleanVar(master=self.bruteforce_tab)
        self.numerical_digits = BooleanVar(
            master=self.bruteforce_tab, value=True)
        self.special_letters = BooleanVar(master=self.bruteforce_tab)
        self.white_space = BooleanVar(master=self.bruteforce_tab)
        self.password_length = IntVar(self.bruteforce_tab, value=4)

        # Making 2x2 grid for 4 checboxes
        CTkCheckBox(self.bruteforce_tab, text="Include all lowercase letters", font=DEFAULT_CHECKBOX_FONT, variable=self.uppercase_letters).grid(
            row=0, column=0, sticky=W, padx=10, pady=15)
        CTkCheckBox(self.bruteforce_tab, text="Include all uppercase letters", font=DEFAULT_CHECKBOX_FONT, variable=self.lowercase_letters).grid(
            row=0, column=1, sticky=W, padx=10, pady=15)
        CTkCheckBox(self.bruteforce_tab, text="Include all digits", font=DEFAULT_CHECKBOX_FONT, variable=self.numerical_digits).grid(
            row=1, column=0, sticky=W, padx=10, pady=15)
        CTkCheckBox(self.bruteforce_tab, text="Include all special letters", font=DEFAULT_CHECKBOX_FONT, variable=self.special_letters).grid(
            row=1, column=1, sticky=W, padx=10, pady=15)
        CTkCheckBox(self.bruteforce_tab, text="Include whitespace", font=DEFAULT_CHECKBOX_FONT, variable=self.white_space).grid(
            row=2, column=0, columnspan=2, pady=15)

        # Taking Password Length using CTkSlider
        self.password_length_label = CTkLabel(
            self.bruteforce_tab, text=f"Password Length: {self.password_length.get()}", font=DEFAULT_CHECKBOX_FONT)
        self.password_length_label.grid(row=3, column=0)

        CTkSlider(master=self.bruteforce_tab, from_=1,
                  to=10, command=self.password_length_slider_method).grid(row=3, column=1, pady=20)

    def create_dictionary_tab(self):
        self.dictionary_tab.grid_columnconfigure((0, 1), weight=1)
        self.dictionary_tab.grid_rowconfigure(0, weight=1)

        self.password_file_entry = CTkEntry(
            master=self.dictionary_tab, placeholder_text="Select a password file", width=400, height=40)
        self.password_file_entry.grid(row=0, column=0, padx=10, sticky=E)

        CTkButton(
            master=self.dictionary_tab, text="Browse", height=40, command=self.select_password_file).grid(row=0, column=1, sticky=W)

    def create_file_selection(self):

        self.select_file_entry = CTkEntry(
            master=self, placeholder_text="Select a file to crack", width=400, height=40)
        self.select_file_entry.grid(row=1, column=0, sticky=E, padx=10, pady=8)
        CTkButton(
            master=self, text="Browse", font=DEFAULT_BUTTON_FONT, height=40, command=self.select_locked_file).grid(row=1, column=1, sticky=W, pady=8)

        self.output_path_entry = CTkEntry(
            master=self, placeholder_text="Select output path", width=400, height=40)
        self.output_path_entry.grid(row=3, column=0, sticky=E, padx=10, pady=8)

        CTkButton(
            master=self, text="Browse", font=DEFAULT_BUTTON_FONT, height=40, command=self.select_output_path).grid(row=3, column=1, sticky=W, pady=8)

    def create_start_button(self):
        self.start_button = CTkButton(master=self, text="START",
                                      font=DEFAULT_LARGE_BUTTON_FONT, width=200, height=45, command=self.start_button_method)
        self.start_button.grid(row=4, column=0, columnspan=2,  padx=(80, 80),
                               pady=(16, 24))

    def select_password_file(self):
        FILE_TYPES = (
            ("Text Files", "*.txt"),
        )
        password_file = filedialog.askopenfilename(filetypes=FILE_TYPES)

        if password_file:
            self.password_file_entry.delete(0, END)
            self.password_file_entry.insert(0, password_file)

    def select_locked_file(self):
        FILE_TYPES = (
            ("Zip Files", "*.zip"),
            ("Rar Files", "*.rar"),
        )
        file_name = filedialog.askopenfilename(filetypes=FILE_TYPES)

        if file_name:
            self.select_file_entry.delete(0, END)
            self.select_file_entry.insert(0, file_name)

    def select_output_path(self):
        output_path = filedialog.askdirectory()

        if output_path:
            self.output_path_entry.delete(0, END)
            self.output_path_entry.insert(0, output_path)

    def validate_password_file(self):
        PASSWORD_FILE = self.password_file_entry.get()

        if os.path.exists(PASSWORD_FILE) and PASSWORD_FILE.endswith(".txt"):
            return True

        CTkMessagebox(master=self,
                      title="Invalid Password File", message="Please select a valid .txt password file.", icon="cancel", header=True)
        return False

    def validate_output_path(self):
        OUTPUT_PATH = self.output_path_entry.get()

        if not OUTPUT_PATH:
            OUTPUT_PATH = None
            return True
        elif os.path.exists(OUTPUT_PATH) and os.path.isdir(OUTPUT_PATH):
            return True

        CTkMessagebox(master=self,
                      title="Invalid output path", message="Please select a valid output path or do not select output path.", icon="cancel", header=True)
        return False

    def validate_locked_file(self):
        FILENAME = self.select_file_entry.get()

        if FILENAME and os.path.exists(FILENAME) and (FILENAME.endswith(".zip") or FILENAME.endswith(".rar")):
            return True

        CTkMessagebox(master=self,
                      title="Invalid File", message="Please select a valid .zip or .rar file.", icon="cancel", header=True)
        return False

    def make_password(self):
        PASSWORD_SET = ""

        if self.lowercase_letters.get():
            PASSWORD_SET += string.ascii_lowercase
        if self.uppercase_letters.get():
            PASSWORD_SET += string.ascii_uppercase
        if self.numerical_digits.get():
            PASSWORD_SET += string.digits
        if self.special_letters.get():
            PASSWORD_SET += string.punctuation
        if self.white_space.get():
            PASSWORD_SET += " "

        if PASSWORD_SET == "":
            CTkMessagebox(master=self.bruteforce_tab, title="Empty Password Set",
                          message="Please select atleast one checkbox.", icon='cancel')
            return False

        return PASSWORD_SET

    def toggle_start_button_state(self):
        current_state = self.start_button.cget("state")
        if current_state == NORMAL:
            self.start_button.configure(state=DISABLED)
        else:
            self.start_button.configure(state=NORMAL)

    def password_found_box(self, password):
        CTkMessagebox(master=self, title="Password Found",
                      message=f"The Correct Password is {password}.", icon="check", header=True)

    def password_not_found_box(self):
        CTkMessagebox(master=self, title="Password Not Found",
                      message=f"No Correct Password Found", icon="cancel", header=True)

    def start_button_method(self):
        filename = self.select_file_entry.get()
        output_path = self.output_path_entry.get()

        if not self.validate_locked_file():
            return

        if not self.validate_output_path():
            return

        if self.tabview.get() == "Dictionary":
            if not self.validate_password_file():
                return

            thread = Thread(target=self.dictionary_thread,
                            args=(filename, output_path))
            thread.daemon = True
            thread.start()

        elif self.tabview.get() == "Bruteforce":
            password_set = self.make_password()
            password_length = self.password_length.get()
            if not password_set:
                return

            thread = Thread(target=self.bruteforce_thread, args=(
                filename, output_path, password_set, password_length))
            thread.daemon = True
            thread.start()

    def bruteforce_thread(self, filename, output_path, password_set, password_length):
        self.toggle_start_button_state()
        password = bruteforce(file_path=filename, password_set=password_set,
                              output_path=output_path, password_length=password_length)
        if password:
            self.password_found_box(password)
        else:
            self.password_not_found_box()
        self.toggle_start_button_state()

    def dictionary_thread(self, filename, output_path):
        try:
            self.toggle_start_button_state()
            password_file = self.password_file_entry.get()
            password = dictionary_attack(password_file=password_file,
                                         file_path=filename, output_path=output_path)
            if password:
                self.password_found_box(password)
            else:
                self.password_not_found_box()
        except rarfile.RarExecError:
            CTkMessagebox(self, header=True, title="Unrar Error",
                          message="Please add UnRar to path or in this folder.", icon="cancel")
        finally:
            self.toggle_start_button_state()
