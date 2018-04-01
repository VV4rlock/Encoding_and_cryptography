import numpy as np
import random

from PyQt5.QtWidgets import QWidget, QTextEdit, QGridLayout, QApplication, QPushButton, QHBoxLayout, QLabel, QMessageBox
import sys

class RSA():

    def __init__(self,binary_length=512):
        p = RSA.generate_big_prime(binary_length)
        q = RSA.generate_big_prime(binary_length)

        while(p == q):
            q = RSA.generate_big_prime(binary_length)
            print("warning: p == q ")

        self.__n= p * q

        self.__n_length=self.__n.bit_length()
        self.__phi_n= (p - 1) * (q - 1)
        self.__e=RSA.generate_big_prime(self.__n_length//3)

        while(self.__phi_n%self.__e==0):
            self.__e=RSA.generate_big_prime(self.__n_length//3)
            print("warning: phi_n % e == 0")

        self.__d=RSA.extend_evklid(self.__e, self.__phi_n)

        #print("ed%phi: ",self.__e*self.__d%self.__phi_n)

        self.__binary_e=np.array(list(map(int,bin(self.__e)[2:])))
        self.__binary_d = np.array(list(map(int, bin(self.__d)[2:])))

    def set(self,N,phi_n,d,e):
        self.__n=N
        self.__phi_n=phi_n
        self.__d=d
        self.__e=e
        self.__binary_e = np.array(list(map(int, bin(self.__e)[2:])))
        self.__binary_d = np.array(list(map(int, bin(self.__d)[2:])))

    def get_params(self):
        return (self.__n, self.__phi_n, self.__d, self.__e)


    def get_private_key(self):
        return (self.__phi_n, self.__d)

    def get_public_key(self):
        return (self.__n, self.__e)

    def e_pow_modN(self,a): #a^e%N
        c = a
        for i in range(1, len(self.__binary_e)):
            c = c * c * a % self.__n if self.__binary_e[i] == 1 else c * c % self.__n
        return c

    def d_pow_modN(self,a): #a^d%N
        c = a
        for i in range(1, len(self.__binary_d)):
            c = c * c * a % self.__n if self.__binary_d[i] == 1 else c * c % self.__n
        return c

    def print_params(self):
        print("PUBLIC_KEY: {}".format(self.get_public_key()))
        print("PRIVATE_KEY: {}".format(self.get_private_key()))



    def encode(self, data):
        block_length_in_bytes=(self.__n_length)//8
        block_for_transf = (self.__n_length + 7) // 8 #из байт в число и обратно
        #print("n_length: ",self.__n_length)
        #print("block_length: ",block_length_in_bytes)
        number_of_blocks=(len(data)+block_length_in_bytes-1)//block_length_in_bytes
        fill_block=number_of_blocks*block_length_in_bytes-len(data)
        while(fill_block>0): #дополняем массив данных до полного блока
            data.append(0)
            fill_block -= 1
        encoded=[]
        #mes=[]
        #right=[]
        #print(self.__n)
        for i in range(number_of_blocks):
            index=i*block_length_in_bytes
            A=int.from_bytes(data[index:index + block_length_in_bytes], 'big')
            #mes.append(A)
            encoded.append(self.e_pow_modN(A))
            #right.append(pow(encoded[-1],self.__d,self.__n))
        #print(mes)
        #print(encoded)
        #print(right)
        out=bytearray()
        for i in encoded:
            out.extend(bytearray(i.to_bytes(block_for_transf, 'big')))
        return out



    def decode(self,enc_data):
        block_length_in_bytes = (self.__n_length+7) // 8
        block_for_transf=self.__n_length // 8
        decoded=[]
        e_m=[]
        for i in range(len(enc_data)//block_length_in_bytes):
            index=i*block_length_in_bytes
            B=int.from_bytes(enc_data[index:index+block_length_in_bytes], 'big')
            e_m.append(B)
            decoded.append(self.d_pow_modN(B))
        #print(e_m)
        #print(decoded)
        out=bytearray()
        for i in decoded:
            out.extend(bytearray(i.to_bytes(block_for_transf, 'big')))
        while(out[-1]==0):
            out.pop()
        return out




    @staticmethod
    def generate_big_integer(length_in_bits):
        temp=np.random.randint(0,2,length_in_bits,np.int8)
        temp[-1]=1
        return int("".join([str(i) for i in temp]),2)



    @staticmethod
    def pow(a,b,n): # a^b mod n
        t = bin(b)[2:]
        c=a
        for i in range(1,len(t)):
            c=c*c*a % n if t[i]=='1' else c*c%n
        return c




    @staticmethod
    def miller_rabin(n,k=20): #k=len(bin(N))
        t = n - 1
        s = 0
        while t % 2 == 0:
            s += 1
            t //= 2
        a_list=[]
        for _ in range(k):  # n-1=2^s*t
            a = random.randint(2, n - 1)
            while(a in a_list):
                a = random.randint(2, n - 1)
            a_list.append(a)
            x = RSA.pow(a, t, n)
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
    def generate_big_prime(length_in_bits,rounds_count=None):
        if rounds_count is None:
            rounds_count=length_in_bits
        big_int=RSA.generate_big_integer(length_in_bits)
        while not RSA.miller_rabin(big_int,rounds_count):
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





class vis(QWidget):
    def __init__(self):
        super().__init__()
        grid=QGridLayout()
        self.setLayout(grid)

        N_box=QHBoxLayout()
        self.N=QTextEdit()
        self.N.setFixedHeight(30)
        N_box.addStretch()
        N_box.addWidget(QLabel("N=",self))
        N_box.addWidget(self.N)
        grid.addLayout(N_box, 0, 0)

        phi_N_box = QHBoxLayout()
        self.phi_N = QTextEdit()
        self.phi_N.setFixedHeight(30)
        phi_N_box.addStretch()
        phi_N_box.addWidget(QLabel("phi(N)=", self))
        phi_N_box.addWidget(self.phi_N)
        grid.addLayout(phi_N_box, 0, 1)

        e_box = QHBoxLayout()
        self.e = QTextEdit()
        self.e.setFixedHeight(30)
        e_box.addStretch()
        e_box.addWidget(QLabel("e=", self))
        e_box.addWidget(self.e)
        grid.addLayout(e_box, 1, 0)

        d_box = QHBoxLayout()
        self.d = QTextEdit()
        self.d.setFixedHeight(30)
        d_box.addStretch()
        d_box.addWidget(QLabel("d=", self))
        d_box.addWidget(self.d)
        grid.addLayout(d_box, 1, 1)


        self.message=QTextEdit()
        self.message.setPlainText("message")
        grid.addWidget(self.message,2,0)

        self.result_text = QTextEdit()
        grid.addWidget(self.result_text,2,1)

        hbox = QHBoxLayout()

        encode_btn = QPushButton("encode")
        decode_btn = QPushButton("decode")
        generate_btn = QPushButton("generate")

        encode_btn.clicked.connect(self.on_encode_clicked)
        decode_btn.clicked.connect(self.on_decode_clicked)
        generate_btn.clicked.connect(self.on_generate_clicked)

        hbox.addStretch()
        hbox.addWidget(generate_btn)
        hbox.addWidget(decode_btn)
        hbox.addWidget(encode_btn)


        grid.addLayout(hbox, 3, 0, 1, 3)


        self.show()




    def on_encode_clicked(self):
        mes=bytearray(self.message.toPlainText().encode("utf-8"))
        self.r.set(*self.get_params())
        try:
            enc=self.r.encode(mes)
        except:
            QMessageBox.warning(self,"warning!","не удалось закодировать!")
        self.result_text.setPlainText(str(enc)[10:-1])


    def on_decode_clicked(self):
        enc=eval(self.result_text.toPlainText())
        try:
            self.message.setPlainText(self.r.decode(enc).decode("utf-8"))
        except:
            QMessageBox.warning(self,"warning!","не удалось декодировать")

    def get_params(self):
        a=[self.N.toPlainText(), self.phi_N.toPlainText(), self.d.toPlainText(), self.e.toPlainText()]
        a=list(map(int,a))
        return a


    def on_generate_clicked(self):
        self.r=RSA(20)
        par=self.r.get_params()
        self.N.setPlainText(str(par[0]))
        self.phi_N.setPlainText(str(par[1]))
        self.d.setPlainText(str(par[2]))
        self.e.setPlainText(str(par[3]))

if __name__=="__main__":
    app = QApplication(sys.argv)
    ex = vis()
    sys.exit(app.exec_())
