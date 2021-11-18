# Author: 218005822 - Rikesh Kylas
# Digital Image Watermarking based on a uniquely new Kaleidoscope Collage Replication Watermark for Copyright Protection
# UKZN Westville Honours Research Project - Superisor: Dr. Brett Van Niekerk
import sys
import time
import imagehash
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi
import hashlib
import os
from PIL import Image

''' Login class to create the methods required to define the login ui as well as set
the window dimensions and enable transitions between screens '''
class Login(QDialog):
    # Load the UI for login and connect methods defined below to buttons for functionality
    def __init__(self):
        super(Login, self).__init__()
        loadUi("Login.ui", self)
        self.btnLogin.clicked.connect(self.loginfunction)
        self.txtPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btnRegister.clicked.connect(self.signuppage)
        self.cboxShow.clicked.connect(self.showPassw)

    # Tests input to login against existing account details in userInfo textfile to allow users to sign in
    def loginfunction(self):
        # Checks if no input given by user to prevent false log in
        username = self.txtUser.text()
        password = self.txtPass.text()
        if (username == '') or (password == ''):
            print("Blank password and/or username entered!")
            QMessageBox.information(self, "Login Failed", "Blank password and/or username entered!")
            return
        # Reads and stores user accounts from text file into a dictionary mapping for quick access
        usersInfo = {}
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line = line.split()
                usersInfo.update({line[0]: line[1]})

            username = sanitizeName(username)
        # Tests user input against accounts for validation and outputs if account:
        # Username does not exist
        if username not in usersInfo:
            print("You Are Not Registered. Please register to continue.")
            QMessageBox.information(self, "Login Failed", "You Are Not Registered. Please register to continue.")
            return
        # Password for the corresponding username is incorrect
        elif not check_password_hash(password, usersInfo[username]):
            print("Incorrect Password. Please try again!")
            QMessageBox.information(self, "Login Failed",  "Incorrect Password. Please try again!")
        # Correct account details entered and successful login
        else:
            print()
            print("Logged In!")
            # Define a new instance of the LSB window and transition to it enabling Digital Watermarking
            lsb1 = LSBImg()
            # Push the username from here to the Image processor for later use in LSB class
            lsb1.lblWatermrk.setText(username)
            # Set label text values, add widget to the system counter and define LSB ui window dimensions
            lsb1.lblEMsg.setText("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            lsb1.lblDMsg.setText("XXXXXXXXXXXXXXXXXXXXXXXXX")
            widget.addWidget(lsb1)
            widget.setCurrentIndex(widget.currentIndex()+1)
            widget.setFixedWidth(702)
            widget.setFixedHeight(577)
    # Extra security measure method to enable the password visibility during user input
    def showPassw(self):
        self.txtPass.setEchoMode(QtWidgets.QLineEdit.Normal)
        if self.cboxShow.isChecked() == 0:
            self.txtPass.setEchoMode(QtWidgets.QLineEdit.Password)

# Linking the signup gui page to the login page for screen transitioning
    def signuppage(self):
        signup=SignUp()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex()+1)

# -----------------------------------------------------------------------------------------------
''' SignUp ui is defined with methods to allow users to create accounts which will
then be stored and have unique kaleidoscope watermarks assigned to them enabling 
them to easily log in after a successful sign up and use this tool for watermarking.'''

class SignUp(QDialog):
    # Load the UI for this page and link the signup button to its method
    def __init__(self):
        super(SignUp, self).__init__()
        loadUi("SignUp.ui", self)
        self.btnSignUp.clicked.connect(self.createAccfunction)
