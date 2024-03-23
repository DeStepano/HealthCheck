import hashlib

def get_hash_id(user_id: int) -> str:
    
    # s1 = str(hashlib.sha256(str(user_id).encode()).hexdigest())
    s2 = int(hashlib.sha1(str(user_id).encode()).hexdigest(),16)
    print(s2%10000000000)
    # s3 = str(hashlib.sha224(str(user_id).encode()).hexdigest())
    # s4 = str(hashlib.sha384(str(user_id).encode()).hexdigest())
    # s5 = str(hashlib.sha512(str(user_id).encode()).hexdigest())
    # s6 = str(hashlib.blake2b(str(user_id).encode()).hexdigest())
    # s7 = str(hashlib.blake2s(str(user_id).encode()).hexdigest())
    # print(s1)
    print(s2)
    # print(s3)
    # print(s4)
    # print(s5)
    # print(s6)
    # print(s7)