# File Injector

#### If you want to use a previous version (1.0.2 or lower), where you needed the original image to extract the file, you can download it [here](https://github.com/carlospuenteg/File-Injector/archive/refs/tags/v1.0.2.zip).

## Index
* [1. Description](#1-description)
* [2. Getting Started](#2-getting-started)
  * [Install requirements](#install-requirements)
  * [Run the script](#run-the-script)
  * [Choose input](#choose-input)
    * [Choose a base image/audio](#choose-a-base-imageaudio)
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

File Injector is a script that allows you to **store any file** (`.zip`, `.png`, `.txt`, `.gba`...) and its **filename** in an **image/audio** as **noise**, using [steganography](https://en.wikipedia.org/wiki/Steganography).

You can also choose to **encrypt** the input file before storing it.

Then, to **extract** the file from the modified image/audio, you **DON'T need the original image/audio**, just the **encryption key** if the file has been encrypted.




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

#### Choose a base image/audio

**Choose** a base image/audio for storing the file from the `files/base` folder.

You can also add your **own** images/audios to this folder. 
- The images can be `.png` or (`.jpg`/`.jpeg`), but they will be converted to `.png` when the script is run.
- The audios have to be `.mp3` or `.wav`, but they will be converted to `.mp3` when the script is run.


#### Choose an input file

**Choose** a file to be stored in the image/audio from the `files/input` folder.

You can add your **own** files to this folder. They can be any type of files.


#### Choose a modified image/audio

**Choose** a modified image/audio for extracting the file from the `files/modified` folder.

You can also add your **own** modified images/audios to this folder.


#### Choose/Generate an encryption key

You can **choose** a key from the `files/$encryption-keys` folder or **generate** one there.

The key file must have the `.key` extension

You don't need to choose a particular one when decrypting a file, it will be selected automatically from the folder.



## 3. Results

This **17.1MP** image contains an **encrypted** **9MB** `.zip` file and its **filename** stored as noise.

<img src="readme-assets/17'1MP_mod.png" width=500>


This **1.7MP** image contains an **encrypted** **0.93MB** `.zip` file and its **filename** stored as noise.

<img src="readme-assets/1'7MP_mod.png" width=500>


This **42MB** audio file contains an **encrypted** **9MB** `.zip` file and its **filename** stored as noise.

https://user-images.githubusercontent.com/65092569/202014519-24514110-4bd2-4c2b-9307-237964df0c2b.mp4





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
| `MOD_PREFIX` | Prefix the modified image/audio will have | `""` |
| `MOD_SUFFIX` | Suffix the modified image/audio will have | `"_mod"` |
| `STORE_RANDOM` | Store random data in the modified image so that the limit between the part with the stored data and the part without is not so obvious | `True` |
| `TEST_MODE` | Enables/Disables Test Mode: Test with predefined images/audios and files | `True` |




## 6. What it does

The **injection** is done by **storing** the file in the **X less significant bits** of each element of the array created by flattening the array of image/audio.
- Each element has **8 bits** (if the base file is an **image**) or **16 bits** (if the base file is an **audio**)
- This script changes from **1 to all** the bits of each element, depending on the **size** of the file to be stored compared to the base image/audio.
- If you store a **bigger file** or if the **base image/audio is smaller**, **more bits** will be changed and the changes will be **more noticeable**.
- If you store a **smaller file** or if the **base image/audio is bigger**, **less bits** will be changed and the changes will be **less noticeable**.
- If the **base image/audio is too small** to store the file, the script will **stop** and **warn** you.
- If you choose to **encrypt the file**, its **size will increase by ≈1/3**.




## 7. How it works

### Options

| Option | Description |
|-|-|
| [0] EXIT | Exit the script |
| [1] Inject file | Calls [`inject_file_func()`](#inject_file_func) |
| [2] Extract file | Calls [`extract_file_func()`](#extract_file_func) |


### [`inject_file_func()`](menu.py)

1. If `TEST_MODE` == `True`, it will use the predefined base image/audio and input file. Otherwise, it will ask for the base image/audio and input file.
2. Read the file (in bytes)
3. Read the image/audio and store it in a numpy array
4. Read the filename (in bytes)
5. If the user wants to encrypt the file:
   1. Get the key with [`get_fernet()`](#get_fernet)
   2. Encrypt the file and filename
6. Try to inject the file and filename in the image/audio with [`inject_file()`](#inject_file). 
   1. If the image/audio is too small to store the file, raise an error
   2. Else, return the modified image/audio.
7. Save the modified image/audio


### [`extract_file_func()`](menu.py)

1. If `TEST_MODE` == `True`, it will use the predefined modified image/audio. Otherwise, it will ask for the modified image/audio.
2. Read the modified image/audio
3. Extract file and filename as bytes with [`extract_file()`](#extract_file)
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
| `arr` | `np.ndarray` | Image/audio as a numpy array |
| `file` | `bytes` | File as bytes |
| `filename` | `bytes` | Filename as bytes |
| `store_random` | `boolean` | Whether or not to store random data in the modified image/audio |

Returns the **modified image/audio array** (`np.ndarray`, with same shape as `arr`)


### [`extract_file()`](utils/injection.py)

| Parameter | Type | Description |
|-|-|-|
| `mod_arr_flat` | `np.ndarray` | Flattened modified image/audio |

Returns a **dictionary** with the extracted **file** and **filename**, both in (`bytes`) format