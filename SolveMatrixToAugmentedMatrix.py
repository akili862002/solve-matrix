from numpy import array as ToArray
from copy import deepcopy

def multiplyArray(arr, mul):
	for i in range(len(arr)):
		arr[i] *= mul
	return arr

def getSizeOfMatrix(matrix):
	m = len(matrix)
	n = len(matrix[0])
	return m, n

def isZeroRow(row):
	for i in range(0, len(row)):
		if row[i] != 0:
			return False
	return True

def shortFloat(num):
	return float("{0:.5f}".format(num))

def printMatrix(a):
	try:
		m, n = getSizeOfMatrix(a)
		# Clear matrix
		for i in range(m):
			for j in range(n):
				if a[i][j] == 0:
					a[i][j] = 0
				a[i][j] = shortFloat(a[i][j])
		print( ToArray(a))
	except:
		print("Print matrix Error!")

def getIndexOfFirstValidNumberInRow(row):
	for i in range(0, len(row)):
		if row[i] != 0:
			return i
	return len(row) - 1

def isAugmentedMatrix(matrix):
	m, n = getSizeOfMatrix(matrix)
	a = matrix

	if (a[0][0] == 0):
		return False

	for i in range(1, m):
		# wasDoneWithThisRow gonna be True if we found the first number
		#    which don't equal zero in this row.
		wasDoneWithThisRow = False
		for j in range(1, n):
			if (wasDoneWithThisRow == False) and (a[i][j] != 0):
				if (i != m - 1) and (a[i+1][j] != 0): 
					# if item which below this item wasn't 0,
					 # that mean this matrix is not augmented
					return False
				#  Else, we won't do anything with the rest of this row
				wasDoneWithThisRow = True 

			elif (wasDoneWithThisRow == False) and (j == n - 1):
				# If this item is last item of row, that mean this is "zero row"
				if (i != m - 1) and (isZeroRow(a[i + 1]) == False):
					# if this is not a last row and the next row isn't a "zero row"
					return False

	# If this matrix pass everything condition,
	#   That means this is Augmented matrix
	return True

def sortMatrix(matrix):
	m, n = getSizeOfMatrix(matrix)
	a = matrix
	# first, let make a array which contains index of first number which don't equal 0 in each row
	indexsOfEachRow = []
	for i in range(0, m):
		wasDoneWithThisRow = False
		for j in range(0, n):
			if (wasDoneWithThisRow == False):
				if (a[i][j] != 0) or (j == n - 1):
					# If this item don't equal 0 or is last item of row
					indexsOfEachRow.append(j)
					wasDoneWithThisRow = True

	# Now we got all indexs array. Next, we need to sort it how to 
	#   shape it like augmented matrix
	# Because we need to swap each row so it quite complex to use Quick Sort
	#  Just use normal sort
	for i in range(0, len(indexsOfEachRow)):
		for j in range(i + 1, len(indexsOfEachRow)):
			if indexsOfEachRow[i] > indexsOfEachRow[j]:
				# Swap item in indexsOfEachRow
				indexsOfEachRow[i], indexsOfEachRow[j] = indexsOfEachRow[j], indexsOfEachRow[i]
				# Swap row in matrix
				a[i], a[j] = a[j], a[i]

	return a

def createZeroInIndexOfCurrentRowByAnotherRow(rowA, rowB, index):
	commonMultiple = rowA[index] * rowB[index]
	rowA_divisor = commonMultiple/rowA[index]
	rowB_divisor = commonMultiple/rowB[index]
	for i in range(0, len(rowA)):
		rowA[i] = rowA[i]*rowA_divisor - rowB[i]*rowB_divisor

	return rowA

def createElementoryMatrix(n):
	elementoryMatrix = []
	for i in range(0, n):
		row = [0]*n
		row[i] = 1
		elementoryMatrix.append(row);

	return elementoryMatrix

def concatTwoMatrix(matrixA, matrixB):
	# ( [a1 a2...], [b1 b2...]) --> ([a1 a2... b1 b2...])
	result = matrixA

	for i in range(0, len(result)):
		result[i] += matrixB[i]

	return result

def splitMatrix(matrix, cutPoint):
	firstMatrix = []
	secondMatrix = []
	for i in range(0, len(matrix)):
		firstMatrix.append(matrix[i][:cutPoint])
		secondMatrix.append(matrix[i][cutPoint:])

	return firstMatrix, secondMatrix

def convertToCompactMatrix(matrix):
	m, n = getSizeOfMatrix(matrix)
	a = matrix

	# Process with every row expect first row
	for i in range(m-1, 0, -1): # (m-1 --> 1)
		# if this row is a "zero row", just ignore it
		# Else,
		if (isZeroRow(a[i]) == False):
			IOFVN_in_row = getIndexOfFirstValidNumberInRow(a[i])
			# Every number on top of IOFVN of this row have to equal zero
			for countdownRow in range(i-1 , -1, -1): # (i - 1 --> 0)
				if a[countdownRow][IOFVN_in_row] != 0:
					a[countdownRow] = createZeroInIndexOfCurrentRowByAnotherRow(
						a[countdownRow], 
						a[i], 
						IOFVN_in_row
					)

	# Next step
	# make first valid number in each row equal 1
	for i in range(0, m):
		if isZeroRow(a[i]) == False:
			IOFVN_in_row = getIndexOfFirstValidNumberInRow(a[i])
			a[i] = multiplyArray(a[i], 1/a[i][IOFVN_in_row])

	return a 



