# File Injector

#### If you want to use a previous version (1.0.2 or lower), where you needed the original image to extract the file, you can download it [here](https://github.com/carlospuenteg/File-Injector/archive/refs/tags/v1.0.2.zip).

## Index
* [1. Description](#1-description)
* [2. Getting Started](#2-getting-started)
  * [Install requirements](#install-requirements)
  * [Run the script](#run-the-script)
  * [Choose input](#choose-input)
    * [Choose a base image](#choose-a-base-image)
    * [Choose an input file](#choose-an-input-file)
    * [Choose/Generate an encryption key](#choosegenerate-an-encryption-key)
* [3. Results](#3-results)
* [4. Examples of use](#4-examples-of-use)
  * [Injection](#injection)
  * [Extraction](#extraction)
* [5. Configuration](#5-configuration)
* [6. What it does](#6-what-it-does)
* [7. How it works](#7-how-it-works)
  * [Options](#options)
  * [inject_file_func](#inject_file_func)
  * [extract_file_func](#extract_file_func)
  * [get_fernet](#get_fernet)
  * [decrypt_content](#decrypt_content)
  * [inject_file](#inject_file)
  * [extract_file](#extract_file)



## 1. Description

File Injector is a script that allows you to **store any file** (`.zip`, `.png`, `.txt`, `.gba`...) and its **filename** in an **image** as **noise**, using [steganography](https://en.wikipedia.org/wiki/Steganography).

You can also choose to **encrypt** the input file before storing it.

Then, to **extract** the file from the modified image, you **DON'T need the original image**, just the **encryption key** if the file has been encrypted.




## 2. Getting Started

### Install Requirements

```bash
python3 -m pip install -r requirements.txt
```
If that doesn't work, you can try:
```bash
py -m pip install -r requirements.txt
```


### Run the script

```bash
python3 main.py
```


### Choose input

#### Choose a base image

**Choose** a base image for storing/retrieving the file from the `files/base-images` folder.

You can add your **own** images to this folder. They can be `.png` or (`.jpg`/`.jpeg`), but they will be converted to `.png` when the script is run.


#### Choose an input file

**Choose** a file to be stored in the image from the `files/input-files` folder.

You can add your **own** files to this folder. It can be any file type.


#### Choose/Generate an encryption key

You can **choose** a key from the `files/$encryption-keys` folder or **generate** one there.

The key file must have the `.key` extension

You don't need to choose a particular one when decrypting a file, it will be selected automatically from the folder.



## 3. Results

<img src="readme-assets/17'1MP_mod.png" width=500>

This **17.1MP** image contains an **encrypted** **9MB** `.zip` file and its **filename** stored in the noise.

<img src="readme-assets/1'7MP_mod.png" width=500>

This **1.7MP** image contains an **encrypted** **0.93MB** `.zip` file and its **filename** stored in the noise.



## 4. Examples of use

### Injection

```text
... File-Injector % python3 main.py
[0] EXIT
[1] Inject file
[2] Extract file

Option: 1
File to be stored: images.zip
Filename of the base image: 2'2MP
Encrypt the file? (y/n): y

Do you want to use an existing key or generate a new one?
[0] Existing key
[1] New key

Option: 1
Filename of the new key file (blank for default): 
Key generated and saved to files/$encryption-keys/key9.key

Preparing...

Modified bits per channel: 2
Image modification: 1.56%

✅ Storing... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ [100.0%]

Generating random values...

Storing random values...

Reshaping...

Modified image saved in files/modified-images/2'2MP_mod.png

Done in 7.5892 seconds
```

### Extraction

```
... File-Injector % python3 main.py
[0] EXIT
[1] Inject file
[2] Extract file

Option: 2
Filename of the modified image: 2'2MP_mod

Preparing...

Retrieving filename...

Retrieving input file...
Decrypted with "files/$encryption-keys/key2.key"

Output file saved in files/output-files/images.zip

Done in 1.4083 seconds
```



## 5. [Configuration](config.py)

You can change the configuration in the [config.py](config.py) file.

| Constant | Description | Default value |
|-|-|-|
| `MOD_PREFIX` | Prefix the modified image will have | `""` |
| `MOD_SUFFIX` | Suffix the modified image will have | `"_mod"` |
| `STORE_RANDOM` | Store random data in the modified image so that the limit between the part with the stored data and the part without is not so obvious | `True` |
| `TEST_MODE` | Enables/Disables Test Mode: Test with predefined images and files | `True` |




## 6. What it does

The **injection** is done by **storing** the information in the **X less significant bits** of the image's **channels**
- Each channel (R, G and B) has **8 bits**, and this script changes from **1 to 4** bits of each channel, depending on the **size** of the file to be stored.
- If you store a bigger file, **more bits** will be changed and the changes will be **more noticeable**.
- If you store a smaller file, **less bits** will be changed and the changes will be **less noticeable**.
- If you choose to **encrypt the file**, its **size will increase by ≈1/3**.

| Changed bits | ≈Image size (MP) | ≈Max file size (MB)  |
| :-: | :-: | :-: |
| 1 | 1 | 0.375 |
| 2 | 1 | 0.5 |
| 3 | 1 | 0.75 |
| 4 | 1 | 1.5 |




## 7. How it works

### Options

| Option | Description |
|-|-|
| [0] EXIT | Exit the script |
| [1] Inject file | Calls [`inject_file_func()`](#inject_file_func) |
| [2] Extract file | Calls `extract_file_func()` |


### [`inject_file_func()`](menu.py)

1. If `TEST_MODE` == `True`, it will use the predefined base image and file. Otherwise, it will ask for the input file and the base image.
2. Read the file
3. Read the image and store it in a numpy array
4. If the user wants to encrypt the file:
   1. Get the key with [`get_fernet()`](#get_fernet)
   2. Encrypt the file and filename
5. Convert the file and filename to hexadecimal
6. Try to inject the hexadecimal file and filename in the image with [`inject_file()`](#inject_file). 
   1. If the image is too small to store the file, raise an error
   2. Else, return the modified image.
7. Save the modified image


### [`extract_file_func()`](menu.py)

1. If `TEST_MODE` == `True`, it will use the predefined modified image. Otherwise, it will ask for the modified image.
2. Flatten the modified image
3. Extract the hexadecimal file and filename with [`extract_file()`](#extract_file)
4. If the file and filename have been encrypted (they start with `gAAAAA`), decrypt them with [`decrypt_content`](#decrypt_content)
5. Decode the filename to **UTF-8**
6. Save the file with the decoded filename


### [`get_fernet()`](utils/cryptography.py)

| Option | Description |
|-|-|
| [0] Existing key | Use an existing key |
| [1] New key | Generate a new key |

[0] Existing key
1. Choose a key to use from the `files/$encryption-keys` folder

[1] New key
1. Choose a filename for the new key (or leave it blank for the default one (e.g. **key8.key**))
2. Generate a new key and save it with the chosen filename
3. Return the Fernet object with the new key


### [`decrypt_content()`](utils/cryptography.py)

1. For each key in the `files/$encryption-keys` folder:
   1. Try to decrypt the file and filename with it
   2. If **InvalidToken** is raised:
      1. It means that the key is not the right one
      2. Try with other key
   3. Else, return the key
2. If no key is found, raise an Exception


### [`inject_file()`](utils/injection.py)

| Parameter | Type | Description |
|-|-|-|
| `img_arr` | `np.ndarray` | Image as a numpy array |
| `file` | `str` | File in hexadecimal |
| `filename` | `str` | Filename in hexadecimal |
| `store_random` | `boolean` | Whether or not to store random data in the modified image |

returns the **modified image array** (not flattened `np.ndarray`)


### [`extract_file()`](utils/injection.py)

| Parameter | Type | Description |
|-|-|-|
| `mod_img_arr_flat` | `np.ndarray` | Flattened modified image |

returns a **dictionary** with the extracted **file** and **filename**, both in (`bytes`) format