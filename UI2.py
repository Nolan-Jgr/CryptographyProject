# Nolan Jaeger

import random
from tkinter import *

from Functions import *

# generates a list all the prime numbers within the given range
primeList = primesInRange(26, 50)
# generates a random integers to choose a prime from the list above
primeIndex = random.randint(0, len(primeList) - 1)
# sets the prime value using the random index within the prime list
prime = primeList[primeIndex]
# prints the chosen prime number to the screen
print("Prime: " + str(prime))
# generates all the primitive roots of the chosen prime number
roots = primRoots(prime)
# generates a random integer to choose a root from the list above
rootIndex = random.randint(0, len(roots) - 1)
# sets the alpha given the random index within the roots list
alpha = roots[rootIndex]
# prints alpha to the screen
print("Alpha: " + str(alpha))
# hardcoded private keys for both parties involved
john_pr = 3
jane_pr = 7
# calculates both parties public keys and prints them to the screen
john_pub = pow(alpha, john_pr) % prime
print("John's Public Key: " + str(john_pub))
jane_pub = pow(alpha, jane_pr) % prime
print("Jane's Public Key: " + str(jane_pub))


# this function is for when party 1 clicks the send button
def labelConfig1(string):
    # if the message box is empty nothing happens
    if string == "":
        return
    else:
        # the ciphertext is generated using the dedicated prime value, alpha value,
        # party 2's public key, and the messaging attempting to be sent
        ciphertxt = elgamal_encrypt(prime, alpha, jane_pub, string)
        # prints the ciphertext to the screen
        print(ciphertxt)
        # if the shared key and the random prime do not have an inverse,
        # the error is caught here, a message is displayed to the senders screen
        if elgamal_decrypt(prime, ciphertxt, jane_pr) is None:
            text = frame_textArea.cget("text") + "COULD NOT SEND MESSAGE TRY AGAIN\n"
            frame_textArea.configure(text=text)
            return
        # the text is decrypted and displayed using the prime number,
        # the cipher text sent from party 1, and party 2's private key.
        # the message is then displayed to party 2's screen
        text = frame_textArea1.cget("text") + "John : " + elgamal_decrypt(prime, ciphertxt, jane_pr) + "\n"
        frame_textArea1.configure(text=text)
        # this line clears party 1's entry field
        frame_message.delete(0, END)


# this function is for when party 2 clicks the send button
def labelConfig2(string):
    # if the message box is empty nothing happens
    if string == "":
        return
    else:
        # the ciphertext is generated using the dedicated prime value, alpha value,
        # party 1's public key, and the messaging attempting to be sent
        ciphertxt = elgamal_encrypt(prime, alpha, john_pub, string)
        # prints the ciphertext to the screen
        print(ciphertxt)
        # if the shared key and the random prime do not have an inverse,
        # the error is caught here, a message is displayed to the senders screen
        if elgamal_decrypt(prime, ciphertxt, john_pr) is None:
            text = frame_textArea1.cget("text") + "COULD NOT SEND MESSAGE TRY AGAIN\n"
            frame_textArea1.configure(text=text)
            return
        # the text is decrypted and displayed using the prime number,
        # the cipher text sent from party 2, and party 1's private key.
        # the message is then displayed to party 1's screen
        text = frame_textArea.cget("text") + "Jane : " + elgamal_decrypt(prime, ciphertxt, john_pr) + "\n"
        frame_textArea.configure(text=text)
        # this line clears party 2's entry field
        frame_message1.delete(0, END)


# this section of code uses the tkinter library to create a GUI
# two windows for each party
window = Tk()
window1 = Tk()
window.title("John Doe")
window1.title("Jane Doe")

# this section is for party 1's window
# components include a frame, a label for the messages, a label to indicate
# entry area, the entry area itself, and a button for functionality
frame = LabelFrame(window, bg='#2E424D')
frame_textArea = Label(frame, height=10, width=50, bg='#98DAD9',
                       anchor='nw', highlightbackground='#5B8291', highlightthickness=2,
                       fg="black", justify=LEFT)
frame_label = Label(frame, text="Enter Message: ", width=12, bg='#2E424D',
                    font=('Century Gothic', 10), fg="white")
frame_message = Entry(frame, width=25, font=('Century Gothic', 10))
frame_send = Button(frame, text="Send", width=10,
                    command=lambda: labelConfig1(frame_message.get()),
                    bg='#5B8291', activebackground='#98DAD9',
                    font=('Century Gothic', 10), fg="white")

frame_textArea.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 0))
frame_label.grid(row=1, column=0)
frame_message.grid(row=1, column=1, columnspan=3)
frame_send.grid(row=2, column=0, columnspan=4, pady=(0, 10))

frame.pack()

##############################################

# this section is for party 2's window
# components include a frame, a label for the messages, a label to indicate
# entry area, the entry area itself, and a button for functionality
frame1 = LabelFrame(window1, bg='#2E424D')
frame_textArea1 = Label(frame1, height=10, width=50, bg='#98DAD9',
                        anchor='nw', highlightbackground='#5B8291', highlightthickness=2,
                        fg="black", justify=LEFT)
frame_label1 = Label(frame1, text="Enter Message: ", width=12, bg='#2E424D',
                     font=('Century Gothic', 10), fg="white")
frame_message1 = Entry(frame1, width=25, font=('Century Gothic', 10))
frame_send1 = Button(frame1, text="Send", width=10,
                     command=lambda: labelConfig2(frame_message1.get()),
                     bg='#5B8291', activebackground='#98DAD9',
                     font=('Century Gothic', 10), fg="white")

frame_textArea1.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 0))
frame_label1.grid(row=1, column=0)
frame_message1.grid(row=1, column=1, columnspan=3)
frame_send1.grid(row=2, column=0, columnspan=4, pady=(0, 10))

frame1.pack()

# these lines indicate the placement of the windows on the screen when executed
# as well as making it so the windows cannot be resized
window.geometry("+50+200")
window1.geometry("+450+200")
window.resizable(0, 0)
window1.resizable(0, 0)
window.mainloop()
window1.mainloop()
