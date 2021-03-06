# COMPHonoursProject
Digital Watermarking using LSB - COMP700 Honours Project by 218005822 (RIkesh Kylas)

------------ Kaleidoscope Digital Watermarking System Execution Steps ---------------

Welcome to the step by step guide on how to operate this software:

------------------------------------- E X E C U T I O N ----------------------------------------

* Multiple files (Dependancies) and a Single exe file:
 
1) Simply extract and locate the folder in which all program files, dependencies and python files 
   are located.
     (Ensure the folder with these operation files is unzipped and stored locally)
     
2) Locate the DigitalWatermarking.exe file in the root of this file and simply double click
to execute this program. 

3) After a short wait, you will then be prompted with the GUI login screen of this system in which
you can follow the User guide manual (provided with screenshots and instruction steps in sequence)
provided to learn how everything works with visual examples
OR Skip below to the 'GUI RUNTIME' section for quick run instructions.


NOTE: All image files for digitally watermarking, watermark extraction as well as user identification
must be stored in the same file directory/path as this .exe file for successful usage.

* Python IDE Run:

1) Open main.py using an IDE (preferrably PyCharm) and run the build, GUI will display and continue.
   (Dependancies must be in this program folder and required libraries must be installed)

NOTE: All image files for digitally watermarking, watermark extraction as well as user identification
must be stored in the same file directory/path as this .py file for successful usage.

# Dataset included as folder KDb with submission (small dataset - no link required to download)
# Sample account details for quick testing:
# Username: content creator
# Password: 0123456789012
------------------------------------------------------------------------------------------------------

This software will NOT run in an IDE that does NOT support UI files and GUI execution (such as colab)

----------------------------------- G U I     R U N T I M E --------------------------------------------

1) As a new user, you should locate the Sign Up button in the bottom right corner of the GUI interface
and click it to be redirected to a Sign Up page.

2) On this Sign up page, as a new user, you are required to input:
*Username - which should strictly be your content creator ID and prefferably in the format "Name Surname"
*Password - this should be your 13 digit ID number, which is a secure unique identifier for each user, this
            ensures safety and authenticates uniqueness to each registered user.
*Confirm Password - this is a security measure taken to ensure you retype the password and that it matches
                    your previously entered ID number, to help avoid mistyped input and allow users to 
                    remember their accounts for sign up next time.

3) Hereafter, upon successful registration, you will be taken back to the log in screen where you can use
the account details you entered to log into the system.

4) Entering your correct login details will take you to the LSB Digital Watermarking system.

5) Here, you will be able to perform digital watermark functions, identify users and view your watermark: 
+View your kaleidoscope:
-  Clicking this button located on the top right of this video will display the Kaleidoscope collage
   watermark assigned to you by the system which will be used to identify your watermarked content
   and authenticate your content. Every user's kaleidoscope is unique and resembles their digital
   signature in this system. View your kaleidoscope to know what gets embedded behind your content.

LSB encoding and decoding techniques for digital watermarking + watermark extraction:
+Digitally watermark an image by (middle left section of this window):
- Placing your image file to watermark in the same directory as this software and then enter the name of
  the image file (eg. myArt.jpg) in the textfield space provided. (Ensure jpg images are used!!!)
  ( A sample image to test this program, named 'pepper.jpg' is provided for testing purposes)
- After clicking the button to encode, you will then recieve a message upon successful encoding and the 
  encoded watermark will be displayed, as well as the output watermarked image file name (called 'encoded.png'
  by default) will be generated and saved to the same file directory of this software.
  
+Digital watermark extraction (middle right section) can also be performed in a similar process, but with same 
storage instructions given above, as well as user input required for the encoded images' filename.

6) User identification tool (bottom right corner of this window):
-  This tool enables the ownership authentication function required to protect copyright infringements and 
   give due credit to content owned by creators.
-  NOTE: This step should ONLY be done upon decoding a digitally watermark, because after watermark image
   extraction, the system labels the extracted watermark as 'decoded.png' and utilizes the identification
   process upon the fact that this image is purely extracted from a watermarked image of this software and
   not an external image that is not a kaleidoscope watermark or relevant image at all for comparison to 
   identify users within this software's database.

All these functions give the system complete functionality and this system can be closed and reopened at any
time using the above steps to log in (accounts will be saved securely) and watermark content at any time, as
well as extract watermarks from watermarked content and verifiy ownership of images encoded using this system.

EXTRA FEATURE: This system does have the ability to decode any possible LSB encoded images (external to the system) which
are not kaleidoscope collages that authenticate users in this system. However, owner identification will not be possible
and using the tool in (6) might cause system failures.
