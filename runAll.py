import kallxo
import koha
import kosovaSot
import telegrafi
import time

print("Running Server!")
while True:
    kallxo.getData()
    koha.getData()
    kosovaSot.getData()
    telegrafi.getData()
    time.sleep(3600)