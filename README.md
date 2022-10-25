# File Inyector

## Index
* [Description](#description)
* [Getting Started](#getting-started)
  * [Install requirements](#install-requirements)
  * [Store an image](#store-an-image)
  * [Run the script](#run-the-script)
* [Results](#results)
* [Configuration](#configuration)
* [How it works](#how-it-works)
  * [Added/Subtracted bpp (bits per pixel)](#addedsubtracted-bpp-bits-per-pixel)
  * [Bit storing](#bit-storing)
  * [Process](#process)

## Description

File Injector is a script that allows you to **store any file** (`.zip`, `.png`, `.txt`, `.gba`...) and its **filename** in an **image** using [steganography](https://en.wikipedia.org/wiki/Steganography). 

You can also choose to **encrypt** the stored file.

Then, if you have the **original** image (and the **encryption key** if the file has been encrypted), you can **extract the file** from it.




## Getting Started

### Install Requirements

```bash
python3 -m pip install -r requirements.txt
```


### Run the script

```bash
python3 main.py
```


### Choose input

#### Choose a base image

Choose a base image for storing/retrieving the file from the `files/base-images` folder.

You can add your own images to this folder. They can be `.png` or `.jpg`, but they will be converted to `.png` when the script is run.


#### Choose a file

Choose a file to be stored in the image from the `files/input-files` folder.

You can add your own files to this folder. It can be any file type.


#### Choose/Generate an encryption key

You can choose a key from the `files/$encryption-keys` folder or generate one there.

In that folder, can store an encryption key (that you or other user has generated with this script)

The key file must have the `.key` extension

But you don't need to choose a particular one when decrypting a file, it will be selected automatically from the folder.


### Examples of use

#### Encryption

<img src=readme-assets/example_encryption.png width=400>

#### Decryption

<img src=readme-assets/example_decryption.png width=400>




## Results

#### Comparison between the original and the modified image

The bigger the image, the more difficult it is to notice the difference (the difficulty grows exponentially, since with more pixels you can store more data and it is more difficult to notice the noise when zoomed out). This one is 17.1MP.

| Original | Modified |
|-|-|
| <img src=readme-assets/base_img.png width=400> | <img src=readme-assets/mod_img.png width=400> |





## Configuration

You can change the configuration in the [config.py](config.py) file.

| Constant | Description | Default value |
|-|-|-|
| `MOD_PREFIX` | Prefix the modified image will have | `"mod_"` |
| `MOD_SUFFIX` | Suffix the modified image will have | `"_mod"` |
| `STORE_RANDOM` | Store random data in the modified image so that the limit between the part with the stored data and the part without is not so obvious | `True` |
| `TEST_MODE` | Enables/Disables Test Mode (test with predefined images and files) | `True` |




## How it works

### Added/Subtracted bpp (bits per pixel)
When you are storing a file, `Added/Subtracted bpp (bits per pixel): n` will appear on your terminal.

These are the number of bits that will be added or subtracted to/from each pixel of the image. Divide it by 3 to get the number of bits that will be added or subtracted to/from each color channel of the pixel.

`n` can be `3, 6, 12, 24, 48`, depending on the size of the file compared with the number of pixels of the base image.

The **bigger the image** and the **smaller the file**, the less `n` will be and the **better** the final result will be.

If the file is too big in comparison with the image, the error: `Image is too small to store the file` will appear.


### Bit storing

- **N**: Bits that we want to add
- **V**: Value of the channel (0-255)
  
If `N + V <= 255`: `V = 255 + N`
Else: `V = V - C`


### Process

#### `main.py`

1. Creates the 5 folders within the `files`folder if they don't exist.
2. Converts all the non-png images within the `base-images`folder to `.png`
3. Runs the [menu](#menu-in-menupy) function


#### `menu()` (in [menu.py](menu.py))

1. Asks the user to choose an option from the menu
   - [0] EXIT
   - [1] [Store file](#store_file_func-in-menupymenupy)
   - [2] [Retrieve file](#retrieve_file_func-in-menupymenupy)


#### `store_file_func` (in [menu.py](menu.py))

1. If you aren't in **TEST_MODE**, you will be asked to:
   - Choose a file to be stored from the `files/input-files` folder.
   - Choose a base image from the `files/base-images` folder.
2. The input file is read in binary mode and stored in a variable, as well as its filename
3. The image is read with the `PIL` library and stored in a numpy array
4. If you choose to **encrypt the file**:
   - You will be asked to either choose an encryption key from the `files/$encryption-keys` folder or generate a new one and store it there.
   - If you choose to generate a new one, it will be generated and stored in the `files/$encryption-keys` folder
   - The encryption key is loaded and used to encrypt the file and filename
5. The input and the filename are converted to hexadecimal
6. [store_file()](#store_file-in-noise_storerpynoise_storerpy) is called:
   - Parameters: Hexadecimal input, hexadecimal filename, Image array
   - Returns: Modified image array
7.  Saves the modified image array in the `files/modified-images` folder


#### `retrieve_file_func()` (in [menu.py](menu.py))

1. If you aren't in **TEST_MODE**, you will be asked to:
   - Choose a base image from the `files/base-images` folder.
   - Choose a modified image from the `files/modified-images` folder.
2. The input images are read with the `PIL` library, then converted to a numpy array, then flattened and then converted to **int8**
3. [retrieve_file()](#retrieve_file-in-noise_storerpynoise_storerpy) is called:
   - Parameters: Base image array (flattened, int8), Modified image array (flattened, int8)
   - Returns:, File content in bytes, Filename in UTF-8
4. If the text starts with `gAAAAA`, it means that it is encrypted and it will be decrypted with [decrypt_content()](#decrypt_content-in-utilscryptographypyutilscryptographypy)
5. The output file content is saved in the `files/output-files` folder, with the filename that was retrieved


#### `store_file()` (in [noise_storer.py](noise_storer.py))
- Parameters: Hexadecimal input, hexadecimal filename, Image array
- Returns: Modified image array
1. Save a flattened image array in a variable
2. Calculate the base (= maximum added/subtracted bits to each pixel + 1):
   - Calculate the number of available pixels by subtracting from the length of the flattened image array:
     - 1 (for storing the base of the image)
     - Maximum size that the filename can have (when converted to binary)
   - Calculate `div` (number of times the hex input is bigger than the number of available pixels) by dividing the avaliblable pixels by the length of the hexadecimal input 
     - `div == 0`:
     - `div >= 4`: base = 2
     - `div >= 3`: base = 4
     - `div >= 2`: base = 8
     - `div >= 1`: base = 16
     - else: raises exception: "Image is too small to store the file"
3. Change the base of the hexadecimal input and the filename to the obtained base
4. [Store](#bit-storing) `base-1` on the first pixel
5. [Store](#bit-storing) the hexadecimal filename on the next pixels
6. [Store](#bit-storing) a divider (the base)
7. [Store](#bit-storing) the hexadecimal input
8. [Store](#bit-storing) a divider (the base)
9. [Store](#bit-storing) random data on the remaining pixels
10. Reshape the flattened image array to the original shape of the image


#### `retrieve_file()` (in [noise_storer.py](noise_storer.py))
 - Parameters: Base image array (flattened, int8), Modified image array (flattened, int8)
 - Returns:, File content in bytes, Filename in UTF-8
1. Get `diff`: Numpy array created by subtracting the base image array from the modified image array
2. Calculate the **base** = `diff[0] + 1`
3. Find the dividers (the base) from the `diff` array
4. Get the filename and the input file's content from the `diff` array and convert them to hexadecimal
5. Convert the hexadecimal filename to bytes and then to UTF-8
6. Convert the hexadecimal input content to bytes
7. Return the filename in UTF-8 and the input content in bytes


#### `decrypt_content()` (in [utils.cryptography.py](utils/cryptography.py))

1. Try to decrypt the content with every key in the `files/$encryption-keys` folder
2. If the decryption is successful, return the decrypted file content and filename, else raise an exception
