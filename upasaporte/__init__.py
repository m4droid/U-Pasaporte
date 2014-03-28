from binascii import a2b_base64
from base64 import b64decode
from collections import OrderedDict
import re
import urlparse

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Util.asn1 import DerSequence
import requests


DEFAULT_CERTIFICATE_URL = 'https://www.u-cursos.cl/upasaporte/certificado'


def verify_data_integrity(signature, request_body, certificate_url=DEFAULT_CERTIFICATE_URL):
    public_key_request = requests.get(certificate_url)
    public_key = public_key_request.content
    rsa_key = __pem_certificate_string_to_der_key(public_key)
    signer = PKCS1_v1_5.new(rsa_key)
    digest = SHA.new()
    digest.update(__request_post_dict_reduce(request_body))
    return signer.verify(digest, b64decode(signature))


def __request_post_dict_reduce(request_body):

    data_dict = OrderedDict(urlparse.parse_qsl(request_body))
    if 'firma' in data_dict.keys():
        del data_dict['firma']
    data_string = ''
    courses_key_count = 0
    for key, value in data_dict.items():
        if re.match('cursos\[\d+\].*', key):
            if courses_key_count == 0:
                courses_key_count += 1
                data_string += 'Array'
                continue
            else:
                courses_key_count += 1
                continue
        data_string += str(value)
    return data_string


def __pem_certificate_string_to_der_key(public_key_string):
    # Convert from PEM to DER
    lines = public_key_string.replace(" ",'').split()
    der = a2b_base64(''.join(lines[1:-1]))

    # Extract subjectPublicKeyInfo field from X.509 certificate (see RFC3280)
    cert = DerSequence()
    cert.decode(der)
    tbsCertificate = DerSequence()
    tbsCertificate.decode(cert[0])
    subjectPublicKeyInfo = tbsCertificate[6]

    # Initialize RSA key
    return RSA.importKey(subjectPublicKeyInfo)
