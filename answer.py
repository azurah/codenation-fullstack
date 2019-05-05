import requests
import json
from decouple import config


def get_challenge(url):
    data = requests.get(url)
    answer_content = json.loads(data.content)
    with open('answer.json', 'w') as f:
        json.dump(answer_content, f)
    return answer_content


def hashing_deciphered(deciphered_text):
    import hashlib
    hash_text = hashlib.sha1()
    hash_text.update(deciphered_text.encode())
    return hash_text.hexdigest()


def cipher_parser(hop, ciphered_text):
    char_deciphered = []
    for letter in ciphered_text:
        char = ord(letter)
        if char == 32: 
            ascii_number = 32
        elif char == 46:
            ascii_number = 46
        elif (char - hop) < 97: 
            ascii_number = (((char - hop) + 122) - 97) + 1
        else: 
            ascii_number = char - hop
        char_deciphered.append(chr(ascii_number))
    return "".join(char_deciphered)


def input_deciphered(deciphered_text):
    get_deciphered_hash = hashing_deciphered(deciphered_text)
    with open('answer.json', 'r+') as f:
        data = json.load(f)
        data['decifrado'] = deciphered_text
        data['resumo_criptografico'] = get_deciphered_hash
        f.seek(0)
        json.dump(data, f)
        f.truncate()


def send_form():
    POST = f"https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={config('TOKEN')}"
    answer = {'answer': open('answer.json', 'rb')}
    submit = requests.post(POST, files=answer)
    print(submit.headers)


if __name__ == '__main__':
    GET = f"https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={config('TOKEN')}"
    challenge = get_challenge(GET)
    numero_casas, cifrado = challenge['numero_casas'], challenge['cifrado']
    deciphered = cipher_parser(numero_casas, cifrado)
    input_deciphered(deciphered)
    send_form()

