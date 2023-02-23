# CODING_SYMBOLS = 256
# TABLE_SIZE = 512
# TABLE_BUILDING_COEFF = 340
#
#
# class Tans:
#     def __init__(self, occurrence):
#         self.occurrence = occure
#         self.offset, self.output_state = createCodingTable(self.ocurrence)
#
# def createCodingTable(occurence: list):
#
#     current_state = 0
#     current_output_state = TABLE_SIZE
#     offset = []
#     output_state = [0] * TABLE_SIZE
#
#     offset.append(0)
#     for x in occurence[:-1]:
#         offset.append(offset[-1] + x)
#
#     for _ in range(0, TABLE_SIZE):
#         output_state[current_state] = current_output_state
#         current_state = (current_state + TABLE_BUILDING_COEFF + 3) % TABLE_SIZE
#
#     return offset, output_state
#
#
# def get_output_state(symbol, input_state):
# 	idx = offset_enc[symbol] + input_state - occ_enc[symbol]
# 	return output_states_enc[idx]
# }
#
# def tans_main_loop(data):
#     for i, n in enumerate(data):
#         I_s_max = (occ[n[i]] << 1) - 1
# 		while I_s>I_s_max:
# 			writeToBitstream(stream, state_p,(unsigned long long)I_s)
# 			I_s >>=1;
# 		I_s = get_output_state(n[i], I_s)
