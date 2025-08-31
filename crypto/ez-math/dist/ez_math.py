import random
from sympy import nextprime, isprime, gcd as sympy_gcd

def get_large_prime(bits):
    while True:
        p_candidate = random.getrandbits(bits)
        if p_candidate % 2 == 0:
            p_candidate += 1
        p = nextprime(p_candidate)
        return p

def generate_challenge_params():
    flag_string = "" 
    m = int.from_bytes(flag_string.encode(), 'big')

    p_bits = 512
    min_delta_bits = 10
    max_delta_bits = 16 
    
    e_prime_component = 65537 

    while True:
        p = get_large_prime(p_bits)
        
        delta = random.randint(2**min_delta_bits, 2**max_delta_bits)
        if delta % 2 != 0:
            delta += 1
            
        q_candidate = p + delta
        
        if not isprime(q_candidate):
            continue 
        q = q_candidate
        n = p * q
        
        if m >= n:
            continue
        phi = (p - 1) * (q - 1)
        
        if phi % 2 != 0: 
            continue 
            
        phi_half = phi // 2
        e = 2 * e_prime_component

        actual_gcd_e_phi = sympy_gcd(e, phi)
        
        if actual_gcd_e_phi == 2:
            if sympy_gcd(e_prime_component, phi_half) == 1:
                break 
    
    c = pow(m, e, n)

    return n, e, c, delta

if __name__ == '__main__':
    n_val, e_val, c_val, delta_val = generate_challenge_params()
    
    print(f"n = {n_val}")
    print(f"e = {e_val}")
    print(f"c = {c_val}")
    print(f"delta = {delta_val}")
