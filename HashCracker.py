# LIBRARIES
import tkinter as tk
from tkinter import ttk, Text, filedialog as fd, messagebox
import os, fnmatch, subprocess, threading


# FUNCTIONS OF THE APP ARE LOCATED HERE
def handshake_search():
    folder_selected = fd.askdirectory()
    search_bar_handshake.delete(0, tk.END)
    search_bar_handshake.insert(tk.END, "Showing from: " + folder_selected)
    tbox.delete("1.0", tk.END)

    def find(pattern, path):
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    tbox.insert(tk.END, folder_selected + "/" + name + "\n")

    find('*.hc22000*', folder_selected)

def database_search():
    # show the open file dialog
    f = fd.askopenfile()
    # read the text file and show its content on the Text but first delete leftovers from textbox
    tbox.delete("1.0", tk.END)
    tbox.insert("1.0", str(f.readlines()))

def crack_handshake():
    # ALL ERROR MESSAGES AND CHECKS HERE AT THE BEGINNING

    # Error message function for choosing more than 1 option
    def error_message():
        tk.messagebox.showerror(title="ERROR", message="TIP 1: Choose one mode.\n"
                                                       "TIP 2: You have to chose only one option from Alphanumerical, Numbers and Letters.")

    # Error for not choosing specific config for Letter option
    def error_letter():
        tk.messagebox.showerror(title="ERROR", message="There seems to be something wrong with the config of Letters only.\n"
                                                       "You can only pick one or both of the options.")

    # Error for not choosing any hash to crack
    def error_empty_hash():
        if h_crack_entry.get() == "":
            tk.messagebox.showerror(title="ERROR", message="No hash was chosen.\n"
                                                           "TIP: Only .hc22000 is supported now")

    # Error for choosing bad combo to crack
    def hashcat_error_combo():
        tk.messagebox.showerror(title="ERROR", message="Hashcat can't compute such combination.\n"
                                                       "Try a different one or check TIPS section.")

    # HERE THE CRACKING BEGINS

    def cracking(command):

        top = tk.Toplevel()
        top.geometry("800x340")
        top.title("Running Scripts")

        def cancel():
            os.system("taskkill /im hashcat.exe /F")
            top.destroy()

        #def save():
        #    return

        def capture_output():

            p = subprocess.Popen(command, stdout=subprocess.PIPE)
            while p.poll() is None:  # process is still running
                output.insert("end", p.stdout.readline())
                output.see("end")
            output.insert("end", "--- done ---\n")

        # Add a Vertical Scrollbar
        scroll_v = tk.Scrollbar(top)
        scroll_v.grid()
        # Add a Horizontal Scrollbar
        # Add a Text widget
        output = Text(top, yscrollcommand=scroll_v.set, wrap="none", relief="sunken", bd=2)
        output.place(x=5, height=220, width=890)
        # Attact the scrollbar with the text widget
        scroll_v.config(command=output.yview)


        ttk.Button(top, text="Cancel", command=lambda: cancel()).grid(row=0, column=0, padx=1, pady=221)
        #ttk.Button(top, text="Save", command=lambda: save()).grid(row=0, column=2, padx=1, pady=221)
        ttk.Button(top, text="Run", command=lambda: threading.Thread(target=capture_output, daemon=True).start()).grid(row=0, column=3, padx=1, pady=221)
        top.mainloop()

    # Collect Data and check if an option is missing OR if user gave more than one in each category
    error_empty_hash()
    # Check the main Option user gave and create the command
    # The only main option now is Brute Force
    if value_inside.get() == "Brute Force":

        # TIMER FOR PRINTING STATUS OF CRACKING
        timer = " --status --status-timer 10"

        # Brute Force with alphanumeric option
        if alpha_num_var.get() == 1 and numbers_var.get() == 0 and letters_var.get() == 0:

            if digit_value_inside.get() == "FULL 8-12":

                # command is Brute Force with alphanumeric option + FULL digits
                command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3 -1 ?d?l?u" + " --increment --increment-min 8 --increment-max 12 ?1?1?1?1?1?1?1?1?1?1?1?1" + timer
                print(command)
                cracking(command)

            elif digit_value_inside.get() == "8":

                # command is Brute Force with alphanumeric option + 8 digits
                command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3 -1 ?d?l?u " + "?1?1?1?1?1?1?1?1" + timer
                print(command)
                cracking(command)

            elif digit_value_inside.get() == "9":

                # command is Brute Force with alphanumeric option + 9 digits
                command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3 -1 ?d?l?u " + "?1?1?1?1?1?1?1?1?1" + timer
                print(command)
                cracking(command)

            elif digit_value_inside.get() == "10":

                hashcat_error_combo()

            elif digit_value_inside.get() == "11":

                hashcat_error_combo()

            elif digit_value_inside.get() == "12":

                hashcat_error_combo()

        else:

            # Brute Force with numbers
            if alpha_num_var.get() == 0 and numbers_var.get() == 1 and letters_var.get() == 0:

                if digit_value_inside.get() == "FULL 8-12":

                    # Brute Force with numbers + FULL digits
                    command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " --increment --increment-min 8 --increment-max 12 ?d?d?d?d?d?d?d?d?d?d?d?d" + timer
                    print(command)
                    cracking(command)

                elif digit_value_inside.get() == "8":

                    # Brute Force with numbers + 8 digits
                    command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?d?d?d?d?d?d?d?d" + timer
                    print(command)
                    cracking(command)

                elif digit_value_inside.get() == "9":

                    # Brute Force with numbers + 9 digits
                    command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?d?d?d?d?d?d?d?d?d" + timer
                    print(command)
                    cracking(command)

                elif digit_value_inside.get() == "10":

                    # Brute Force with numbers + 10 digits
                    command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?d?d?d?d?d?d?d?d?d?d" + timer
                    print(command)
                    cracking(command)

                elif digit_value_inside.get() == "11":

                    # Brute Force with numbers + 11 digits
                    command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?d?d?d?d?d?d?d?d?d?d?d" + timer
                    print(command)
                    cracking(command)

                elif digit_value_inside.get() == "12":

                    # Brute Force with numbers + 12 digits
                    command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?d?d?d?d?d?d?d?d?d?d?d?d" + timer
                    print(command)
                    cracking(command)

            else:

                # Brute Force with Letters THIS IS FOR LOWERCASE
                if alpha_num_var.get() == 0 and numbers_var.get() == 0 and letters_var.get() == 1:

                    # Letters Lowercase only
                    if letters_var_l.get() == 1 and letters_var_u.get() == 0:

                        if digit_value_inside.get() == "FULL 8-12":

                            # Brute Force with letters option + FULL digits + Lowercase only
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " --increment --increment-min 8 --increment-max 12 ?l?l?l?l?l?l?l?l?l?l?l?l" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "8":

                            # Brute Force with letters option + 8 digits + Lowercase only
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?l?l?l?l?l?l?l?l" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "9":

                            # Brute Force with letters option + 9 digits + Lowercase only
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?l?l?l?l?l?l?l?l?l" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "10":

                            # Brute Force with letters option + 10 digits + Lowercase only
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?l?l?l?l?l?l?l?l?l?l" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "11":

                            # Brute Force with letters option + 11 digits + Lowercase only
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?l?l?l?l?l?l?l?l?l?l?l" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "12":

                            # Brute Force with letters option + 12 digits + Lowercase only
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?l?l?l?l?l?l?l?l?l?l?l?l" + timer
                            print(command)
                            cracking(command)


                    # Letters Uppercase only
                    elif letters_var_l.get() == 0 and letters_var_u.get() == 1:

                        if digit_value_inside.get() == "FULL 8-12":

                            # Brute Force with letters option + FULL digits + Uppercase only
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " --increment --increment-min 8 --increment-max 12 ?u?u?u?u?u?u?u?u?u?u?u?u" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "8":

                            # Brute Force with letters option + 8 digits + Lowercase only
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?u?u?u?u?u?u?u?u" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "9":

                            # Brute Force with letters option + 9 digits + Lowercase only
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?u?u?u?u?u?u?u?u?u" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "10":

                            # Brute Force with letters option + 10 digits + Lowercase only
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?u?u?u?u?u?u?u?u?u?u" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "11":

                            # Brute Force with letters option + 11 digits + Lowercase only
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?u?u?u?u?u?u?u?u?u?u?u" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "12":

                            # Brute Force with letters option + 12 digits + Lowercase only
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3" + " ?u?u?u?u?u?u?u?u?u?u?u?u" + timer
                            print(command)
                            cracking(command)


                    # Both Uppercase and lowercase
                    elif letters_var_l.get() == 1 and letters_var_u.get() == 1:

                        if digit_value_inside.get() == "FULL 8-12":

                            # Brute Force with letters option + FULL digits + Both Uppercase / Lowercase
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3 -1 ?l?u" + " --increment --increment-min 8 --increment-max 12 ?1?1?1?1?1?1?1?1?1?1?1?1" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "8":

                            # Brute Force with letters option + 8 digits + Both Uppercase / Lowercase
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3 -1 ?l?u" + " ?1?1?1?1?1?1?1?1" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "9":

                            # Brute Force with letters option + 9 digits + Both Uppercase / Lowercase
                            command = "hashcat.exe -m 22000 " + h_crack_entry.get() + " -a 3 -1 ?l?u" + " ?1?1?1?1?1?1?1?1?1" + timer
                            print(command)
                            cracking(command)

                        elif digit_value_inside.get() == "10":

                            hashcat_error_combo()

                        elif digit_value_inside.get() == "11":

                            hashcat_error_combo()

                        elif digit_value_inside.get() == "12":

                            hashcat_error_combo()

                    else:
                        error_letter()


                else:
                    error_message()




