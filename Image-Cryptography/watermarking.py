from PIL import Image
import matplotlib.pyplot as plt

image = Image.open("watermarking.jpg").convert("RGBA")
logo = Image.open("Nike-Logo.png").convert("RGBA")
logo.thumbnail((250, 250))
image.paste(logo, mask=logo)
plt.imshow(image)
plt.show()
