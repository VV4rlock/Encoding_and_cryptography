import sys
from PyQt5.QtWidgets import QWidget, QTextEdit, QGridLayout, QApplication, QPushButton, QHBoxLayout


class vis(QWidget):
    def __init__(self):
        super().__init__()
        grid=QGridLayout()
        self.setLayout(grid)
        self.key_text=QTextEdit()
        self.key_text.setPlainText("key")
        grid.addWidget(self.key_text,0,0)
        self.message=QTextEdit()
        self.message.setPlainText("message")
        grid.addWidget(self.message,1,0)

        hbox = QHBoxLayout()

        from_str_btn = QPushButton("from str")
        from_hex_btn = QPushButton("from hex")

        from_str_btn.clicked.connect(self.on_click_str)
        from_hex_btn.clicked.connect(self.on_click_hex)

        hbox.addStretch()
        hbox.addWidget(from_hex_btn)
        hbox.addWidget(from_str_btn)

        grid.addLayout(hbox, 3, 0, 1, 2)

        self.result_text=QTextEdit()
        grid.addWidget(self.result_text)

        self.show()




    def on_click_str(self):
        key=self.key_text.toPlainText().encode("utf-8")
        data=self.message.toPlainText().encode("utf-8")
        res=gam.encode(data,key)
        self.result_text.setPlainText(" ".join("%02x"%i for i in res))



    def on_click_hex(self):
        key = bytearray(map(gam.from_hex_to_int,self.key_text.toPlainText().split()))
        data = bytearray(map(gam.from_hex_to_int,self.message.toPlainText().split()))
        res = gam.encode(data, key)
        self.result_text.setPlainText(" ".join("%02x" % i for i in res))





class gam:

    @staticmethod
    def from_hex_to_int(h):
        return int(h,16)

    @staticmethod
    def encode(data,key):
        out=[]
        key_length = len(key)
        for i in range(len(data)):
            out.append(data[i] ^ key[i % key_length])
        return bytearray(out)







if __name__=="__main__":
    app = QApplication(sys.argv)
    ex = vis()
    sys.exit(app.exec_())
