import math
import time

# A global cache (memoization) for the phi function to avoid re-computation.
# This is crucial for performance, especially for the S3 calculation.
PHI_CACHE = {}


def prime_sieve(limit):
    """
    Generates primes up to a given limit using the Sieve of Eratosthenes.
    Returns a list of primes.
    """
    primes = []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, limit + 1):
        if is_prime[p]:
            primes.append(p)
            for i in range(p * p, limit + 1, p):
                is_prime[i] = False
    return primes


def get_pi_table(limit, primes):
    """
    Creates a lookup table for pi(x), the number of primes less than or equal to x.
    pi_table[i] = pi(i).
    """
    pi_table = [0] * (limit + 1)
    prime_idx = 0
    for i in range(1, limit + 1):
        if prime_idx < len(primes) and i == primes[prime_idx]:
            pi_table[i] = pi_table[i - 1] + 1
            prime_idx += 1
        else:
            pi_table[i] = pi_table[i - 1]
    return pi_table


def get_mu_table(limit):
    """
    Generates a lookup table for the Mobius function mu(n) up to a given limit.
    """
    mu = [0] * (limit + 1)
    lp = [0] * (limit + 1)
    primes = []
    mu[1] = 1
    for i in range(2, limit + 1):
        if lp[i] == 0:
            lp[i] = i
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if p > lp[i] or i * p > limit:
                break
            lp[i * p] = p
            if p == lp[i]:
                mu[i * p] = 0
            else:
                mu[i * p] = -mu[i]
    return mu


def phi(x, a, primes):
    """
    Computes the partial sieve function phi(x, a) recursively with memoization.
    phi(x, a) counts numbers <= x with all prime factors > p_a.
    This corresponds to the logic in §5, especially formula (7).
    """
    if (x, a) in PHI_CACHE:
        return PHI_CACHE[(x, a)]
    if a == 0:
        return math.floor(x)

    # Recursive step from Lemma 5.1, formula (7)
    res = phi(x, a - 1, primes) - phi(x / primes[a - 1], a - 1, primes)

    PHI_CACHE[(x, a)] = res
    return res


def S0_calc(x, y, mu_table):
    """
    Computes S0, the contribution of ordinary leaves.
    Corresponds to formula (9) in §5.
    S0 = sum_{n<=y} mu(n) * floor(x/n)
    """
    s0 = 0
    for n in range(1, y + 1):
        if mu_table[n] != 0:
            s0 += mu_table[n] * math.floor(x / n)
    return s0


def P2_calc(x, y, pi_table, primes_sieve):
    """
    Computes P2(x, a), the count of numbers that are a product of two primes > p_a.
    Corresponds to formula (5) in §4.
    P2(x,a) = sum_{y < p <= sqrt(x)} (pi(x/p) - pi(p) + 1)
    """
    p2 = 0
    sqrt_x = int(math.sqrt(x))

    # Find the index of the first prime > y
    start_idx = pi_table[y]
    end_idx = pi_table[sqrt_x]

    for i in range(start_idx, end_idx):
        p = primes_sieve[i]
        p2 += pi_table[int(x / p)] - pi_table[p] + 1

    return p2


def S1_calc(x, y, pi_table):
    """
    Computes S1 as defined in §6.1.
    S1 = ( (pi(y) - pi(x^(1/3))) * (pi(y) - pi(x^(1/3)) - 1) ) / 2
    This counts pairs of primes (p,q) where x^(1/3) < p < q <= y.
    """
    x_1_3 = int(x ** (1 / 3.0))
    pi_y_val = pi_table[y]
    pi_x_1_3 = pi_table[x_1_3]

    term = pi_y_val - pi_x_1_3
    return (term * (term - 1)) // 2


def S2_calc(x, y, pi_table, primes):
    """
    Computes S2 as defined in §6.2.
    This implementation follows the paper's logic of splitting S2 into parts,
    and using the optimized formula for the V component.
    """
    s2 = 0
    x_1_4 = int(x ** (1 / 4.0))
    x_1_3 = int(x ** (1 / 3.0))

    p_start_idx = pi_table[x_1_4]
    p_end_idx = pi_table[x_1_3]

    for i in range(p_start_idx, p_end_idx):
        p = primes[i]

        q_start_idx = pi_table[p]
        q_end_idx = pi_table[y]

        for j in range(q_start_idx, q_end_idx):
            q = primes[j]
            # The paper splits S2 into U and V based on whether x/pq < p.
            # For q > x/p^2 (part U), phi is 1.
            # For q <= x/p^2 (part V), phi is 2 - pi(p) + pi(x/pq).
            if q > x / (p * p):
                s2 += 1  # This is the U part
            else:
                s2 += 2 - pi_table[p] + pi_table[int(x / (p * q))]  # This is the V part

    return s2


