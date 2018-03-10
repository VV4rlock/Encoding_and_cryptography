#!/usr/bin/python3

import argparse


alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
offset_alphabet="абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

def main(text,key,decr=1):
    l=len(alphabet)
    key_length=len(key)
    k=0
    for char in text:
        if char in alphabet:
            print(alphabet[(alphabet.index(char)+decr*offset_alphabet.index(key[k]))%l],end="")
            k=(k+1)%key_length
        else:
            print(char,end="")
    print()





if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("key", help="key")
    parser.add_argument("-d","--decrypt")
    args=parser.parse_args()
    key=args.key.lower()
    for k in key:
        if k not in offset_alphabet:
            print("invalid key!")
            exit(1)
    text=input().lower()
    if args.decrypt:
        main(text,key,-1)
    else:
        main(text,key)