import streamlit as st
from scripts.encryption import encrypt
from scripts.decryption import decrypt

# Function to handle the encryption option
def encryption_option():
    st.header("Encryption")
    image = st.file_uploader("Upload Image")
    message = st.text_input("Enter Message")
    key = st.text_input("Enter Key")
    
    if st.button("Encrypt"):
        if image and message and key:
            # Call the encrypt function from the encryption.py file
            encrypted_image = encrypt(image, message, key)
            st.image(encrypted_image, caption="Encrypted Image")
        else:
            st.error("Please provide all the required inputs.")

# Function to handle the decryption option
def decryption_option():
    st.header("Decryption")
    image = st.file_uploader("Upload Encrypted Image")
    key = st.text_input("Enter Key")
    
    if st.button("Decrypt"):
        if image and key:
            # Call the decrypt function from the decryption.py file
            decrypted_message = decrypt(image, key)
            st.success(f"Decrypted Message: {decrypted_message}")
        else:
            st.error("Please provide all the required inputs.")

# Main function to run the Streamlit app
def main():
    st.title("Image Encryption and Decryption")
    option = st.sidebar.radio("Select Option", ("Encryption", "Decryption"))
    
    if option == "Encryption":
        encryption_option()
    elif option == "Decryption":
        decryption_option()

if __name__ == "__main__":
    main()
