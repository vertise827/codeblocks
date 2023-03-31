import jwt
from cryptography.hazmat.primitives import serialization
from OpenSSL import crypto
from datetime import datetime,timedelta


def construct_jwt():
    ida_client_id = "MyIDAClient"
    ida_url = "MyIDAUrl"

    # Load the private key from a file
    with open('private_key.pem', 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    # Load the certificate from a file
    with open('certificate.pem', 'rb') as cert_file:
        certificate = cert_file.read()
    
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, certificate)

    # Define the elements for the JWT token
    kid = cert.digest('sha1').decode.replace(":", "")
    jwt_headers = {"kid": kid}
    payload = {
        'iss': ida_client_id,
        'aud': ida_url,
        'sub': ida_client_id,
        'sub': '1234567890',
        'iat': datetime.utcnow,
        'exp': datetime.utcnow() +timedelta(hours=1),
        'jti': 'uniqueidentifier-appname'
    }

    # Generate the RS256 JWT token
    token = jwt.encode(payload, private_key, algorithm='RS256', headers=jwt_headers)

    return token