def clear_output_box():
    tbox.delete("1.0", tk.END)

def guide():
    tbox.delete("1.0", tk.END)
    tbox.insert(tk.END, "--------------------------------------------GUIDE------------------------------------------------"
                        """
Step 1:
Search for Handshakes in your machine. (press 'search Handshakes')

Step 2:
Copy paste the path to the search bar from this Output box right next to the 'Crack Handshake' button.

Step 3:
Select Cracking Options (if not sure check tips for Right and Wrong combinations)

Step 4:
Press "Crack Handshake" button to begin proccess.
                            """)

def TIPS():
    tbox.delete("1.0", tk.END)
    tbox.insert(tk.END, "---------------------------------------------TIPS------------------------------------------------"
                """
OPTIONS COMBOS:
Choose only one of these (Alphanumerical, Numbers, Letters).
If you choose "Letters Only" DONT FORGET to choose lower case or uppercase or both.

For Alphanumerical stop at 9 digits.
For Numbers you can use all digits up to 12.
For Letters if you choose both uppercase and lower case stop at 9 digits, otherwise up to 12.

Q: Why no more than 12?
A: Even at this limit some config combinations can't go more than 9 digits.

Searching for Handshakes tips:
It is recommended to store handshakes in the main folder of the application.

If you cannot find the handshake file you are looking for maybe it is not .hc22000.
To convert any file like .pcap to .hc22000 go to this online converter or use your own.
https://hashcat.net/cap2hashcat/ 

Use only the latest Hashcat version or > v6.0.
""")





