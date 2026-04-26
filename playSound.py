import serial
import pygame

# Initialize pygame mixer
pygame.mixer.init()
sound1 = pygame.mixer.Sound("Rare Achievement - Minecraft Sound Effect (HD).mp3")
sound2 = pygame.mixer.Sound("Minecraft Lava Death - Sound Effect.mp3")

# Connect to the Pico (change COM3 to your port)
ser = serial.Serial("/dev/tty...", 115200, timeout=1)

print("Listening for Pico commands...")

while True:
    line = ser.readline().decode("utf-8").strip()
    if line == "PLAY_WIN_SOUND":
        print("Playing sound!")
        sound1.play()
    if line == "PLAY_OVERLOAD":
        print("Playing sound!")
        sound2.play()