def read_file(file_name_in):
    '''
    Read matrix from file

    Inputs:
        file_name_in : str
            The name of input file

    Outputs:
        marix : list (of list)
            Matrix which is read from file
    '''
    # Open file
    file = open(file_name_in, "r")
    # Initiate a list
    matrixList = []

    # Analyzing info in file
    for each_row in file:
        temp = []
        # Remove all separators then put into a list
        value = each_row.split()
        # Get each value in a set of value
        for i in value:
            temp.append(int(i))
        matrixList.append(temp)

    # Close file
    file.close()
    return matrixList

def write_file(file_name_out, determinant, inverse_matrix):
    '''
    Write determinant and inversed matrix into file

    Inputs:
        file_name_out : str
            The name of output file

        determinant : int or float
            The determinant of matrix read from input file

        inversed_matrix : list (of list)
            The inverse of matrix read from input file
    '''

    outFile = open(file_name_out, "w")
    outFile.write("Det: " + str(int(determinant)) + '\n\n')
    outFile.write("Inverse Matrix:\n")
    if(determinant == 0):
        outFile.write("None")
    else:
        for row in range(len(inverse_matrix)):
            for col in range(len(inverse_matrix)):
                outFile.write(str(inverse_matrix[row][col]) + " ")
            outFile.write("\n") 
    outFile.close()

def _Duplicate(matrix):
    dupMatrix = []
    for each_row in matrix:
        temp = []
        for value in each_row:
            temp.append(value)
        dupMatrix.append(temp)
            
    return dupMatrix

def _isZeroMatrix(matrix):
    for each_row in matrix:
        for value in each_row:
            if(value != 0):
                return False
    return True

def _swapRow(matrix):
    _nonZero = None
    matrix_size = len(matrix)
    if(matrix[0][0] == 0):
        _isZero = 0
        for row in range(matrix_size):
            if(matrix[row][0] != 0):
                _nonZero = row
                break
    if(_nonZero != None):
        matrix[_isZero], matrix[_nonZero] = matrix[_nonZero], matrix[_isZero]
        return True
    return False

def swapRow_iMatrix(iMatrix, matrix):
    _nonZero = None
    for i in range(len(matrix)):
        if(matrix[i][0] != 0):
            _nonZero = i
            break
    iMatrix[0], iMatrix[_nonZero] = iMatrix[_nonZero], iMatrix[0]

def eyeMatrix_Initializer(size):
    iMatrix = []
    for row in range(size):
        temp = []
        for col in range(size):
            temp.append(1) if (row == col) else temp.append(0)
        iMatrix.append(temp)
    return iMatrix

def _formatMatrix(iMatrix):
    for row in range(len(iMatrix)):
        for col in range(len(iMatrix)):
            iMatrix[row][col] = round(iMatrix[row][col], 2)
                        
def calc_determinant_row_operation(matrix):
    '''
    Calculate determinant of input matrix

    Inputs:
        marix : list (of list)
            Matrix which is read from file

    Outputs:
        determinant : int or float
            The determinant of input matrix
    '''
    # Return 0 as soon as a zero matrix
    if(_isZeroMatrix(matrix)):
        return 0
        
    matrix_size = len(matrix)
    # Create a replica of original matrix cause we don't want to mess up the main one
    dupMatrix = _Duplicate(matrix)
    # Check if a swap is implemented
    isSwap = _swapRow(dupMatrix)            
    
    for diag_i in range(matrix_size):
        for below_diag in range(diag_i + 1, matrix_size):
            if(dupMatrix[diag_i][diag_i] == 0):
                dupMatrix[diag_i][diag_i] = 1.0e-18
            row_Scaler = dupMatrix[below_diag][diag_i] / dupMatrix[diag_i][diag_i]
            for value_i in range(matrix_size):
                dupMatrix[below_diag][value_i] = dupMatrix[below_diag][value_i] - row_Scaler * dupMatrix[diag_i][value_i]
    
    determinant_Val = 1.0
    for i in range(matrix_size):
        determinant_Val *= dupMatrix[i][i]
    determinant_Val = round(determinant_Val, 2)
    if(abs(determinant_Val) == 0.0): 
        return 0.0
    return determinant_Val * (-1.0) if isSwap == True else determinant_Val

def invert_matrix_row_operation(matrix):
    '''
    Invert a matrix

    Inputs:
        marix : list (of list)
            Matrix which is read from file

    Outputs:
        inverse_matrix : list (of list) or None
            The inverse of input matrix
            `None` when the input matrix is not invertible
    '''

    if(calc_determinant_row_operation(matrix) == 0.0):
        return None
    
    # Create identity matrix
    iMatrix = eyeMatrix_Initializer(len(matrix))
    
    # Create a copy of original matrix
    dupMatrix = _Duplicate(matrix)
    
    # Check if any swaps are implemented 
    if(_swapRow(dupMatrix)):
        swapRow_iMatrix(iMatrix, matrix)
    matrix_size = len(matrix)
    for diag_i in range(matrix_size):
        diag_scaler = dupMatrix[diag_i][diag_i]
        # if the current value in diagonal that equals to zero, we need to swap with another row whose value is non-zero
        if(diag_i > 0 and diag_scaler == 0.0):
            next_row = diag_i + 1
            while(dupMatrix[next_row][diag_i] == 0.0):
                next_row += 1
            dupMatrix[diag_i], dupMatrix[next_row] = dupMatrix[next_row], dupMatrix[diag_i]
            iMatrix[diag_i], iMatrix[next_row] = iMatrix[next_row], iMatrix[diag_i]
            diag_scaler = dupMatrix[diag_i][diag_i]
        # Execute row which has diagonal element
        for value_i in range(matrix_size):
            dupMatrix[diag_i][value_i] /= diag_scaler
            iMatrix[diag_i][value_i] /= diag_scaler
        # Execute relevant rows
        # for row in matrix[0, diag_i] + matrix[diag_i + 1, 0]:
        for row in range(matrix_size):
            if(row == diag_i):
                continue
            row_scaler = dupMatrix[row][diag_i]
            for col in range(matrix_size):
                dupMatrix[row][col] = dupMatrix[row][col] - row_scaler * dupMatrix[diag_i][col]
                iMatrix[row][col] = iMatrix[row][col] - row_scaler * iMatrix[diag_i][col]
    _formatMatrix(iMatrix)
    return iMatrix
    
def main():
    matrix = read_file(file_name_in='input.txt')
 
    det = calc_determinant_row_operation(matrix)
    
    inv_mat = invert_matrix_row_operation(matrix) 
    write_file(file_name_out='19127017_output.txt', determinant=det, inverse_matrix=inv_mat)


if __name__ == '__main__':
    main()
