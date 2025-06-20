import bcrypt

# Пароли для хеширования
passwords = ["admin", "12345678"]

# Хешируем каждый пароль
for pw in passwords:
    hashed = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
    print(f"Пароль: {pw} -> Хеш: {hashed.decode('utf-8')}")