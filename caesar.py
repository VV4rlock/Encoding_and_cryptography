#!/usr/bin/python3

import argparse

alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
offset = 5

def main(text):
    l=len(alphabet)
    for char in text:
        if char in alphabet:
            print(alphabet[(alphabet.index(char)+offset)%l], end="")
        else:
            print(char, end="")
    print()


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-o","--offset", help="caesar offset. default offset - 5")
    args=parser.parse_args()
    if args.offset:
        try:
            offset=int(args.offset)
        except:
            print("Invalid offset!!!")
            exit(1)
    text = input().lower()
    main(text)
