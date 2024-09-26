import math

# Helper function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to get a prime number from the user
def get_prime(prompt):
    while True:
        try:
            num = int(input(prompt))
            if is_prime(num):
                return num
            else:
                print("That's not a prime number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Function to find e where gcd(e, phiN) == 1
def find_e(phiN):
    for i in range(2, phiN):  # Start from 2
        if math.gcd(i, phiN) == 1:
            return i
    return None

# Extended Euclidean Algorithm to find d (modular inverse of e mod phiN)
def mod_inverse(e, phiN):
    # Initialize variables for the extended Euclidean algorithm
    t, new_t = 0, 1
    r, new_r = phiN, e

    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r

    # Make sure t is positive
    if t < 0:
        t = t + phiN

    return t

# Main function for RSA Algorithm 
def main():
    # Step 1: Get two prime numbers
    p = get_prime("Enter prime number 1: ")
    q = get_prime("Enter prime number 2: ")

    # Step 2: Find n by multiplying p and q
    n = p * q

    # Step 3: Get φ(n) by calculating (p-1) * (q-1)
    phiN = (p - 1) * (q - 1)

    # Step 4: Find e such that e is coprime with φ(n)
    e = find_e(phiN)

    # Step 5: Find d such that (e * d) % phiN == 1 using the Extended Euclidean Algorithm
    d = mod_inverse(e, phiN)

    # Step 6: Construct key pairs public 
    print(f"Public Key Pair: ({n}, {e})")
    print(f"Private Key: {d}")
    # Output the results
    # print(f"Prime number 1 (p): {p}")
    # print(f"Prime number 2 (q): {q}")
    # print(f"n (p * q): {n}")
    # print(f"φ(n) ((p-1) * (q-1)): {phiN}")
    # print(f"e (where gcd(e, φ(n)) = 1): {e}")
    # print(f"d (modular inverse of e mod φ(n)): {d}")

# Entry point for program
if __name__ == "__main__":
    main()