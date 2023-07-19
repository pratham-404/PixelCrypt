import binascii
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def encrypt(img, msg, key):

    key_bytes = str(key).encode("utf-8").rjust(16)
    iv = key_bytes # Initalization Vector

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    padded_msg = pad(msg.encode("utf-8"), 16)
    encrypted_msg = cipher.encrypt(padded_msg)

    hex_msg = binascii.hexlify(encrypted_msg)
    bin_msg = bin(int(hex_msg, 16))[2:].zfill(8 * ((len(hex_msg) + 1) // 2))
    bin_msg_arr = np.fromiter(bin_msg, dtype=int)

    delimiter = key # Delimiter. Delimiter is used so that we know till where to iterate.
    hex_end = binascii.hexlify(delimiter.encode())
    bin_end = bin(int(hex_end, 16))[2:].zfill(8 * ((len(hex_end) + 1) // 2))
    bin_end_arr = np.fromiter(bin_end, dtype=int)

    # append delimiter to msg
    msg_arr = np.concatenate((bin_msg_arr, bin_end_arr))
    msg_size = msg_arr.shape[0]

    # STEGANOGRAPHY - Encrypting into image

    lsb_plane = np.uint8(img & 1)
    lsb_size = lsb_plane.shape
    lsb_plane = np.ravel(lsb_plane)

    # replacing lsb bits of images by msg array
    lsb_plane[:msg_size] = msg_arr  

    lsb_plane = np.reshape(lsb_plane, lsb_size)

    cipher_img = np.uint8((img & 254) | lsb_plane)

    return cipher_img