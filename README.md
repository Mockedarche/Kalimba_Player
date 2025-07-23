SPECIAL THANKS TO 

https://github.com/kevinmcaleer/pca9685_for_pico

AND

https://www.instructables.com/ESP32-Micro-SD-Card-Interface/

AND

https://github.com/0x3b29/Electric-Kalimba

This is a place for all my files related to my prototype of a ESP controlled Kalimba player


I've written drivers for different hardware but ultimately for a prototype it would likely take longer than the protoype. Both of these for the PCA9685 (with servo support) and that sdcard driver for micropython sped things up a lot.


This project is my prototype at a automatic kalimba player. I expect this over the next few months will get pushes all giving more support. Importantly this is a place for all files related to this project. Meaning CAD files, Notes, Python scripts, C/arduino code, microhydra code, etc. I ended up editing every STL provided by @olivier.berlin.
This project was fun but will likely be a bit more of a back burner project. Essentially this project is as follows 
1. Cardputer controls the kalimba player either directly saying what notes to play or it selects a song.
2. Kalimba player plays the tines as instructed by either the cardputer or the selected song

This is one of those projects were execution is the most important factor in the quality of the project. As such I came up with my own way of controlling, creating, and tuning each "pluck" as shown by the stls and all the code. Oliver wasn't my source of inspiration for the project and had been day dreaming about it for quite. Seeing their video showcased a really good stepping off point with the included cad files so thanks.


Things I'm happy with the project. 
1. Code it works reliably and in a determistic manner (different input combinations results in a intended behavior)
2. The cardputer controller software looks relatively nice and has a lot of really cool functionality such as playing songs, live playing (presses tell kalimba to play that tine), recording songs meaning you can play something live or in demo mode and save it wirelessly to the kalimba over local wifi, the kalimba player has an SD card so it can keep songs and there isn't any inherent limitation of length, speed, etc.
3. The kalimba player plays reliably and consistently meaning sounds are really constant and importantly the plucks piece that actually touches the tines are made from TPU meaning they will last an incredible amount of time.

Things that aren't satisfactory with this project
1. Code maturity is still really young. Often times the naive way was chosen and while nothing is really unoptimized im sure it could use less resources and be faster (especially connecting to the kalimba).
2. Sound quality of the kalimba player I can say with a lot of certainty that Oliver (third link) will admit that this doesn't sound as nice as a even decent person playing it. The plucks are one strength, sound different on pressing down vs lifting, and in my case the force required actually causes vibrations in the metal wire causing sound.


Things to do
1. Commect all of the code files to make picking the project up easier
2. Tune each pluck by changing the TPUs thickness and length so that keys are played in a more natural way.
3. Build some kind of case for the entire player that includes a sound chamber for the Kalimba
4. Create a desktop app that allows atleast selecting a song
5. Lube the servos to reduce their sound
6. find a way to dampen or completely cancel out the sound made by the metal wires on pluck


This is a back burner project im moving onto creating a 5 legged robot similar to https://youtu.be/IvK2I_ASXLo  

Photos
Kalimba controller (cardputer)
![](https://github.com/Mockedarche/Kalimba_Player/blob/main/Photos/IMG_3504.png)

Kalimba Player
![](https://github.com/Mockedarche/Kalimba_Player/blob/main/Photos/IMG_3505.PNG?raw=true)




