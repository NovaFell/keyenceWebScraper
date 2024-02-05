

This is a python application that bypasses some keyence bs and makes monitoring the video feed from their webpage easier and usable on monitor screens in industrial settings.

Keyence does a thing where you can go to their vision sensor webpages and see the live video feed, but they make it very difficult to pull that video feed to isolate it for monitoring purposes. They also make things difficult by not having the url to the video be an actual mjpeg, but instead, be a bunch of updating still images that changes the url every second.

You are probably asking, "Wait a minute, keyence allows you to buy a monitor to view these. Why don't we just buy one?"

The issue is that keyence did more bs to make clients rip their hair out by only allowing one monitor to view the camera feed at a time.

Screw that.

This code bypasses keyence shitfuckery using BeautifulSoup4 and selenium so that you can have access to the video feed on as many monitors as your heart desires.

This code has been made in such that by changing the url variable, you can pull the live video feed from any kenece vision sensor webpage.

STEPS TO MAKE THIS WORK:

    Change the url on line 26 to be the address of the main page of the keyence vision sensor web view

    Save the file.... duh, but you wouldn't believe how many times I have forgotten to save and wondered why my changes are not working

    run the command pip install pyinstaller. This is the program that I used to turn the python script into an executable which is easier for the operators to use.

    run the command pyinstaller .\webscraper.py --name nameOfTheCameraYouAreUsing --onefile -w. --name changes the name of the executable, --onefile creates the executable in a single file for easier deployment, -w makes the executable run without a stdout terminal and just runs the program.

    running this command will create a few folders and files, the one that is important is in the dist folder that is created. This is the executable that you will install on whatever machine you are trying to monitor the vision sensor from.

NOTES:

    If you are running into issues with the program not running on the machine, do these STEPS

    verify that google chrome is installed. this program was made for chrome and chrome only. edge and firefox do not work with this program. make sure that chrome is installed on the machine
    move all the files that the pyinstaller command created to the machine you are trying to run the executable from. IDK why, but sometimes the executable does not always have all the dependencies built into it, which is should, and needs them to be there on first startup. you can delete them or put them somewhere else after first startup.

anyways, that is all. if you run into any issues with this program, there is an issues tab above. create an issue request and i'll get to it.
