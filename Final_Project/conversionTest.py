import numpy as np
import matplotlib.pyplot as plt

def willthiswork(words):
    whoIsJohnGalt = "You typed the phrase : {}".format(words)
    n=0
    while True:
        if n:
            print(whoIsJohnGalt)
            break
        else:
            for i in np.arange(10):
                print("WTF?")
            n=1
        

willthiswork("Fuck me.")
