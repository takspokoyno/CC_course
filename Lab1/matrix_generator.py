import numpy as np

# Define the size of the matrices
SIZE = 1000

# Generate random matrices with integers between 1 and 9
matrix1 = np.random.randint(0, 10, size=(SIZE, SIZE))
matrix2 = np.random.randint(0, 10, size=(SIZE, SIZE))

# Save matrices to a text file
with open("matrices.txt", "w") as file:

    for row in matrix1:
        file.write(" ".join(map(str, row)) + "\n")

    file.write("\n")
    for row in matrix2:
        file.write(" ".join(map(str, row)) + "\n")

print("Matrices have been saved to matrices.txt")