# This function gives the sign up button functionality to create and store an account
    def createAccfunction(self):
        # Extract user input for the new account
        uname = self.username.text()
        pword = self.passw.text()
        ans = self.secanswer.text()
        uname = sanitizeName(uname)
        # Test to see if the username already exists, hence a user cannot sign up twice but should log in
        if userAlreadyExist(uname):
            print("User already exists!!! Please Log in with your account details.")
            QMessageBox.information(self, "Sign-up Failed!", "User already exists!!! Please Log in with your account details.")
            return
        else:
            # If the user does not exist, check:
            # To ensure password is not blank
            if pword == '':
                print("Password is blank or not a SA ID number")
                QMessageBox.information(self, "Sign-up Failed!", "Password is blank or not a SA ID number")
                return
            # Security measure to ensure the password entered is correct to the user by requesting a retype
            if pword != ans:
                print("Password confirmation: Incorrect!")
                QMessageBox.information(self, "Sign-up Failed!", "Passwords do not match")
                return
            else:
                # Test to see if the user account, both name and password already exists and is stored.
                if userAlreadyExist(uname, pword):
                    print("User already exists! Please Log in with your account details.")
                    QMessageBox.information(self, "Sign-up Failed!", "User already exists! Please Log in with your account details")
                    return
        # Upon all checks above completed, add the user with username and hashed password to the textfile
        addUserInfo([uname, hash_password(pword)])
        QMessageBox.information(self, "Sign-up Success!", " Enjoy your experience!")
        print("Registered Successfully!")
        # Transition back to the login screen UI to allow the user to login
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
# ------------------------------------------------------------------------------------------
# Image processing - encode+decode functions + image comparison and ownership verification

# LSB class containing functions to encode, decode, view watermark and identify users
class LSBImg(QDialog):
    # Load DigitalWatermarking UI interface
    # Connect buttons to methods for functionality in this class
    def __init__(self):
        super(LSBImg, self).__init__()
        loadUi("DigitalWatermarking.ui", self)
        self.btnEncode.clicked.connect(self.encode)
        self.btnDecode.clicked.connect(self.decode)
        self.btnDecode_2.clicked.connect(self.cropDecode)
        self.btnHelp.clicked.connect(self.showUserKaleido)

# LSB encoding technique for the digital watermarking:
# I would like to give acknowledgement to Mohta Rahul Suresh's Hiding an image inside another image
# - steganography using python tutorial on CPPsecrets (link in sources folder), whose concept of LSB
# was adapted and specialized to suit the functionality of Digital Watermarking in this software.

