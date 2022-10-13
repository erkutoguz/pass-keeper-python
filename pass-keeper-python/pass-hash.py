import bcrypt

key = bcrypt.kdf(
    password=b'****************',
    salt=b'121asdfasdasdfasdf2t',
    desired_key_bytes=64,
    rounds=100)
print(key)
