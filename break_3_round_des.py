from des import *
from break_des import *

def break_3_round_des():
    def get_possible_k3(des, ciphertext):

        # L0: left half of plaintext, R0: right half of plaintext
        L0_1, R0_1 = divide_half(des[0].text)
        L0_2, R0_2 = divide_half(des[1].text)

        R3_1, L3_1 = divide_half(ciphertext[0])
        R3_2, L3_2 = divide_half(ciphertext[1])

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

        assert F_L3_K3_ == xor(des[0].data["F2"], des[1].data["F2"])

        F_L3_K3_ = nsplit(F_L3_K3_, 4)

        # E_R2' = Expand(R2)'
        # R2' = L3'
        L3_ = xor_string(L3_1, L3_2)
        R2_ = L3_
        E_R2_ = des[0].expand(R2_, E)

        assert E_R2_ == xor(des[0].data["E2"], des[1].data["E2"])

        E_R2_ = nsplit(E_R2_, 6)

        return get_possible_subkeys_from_sbox(E_R2_, F_L3_K3_)

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

    # ptp1 = ("HQHQMAMA", "ZXWSMAMA")
    # ptp2 = ("AOMEZZSS", "QIELZZSS")
    # ptp3 = ("EXKIGHJK", "OPAWGHJK")

    # sk = "secret_k"

    # dp1 = (des(round=3), des(round=3))
    # dp2 = (des(round=3), des(round=3))
    # dp3 = (des(round=3), des(round=3))

    # ctp1 = (dp1[0].encrypt(key=sk, text=ptp1[0]), dp1[1].encrypt(key=sk, text=ptp1[1]))
    # ctp2 = (dp2[0].encrypt(key=sk, text=ptp2[0]), dp2[1].encrypt(key=sk, text=ptp2[1]))
    # ctp3 = (dp3[0].encrypt(key=sk, text=ptp3[0]), dp3[1].encrypt(key=sk, text=ptp3[1]))

    # possible_subkeys = []

    # possible_subkeys.append(get_possible_k3(dp1, ctp1))
    # possible_subkeys.append(get_possible_k3(dp2, ctp2))
    # possible_subkeys.append(get_possible_k3(dp3, ctp3))

    # get_intersect_keys = get_intersect_key_dict_diff(possible_subkeys[0], possible_subkeys[1], possible_subkeys[2])

    # print(get_intersect_keys)

    # K3 = get_intersect_key_diff(possible_k_pt1, possible_k_pt2, possible_k_pt3)
    # actual_K3 = key_to_subkeys(dp1[0].keys[3], 6)

    # print(f"""found K1: \t\t{K3}""")
    # print(f"""actual K1: \t\t{actual_K3}""")










    # assert K3 == actual_K3

    # def get_possible_k2(des, ciphertext):

    #     # L0: left half of plaintext, R0: right half of plaintext
    #     L0, R0 = divide_half(des.text)

    #     # L1 = R0
    #     L1 = R0

    #     # L1: left half of ciphertext, R1: right half of ciphertext
    #     R2, L2 = divide_half(ciphertext)

    #     # R1 = L2
    #     R1 = L2

    #     # expansion box input (E is Expansion table)
    #     E_R1 = des.expand(string_to_bit_array(R1), E)

    #     assert E_R1 == des.data["E1"]

    #     E_R1 = nsplit(E_R1, 6)

    #     # L2 = R1 = L0 + f (R0, k 1)
    #     # L2 = L0 + f(R0, k1)
    #     # f(R0, k1) =  L2 + L0

    #     # F(R1, K2) = R2 + L1
    #     F_R1_K2 = des.xor(string_to_bit_array(R2), string_to_bit_array(L1))

    #     # F_R0_K1
    #     assert F_R1_K2 == des.data["F1"]

    #     F_R1_K2 = nsplit(F_R1_K2, 4)

    #     return get_possible_sbox_input(E_R1, F_R1_K2)

    # possible_k_pt1 = get_possible_k2(d1, ct1)
    # possible_k_pt2 = get_possible_k2(d2, ct2)
    # possible_k_pt3 = get_possible_k2(d3, ct3)

    # K2 = get_intersect_key(possible_k_pt1, possible_k_pt2, possible_k_pt3)

    # print(f"""found K2: \t\t{K2}""")
    # print(f"""actual K2: \t\t{d1.keys[2]}""")

    # assert K2  == d1.keys[1]
