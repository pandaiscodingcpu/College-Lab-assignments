import array as arr

mat_A = [[i for i in range(5)] for j in range(5)]
mat_B = [[i for i in range(6,11)] for j in range(5)]
mat_C = [[0]*5]*5
for i in range(5):
    for j in range(5):
        mat_C[i][j] = mat_A[i][j] + mat_B[i][j]

'''
for i in range(5):
    print(mat_C[i])
'''
print(mat_C)
