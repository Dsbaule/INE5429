from RandomNumberGeneration import LinearCongruentialGenerator, XorShiftGenerator
import time

def bitLen(int_type):
    length = 0
    while (int_type):
        int_type >>= 1
        length += 1
    return(length)

numBitsList = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
sampleSize = 50;

seed = int(time.time())
lcg = LinearCongruentialGenerator(seed)
xsg = XorShiftGenerator(seed)

print('---------- Linear Congruential Generator ----------')
for numBits in numBitsList:
    lcg.setMinBits(numBits)
    averageTime = 0.0;
    print('\tGenerating ' + str(numBits) + ' bits numbers:')
    for _ in range(sampleSize):

        startTime = time.time()
        next = lcg.next()
        curTime = (time.time() - startTime)

        len = bitLen(next)
        averageTime += curTime/sampleSize

        print('\t\t' + str(len) + ' - ' + str(curTime))
    print('\t\tAverage Time: ' + str(averageTime))

print('---------- Xorshift ----------')
for numBits in numBitsList:
    averageTime = 0.0;
    print('\tGenerating ' + str(numBits) + ' bits numbers:')
    for _ in range(sampleSize):

        startTime = time.time()
        next = xsg.getNumber(numBits)
        curTime = (time.time() - startTime)

        len = bitLen(next)
        averageTime += curTime/sampleSize

        print('\t\t' + str(len) + ' - ' + str(curTime))
    print('\t\tAverage Time: ' + str(averageTime))
