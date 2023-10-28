# Canvas of the Conquered

Tags: Peter Scottsen, accessible
: Koray Akduman, Addison Goolsbee

# Canvas of the Conquered

[https://github.com/AddisonGoolsbee/blindfold-art](https://github.com/AddisonGoolsbee/blindfold-art)

Gamma Gary, formerly a famous artist, was blinded during the Seige of Smelton Keep and subsequently exiled. Now, Gamma Gary must team up with the exiled former war criminal Peter Scottsen to regain his artistic abilities and return home.

## How to Play

You and your teammate play the roles of Gamma Gary and Peter Scottsen. Together, you will create a sketch of a random object.

Gamma Gary paints by holding a black box to his nose. By varying the amount of force with which Gary shoves his face into the box, Gary can vary his brush thickness. Gary can look up or down, and tilt his head left or right, to move the position of the cursor. He must have both hands on the box in order to paint.

Peter Scottsen should offer (or yell) instructions to Gamma Gary, keeping in mind that the objective of the game is to create a coherent drawing of the word displayed on the screen in a limited 1-minute time frame.

The game can be played with 2+ players. If more than 2 players want to play, multiple Peter Scottsens can vie for Gamma Gary’s attention, increasing the chaotic nature of the game. Teams can also be formed, showing which pairing has the best chemistry among the individuals playing.

### Example

Running at boot:

[https://youtu.be/FT7aO8jUFfY](https://youtu.be/FT7aO8jUFfY)

Playing a full game:

[https://youtu.be/JQTGooub0d4](https://youtu.be/JQTGooub0d4)

## Design Process

### Software

This project created the most integrated codebase of our projects so far. We used the Python Pygame that we used for Module 1 to draw the output from the remote, and we used code for the ESP32 often modeled after that in Module 2. We used new techniques for Module 3 for wireless connectivity, allowing for a more involved experience. With one user being blindfolded and moving, this also improves the safety restrictions regarding tripping over wires. And it looks SICK (in a cool way rather than a diseased way).

The most difficult part here was the cursor to show the position of the brush. With the limitations of Pygame, we ran into a problem where the cursor would erase the white brush marks made earlier in the game. We could not find a way to eliminate this problem without using too many resources and creating added latency when running on the Raspberry Pi. In the end, the lines created by the cursor did not significantly affect the final project or the process other than being a minor annoyance, so we opted to live with them.

An unavoidable limitation of this project was that it had to run on the Raspberry Pi. Our code was performance-intensive for the Pi, requiring us to heavily optimize the Python code so the Pi could process it with limited latency. While we optimized the code, it was not as sufficient as we were hoping, and there is still some latency when using the Pi. One could argue that this latency creates even more of an unseen effect, though, and that the second player (i.e. Peter Scottsen) must think ahead before giving instructions.

### Hardware

This project uses 3 primary forms of sensor input:

- A force sensor: detects the force with which “Gary” shoves his nose into the device to vary the thickness of the brush.
- An accelerometer: records X, Y, and Z accelerometer data which is later used to calculate pitch and roll to adjust the position of the cursor.
- A homemade touch sensor: using two metal bolts, it uses Gary’s body to create a complete circuit. This enables restarting the game when the players switch, and the sensor enables a requirement that the device is held with both hands, forcing Gary to paint using his nose.
- A switch enables/disables the battery power.

While the sensors were few, each came with their own unique set of problems, and troubleshooting these problems were the most time-intensive part of this project.

Obtaining a formula to calculate pitch and roll from X, Y, and Z accelerometer data proved difficult, as did obtaining the accelerometer data in the first place. The data is communicated over an I2C protocol, requiring us to read 6 8-bit registers from the accelerometer to obtain 3 16-bit values.

The force sensor is extremely finnicky, an initial bug that we partially embraced and partially corrected. We remounted the sensor a couple of times to obtain a background level of force, and we embraced the additional noise and delay in the force sensor’s input as a source of randomness that would make the output less 1-to-1.

The touch sensor was most fascinating. Our device would work with Koray but not Addison, puzzling us over its incredible ability to discriminate between its players. We learned that it also worked with Addison’s tongue, leading to the discovery that Koray is a more conductive person than Addison due to Koray’s sweatier hands. After Addison began wetting his hands with water, the touch sensor worked for him as well. This surprise opened a new tradition, making some people worthy of being Gamma Gary while others must dip their hands in a concoction of conductivity (i.e. water) before playing.

Our ESP32 burned once. Just once though! We predict that this was because the ESP32 was connected to USB power and 5V power simultaneously, burning out the ESP32 in a relatively short period of time. We ensured that the second ESP32 was disconnected from battery power until we absolutely needed it, making sure to disconnect from USB power before enabling battery power.

### Assembly

We were confused regarding ideation for a while. Removing 1-to-1 interaction and creating an “unseen effect” proved conceptually difficult, especially when creating a 2-player game. With most games, a user must observe the effects of their actions immediately to receive feedback about how they are doing in the game and improve their performance. We created two distinct roles in the game that effectively work together, creating an additional artwork consisting of the chemistry and teamwork between the two players. The sketch, while fun to create and look at, is ultimately not the primary form of artwork that our project creates.

We first assembled the components individually, spoofing data from the accelerometer with a sine function to explore the full range of motion, and spoofing data for hand input and nose force as well. This enabled us to split work more effectively and assemble the software and hardware simultaneously rather than creating a back-and-forth cycle between the two. We had a mostly-working program relatively quickly that could work with some components missing, allowing for better program development over time and a more effective assembly that reflected the intended functionality.

![Untitled](Canvas%20of%20the%20Conquered%209649b32d6a8e400ab6980500b9ba77a7/Untitled.png)

**Figure 1**: Spoofing data initially, then assembling the circuit outside of the container, allowed for more efficient program development and debugging.

Keeping in mind that this device was meant to last 2-weeks without any intervention, we wanted to minimize power usage and determine the amount of energy storage that we needed. Using 2x 3000mAh at 3.7V / 11.1 Wh batteries, and measuring the current draw at 65mA at 5.0V / 0.33W  on average, we determined that our contraption would have approximately 68 hours of usage available with 2 fully charged batteries, allowing for 2 weeks of ~34 hour usage each — a reasonably high estimate.

![Untitled](Canvas%20of%20the%20Conquered%209649b32d6a8e400ab6980500b9ba77a7/Untitled%201.png)

**Figure 2**: We measured the current draw to determine the necessary power supply for the circuit.

Our final assembled circuit did not fit in one project box (we could not find any of the large project boxes we used for Wattage Warlords), so we taped two smaller project together in a seamless fashion to ultimately create a clean product. As the CEID was out of super glue and hot glue, and because Elmer’s glue proved too weak, many components, such as the switch, were held together with friction. The inside of the box contains layers of foam board that apply pressure between the battery pack and the switch, preventing both from jiggling due to the friction with the box walls.

![Untitled](Canvas%20of%20the%20Conquered%209649b32d6a8e400ab6980500b9ba77a7/Untitled%202.png)

**Figure 3**: the completed box, showing an on/off switch, two handles functioning as a touch sensor, and a force sensor that is pushed with one’s nose.

### End Results

![Untitled](Canvas%20of%20the%20Conquered%209649b32d6a8e400ab6980500b9ba77a7/Untitled%203.png)

![Untitled](Canvas%20of%20the%20Conquered%209649b32d6a8e400ab6980500b9ba77a7/Untitled%204.png)

**Figure 4**: Our fairy, in-progress, created by Koray giving Addison instructions during an original 2-minute period. This period was later reduced to 1-minute after we played the game and realized that our 2-minute estimate was longer than it actually should have taken.

![IMG_0308.jpg](Canvas%20of%20the%20Conquered%209649b32d6a8e400ab6980500b9ba77a7/IMG_0308.jpg)

****************Figure 5****************: We maintained a circuit diagram as we completed the project, ultimately producing the diagram above.