# Digitally watermark a Kaleidoscope image using LSB encode method
    def encode(self):
        # Set the number of bits to use from an image to 2
        # 2 bits was found to hold enough image information of the watermark
        # while still keeping the watermark well hidden in the host image
        n_bits = 2
        # Extract current file path directory
        path = os.getcwd()
        # Get the filename of the Kaleidoscope watermark assigned to the user logged in
        flename = getuserKaleido(self.lblWatermrk.text())
        to_hidepath = os.path.join(path, flename)
        # Use pillow to open the image and store the image dimensions of the watermark
        image_to_hide = Image.open(to_hidepath)
        w, h = image_to_hide.size
        print("Your Kaleidoscope opened!")
        # Retrieve host image (to be watermarked) filename from user
        hostImgName = str(self.encodeName.text())
        # Ensures the input image file name is entered and is a jpg image
        if hostImgName == '':
            QMessageBox.information(self, "Invalid filename", "No file name entered!")
            return
        if not hostImgName.endswith('jpg'):
            QMessageBox.information(self, "Invalid file extension", "Filename does not have .jpg extension!")
            return
        image_to_hide_in1 = Image.open(os.path.join(path, self.encodeName.text()))
        print("Successfully opened image to encode")
        # Resize host image to dimensions of the watermark
        # This avoids loss of watermark data + array out of index errors when inserting bits
        image_to_hide_in = image_to_hide_in1.resize((w, h), Image.ANTIALIAS)
        # Extract dimensions to iterate each pixel of the image pixel matrix
        width, height = image_to_hide.size
        # Load the host and watermark images to provide pixel access and perform LSB encoding
        hide_image = image_to_hide.load()
        hide_in_image = image_to_hide_in.load()
        print("Successfully loaded images")
        # This will store the pixel value for all pixels in the image as a pixel matrix
        data = []
        # Iterate through every pixel of the Kaleidoscope watermark image - hide_image
        for y in range(height):
            for x in range(width):
                # Extract R, B and B pixel values for an individual pixel of watermark image
                r_hide, g_hide, b_hide = hide_image[x, y]
                # Extract the 2 MSB values for each RGB value from the watermark image
                r_hide = get_n_most_significant_bits(r_hide, n_bits)
                g_hide = get_n_most_significant_bits(g_hide, n_bits)
                b_hide = get_n_most_significant_bits(b_hide, n_bits)
                # Extract R, B and B pixel values for an individual pixel of the host image
                r_hide_in, g_hide_in, b_hide_in = hide_in_image[x, y]
                # Remove the 2 LSB values for each RGB value of the host image
                r_hide_in = remove_n_least_significant_bits(r_hide_in, n_bits)
                g_hide_in = remove_n_least_significant_bits(g_hide_in, n_bits)
                b_hide_in = remove_n_least_significant_bits(b_hide_in, n_bits)
                # Append the watermark's 2 MSB to the end of where the 2 LSB have been
                # removed of the host image for each R, G and B value to combine the 2 images
                # Add these combined bit value components to data to construct the pixel matrix
                # of the newly watermarked/LSB encoded image
                data.append((r_hide + r_hide_in,
                             g_hide + g_hide_in,
                             b_hide + b_hide_in))
        # Create, save and display the produced encoded image as the watermarked image
        encImg = make_image(data, image_to_hide.size)
        # Notify user of success and image name for their retrieval
        QMessageBox.information(self, "Success!", "Your image is now Digitally Watermarked")
        self.lblEMsg.setText("[Image Encoded] Successfully!!! Filename: encoded.png")
        encImg.save("./encoded.png")
        imgx = Image.open(os.path.join(path, "encoded.png"))
        imgx.show()
        time.sleep(10)

# Extract watermarked Kaleidoscope image using LSB decode method
    def decode(self):
        n_bits = 2
        path = os.getcwd()
        # Retrieve user's watermarked image filename
        waterImgName = self.decodeName.text()
        # Ensures the input image file name is entered and is a png image
        if waterImgName == '':
            QMessageBox.information(self, "Invalid filename", "No file name entered!")
            return
        if not waterImgName.endswith('png'):
            QMessageBox.information(self, "Invalid file extension", "Filename does not have .png extension!")
            return

        image_to_decode = Image.open(os.path.join(path, self.decodeName.text()))
        # Extract image dimensions for size of pixels to iterate
        width, height = image_to_decode.size
        # Similar to encode, open the LSB encoded / watermarked image to access pixel values
        encoded_image = image_to_decode.load()
        # Store the extracted LSB pixel values to reconstruct the watermark
        data = []
        # Iterate through the image to access individual pixel values for LSB extraction
        # Note: The 2 LSB of this encoded image (for every RGB) is the 2 MSB of the encoded
        # kaleidoscope watermark image and is used to reproduce the watermark
        for y in range(height):
            for x in range(width):
                # Extract individual pixels RGB values for each pixel in the image's pixel matrix
                r_encoded, g_encoded, b_encoded = encoded_image[x, y]
                # Obtain the last 2 LSB of this pixel value
                r_encoded = get_n_least_significant_bits(r_encoded, n_bits)
                g_encoded = get_n_least_significant_bits(g_encoded, n_bits)
                b_encoded = get_n_least_significant_bits(b_encoded, n_bits)
                # Now these 2 bits: (eg. 11) need to be adjusted to fit an 8bit image pixel value in
                # order to reconstruct the watermark image, so shift the bits to the left so
                # it becomes MSB of extracted watermark image (11<-shifted becomes 11000000)
                r_encoded = shift_n_bits_to_8(r_encoded, n_bits)
                g_encoded = shift_n_bits_to_8(g_encoded, n_bits)
                b_encoded = shift_n_bits_to_8(b_encoded, n_bits)
                # Now append these extracted LSB values, shifted to become MSB
                # to data for each RGB value
                data.append((r_encoded, g_encoded, b_encoded))
        # Create, save and display the produced decoded image as the extracted watermark
        imgd = make_image(data, image_to_decode.size)
        imgd.save("decoded.png")
        print("Successfully decoded your image!")
        # Notify user of success and image name for their retrieval
        QMessageBox.information(self, "Success!", "Watermark extraction complete")
        img1 = Image.open(os.path.join(path, "decoded.png"))
        img1.show()
        time.sleep(5)
        self.lblDMsg.setText("[Image Decoded] Filename: decoded.png")