# HERE BEGINS THE APP
if __name__ == "__main__":
    # LOAD THE MAIN GUI
    # MAIN Window Settings
    main_window = tk.Tk()
    main_window.title("HashCracker v.1.0")
    main_window.geometry("800x500")

    style = ttk.Style(main_window)
    #style.theme_use("clam")

    # BUTTONS
    # button for opening folder with handshakes
    ttk.Button(main_window, text="Search Handshakes", command=lambda: handshake_search()).grid(column=0, row=0, sticky="w")

    # button for opening any kind of database (DO NOT FORGET TO ADD SUPPORT FOR MANY KINDS)
    ttk.Button(main_window, text="Open Database", command=lambda: database_search()).grid(column=0, row=1, sticky="w")

    # button for cracking the selected handshake
    ttk.Button(main_window, text="Crack Handshake", command=lambda: crack_handshake()).grid(column=0, row=2, sticky="w")

    # button for clearing the output box
    ttk.Button(main_window, text="Clear Output Box", command=lambda: clear_output_box()).grid(column=0, row=3, sticky="w")

    # button for guide
    ttk.Button(main_window, text="Guide", command=lambda: guide()).grid(column=2, row=0, sticky="e", padx=276)

    # button for TIPS
    ttk.Button(main_window, text="Tips", command=lambda: TIPS()).grid(column=2, row=1, sticky="e", padx=276)

    # button for hash converter online
    # we will see about that




    # SEARCH BOX
    # search for handshakes
    search_bar_handshake = ttk.Entry(main_window, width=50)
    search_bar_handshake.grid(column=1, row=0, sticky="w")

    # search box for cracking the handshake
    h_crack_entry = ttk.Entry(main_window, width=50)
    h_crack_entry.grid(column=1, row=2, sticky="w")

    # OUTPUT BOX
    tbox = Text(main_window, wrap="none" ,bd=2, relief="sunken")
    tbox.place(x=7, y=275, height=220, width=785)
    # default message of the output box
    tbox.insert("1.0", "No Output Yet.")

    # SCROLL BAR
    scrollbar_main_tbox = ttk.Scrollbar(main_window, orient="vertical", command=tbox.yview)
    scrollbar_main_tbox.place(x=7, y=275, height=1, width=1)

    # CRACKING OPTIONS
    tk.Label(main_window, text="Select Cracking Options:").grid(row=4, column=0, pady=10)
    # MAIN METHODS
    available_options = ["Brute Force"]
    value_inside = tk.StringVar(main_window)
    value_inside.set("Select Option")
    cracking_options_menu = tk.OptionMenu(main_window, value_inside, *available_options)
    cracking_options_menu.grid(row=5, column=0, sticky="w")
    # OPTIONS
    numbers_var = tk.IntVar()
    letters_var = tk.IntVar()
    letters_var_l = tk.IntVar()
    letters_var_u = tk.IntVar()
    alpha_num_var = tk.IntVar()

    R1 = tk.Checkbutton(main_window, text="Alphanumerical", variable=alpha_num_var).grid(sticky='w')
    R2 = tk.Checkbutton(main_window, text="Numbers Only", variable=numbers_var).grid(sticky="w")
    R3 = tk.Checkbutton(main_window, text="Letters Only", variable=letters_var).grid(sticky="w")
    R3L = tk.Checkbutton(main_window, text="Lowercase", variable=letters_var_l).grid(row=8, column=1, sticky="w")
    R3U = tk.Checkbutton(main_window, text="Uppercase", variable=letters_var_u).grid(row=8, column=1, sticky="s")

    # OPTIONS 2
    available_digit_options = ["FULL 8-12", "8", "9", "10", "11", "12"]
    digit_value_inside = tk.StringVar(main_window)
    digit_value_inside.set("How many Digits?")
    digit_menu = tk.OptionMenu(main_window, digit_value_inside, *available_digit_options)
    digit_menu.grid(row=5, column=1, sticky="w")


    # MAINLOOP
    main_window.mainloop()

