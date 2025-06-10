import time

def generate_unique_id():
    return str(int(time.time() * 1000))[-6:]