# This function is used as the watermark identification tool, to prove content ownership
    def cropDecode(self):
        path = os.getcwd()
        # Calculate computational score for the extracted watermark image
        basev = comp_ave_hash_score_base(os.path.join(path, "decoded.png"))
        # Define a very high computational score for the imagehash score in order to
        # extract the minimum value among all the images traversed below
        maxCompScore = 1002321
        # Read each line in the text file containing the assigned kaleidoscopes and corresponding users
        with open("kUsed.txt", "r") as fs1:
            for linex in fs1:
                currentline = linex.split(",")
                # Store each user's name
                ownName = str(currentline[0])
                print(ownName)
                # Store the file name of the kaleidoscope that belongs to that user
                fileT = os.path.join(path, str(currentline[1]))
                print(fileT)
                # Calculate the computational score for the user's kaleidoscope
                compv = comp_ave_hash_score_comp(fileT)
                # Use the ImageHash library function to find image similarity score
                compscore = img_similar(basev, compv)
                print(compscore)
                # Obtain and store the lowest computational score upon all iterations between user
                # kaleidoscopes and the extracted watermark, as well as the kaleidoscope owner's name
                if compscore < maxCompScore:
                    maxCompScore = compscore
                    ownerName = str(currentline[0])

        print(maxCompScore)
        # Display the owner of the user who's kaleidoscope is most similar to the extracted watermark
        print("The owner of this Kaleidoscope is: ", ownerName)
        QMessageBox.information(self, "Kaleidoscope Owner Verified", "Owner Identified: "+ownerName)

# This function displays the user's kaleidoscope that is assigned to them, so they can
# visually analyse and view their unique watermark at anytime that identifies them
    def showUserKaleido(self):
        path = os.getcwd()
        # Use the user's name to extract the kaleidoscope path
        flename = getuserKaleido(self.lblWatermrk.text())
        # Open and display the user's kaleidoscope watermark
        thisKaleidopath = os.path.join(path, flename)
        imgKaleido = Image.open(thisKaleidopath)
        imgKaleido.show()
        time.sleep(10)
        print("Display user's Kaleidoscope")

# Opens the text file containing users and their assigned kaleidoscopes to use the
# given username to obtain and output the filename of the kaleidoscope watermark assigned to them
def getuserKaleido(usrName):
    with open("kUsed.txt", "r") as fs1:
        for linex in fs1:
            currentline = linex.split(",")
            if (currentline[0] == usrName):
                return str(currentline[1])

# ----------------------------- L S B   B I T   F U N C T I O N S --------------------------------------
# Functions for manipulation of bits (shifts etc.) using python's bit functions << >>
# Define max bits for 8bit image and get the max pixel intensity value (2^8 = 256 -> 0-255)
MAX_COLOR_VALUE = 255
MAX_BIT_VALUE = 8
# Creates the image from the given data pixel matrix obtained from LSB encode and decode
# functions and the given image dimensions - width and height for resolution
def make_image(data, resolution):
    image = Image.new("RGB", resolution)
    image.putdata(data)
    return image
# Deletes n number of bits (2 for this software) from an inputted bit value (8bit values in this case)
def remove_n_least_significant_bits(value, n):
    value = value >> n 
    return value << n
