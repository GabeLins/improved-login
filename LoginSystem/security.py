from OpenSSL import crypto, SSL

# This function generates an SSL certificate and encryption key to prevent
# Man-in-the-Middle (MitM) attacks.
def generate_ssl ():
    # Generate a key pair using a 4096-bit RSA key
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 4096)

    # Create a X.509 certificate
    cert = crypto.X509()

    # Get issuer information
    cert.get_subject().C = input('Country ISO 3166-2 Code: ')
    cert.get_subject().ST = input('State or Province Name: ')
    cert.get_subject().L = input('Locality Name: ')
    cert.get_subject().O = input('Organization Name: ')
    cert.get_subject().OU = input('Organizational Unit Name: ')
    cn = input('Common Name [Leave blank for localhost]: ') or 'localhost' 
    cert.get_subject().CN = cn
    expyears = int(input('Expiration Time [Years]: '))
    expyears *= 365*24*60*60

    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(expyears)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)

    # Add the subjectAltName extension to prevent security warnings when 
    # acessing the page
    cert.add_extensions([
        crypto.X509Extension(
            b'subjectAltName', False, bytes(f'DNS:{cn}', encoding='utf-8')
        )
    ])

    cert.set_version(2)
    cert.sign(key, 'sha256')

    # Write the certificate file
    with open('server.crt', 'wb') as certfile:
        certfile.write(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
        )
    
    # Write the encryption key file
    with open('server.key', 'wb') as keyfile:
        keyfile.write(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
        )

    return 0
