from hashlib import sha1
from typing import List, Tuple

# (r, g, b) from a byte
def get_color(hexdigest: str) -> Tuple[int, int, int]:
  r = int(hexdigest[6:8], 16)
  g = int(hexdigest[8:10], 16)
  b = int(hexdigest[10:12], 16)
  return (r, g, b)

# generate a 5x5 array of bits
def generate_bit_array(hexdigest: str) -> List[List[int]]:
  bit_array = []

  # only need 5 hex digits — one for each row
  for i in range(5):
    row_int_val = int(hexdigest[i], 16)
    row_array = [(row_int_val >> j) & 1 for j in range(3)] # only need 3 bits and then mirror
    row_array += row_array[:2][::-1] # mirror
    bit_array.append(row_array)

  return bit_array

def hash_user_id(user_id: str) -> str:
  return sha1(user_id.encode()).hexdigest()

def main():
  user_id = input("UserID: ")
  hexdigest = hash_user_id(user_id)
  bit_array = generate_bit_array(hexdigest)

if __name__ == '__main__':
  main()
  