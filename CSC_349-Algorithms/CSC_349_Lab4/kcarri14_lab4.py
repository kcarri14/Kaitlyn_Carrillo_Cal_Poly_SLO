import sys

def Levenchstein_distance(str1, str2, m, n):
    if m == 0:
        return n
    if n == 0:
        return m
    if str1[m-1] == str2[n-1]:
        return Levenchstein_distance(str1, str2, m-1 , n-1 )

    return 1 + min(
        Levenchstein_distance(str1, str2, m, n-1),
        min( Levenchstein_distance(str1, str2, m-1, n),
            Levenchstein_distance(str1, str2, m-1, n-1))
    )

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py string1 string2")
        sys.exit(1)
    str1 = sys.argv[1].upper()
    str2 = sys.argv[2].upper()

    answer = Levenchstein_distance(str1, str2, len(str1), len(str2))

    print(answer)

if __name__ == '__main__':
    main()



     