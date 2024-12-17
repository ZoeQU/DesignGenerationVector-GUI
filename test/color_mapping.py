# -*- coding:utf-8 -*-

# def find_corresponding_c(A, B, C):
#     # Create a mapping from elements of B to elements of C
#     mapping = {tuple(b): c for b, c in zip(B, C)}
    
#     # Find corresponding elements in C for each element in A
#     result = [mapping[tuple(a)] for a in A]
    
#     return result

# # Example usage
# A = [[12, 23, 23], [231, 124, 87], [43, 68, 178]]
# B = [[43, 68, 178], [12, 23, 23], [231, 124, 87]]
# C = [[16, 213, 213], [231, 224, 53], [49, 168, 278]]

# corresponding_C = find_corresponding_c(A, B, C)
# print(corresponding_C)

# def find_corresponding_color(value, A, B, C):
#     # Create a mapping from sorted A to C using B as intermediate
#     mapping = {tuple(b): c for b, c in zip(B, C)}
    
#     # Sort A to match the order of B
#     sorted_A = sorted(A, key=lambda x: B.index(x))
    
#     # Find the index of the value in sorted A
#     index = sorted_A.index(value)
    
#     # Get the corresponding B value
#     b_value = B[index]
    
#     # Return the corresponding C value
#     return mapping[tuple(b_value)]

# # Example usage
# A = [[12, 23, 23], [231, 124, 87], [43, 68, 178]]
# B = [[43, 68, 178], [12, 23, 23], [231, 124, 87]]
# C = [[16, 213, 213], [231, 224, 53], [49, 168, 278]]

# input_value = [12, 23, 23]
# corresponding_C_value = find_corresponding_color(input_value, A, B, C)
# print(corresponding_C_value)

def create_mapping(A, B, C):
    # Create a mapping from sorted A to C using B as intermediate
    return {tuple(a): mapping for a, mapping in zip(A, C)}

def find_corresponding_color(value, mapping):
    # Find the corresponding C value for the given A value
    return mapping.get(tuple(value))

# Example usage
A = [[12, 23, 23], [231, 124, 87], [43, 68, 178]]
B = [[43, 68, 178], [12, 23, 23], [231, 124, 87]]
C = [[16, 213, 213], [231, 224, 53], [49, 168, 278]]

# Create the mapping
mapping = create_mapping(B, A, C)

# Input value from A
input_value = [43, 68, 178]

# Find corresponding C value
corresponding_C_value = find_corresponding_color(input_value, mapping)
print(corresponding_C_value)