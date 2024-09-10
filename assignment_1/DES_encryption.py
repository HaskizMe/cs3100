pc1Table = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

shiftTable = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
subKeys = []

def getBinary(hex):
    # Convert hex to integer, then to binary, and pad with leading zeros to make it 64 bits
    return bin(int(hex, 16))[2:].zfill(64)
    
def getHex(binary):
    # Convert the binary string to an integer and then to a hexadecimal string
    hex_value = hex(int(binary, 2))[2:].upper()
    return hex_value.zfill(16)  # zfill to make sure it matches a 64-bit hex (16 hex digits)

def findBit(binary, position):
    # position is subtracted by 1 so that we start at number 1 and not 0
    position = position - 1
    if(position > len(binary) - 1 or position < 0):
        return print("Out of range")
    else:
        return binary[position]
    
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

# Defining main function
def main():
    message = "0123456789ABCDEF"
    key = "133457799BBCDFF1"
    # print(getBinary(key))
    # print(findBit(getBinary(key), 1))
    rearrangeBits(pc1Table, getBinary(key))
    print(getLeftHalf(rearrangeBits(pc1Table, getBinary(key))))
    print("1111000011001100101010101111\n")
    print(getRightHalf(rearrangeBits(pc1Table, getBinary(key))))
    print("0101010101100110011110001111")
    # print("11110000110011001010101011110101010101100110011110001111")



# Entry point for program
if __name__=="__main__":
    main()
