from Crypto.Util.number import long_to_bytes, GCD
import gmpy2

def ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    d, x1, y1 = ext_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y

def mod_inv(a, m):
    d, x, _ = ext_gcd(a, m)
    if d != 1:
        return None 
    return (x % m + m) % m

def factor_p_next_p(n):
    s_n = gmpy2.isqrt(n)
    for i in range(200000): 
        pc = s_n - i
        if pc <= 1: break
        if n % pc == 0:
            qc = n // pc
            if gmpy2.is_prime(pc) and gmpy2.is_prime(qc):
                if gmpy2.next_prime(pc) == qc:
                    return pc, qc
                elif gmpy2.next_prime(qc) == pc:
                     return qc, pc
    
    a = gmpy2.isqrt(n) 
    if a * a < n:
        a += 1
    for _ in range(200000): 
        b_sq = a * a - n
        if b_sq < 0: 
            a +=1
            continue
        if gmpy2.is_square(b_sq):
            b_val = gmpy2.isqrt(b_sq)
            pc = a - b_val
            qc = a + b_val
            if pc * qc == n:
                if gmpy2.is_prime(pc) and gmpy2.is_prime(qc):
                    if gmpy2.next_prime(pc) == qc:
                        return pc, qc
                    elif gmpy2.next_prime(qc) == pc:
                        return qc, pc
        a += 1
        if a > n // 2 + 2 : 
            break
    return None, None

def solve():
    n1 = 6812896682529270617889699041268397231216344502100994418898483090399363050725238802825519610890413646309466494321918636827383749031784541498873387892731639
    e1 = 65537
    c1 = 4427729071087402462891221302870960264377546560852404414763265602889920597278631371895561554533422266459579128710764143355754615245149034250540901716118396
    p1g = 83018022170775357156881992679804004613671250493281300137495505566721083549673
    
    n2 = 8618941019390135762450560251440447449812344988348002904674567734387521342905027779518989812368861070593805164745239666403382823700616097172234834567736147
    e2 = 65537
    c2 = 5090157394401735030895991956180326655655690673641213577889910602055845449426923727333236685488219458241927620516575355892867356153466992699239192192910803
    p2m = 0 
    q2m = 0
    
    n3 = 44935859354785283479720490973543160302824014776763758544522532443340696020267
    e3 = 3
    c3 = 345422409558921105091064923418692102360936093114398968000
    
    n4 = 8050202063335318202668477773676061807230884209991655693527143039730083343444420055444708024772406517257344636757261685775610919720030730312364281795306843
    e4a = 65537
    c4a = 5944697746898769084130690069563137465626689325180948580645355816012208942196895961186706314322689146225405184339425445878469418993890870252122256787094490
    e4b = 65539
    c4b = 590873621149745423995166880880817186889129377479311590030588253033344142558245476231076545393071246375504750217939956792516706707037717951120503693278372
    
    flags = [None, None, None, None]

    p1s = p1g
    q1s = n1 // p1s
    phi1s = (p1s - 1) * (q1s - 1)
    d1s = gmpy2.invert(e1, phi1s) 
    m1s = pow(c1, d1s, n1)
    flags[0] = long_to_bytes(int(m1s)).decode()

    p2f, q2f = None, None
    if p2m and q2m:
        if p2m * q2m == n2:
             p2f, q2f = p2m, q2m
    if not (p2f and q2f): 
        p2f, q2f = factor_p_next_p(n2)

    phi2s = (p2f - 1) * (q2f - 1)
    d2s = gmpy2.invert(e2, phi2s)
    m2s = pow(c2, d2s, n2)
    flags[1] = long_to_bytes(int(m2s)).decode()

    m3c, exact = gmpy2.iroot(c3, e3)
    if exact:
        flags[2] = long_to_bytes(int(m3c)).decode()

    g, x, y = ext_gcd(e4a, e4b)
    
    ic4a = mod_inv(c4a, n4)
    ic4b = mod_inv(c4b, n4)

    t1 = pow(c4a, x, n4)
    if x < 0:
        t1 = pow(ic4a, -x, n4)

    t2 = pow(c4b, y, n4)
    if y < 0:
        t2 = pow(ic4b, -y, n4)
            
    m4s = (t1 * t2) % n4
    flags[3] = long_to_bytes(int(m4s)).decode()

    if all(part is not None for part in flags):
        full_flag = "".join(flags)
        print(f"{full_flag}")

if __name__ == "__main__":
    solve()
