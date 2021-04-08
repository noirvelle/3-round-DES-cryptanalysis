from des import *
from break_des import *

def break_2_round_des():
    print(f"""
===========================
    BREAK 2 ROUND DES
===========================
    """)
    pt1 = "PAPAMAMA"
    pt2 = "HAHAHIHI"
    pt3 = "ASDFGHJK"

    sk = "secret_k"

    d1 = des(round=2)
    d2 = des(round=2)
    d3 = des(round=2)

    ct1 = d1.encrypt(key=sk, text=pt1)
    ct2 = d2.encrypt(key=sk, text=pt2)
    ct3 = d3.encrypt(key=sk, text=pt3)

    def get_possible_k1(des, ciphertext):

        # L0: left half of plaintext, R0: right half of plaintext
        L0, R0 = divide_half(des.text)

        # L1 = R0
        L1 = R0

        # L1: left half of ciphertext, R1: right half of ciphertext
        R2, L2 = divide_half(ciphertext)

        # expansion box input (E is Expansion table)
        E_R0 = des.expand(string_to_bit_array(R0), E)

        assert E_R0 == des.data["E0"]

        E_R0 = nsplit(E_R0, 6)

        # L2 = R1 = L0 + f (R0, k 1)
        # L2 = L0 + f(R0, k1)
        # f(R0, k1) =  L2 + L0
        F_R0_K1 = des.xor(string_to_bit_array(L2), string_to_bit_array(L0))

        # F_R0_K1
        assert F_R0_K1 == des.data["F0"]

        F_R0_K1 = nsplit(F_R0_K1, 4)

        return get_possible_sbox_input(E_R0, F_R0_K1)

    possible_k_pt1 = get_possible_k1(d1, ct1)
    possible_k_pt2 = get_possible_k1(d2, ct2)
    possible_k_pt3 = get_possible_k1(d3, ct3)

    K1 = get_intersect_key(possible_k_pt1, possible_k_pt2, possible_k_pt3)

    print(f"""found K1: \t\t{K1}""")
    print(f"""actual K1: \t\t{d1.keys[0]}""")

    assert K1  == d1.keys[0]

    def get_possible_k2(des, ciphertext):

        # L0: left half of plaintext, R0: right half of plaintext
        L0, R0 = divide_half(des.text)

        # L1 = R0
        L1 = R0

        # L1: left half of ciphertext, R1: right half of ciphertext
        R2, L2 = divide_half(ciphertext)

        # R1 = L2
        R1 = L2

        # expansion box input (E is Expansion table)
        E_R1 = des.expand(string_to_bit_array(R1), E)

        assert E_R1 == des.data["E1"]

        E_R1 = nsplit(E_R1, 6)

        # L2 = R1 = L0 + f (R0, k 1)
        # L2 = L0 + f(R0, k1)
        # f(R0, k1) =  L2 + L0

        # F(R1, K2) = R2 + L1
        F_R1_K2 = des.xor(string_to_bit_array(R2), string_to_bit_array(L1))

        # F_R0_K1
        assert F_R1_K2 == des.data["F1"]

        F_R1_K2 = nsplit(F_R1_K2, 4)

        return get_possible_sbox_input(E_R1, F_R1_K2)

    possible_k_pt1 = get_possible_k2(d1, ct1)
    possible_k_pt2 = get_possible_k2(d2, ct2)
    possible_k_pt3 = get_possible_k2(d3, ct3)

    K2 = get_intersect_key(possible_k_pt1, possible_k_pt2, possible_k_pt3)

    print(f"""found K2: \t\t{K2}""")
    print(f"""actual K2: \t\t{d1.keys[1]}""")

    assert K2  == d1.keys[1]

if __name__ == "__main__":
    break_2_round_des()