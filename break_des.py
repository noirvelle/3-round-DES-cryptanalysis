from itertools import product
from des import *

import random

def get_possible_sbox_inputs(sbox_index, expand_result, sbox_ouput):
    output = bit_list_to_integer(sbox_ouput)
    possible_sbox_input = []
    for row in range(len(S_BOX[sbox_index])):
        for column in range(len(S_BOX[sbox_index][row])):
            if S_BOX[sbox_index][row][column] == output:
                roww = [int(x) for x in list('{0:0b}'.format(row))]
                coll = [int(x) for x in list('{0:0b}'.format(column))]

                while len(roww) < 2:
                    roww = [0] + roww
                while len(coll) < 4:
                    coll = [0] + coll

                possible_sbox_input.append([roww[0], coll[0], coll[1], coll[2], coll[3], roww[1]])
    return possible_sbox_input


def right_shift(bit_list, n):
    from collections import deque
    bit_list_shifted = deque(bit_list)
    bit_list_shifted.rotate(n)
    return list(bit_list_shifted)


def get_possible_sbox_input(E_R, F_R_K):
    possible_k_list = []
    for i in range(len(E_R)):
        # getting possible row column value to construct S_Box input
        # getting row0,col0,col1,col2,col3,row1
        # there are four possible inputs SBOX
        possible_row_col = get_possible_sbox_inputs(i, E_R[i], F_R_K[i])

        # row0,col0,col1,col2,col3,row1 = E(R0) + K1
        # K1 = row0,col0,col1,col2,col3,row1 + E(R0)  
        # this possible key just contains of 6 bit of total 48 key bit
        possible_k_list.append([ xor(E_R[i], possible_input) for possible_input in possible_row_col ])
    return possible_k_list


def get_possible_subkeys_from_sbox(sbox_input, sbox_output):
    possible_k_list = {}
    for i in range(len(sbox_input)):
        # getting possible row column value to construct S_Box input
        # getting row0,col0,col1,col2,col3,row1
        # there are four possible inputs SBOX
        possible_row_col = get_possible_sbox_inputs(i, sbox_input[i], sbox_output[i])

        # row0,col0,col1,col2,col3,row1 = E(R0) + K1
        # K1 = row0,col0,col1,col2,col3,row1 + E(R0)  
        # this possible key just contains of 6 bit of total 48 key bit
        possible_k_list[f"K{i+1}"] = [ xor(sbox_input[i], possible_input) for possible_input in possible_row_col ]
    return possible_k_list


def get_intersect_key(possible_k_pt1, possible_k_pt2, possible_k_pt3):
    retrieved_key = []
    for s in range(8):
        for i,j,k in product(list(range(4)), list(range(4)), list(range(4))):
            if possible_k_pt1[s][i] == possible_k_pt2[s][j] == possible_k_pt3[s][k]:
                retrieved_key += possible_k_pt1[s][i]
                break

    return retrieved_key


def get_intersect_key_diff(possible_k_pt1, possible_k_pt2, possible_k_pt3):
    retrieved_key = {}
    for s in range(8):
        for i,j,k in product(list(range(4)), list(range(4)), list(range(4))):
            if possible_k_pt1[s][i] == possible_k_pt2[s][j] or possible_k_pt2[s][j] == possible_k_pt3[s][k] or possible_k_pt1[s][i] == possible_k_pt3[s][k]:
                retrieved_key[f"K{s}"] = possible_k_pt1[s][i]
                break

        # if len(retrieved_key) != (s+1) * 6:
        #     retrieved_key += [-1] * 6

    return retrieved_key


def get_intersect_key_dict_diff(possible_k_pt1, possible_k_pt2, possible_k_pt3):
    retrieved_key = {}
    for s in range(8):
        for i,j,k in product(list(range(4)), list(range(4)), list(range(4))):
            if possible_k_pt1[f"K{0+1}"][i] == possible_k_pt2[f"K{0+1}"][j] or possible_k_pt2[f"K{0+1}"][j] == possible_k_pt3[f"K{0+1}"][k] or possible_k_pt1[f"K{0+1}"][i] == possible_k_pt3[f"K{0+1}"][k]:
                retrieved_key[f"K{0+1}"] = possible_k_pt1[f"K{0+1}"][i]
                break

        # if len(retrieved_key) != (s+1) * 6:
        #     retrieved_key += [-1] * 6

    return retrieved_key


def key_to_subkeys(keys, n):
    keys_splitted = nsplit(keys, n)
    subkeys = {}
    for subkey in range(len(keys_splitted)):
        subkeys[f"K{subkey}"] = keys_splitted[subkey]
    return subkeys


# def get_intersect_keys(list_of_possible_keys):
#     retrieved_key = {}
#     for s in range(8):
#         for i,j,k in product(list(range(4)), list(range(4)), list(range(4))):
#             if possible_k_pt1[s][i] == possible_k_pt2[s][j] or possible_k_pt2[s][j] == possible_k_pt3[s][k] or possible_k_pt1[s][i] == possible_k_pt3[s][k]:
#                 retrieved_key[f"K{s}"] = possible_k_pt1[s][i]
#                 break

#         # if len(retrieved_key) != (s+1) * 6:
#         #     retrieved_key += [-1] * 6

#     return retrieved_kes


def arrange_key(list_of_possible_subkeys):
    possible_keys = []
    for possible_subkey in list_of_possible_subkeys:
        # possible_subkey {K1: [a,b..], [c,d..], K2: []}
        pass

class PlaintextRandomGenerator:
    def generate(self, difference=None):
        # TODO validate difference

        plaintext = random.randint(0, 2 ** 64 - 1)
        plaintext = "{:0>16x}".format(plaintext)
        plaintext = bytearray.fromhex(plaintext)

        if difference == None:
            return plaintext

        plaintext = (
            plaintext,
            bytearray(p ^ d for p, d in zip(plaintext, difference))
        )

        return plaintext
