import hashlib


def approximates(i1: int, i2: int, tolerance_level: int) -> bool:
    '''
    i1とi2が±tolerance_level内であればTrueを返す
    '''
    if abs(i1 - i2) <= tolerance_level:
        return True
    else:
        return False


def get_partial_hash_sha256(file_path):
    '''
    fileの先頭からchunk_sizeに指定した分のhash値を計算して返す
    '''  
    chunk_size = 1024*1024 # 1MB
    hash_function = hashlib.sha256()  # 好きなハッシュ関数を使える
    with open(file_path, 'rb') as f:
        chunk = f.read(chunk_size)
        hash_function.update(chunk)
    return hash_function.hexdigest()