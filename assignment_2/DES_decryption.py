from global_values import *

subKeys = []

# This function converts and returns a binary number with the given hexadecimal value
def getBinary(hex):
    # Convert hex to integer, then to binary, and pad with leading zeros to make it 64 bits
    return bin(int(hex, 16))[2:].zfill(64)

# This function converts and returns a binary number to a decimal
def getDecimal(binary):
    decimal = int(binary, 2)  # Convert binary to decimal
    return decimal

# This function converts and returns a binary value to hexadecimal. Also adds padding so that there are 64 bits
def getHex(binary):
    # Convert the binary string to an integer and then to a hexadecimal string
    hex_value = hex(int(binary, 2))[2:].upper()
    return hex_value.zfill(16)  # zfill to make sure it matches a 64-bit hex (16 hex digits)

# This function finds and returns the bit at the given position
def findBit(binary, position):
    # position is subtracted by 1 so that we start at number 1 and not 0
    position = position - 1
    if(position > len(binary) - 1 or position < 0):
        return print("Out of range")
    else:
        return binary[position]

# This function rearranges the bits based on the given table and binary table
def rearrangeBits(table, originalBinary):
    permutedBinary = ""
    for i in range(len(table)):
        tablePosition = table[i]
        binaryBit = findBit(originalBinary, tablePosition)
        permutedBinary += binaryBit
    return permutedBinary

# Splits the binary number in half and gets the left half
def getLeftHalf(binary):
    half = len(binary) // 2 # Get the midpoint of the string
    leftHalf = binary[:half] # Slicing from beginning to half way
    return leftHalf

# Splits the binary number in half and gets the right half
def getRightHalf(binary):
    half = len(binary) // 2  # Integer division to get the halfway point
    rightHalf = binary[half:]  # Slicing from halfway to the end
    return rightHalf

# Get all subkeys (16 keys) from c0 and d0 using left shift rotation
def getSubKeys(c0, d0):
    cN, dN = c0, d0
    for shift in shiftTable:
        # Shifts x amount of bits to left on c sub n and d sub n
        cN = cN[shift:] + cN[:shift]  
        dN = dN[shift:] + dN[:shift]
        # Concatenates c sub n and d sub n and rearranges the bits using the pc2 table
        subKeyN = rearrangeBits(pc2table, cN + dN)
        subKeys.append(subKeyN)  # Appends the subkey to subkeys list

# The fBox function, which uses the expanded right side and the subkey to perform XOR, applies s-boxes, and then permutes the result
def fBox(rightSideCurrent, subKey):
    # Get expansion from 32 bits to 48 bits
    expanded = rearrangeBits(expansionTable, rightSideCurrent)

    # Convert the binary strings to integers
    a_int = int(subKey, 2)
    b_int = int(expanded, 2)

    # Perform XOR
    result = a_int ^ b_int

    # Convert the result back to a binary string
    result_bin = bin(result)[2:].zfill(48)

    finalResultBin = ''

    # An array of 2D arrays for the 8 s-boxes
    s_boxes = [s1, s2, s3, s4, s5, s6, s7, s8]

    # Loop through the binary string in 6-bit segments
    for i in range(0, len(result_bin), 6):
        # Grab a 6-bit segment
        segment = result_bin[i:i + 6]

        # Construct the row and column strings based on the bits from the segment
        rowNumber = int((segment[0] + segment[5]), 2)  # First and last bit for row
        columnNumber = int(segment[1:5], 2)            # Bits from position 1 to 4 for column

        # Access the appropriate s-box using the index
        s_box = s_boxes[i // 6]  # This will switch to the next s-box in each iteration

        # Get the value from the s-box
        newSBoxValueDecimal = s_box[rowNumber][columnNumber]
        newSBoxValueBin = bin(newSBoxValueDecimal)[2:].zfill(4)  # Convert to 4-bit binary

        # Concatenate binary number
        finalResultBin = finalResultBin + newSBoxValueBin

    # Rearrange bits using the f-box permutation table
    return rearrangeBits(fBoxPermutation, finalResultBin)

# Perform 16 decryption rounds (subkeys are applied in reverse)
def doDecryptionRounds(l0, r0):
    leftSideCurrent = l0
    rightSideCurrent = r0

    # Loop in reverse for decryption (apply subkeys in reverse)
    for i in reversed(range(16)):
        # XOR the left side and f-box result
        fBoxResult = int(fBox(rightSideCurrent, subKeys[i]), 2)
        rightSideNext = bin(int(leftSideCurrent, 2) ^ fBoxResult)[2:].zfill(32)  # Convert back to binary format

        # Swap the left and right sides
        leftSideCurrent = rightSideCurrent
        rightSideCurrent = rightSideNext

    # Final round: concatenate right and left, then apply final permutation
    finalRoundBin = rightSideCurrent + leftSideCurrent
    return rearrangeBits(finalPermutation, finalRoundBin)

# Main function for decryption process
def main():
    # Get ciphertext input from user and convert it to binary
    cipherText = input("Input ciphertext as a hex value: ")
    binaryCipherText = getBinary(cipherText)

    # Step 1: Create 16 subkeys, each of which is 48-bits long (the same as in encryption)
    # Get k+ by taking the key and rearranging using pc1 table
    kPlus = rearrangeBits(pc1Table, getBinary(key))
    # Get the left and right halves of k+
    c0 = getLeftHalf(kPlus)
    d0 = getRightHalf(kPlus)
    # Generate 16 subkeys
    getSubKeys(c0, d0)

    # Step 2: Perform the decryption
    # Rearrange ciphertext with the initial permutation table
    initialPermutedCipherText = rearrangeBits(initialPermutationTable, binaryCipherText)

    # Split rearranged ciphertext in half to get left and right halves
    l0 = getLeftHalf(initialPermutedCipherText)
    r0 = getRightHalf(initialPermutedCipherText)

    # Do 16 rounds of decryption
    plainTextBinary = doDecryptionRounds(l0, r0)
    
    # Convert binary result to hex and print the decrypted plaintext
    plainTextHex = getHex(plainTextBinary)
    print("Decrypted plaintext (hex):", plainTextHex)

# Entry point for program
if __name__ == "__main__":
    main()