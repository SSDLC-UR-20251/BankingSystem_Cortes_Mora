from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def hash_with_salt(texto):
    # Generar un salt aleatorio
    salt = get_random_bytes(32)
    # Convertir el texto en claro a bytes
    texto_bytes = texto.encode('utf-8')
    # Crear un objeto de hash SHA-256
    hash_obj = SHA256.new()
    # Agregar la sal y el texto plano al hash
    hash_obj.update(salt)
    hash_obj.update(texto_bytes)
    # Calcular el hash final
    final_hash = hash_obj.digest()
    # Devolver el hash
    return final_hash, salt

def hash_compare(texto, hash, salt):
    # Convertir el texto en claro a bytes
    texto_bytes = texto.encode('utf-8')
    # Crear un objeto de hash SHA-256
    hash_obj = SHA256.new()
    # Agregar la sal y el texto plano al hash
    hash_obj.update(salt)
    hash_obj.update(texto_bytes)
    # Calcular el hash final
    final_hash = hash_obj.digest()
    # Comparar el hash final con el hash proporcionado
    return final_hash == hash

def decrypt_aes(texto_cifrado_str, nonce_str, clave):
    # Convertir el texto cifrado y el nonce de cadena de texto a bytes
    texto_cifrado_str_bytes = bytes.fromhex(texto_cifrado_str)
    nonce_bytes = bytes.fromhex(nonce_str)
    # Crear un objeto AES con la clave y el nonce proporcionados
    cipher = AES.new(clave, AES.MODE_EAX, nonce_bytes)
    # Descifrar el texto
    texto_descifrado_bytes = cipher.decrypt(texto_cifrado_str_bytes)
    # Convertir los bytes del texto descifrado a una cadena de texto
    texto_descifrado = texto_descifrado_bytes.decode()
    # Devolver el texto descifrado
    return texto_descifrado


def encrypt_aes(texto, clave):
    # Convertir el texto a bytes
    texto_bytes = texto.encode()
    # Crear un objeto AES con la clave proporcionada
    cipher = AES.new(clave, AES.MODE_EAX)
    # Cifrar el texto
    nonce = cipher.nonce
    texto_cifrado, tag = cipher.encrypt_and_digest(texto_bytes)
    # Convertir el texto cifrado en bytes a una cadena de texto
    texto_cifrado_str = texto_cifrado.hex()
    # Devolver el texto cifrado y el nonce
    return texto_cifrado_str, nonce.hex()

if __name__ == '__main__':
    texto = "Hola Mundo"
    clave = get_random_bytes(16)
    texto_cifrado, nonce = encrypt_aes(texto, clave)
    print("Texto cifrado: " + texto_cifrado)
    print("Nonce: " + nonce)
    des = decrypt_aes(texto_cifrado, nonce, clave)
    print("Texto descifrado: " + des)

    texto_hash = "Hola Mundo"
    hash, salt = hash_with_salt(texto_hash)
    print("Hash: " + hash.hex())
    print("Salt: " + salt.hex())