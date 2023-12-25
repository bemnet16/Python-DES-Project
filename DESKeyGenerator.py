from DESConstants import permutation_choice_1_table,permutation_choice_2_table

class Key_Generation:
    def __init__(self):
        self.key = ""
        self.round_keys = []
        self.initial_permuted_msg = [0] * 64
    
    def onPermuteChoiceOne(self):
        permuted_choice_1 = [0] * 56
        for idx,val in enumerate(permutation_choice_1_table):
            permuted_choice_1[idx] = self.key[val-1] #since 57 in permutation_choice_1_table means 57th position 

        c0 = permuted_choice_1[:28]
        d0 = permuted_choice_1[28:]

        self.round_keys = [[c0,d0]]

    def leftShif(self):
        c,d = self.round_keys.pop()
        for round in range(1,17):  # since there are 16 round in DES
            if round == 1 or round == 2 or round == 9 or round == 16:
                c = c[1:] + [c[0]]
                d = d[1:] + [d[0]]
            else:
                c = c[2:] + [c[0]] + [c[1]]
                d = d[2:] + [d[0]] + [d[1]]
            
            shifted_round_key = "".join(c + d)
            self.onPermuteChoiceTwo(shifted_round_key)
        
        return self.round_keys

    def onPermuteChoiceTwo(self,shifted_round_key):
        permuted_choice_2 = [0] * 48
        for idx,val in enumerate(permutation_choice_2_table):
            permuted_choice_2[idx] = shifted_round_key[val - 1]
        self.round_keys.append("".join(permuted_choice_2))

    def roundKeyGenerator(self,key):
        self.key = key
        self.onPermuteChoiceOne()
        return self.leftShif()