from RandomNumberGeneration import LinearCongruentialGenerator, XorShiftGenerator
from PrimeTests import MillerRabin
import time

def bitLen(int_type):
    length = 0
    while (int_type):
        int_type >>= 1
        length += 1
    return(length)

numBitsList = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
sampleSize = 1;

seed = int(time.time())
lcg = LinearCongruentialGenerator(seed)
xsg = XorShiftGenerator(seed)

for numBits in numBitsList:
    averageTime = 0.0;
    print('Generating ' + str(numBits) + ' bits numbers:')
    for _ in range(sampleSize):
        startTime = time.time()

        next = xsg.getNumber(numBits)

        while not MillerRabin.testPrime(next):
            next = xsg.getNumber(numBits)

        len = bitLen(next)

        curTime = (time.time() - startTime)
        averageTime += curTime/sampleSize

        print('\t' + str(len) + ' - ' + str(curTime))
        print('\t' + str(next))
    print('\tAverage Time: ' + str(averageTime))

'''
for numBits in numBitsList:
    lcg.setMinBits(numBits)
    averageTime = 0.0;
    print('Generating ' + str(numBits) + ' bits numbers:')
    for _ in range(sampleSize):
        startTime = time.time()

        next = lcg.next()

        while not MillerRabin.testPrime(next):
            next = lcg.next()

        len = bitLen(next)

        curTime = (time.time() - startTime)
        averageTime += curTime/sampleSize

        print('\t' + str(len) + ' - ' + str(curTime))
        print('\t' + str(next))
    print('\tAverage Time: ' + str(averageTime))

'''