def convertMatrixToAugmentedMatrix(matrix):
	m, n = getSizeOfMatrix(matrix)
	a = matrix

	# i = 1
	# # Handle matrix from step 1 to step 4
	# while (isAugmentedMatrix(a) == False):
	# 	# The first step: Sort martrix
	# 	matrix = sortMatrix(matrix)
	# 	# The second step:

	a = sortMatrix(a)
	# print('Matrix sorted:\n', ToArray(a), '\n');

	#[NOTE]: (IOFVN stands for "index of first valid number")
	IOFVN_in_previos_row = 0

	# We will process with all row except first row
	for i in range(1, m):
		IOFVN_in_row = getIndexOfFirstValidNumberInRow(a[i])
		if (IOFVN_in_row == IOFVN_in_previos_row) and (isZeroRow(a) == False):
			# Now we need to replace this row by a new row which has IOFVN in this row
			#   smaller IOFVN in previos row 
			previosRow = a[i - 1]
			currentRow = a[i]
			index = IOFVN_in_row

			a[i] = createZeroInIndexOfCurrentRowByAnotherRow(currentRow, previosRow, index)

			IOFVN_in_previos_row = getIndexOfFirstValidNumberInRow(currentRow)
		elif IOFVN_in_row < IOFVN_in_previos_row: 
			return convertMatrixToAugmentedMatrix(a)
		else:
			IOFVN_in_previos_row = getIndexOfFirstValidNumberInRow(a[i])

		# print('Matrix Solving -- step ' + str(i) + ':\n', ToArray(a), '\n');

	if (isAugmentedMatrix(a) == False):
		return convertMatrixToAugmentedMatrix(a)
	else:
		return a
		# return a

def getRootOfCompactMatrix(compactMatrix):
	# First, remove all zero row to compact matrix
	while isZeroRow(compactMatrix[len(compactMatrix) - 1]):
		del compactMatrix[len(compactMatrix) - 1]

	m, n = getSizeOfMatrix(compactMatrix)
	if (m >= n):
		return "no-roots"
	elif (m < n-1):
		return "countless-roots"
	elif (m == n-1):
		if (compactMatrix[m-1][n-1] == 0):
				return "no-roots"
		roots = []
		for i in range(0, m):
			row = compactMatrix[i]
			x = row[n-1]/row[i]
			x = shortFloat(x)
			roots = [x] + roots

		return roots


def getInvertibleMatrix(matrix):
	m, n = getSizeOfMatrix(matrix)
	if (m != n):
		print("   [FAIL] Cannot get invertible matrix. Because this matrix is not square!")
		return;

	elementoryMatrix = createElementoryMatrix(n)
	combinedMatrix = concatTwoMatrix(matrix, elementoryMatrix)

	augumentedMatrix = convertMatrixToAugmentedMatrix(combinedMatrix)
	compactMatrix = convertToCompactMatrix(augumentedMatrix)

	firstMatrix, secondMatrix = splitMatrix(compactMatrix, n)

	if (firstMatrix != elementoryMatrix):
		print("   [FAIL] Cannot get invertible matrix. Because the root of matrix is not a elementory!")
		return;

	return secondMatrix

# ---------------    < INPUT >    ---------
#  Please type your matrix here //////
initial_matrix = [
	[0, 1, 2],
	[1, 0, 3],
	[4, -3, 8]
]
# -------------------------

matrixInput = deepcopy(initial_matrix)

print('[INPUT-INFO] Initial Matrix: <<')
printMatrix(matrixInput)
print('>>')

print('\n[SYSTEM-INFO] Start Solving...\n')

print('[RESULT-INFO] Augmented Matrix: <<')
augumentedMatrix = convertMatrixToAugmentedMatrix(deepcopy(matrixInput)) 
printMatrix( augumentedMatrix )
print(">>\n")

print('[RESULT-INFO] Compact Matrix: <<')
compactMatrix = convertToCompactMatrix(deepcopy(augumentedMatrix))
printMatrix( compactMatrix )
print(">>\n")

print('[RESULT-INFO] Solve matrix equation: <<')
print('  -> Root of matrix: X =', getRootOfCompactMatrix(deepcopy(compactMatrix)) )
print(">>\n")

print('[RESULT-INFO] Invertible Matrix: <<')
printMatrix( getInvertibleMatrix(deepcopy(initial_matrix)) )
print(">>")


# This code was written by Nguyen Tien Dung
# Student-code: 20110090