def S3_calc(x, y, pi_table, mu_table, primes):
    """
    Computes S3 as defined in §7 and formula (11).
    S3 = - sum_{p <= x^(1/4)} sum_{m} mu(m) * phi(x/mp, pi(p)-1)
    where delta(m) > p and y/p < m <= y.
    """
    s3 = 0
    x_1_4 = int(x ** (1 / 4.0))

    # Sum over primes p up to x^(1/4)
    p_limit_idx = pi_table[x_1_4]
    for i in range(p_limit_idx):
        p = primes[i]
        pi_p_minus_1 = pi_table[p - 1]

        # Sum over m such that y/p < m <= y and smallest prime factor of m is > p
        m_start = int(y / p) + 1
        for m in range(m_start, y + 1):
            # Check if smallest prime factor of m is > p.
            # This check is slow. A better way would be to generate such m's.
            is_valid_m = True
            for prime_check_idx in range(i + 1):
                if m % primes[prime_check_idx] == 0:
                    is_valid_m = False
                    break

            if is_valid_m:
                # Correctly multiply by mu(m) as per formula (11)
                s3 -= mu_table[m] * phi(x / (m * p), pi_p_minus_1, primes)

    return s3


def pi_deleglise_rivat(x):
    """
    Main function to compute pi(x) using the Deleglise-Rivat method.
    Main formula from §3: pi(x) = phi(x, a) + a - 1 - P2(x, a)
    where phi(x, a) is decomposed into S0 + S, and S = S1 + S2 + S3.
    """
    if x < 2:
        return 0, 0.0
    if x <= 10000:  # For small x, a direct sieve is much faster
        return len(prime_sieve(int(x))), 0.0

    start_time = time.time()

    # --- Step 1: Parameter setup and pre-computation ---
    # Choose parameter y. The paper suggests y near x^(1/3).
    y = int(x ** (1 / 3.0))

    # **FIXED**: The sieve limit must be large enough for P2_calc.
    # The P2 calculation requires pi(x/p) where p > y. The largest value
    # needed is pi(x/y), so we must sieve up to at least x/y.
    sqrt_x = int(math.sqrt(x))
    sieve_limit = max(sqrt_x, int(x / y) + 2)  # Add a buffer

    # print(f"Calculating pi({x}) with y = {y}, sieve_limit = {sieve_limit}")

    # We need primes and pi_table up to the new sieve_limit
    # print("Sieving primes and creating lookup tables...")
    primes_sieve = prime_sieve(sieve_limit)
    pi_table = get_pi_table(sieve_limit, primes_sieve)
    mu_table = get_mu_table(y)

    # 'a' is the number of primes up to y
    a = pi_table[y]
    primes_y = primes_sieve[:a]

    # --- Step 2: Calculate the main components ---

    # P2: Sum over products of two large primes
    # print("Calculating P2...")
    p2 = P2_calc(x, y, pi_table, primes_sieve)

    # S0: Contribution from ordinary leaves
    # print("Calculating S0...")
    s0 = S0_calc(x, y, mu_table)

    # S1: Contribution from pairs of primes (p,q) where x^(1/3) < p < q <= y
    # print("Calculating S1...")
    s1 = S1_calc(x, y, pi_table)

    # S2: Contribution from pairs of primes (p,q) where x^(1/4) < p <= x^(1/3)
    # print("Calculating S2...")
    s2 = S2_calc(x, y, pi_table, primes_y)

    # S3: Contribution from more complex special leaves. This is the hardest part.
    # print("Calculating S3...")
    s3 = S3_calc(x, y, pi_table, mu_table, primes_y)

    # The full phi(x,a) is the sum of these components
    phi_val = s0 + s1 + s2 + s3

    # --- Step 3: Combine results using the main formula ---
    # pi(x) = phi(x, a) + a - 1 - P2(x, a)
    result = phi_val + a - 1 - p2

    end_time = time.time()
    # print(f"\n--- Calculation Summary ---")
    # print(f"P2       = {p2}")
    # print(f"S0       = {s0}")
    # print(f"S1       = {s1}")
    # print(f"S2       = {s2}")
    # print(f"S3       = {s3}")
    # print(f"phi(x,a) = {phi_val}")
    # print(f"a        = {a}")
    # print(f"Result (phi + a - 1 - P2) = {result}")
    # print(f"Total time: {end_time - start_time:.2f} seconds")

    return int(result), end_time - start_time


# --- Example Usage ---
# NOTE: This implementation is for educational purposes to demonstrate the
# algorithm's structure. It is NOT optimized for speed and will be very slow
# for large x (e.g., > 10^8) due to the non-optimized S2 and S3.
# The paper's performance claims rely on C++ and complex low-level optimizations.

if __name__ == "__main__":
    # A small value to test correctness
    x_val = 100000
    print(f"\nCalculating for x = {x_val}...")
    pi_val, total_time = pi_deleglise_rivat(x_val)

    # Verification
    actual_pi = len(prime_sieve(x_val))
    print(f"\nFinal Result for pi({x_val}): {pi_val}")
    print(f"Actual value for pi({x_val}): {actual_pi}")
    print(f"Difference: {actual_pi - pi_val}")

    # A larger value that will be slow with this Python script
    # x_val_large = 10**7
    # print(f"\nCalculating for x = {x_val_large}...")
    # pi_val_large, _ = pi_deleglise_rivat(x_val_large)
    # print(f"\nFinal Result for pi({x_val_large}): {pi_val_large}")
    # actual_pi_large = len(prime_sieve(x_val_large))
    # print(f"Actual value for pi({x_val_large}): {actual_pi_large}")
