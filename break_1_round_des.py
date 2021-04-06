from des import *
from break_des import *

def break_1_round_des():
    print(f"""
===========================
    BREAK 1 ROUND DES
===========================
    """)

    pt1 = "PAPAMAMA"
    pt2 = "HAHAHIHI"
    pt3 = "ASDFGHJK"

    sk = "secret_k"

    d1 = des(round=1)
    d2 = des(round=1)
    d3 = des(round=1)

    ct1 = d1.encrypt(key=sk, text=pt1)
    ct2 = d2.encrypt(key=sk, text=pt2)
    ct3 = d3.encrypt(key=sk, text=pt3)

    def get_possible_k1(des, ciphertext):

        # L0: left half of plaintext, R0: right half of plaintext
        L0, R0 = divide_half(des.text)
        # L1: left half of ciphertext, R1: right half of ciphertext
        R1, L1 = divide_half(ciphertext)

        # expansion box input (E is Expansion table)
        E_R0 = des.expand(string_to_bit_array(R0), E)
        E_R0 = nsplit(E_R0, 6)

        # FBox output
        # R1 = L0 + F(R0, K1)
        # F(R0, K1) = R1 + L0
        F_R0_K1 = des.xor(string_to_bit_array(R1), string_to_bit_array(L0))
        F_R0_K1 = nsplit(F_R0_K1, 4)

        return get_possible_sbox_input(E_R0, F_R0_K1)

    possible_k_pt1 = get_possible_k1(d1, ct1)
    possible_k_pt2 = get_possible_k1(d2, ct2)
    possible_k_pt3 = get_possible_k1(d3, ct3)

    K1 = get_intersect_key(possible_k_pt1, possible_k_pt2, possible_k_pt3)

    assert K1  == d1.keys[0]

    print(f"""found K1: \t\t{K1}""")
    print(f"""actual K1: \t\t{d1.keys[0]}""")
