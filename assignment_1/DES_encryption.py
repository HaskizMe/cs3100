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

# Splits the binary number in half and get the right half
def getRightHalf(binary):
    half = len(binary) // 2  # Integer division to get the halfway point
    rightHalf = binary[half:]  # Slicing from halfway to the end
    return rightHalf

def getMessageInput():
    while True:
        inputMessage = input("Input message as a hex value: ")
        try:
            return getBinary(inputMessage) # Will check if it can be converted to binary
        except:
            print("ERROR: Please input a valid hex value.")

# Get all sub keys 16 keys from c0 and d0 using left shift rotation
def getSubKeys(c0, d0):
    cN = c0
    dN = d0
    for i in range(len(shiftTable)):
        cN = cN[shiftTable[i]:] + cN[:shiftTable[i]] # Shifts x amount of bits to left on c sub n
        dN = dN[shiftTable[i]:] + dN[:shiftTable[i]] # Shifts x amount of bits to left on d sub n
        subKeyN= rearrangeBits(pc2table, cN + dN) # concatenates c sub n and d sub n and rearranges the bits using pc2 table
        subKeys.append(subKeyN) # Appends the sub key to sub keys list

# Defining main function
def main():
    # message = getMessageInput() # This gets user input
    # print(message)
    message = "0123456789ABCDEF"
    # print(getBinary(message))
    # key = "133457799BBCDFF1"
    # print(getBinary(key))
    # print(findBit(getBinary(key), 1))
    kPlus = rearrangeBits(pc1Table, getBinary(key))
    c0 = getLeftHalf(kPlus)
    d0 = getRightHalf(kPlus)

    getSubKeys(c0, d0)

    initialPermutedMessage = rearrangeBits(initialPermutationTable, getBinary(message))
    l0 = getLeftHalf(initialPermutedMessage)
    r0 = getRightHalf(initialPermutedMessage)
    # print(l0)
    # print(r0)
    #print(initialPermutedMessage)
    # for i in range(len(subKeys)):
    #     print(f"i: {i+1} {subKeys[i]}\n")
    #print(subKeys)
    # print("11110000110011001010101011110101010101100110011110001111")



# Entry point for program
if __name__=="__main__":
    # Step 1: Create 16 sub keys, each of which is 48-bits long:
        # Get k+ by taking key and rearrange using pc1 table
        # Get the left and right half of k+
        # Get 16 sub keys by shifting the bits by rotating on each iteration of left half sub n and right half sub n. Shift using the shift table
        # Concatenate both halves and rearrange new bits with pc2 table

    # Step 2: Encode each 64-bit block of data:
        # Rearrange message with initial permutation table 
        # Split rearranged message in half getting both the left and right half l0 and r0

    main()
