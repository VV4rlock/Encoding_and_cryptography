import numpy as np
import random

class RSA():
    @staticmethod
    def generate_big_integer(length_in_bits):
        temp=np.random.randint(0,2,length_in_bits,np.int8)
        temp[-1]=1
        return int("".join([str(i) for i in temp]),2)

    @staticmethod
    def pow(a,b,n): # a^b mod n
        t = 1
        while (b > 1):
            if b % 2 == 0:
                b /= 2
                a = (a * a) % n
            else:
                t = (t * a) % n
                b -= 1
        return (t * a) % n

    @staticmethod
    def miller_rabin(n,k=20):
        t = n - 1
        s = 0
        while t % 2 == 0:
            s += 1
            t //= 2
        for _ in range(k):  # n-1=2^s*t
            a = random.randint(2, n - 1)
            x = pow(a, t, n)
            if x == 1 or x == n - 1:
                continue
            flag = False
            for i in range(s):
                x = x * x % n
                if x == n - 1:
                    flag = True
                    break
                elif x == 1:
                    return False  # composite
            if flag:
                continue
            else:
                return False  # composite
        return True  # may be is prime

    @staticmethod
    def generate_big_prime(length_in_bits):
        big_int=RSA.generate_big_integer(length_in_bits)
        while not RSA.miller_rabin(big_int):
            big_int+=2
        return big_int

    @staticmethod
    def extend_evklid(b,n):
        '''return b^-1 mod n'''
        stack=[]
        a=n
        while a%b>0:
            stack.append(a//b)
            a,b=b,a%b
        x,y,count=0,1,len(stack)
        while count>0:
            x,y=y,x-y*stack.pop()
            count-=1
        return y if y>0 else y+n


if __name__=="__main__":
    print(RSA.extend_evklid(7,11))