"""
NOTES:

* NOTE-1
Hashcat needs to translate .pcap files  to .hc22000
This process is done by the online tool https://hashcat.net/cap2hashcat/
In this version there is only a notification that leads you to this site.
In next version (FOR LINUX USERS ONLY! it will compile required tools to do it automatically.)


* NOTE-2
SAVED COMMANDS:
./hashcat.exe -m 22000 23661_1661427941.hc22000 -1 ?dl?u -a 3 ?1?1?1?1?1?1?1?1
                        |
                        -> this is the variable but with the default extension .hc22000 

8 digits (New Method):
hashcat.exe -m 22000 8-digit-wpa2.hc22000 -a 3 ?d?d?d?d?d?d?d?d

10 digits (New Method):
hashcat.exe -m 22000 10-digit-wpa2.hc22000 -a 3 ?d?d?d?d?d?d?d?d?d?d

10 digits and alpha (New Method):
hashcat.exe -m 22000 10-digit-letters-wpa2.hc22000 -1 ?d?l?u -a 3 ?1?1?1?1?1?1?1?1?1?1

Increment digits (New Method):
hashcat.exe -m 22000 hash.hc22000 -a 3 --increment --increment-min 8 --increment-max 18 ?d?d?d?d?d?d?d?d?d?d?d?d?d?d?d?d?d?d

Increment digits and alpha (New Method):
hashcat.exe -m 22000 10-digit-letters-wpa2.hc22000 -1 ?d?l?u -a 3 --increment --increment-min 8 --increment-max 12 ?1?1?1?1?1?1?1?1?1?1?1?1



* NOTE-3
PROVIDE TIPS
TIP1 - install cuda toolkit for nvidia drivers in order to work
TIP2 - use the link provided to translate handshakes if needed (only .hc22000 is available now)



#############################
option 1 with BRUTE FORCE
FULL
8 - 12   alphanumerical
         numbers only
         letters only
         
         
brute force 8-12 - ONLY NUMBERS
./hashcat.exe -m 22000 hash.hc22000 -a 3 --increment --increment-min 8 --increment-max 12 ?d?d?d?d?d?d?d?d?d?d?d?d

brute force 8-12 - ONLY LETTERS (lowercase)
./hashcat.exe -m 22000 hash.hc22000 -a 3 --increment --increment-min 8 --increment-max 12 ?l?l?l?l?l?l?l?l?l?l?l?l

brute force 8-12 - ONLY LETTERS (uppercase)
./hashcat.exe -m 22000 hash.hc22000 -a 3 --increment --increment-min 8 --increment-max 12 ?u?u?u?u?u?u?u?u?u?u?u?u

brute force 8-12 Digits - Alphanumerical
./hashcat.exe -m 22000 hash.hc22000 -a 3 -1 ?d?l?u --increment --increment-min 8 --increment-max 12 ?1?1?1?1?1?1?1?1?1?1?1?1

----------------------------------------------------------------------------------------------------------------------








"""
