from time import sleep
from rpi_TM1638 import TMBoards
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


STB = 14
CLK = 15
DIO = 18

TM = TMBoards(DIO, CLK, STB, 0)
TM.clearDisplay()

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 2

# Use for I2C.
#i2c = board.I2C()
#oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Use for SPI
spi = board.SPI()
oled_cs = digitalio.DigitalInOut(board.D5)
oled_dc = digitalio.DigitalInOut(board.D6)
oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

# Load default font.
font = ImageFont.load_default()

# Draw Some Text
text = "On a scale of 1-8 how well are you feeling?"
(font_width, font_height) = font.getsize(text)
draw.text(
    (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
    text,
    font=font,
    fill=255,
)

# Display image
oled.image(image)
oled.show()

for n in range(128,-128,-1):  #these numbers should be calculated by the width of the text
        draw.text(
            (n, oled.height // 2 - font_height // 2),
            text,
            font=font,
            fill=255,
        )

        # Display image
        oled.image(image)
        oled.show()
        sleep(0.005) # How fast the screen refreshes
        draw.rectangle(  #delete innermost area
           (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )
while True:
    for i in range(8):
        TM.leds[i] = True if TM.switches[i] else False