# Extracts n (2) LSB from a given 8bit pixel value from the decode function
def get_n_least_significant_bits(value, n):
    value = value << MAX_BIT_VALUE - n
    value = value % MAX_COLOR_VALUE
    return value >> MAX_BIT_VALUE - n
# Extracts n (2) MSB from a given 8bit pixel value (in watermark img) from the encode function
def get_n_most_significant_bits(value, n):
    return value >> MAX_BIT_VALUE - n
# Shifts bits to the left and pads them to occupy 8 bit spaces
def shift_n_bits_to_8(value, n):
    return value << MAX_BIT_VALUE - n

# -------------------- I M A G E  H A S H I N G  F U N C T I O N S  -------------------------------
# Uses the ImageHash library, I would like to give acknowledgement of adapting this comparison from
# johnbumgarner's GitHub (link in sources folder) and adjusting it for bulk image comparisons within
# the kaleidoscope database and extracted images, using aHash from JohannesBuchner's imagehash module
# Compute aHash score for the base image (extracted watermark) used for comparison
def comp_ave_hash_score_base(baseimg):
    basehash = imagehash.average_hash(Image.open(baseimg))
    return basehash
# Compute aHash score for the comparing image (extracted watermark) used for comparison
def comp_ave_hash_score_comp(comparimg):
    comphash = imagehash.average_hash(Image.open(comparimg))
    return comphash
# Calculate the difference in aHash to draw the comparison between the 2 images
def img_similar(basehash, comphash):
    compscore = (basehash - comphash)
    return compscore
# A lower compscore value is indication of higher similarity in image comparison
# ------------------------------------------------------------------------------------------
# Functions used for login and signup screens to hash passwords, test existing accounts
# against input data and perform verifications:

def addUserInfo(userInfo: list):
    # Add a username to the UserDB
    with open('userInfo.txt', 'a') as file:
        for info in userInfo:
            file.write(info)
            file.write(' ')
        file.write('\n')
    # Take one Kaleidoscope out of those available for use from the DB sequentially
    flines = []
    with open('KAvail.txt', 'r') as fp:
        flines = fp.readlines()

    # Got all the available kaleidoscopes, now delete the one that is being used and keep the name
    kaleidoUsed = ""
    with open('KAvail.txt', 'w') as fp:
        # Iterate and append each line, except the chosen and extracted one
        for num, line in enumerate(flines):
            if num > 0:
                fp.write(line)
            else:
                kaleidoUsed = line.strip()

    # Add this kaleidoscope to the used list to make comparisons easier later
    with open('KUsed.txt', 'a') as f1:
        f1.write("\n"+userInfo[0]+",")
        f1.write(kaleidoUsed+",1KDC")



def userAlreadyExist(userName, userPassword=None):
    if userPassword == None:
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line = line.split()
                if line[0] == userName:
                    return True
        return False
    else:
        userPassword = hash_password(userPassword)
        usersInfo = {}
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line = line.split()
                if line[0] == userName and line[1] == userPassword:
                    usersInfo.update({line[0]: line[1]})
        if usersInfo == {}:
            return False
        return usersInfo[userName] == userPassword

# An extra function that replaces whitespaces with - for easier extraction and error
# prevention (EOF) during textfile manipulation for account management
def sanitizeName(userName):
    userName = userName.split()
    userName = '-'.join(userName)
    return userName
# Obtaines and hashes passwords using the hashlib module with sha256
# and hexdigest for encryption of passwords and improved security of user accounts
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()
# Hashes and compares the hash values of a user inputted password from the
# login screen to see if inputted passwords are correct according to the
# text file account database
def check_password_hash(password, hash):
    return hash_password(password) == hash
# -----------------------------------------------------------------------------------------------
# Creates the main window using the Login class and adds the widget to a stack
# for GUI execution and window transition management
app = QApplication(sys.argv)
mainWindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(420)
widget.setFixedHeight(395)
widget.show()
app.exec_()
# Author: Rikesh Kylas
