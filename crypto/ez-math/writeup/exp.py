import math
from sympy import gcd as sympy_gcd, isprime
from sympy.ntheory.residue_ntheory import sqrt_mod

def extended_gcd(a, b):
    if a == 0: return (b, 0, 1)
    d, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (d, x, y)

def mod_inverse(a, m):
    d, x, y = extended_gcd(a, m)
    if d != 1: raise ValueError()
    return (x % m + m) % m

def chinese_remainder_theorem(remainders, moduli):
    if len(remainders) != len(moduli): raise ValueError()
    if not remainders: return 0
    current_solution = remainders[0]
    current_product_modulus = moduli[0]
    for i in range(1, len(remainders)):
        a_i = remainders[i]; n_i = moduli[i]
        target_remainder = (a_i - current_solution) % n_i
        if target_remainder < 0: target_remainder += n_i
        inv_prod_mod_ni = mod_inverse(current_product_modulus, n_i)
        k = (target_remainder * inv_prod_mod_ni) % n_i
        current_solution = current_solution + k * current_product_modulus
        current_product_modulus = current_product_modulus * n_i
        current_solution %= current_product_modulus 
    return current_solution

def solve_challenge(n, e, c, delta):
    D_squared = delta**2 + 4*n
    s = math.isqrt(D_squared) 
    if s * s != D_squared: raise ValueError()

    p = (s - delta) // 2
    q = (s + delta) // 2

    if p * q != n: raise ValueError()
    if not (isprime(p) and isprime(q)): raise ValueError()
    
    phi = (p - 1) * (q - 1)
    g = sympy_gcd(e, phi)
    
    if g == 0 or phi % g != 0 or e % g != 0: raise ValueError()

    e_div_g = e // g
    phi_div_g = phi // g
    
    if sympy_gcd(e_div_g, phi_div_g) != 1: raise ValueError()

    d_0 = pow(int(e_div_g), -1, int(phi_div_g))
    c_prime = pow(int(c), int(d_0), int(n))

    roots_p_list = sqrt_mod(int(c_prime % p), p, all_roots=True)
    if not roots_p_list: raise ValueError()
    
    roots_q_list = sqrt_mod(int(c_prime % q), q, all_roots=True)
    if not roots_q_list: raise ValueError()

    possible_messages = []
    for m_p_sol in roots_p_list:
        for m_q_sol in roots_q_list:
            m_candidate = chinese_remainder_theorem(
                [int(m_p_sol), int(m_q_sol)], 
                [int(p), int(q)]
            )
            possible_messages.append(m_candidate)
    
    recovered_flag_bytes = None
    for M_cand_int_orig in possible_messages:
        M_cand_int = int(M_cand_int_orig)
        try:
            if M_cand_int == 0: M_cand_bytes = b'\x00' 
            else:
                num_bytes = (M_cand_int.bit_length() + 7) // 8
                M_cand_bytes = M_cand_int.to_bytes(num_bytes, 'big')
            
            if M_cand_bytes.startswith(b"MOCSCTF{") and M_cand_bytes.endswith(b"}"):
                recovered_flag_bytes = M_cand_bytes
                break 
        except Exception:
            pass
        if recovered_flag_bytes: break
            
    return recovered_flag_bytes

if __name__ == '__main__':
    n_val = 21208401986878015279509522874008885348387717522976425897549107866925757464883472532707292352414307231284275855466095807848695851930505579883210137286020323134806664168341784942621973049920656742810171548879957583785367441932643729899314218949826259355033283743694689225666994996363753009170065926908427152749
    e_val = 131074
    c_val = 20194974606745197367737772221849922440788393621466010103426602059294178957113650311453010687769575935575077209414139099142343128133329953414861132909524450986266341050609733478802216907510662374429910390793726485039335883806322677472147031585698217428225766198929161956067849968736395201753976224651535204165
    delta_val = 62420

    try:
        flag_solution_bytes = solve_challenge(n_val, e_val, c_val, delta_val)
        if flag_solution_bytes:
            print(f"Flag: {flag_solution_bytes.decode()}")
        else:
            print("Failed to recover flag.")
    except ValueError:
        print("Error during solution (ValueError).")
    except Exception:
        print("An unknown error occurred.")
