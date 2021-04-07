from des import *
from break_des import *

def break_3_round_des():
    print(f"""
===========================
    BREAK 3 ROUND DES
===========================
    """)

    plaintext_generator = PlaintextRandomGenerator()

    attempts = 2**10
    secret_key = "secretke"
    actual_K3 = ""
    possible_combination = {f"K{i+1}": [] for i in range(8)}

    for i in range(attempts):
        difference = bytearray([random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255), 0x00, 0x00, 0x00, 0x00])
        plaintext1, plaintext2 = plaintext_generator.generate(difference)

        assert plaintext1[4:] == plaintext2[4:]

        des1 = des(round=3)
        des2 = des(round=3)

        ciphertext1 = des1.encrypt(key=secret_key, text=plaintext1)
        ciphertext2 = des2.encrypt(key=secret_key, text=plaintext2)

        assert des1.keys[2] == des2.keys[2]

        actual_F_R0_K1_ = xor(des1.data["F0"], des2.data["F0"])

        assert actual_F_R0_K1_ == [0]*32

        if not actual_K3:
            actual_K3 = des1.keys[2]

        # L0: left half of plaintext, R0: right half of plaintext
        L0_1, R0_1 = divide_half(plaintext1)
        L0_2, R0_2 = divide_half(plaintext2)

        R3_1, L3_1 = divide_half(ciphertext1)
        R3_2, L3_2 = divide_half(ciphertext2)

        # because R0 == R0*
        # f(R0, k1) + f(R0*, k1) == 0

        # f(L3, k3)' 
        # = (R3 + L2) + (R3 + L2)* 
        # = R3 + R3* + (L2 + L2) 
        # = R3' + (L0 + f(R0,K1) + L0* + f(R0,K1)*)
        # = R3'  + L0' + f(R0, K1)' -> f(R0, K1)' = 0
        # = R3' + L0'
        # f(L3, K3)' = R3' + L0'

        # R3 = L0 + f(R0, K1) + f(L3, K3)
        # R3' = [L0 + f(R0, K1) + f(L3, K3)] + [L0* + f(R0, K1)* + f(L3, K3)*]
        # R3' = L0' + f(R0,K1)' + f(L3,K3)' 
        # -> f(R0,K1)' = 0
        # then
        # R3' = L0' + f(L3,K3)' 
        # f(L3, K3)' = R3' + L0'
        R3_ = xor_string(R3_1, R3_2)
        L0_ = xor_string(L0_1, L0_2)

        F_L3_K3_ = xor(R3_, L0_)
        actual_F_L3_K3_ = xor(des1.data["F2"], des2.data["F2"])

        assert F_L3_K3_ == actual_F_L3_K3_

        F_L3_K3_ = nsplit(F_L3_K3_, 4)

        # E_R2' = Expand(R2)'
        # R2' = L3'
        L3_ = xor_string(L3_1, L3_2)
        R2_ = L3_

        E_R2_ = xor(des1.expand(string_to_bit_array(L3_1), E), des1.expand(string_to_bit_array(L3_2), E))
        actual_E_R2_ = xor(des1.data["E2"], des2.data["E2"])

        assert E_R2_ == actual_E_R2_

        E_R2_ = nsplit(E_R2_, 6)

        for key, value in possible_combination.items():
            value.extend(get_integer_possible_subkeys_from_sbox(E_R2_, F_L3_K3_)[key])

    for k,v in possible_combination.items():
        possible_combination[k] = count_frequency(v)

    for k,v in possible_combination.items():
        print(k, v)
        print()

    print([ convert_to_int(x) for x in nsplit(actual_K3, 6)])
