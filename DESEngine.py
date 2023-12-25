import copy
from DESConstants import intial_permutation_table,final_permutation_table,feistel_s_box_tables,feistel_p_box_permutation_table
from DESKeyGenerator import Key_Generation

class DES:
    def __init__(self,type):
        self.key = ""
        self.type = type
        self.round_keys = []
        self.initial_permuted_msg = [0] * 64

    def convertToBinary(self,txt,encrypt=True):
        if self.type == "HEX":
            return self.hexToBin(txt)
        elif self.type == "TEXT":
            return self.TextToBin(txt)
        else:
            return txt
   
    def decodeToDataType(self,bin,encrypt=True):
        if self.type == "HEX":
           return self.BinToHex(bin)
        elif self.type == "TEXT":
            return self.BinToText(bin)
        else:
            return bin

    def hexToBin(self,txt):
        temp = int(txt,16)
        return bin(temp)[2:].zfill(len(txt) * 4)

    def BinToHex(self,bin):
        temp = int(bin,2)
        return hex(temp)[2:].zfill(len(bin) // 4)

    def TextToBin(self,txt): 
        utf8_encoded = txt.encode('latin-1')  
        binary_representation = ''.join(format(byte, '08b') for byte in utf8_encoded)
        return binary_representation

    def BinToText(self, bin): ##Doesn't work since some bits is out of ASCII range
        bytes_data = bytes(int(bin[i:i+8], 2) for i in range(0, len(bin), 8))
        decoded_text = bytes_data.decode('latin-')
        return decoded_text

    def initialPermutation(self,text):
        for idx,val in enumerate(intial_permutation_table):
            self.initial_permuted_msg[idx] = text[val - 1]

    def DES16Rounds(self,encrypt=True):
        for round in range(16):  ## Iterate through each round
            # left_32_bits = initial_permuted_msg[:32]
            left_32_bits = "".join(self.initial_permuted_msg[:32])
            right_32_bits = self.initial_permuted_msg[32:]
            reserved_right_32_bits = "".join(right_32_bits) ## to be used later
            right_32_bits = [right_32_bits[idx:idx+4] for idx in range(0,32,4)]  ## group them in to 4 length word to applay Expansion permutation


            ### EXECUTE ON FEISTEL FUNCTION ###

            ## E-Bit selection (Expansion permutation)
            expanded_right_48_bits = copy.deepcopy(right_32_bits)
            for idx in range(0,8):
                expanded_right_48_bits[idx].insert(0,right_32_bits[idx - 1][-1])
                expanded_right_48_bits[idx].append(right_32_bits[(idx+1)%8][0])

            expanded_right_48_bits=[bit for bits in expanded_right_48_bits for bit in bits]  ## reorder bits in to one dimension array 

            expanded_right_48_bits = "".join(expanded_right_48_bits)

            if encrypt:   ## For encryption
                key_xor_right_48bits = bin(int(self.round_keys[round],2) ^ int(expanded_right_48_bits,2))[2:].zfill(48)  ## key xor with R0
            else:   ## For decryption
                key_xor_right_48bits = bin(int(self.round_keys[15 - round],2) ^ int(expanded_right_48_bits,2))[2:].zfill(48)  ## key xor with R0

            s_box_inputs = [key_xor_right_48bits[idx:idx+6] for idx in range(0,48,6)]  ## divde with 6 bits to perform s-box

            s_box_outputs = []
            for s_box_idx,_6_bit_val in enumerate(s_box_inputs):
                row = int((_6_bit_val[0] + _6_bit_val[-1]),2)
                col = int(_6_bit_val[1:5],2)
                s_box_val = feistel_s_box_tables[s_box_idx][row][col]
                s_box_outputs.append(bin(s_box_val)[2:].zfill(4))

            s_box_outputs = list("".join(s_box_outputs))

            ## feistel final permutation
            feistel_permuted_32_bits = [0] * 32
            for idx,val in enumerate(feistel_p_box_permutation_table):
                feistel_permuted_32_bits[idx] = s_box_outputs[val - 1]
            feistel_permuted_32_bits = "".join(feistel_permuted_32_bits)


            ## xor left_32_bits with final feistel_permuted_32_bits
            right_32_bits = bin(int(left_32_bits,2) ^ int(feistel_permuted_32_bits,2))[2:].zfill(32)
            left_32_bits = reserved_right_32_bits

            self.initial_permuted_msg = list(left_32_bits + right_32_bits)
        
    def swapMsg(self):
        self.initial_permuted_msg = self.initial_permuted_msg[32:] + self.initial_permuted_msg[:32]
    
    def finalPermutation(self):
        final_permuted_msg = [0] * 64
        for idx,val in enumerate(final_permutation_table):
            final_permuted_msg[idx] = self.initial_permuted_msg[val - 1]
        
        return "".join(final_permuted_msg)

    def encrypt_decrypt(self,data,key,encrypt=True):

        temp = int(key,16)
        self.key = bin(temp)[2:].zfill(len(key) * 4)

        # self.roundKeyGenerator()
        self.round_keys = Key_Generation().roundKeyGenerator(self.key)

        all_encrypted_data = []
        msg = self.convertToBinary(data)
        padding = (64 - (len(msg) % 64)) % 64
        msg = msg + ("0" * padding)

        for block in range(0,len(msg),64):
            self.initialPermutation(msg[block:block + 64])
            self.DES16Rounds(encrypt)
            self.swapMsg()
            encrypted_binary = self.finalPermutation()
            encrypted_msg = self.decodeToDataType(encrypted_binary,encrypt)
            all_encrypted_data.append(encrypted_msg)

        return "".join(all_encrypted_data)

    def encryptMsg(self,data,key):
       return self.encrypt_decrypt(data,key)

    def decryptMsg(self,data,key):
       return self.encrypt_decrypt(data,key,False)




## DES
des = DES("TEXT")
message = "Anything is possible what ever you want and dedicated for your DREAM!!"
key = "0001001100110100010101110111100110011011101111001101111111110001"

cipher_text = des.encryptMsg(message,key)
plain_text = des.decryptMsg(cipher_text,key)

print("Message : ",message)
print("Cipher Text : ",cipher_text)
print("Plain Text : ",plain_text)
print()

## DOUBLE DES
double_des = DES("HEX")
plaintxt = "1234567890abcd"
key_1 = "0001001100110100010101110111100110011011101111001101111111110001"
key_2 = "1101011100001010111010010000101110010100101111010111000011011101"

cipher_1 = double_des.encryptMsg(plaintxt,key_1)
cipher_2  = double_des.encryptMsg(cipher_1,key_2)

print("plain Text : ",plaintxt)
print("Cipher Txt 1 : ",cipher_1)
print("Cipher Txt 2 : ",cipher_2)

decrypt_1 = double_des.decryptMsg(cipher_2,key_2)
decrypt_2 = double_des.decryptMsg(decrypt_1,key_1)

print("decrypt Txt 1 : ",decrypt_1)
print("decrypt Txt 2 : ",decrypt_2)






