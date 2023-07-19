import numpy as np
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt(img, key):
    lsb_plane = np.uint8(img & 1)
    lsb_plane = np.ravel(lsb_plane)

    delimiter = key # Delimiter
    hex_end = binascii.hexlify(delimiter.encode())
    bin_end = bin(int(hex_end, 16))[2:].zfill(8 * ((len(hex_end) + 1) // 2))
    bin_end_arr = np.fromiter(bin_end, dtype=int)

    idx = np.where(np.convolve(lsb_plane, bin_end_arr[::-1], mode='valid') == np.sum(bin_end_arr))[0][0]
    lsb_plane = lsb_plane[0:idx]

    bin_str = np.array2string(lsb_plane, separator='')[1:-1].replace(' ', '')
    bin_str = bin_str.replace('\n', '')
    bin_str.encode()

    enc_msg = hex(int(bin_str, 2))[2:]

    #Decrypting the encrypted text that is extracted from the image

    key_bytes = key.encode("utf-8").rjust(16)
    iv = key_bytes

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)

    enc_msg = bytes.fromhex(enc_msg)
    msg = unpad(cipher.decrypt(enc_msg), 16).decode("utf-8")

    return msg