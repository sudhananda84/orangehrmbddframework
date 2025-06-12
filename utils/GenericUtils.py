import time
import random
import string

def generate_unique_id():
    return str(int(time.time() * 1000))[-6:]

def generate_unique_email(domain="email.com"):
    timestamp = int(time.time() * 1000)
    rand = random.randint(1000, 9999)
    return f"user_{timestamp}_{rand}@{domain}"

def generate_unique_string(length=5):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))