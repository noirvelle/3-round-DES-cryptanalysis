from des import *

def get_possible_sbox_input(E_R, F_R_K):
    possible_k_list = []
    for i in range(len(E_R)):
        # getting possible row column value to construct S_Box input
        # getting row0,col0,col1,col2,col3,row1
        # there are four possible inputs SBOX
        possible_row_col = get_list_possible_sbox_input(i, E_R[i], F_R_K[i])

        # row0,col0,col1,col2,col3,row1 = E(R0) + K1
        # K1 = row0,col0,col1,col2,col3,row1 + E(R0)  
        # this possible key just contains of 6 bit of total 48 key bit
        possible_k_list.append([ xor(E_R[i], possible_input) for possible_input in possible_row_col ])
    return possible_k_list

def get_possible_keys(des, ciphertext):

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

def break_1_round_des():
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

    possible_k_pt1 = get_possible_keys(d1, ct1)
    possible_k_pt2 = get_possible_keys(d2, ct2)
    possible_k_pt3 = get_possible_keys(d3, ct3)

    retrieved_key = []

    from itertools import product
 
    for s in range(8):
        for i,j,k in product(list(range(4)), list(range(4)), list(range(4))):
            if possible_k_pt1[s][i] == possible_k_pt2[s][j] == possible_k_pt3[s][k]:
                retrieved_key += possible_k_pt1[s][i]
                break

    print(retrieved_key)
    print(d1.keys[0])


if __name__ == '__main__':
    break_1_round_des()