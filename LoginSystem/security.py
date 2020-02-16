from secrets import token_urlsafe
from OpenSSL import crypto, SSL
import json


def generate_certificate ():
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 4096)

    cert = crypto.X509()
    cert.get_subject().C = input('Country ISO 3166-2 Code: ')
    cert.get_subject().ST = input('State or Province Name: ')
    cert.get_subject().L = input('Locality Name: ')
    cert.get_subject().O = input('Organization Name: ')
    cert.get_subject().OU = input('Organizational Unit Name: ')
    commonName = input('Common Name: ')
    cert.get_subject().CN = commonName
    expyears = int(input('Expiration Time [Years]: '))
    expyears *= 365*24*60*60

    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(expyears)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.add_extensions([
        crypto.X509Extension(
            b'subjectAltName', False, bytes(f'DNS:{commonName}', encoding='utf-8')
        )
    ])

    cert.set_version(2)
    cert.sign(key, 'sha256')

    with open('server.crt', 'wb') as certfile:
        certfile.write(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
        )
    
    with open('server.key', 'wb') as keyfile:
        keyfile.write(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
        )

    return 0


def generate_secret_key ( output ):
    secret_key = input('Secret Key [Leave Blank for a Random Key]: ')

    if ( secret_key == '' ):
        secret_key = token_urlsafe(16)

    with open(output, 'w') as cfg:
        cfg.write(f"SECRET_KEY = '{secret_key}'")

    return 0