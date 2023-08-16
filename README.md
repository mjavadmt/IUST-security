# IUST Security Course

## Image Cryptography

### Steganography
steganography is the process of hiding a message inside a photo. The message could be image or text. In this project I implemented both text and image hiding. It will hide the message in LSB(Least Significant Bit) of image in a consecutive way. So that putting this LSB next to each other will form a meaningful message. The fantastic part of it is that the image doesn't change at all because modifying LSB has the least effect in display of an image.
For text extracting I also implemented meaningfulness of a text. this operation was done based on english dictionary.

- main image after hiding

<p align="center">
<img src="./Image-Cryptography/merged.jpg" heigth="400" width="400">
</p>

- extracted image

<p align="center">
<img src="./Image-Cryptography/splitted.jpg" heigth="200" width="200">
</p>