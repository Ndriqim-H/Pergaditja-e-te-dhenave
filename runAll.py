print("Po përgatitet programi. Ju lutemi prisni!")

import telegrafi
import kosovaSot
import kallxo
import koha
import time
import sys
import datetime


while True:

    print("Fillimi i kërkimit të të dhënave fillon!")
    tel = telegrafi.getData()
    kos = kosovaSot.getData()
    kall = kallxo.getData()
    kohaNet = koha.getData()
    print("\n"+"="*100)
    print("Kërkimi i faqeve përfundoi, tani presim 1 orë.")
    for i in range(3600, 0,-1):
        timeLeft = str(datetime.timedelta(seconds=i))
        sys.stdout.write('Koha e mbetur: '+timeLeft+'\r')
        sys.stdout.flush()
        # print('Koha e mbetur: '+timeLeft+' ', end='\r')
        time.sleep(1)

    # time.sleep(3600)