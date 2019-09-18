
#### Aluno: Daniel de Souza Baulé (16200639)
#### Disciplina: INE5429 - Segurança em Computação
# Trabalho Individual 2 - Número Primos

Este trabalho tem como objetivo a geração de números aleatórios primos de 40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048 e 4096 bits. A geração destes números primos ocorre por meio da geração de números aleatórios utilizando os seguintes algoritmos:

* Linear Congruential Generator
* Xorshift

Uma vez gerados os números aleatórios, são utilizados os seguntes algoritmos para a execução dos testes de primalidade, para verificar se os números gerados são de fato primos:

* Miller-Rabin
* Teste de Primalidade de Fermat

As implementações dos algoritmos foram realizadas na linguagem de programação Python, devido à familiaridade do aluno com a linguagem, além da facilidade de lidar com números nas ordens de grandeza necessárias para a realização da atividade. A principal desvantagem da implementação em Python é a pior performance quando comparada a implementações similares em C ou Java, por exemplo, mas como o foco do trabalho é compreender a implementação destes algoritmos e não a posterior utilização destas implementações, a performance não foi considerada um fator crucial.

## Números Aleatórios

O ponto inicial do trabalho foi a implementação de 2 algoritmos de geração de números aleatórios, sendo escolhidos:

* Linear Congruential Generator
* Xorshift

### Linear Congruential Generator

O primeiro algoritmo para geração de números aleatórios foi o `Linear Congruential Generator`. Pesquisando sobre o algoritmo foi possivel obter uma implementação básica em Python, sendo realizadas adaptações para garantir a geração de números com o número de bits requisitados.

A implementação foi como mostrado abaixo:

``` Python
import time

'''
Linear Congruential Generation
From Wikipedia:
	def lcg(modulus, a, c, seed):
		while True:
			seed = (a * seed + c) % modulus
			yield seed
'''
class LinearCongruentialGenerator:
    def __init__(self, seed=None, numMinBits = 32, m=None, a=1664525, c=1013904223, ):
        self.m = m if m is not None else 2**numMinBits
        self.a = a
        self.c = c
        self.numMinBits = numMinBits;

        # If no seed is provided, use time
        self.state = seed % self.m if seed is not None else int(time.time())

	# Change bit count
    def setMinBits(self, numMinBits):
        self.numMinBits = numMinBits
        self.m = 2 ** numMinBits

    # Generate next random number
    def next(self):
		# Generate next number
        self.state = (self.a * self.state + self.c) % self.m
		# While number doesn't meet bit count requiremente, keep generating
        while self.state < (2**(self.numMinBits - 1)):
            self.state = (self.a * self.state + self.c) % self.m
		# Return random number
        return self.state
```

Analisando a complexidade do algoritmo, desconsiderando as alterações realizadas para obtenção de um número em uma certa faixa, obtemos complexidade linear.

### Xorshift

O outro algoritmo implementado para geração de números aleatórios foi o Xorshift, escolhido devido a sua implementação simples, porém extremamente diferente do algoritmo anterior.

No caso do Xorshift, a implementação foi baseada em uma implementação em linguagem C disponível na pagina da Wikipedia. Foi realizada apenas a implementação direta do algoritmo Xorshift 32 bits, com numeros aleatórios com maior contagem de bits sendo gerados por meio da concatenação de números menores.

A implementação foi como mostrado abaixo:

```Python
'''
Xorshift
From Wikipedia (C implementation):
	struct xorshift32_state {
	  uint32_t a;
	};

	/* The state word must be initialized to non-zero */
	uint32_t xorshift32(struct xorshift32_state *state)
	{
		/* Algorithm "xor" from p. 4 of Marsaglia, "Xorshift RNGs" */
		uint32_t x = state->a;
		x ^= x << 13;
		x ^= x >> 17;
		x ^= x << 5;
		return state->a = x;
	}
'''
class XorShiftGenerator:
	def __init__(self, seed=None):
		self.state = (seed & 0xffffffff if seed is
			not None else (int(time.time()) & 0xffffffff ))

	def next(self):
		self.state ^= (self.state << 13) & 0xffffffff
		self.state ^= (self.state >> 17) & 0xffffffff
		self.state ^= (self.state << 5) & 0xffffffff
		self.state &= 0xffffffff
		return self.state

	def getNumber(self, numBits):
		# Make sure number has specified number of bits (Most significant bit 1)
		numBitsFirstNumber = numBits % 32
		if numBitsFirstNumber == 0:
			numBitsFirstNumber = 32

		# Force number to have specified bit count
		next = self.next()
		number = next & (0xffffffff >> (32 - numBitsFirstNumber))
		number |= (0x80000000 >> (32 - numBitsFirstNumber))
		numBits -= numBitsFirstNumber

		# Concatenate remaining bits
		while numBits > 0:
			number = number << 32
			next = self.next()
			number |= next
			numBits -= 32

		return number
```

Assim como anteriormente, analisando a complexidade do algoritmo, desconsiderando as alterações realizadas para obtenção de um número em uma certa faixa, obtemos complexidade linear.

### Resultados

Para a comparação dos algoritmos, foi realizada a implementação de um simples teste, com a configuração destes para gerar números com os diferentes números de bits requisitados no enunciado, além da contagem do tempo para geração de cada número:

```Python
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
```

É necessário lembrar que a contagem de tempo como implementada pode ser afetada pelo escalonamento de processos do sistema operacional. Para amenizar este erro, o código gera 50 números de cada tamanho, calculando o tempo médio para a geração.

| Algorítmo         |  Tamanho do Número    | Tempo para Gerar (s)	|
| --                | ::                    | -:                    |
| Linear Congruente | 40                    | 7.410049438476564e-06	|
|                   | 56                    | 7.2622299194335965e-06|
|                   | 80                    | 6.308555603027342e-06 |
|                   | 128                   | 6.079673767089844e-06 |
|                   | 168                   | 6.198883056640625e-06 |
|                   | 224                   | 6.561279296874999e-06 |
|                   | 256                   | 6.742477416992189e-06 |
|                   | 512                   | 8.258819580078123e-06 |
|                   | 1024                  | 1.255512237548828e-05 |
|                   | 2048                  | 1.5039443969726562e-05|
|                   | 4096                  | 2.843379974365234e-05 |
|					|						|						|
| Xorshift 			| 40                    | 7.848739624023435e-06 |
|                   | 56                    | 8.530616760253905e-06 |
|                   | 80                    | 8.740425109863282e-06 |
|                   | 128                   | 9.39369201660156e-06  |
|                   | 168                   | 1.1439323425292973e-05|
|                   | 224                   | 1.1687278747558594e-05|
|                   | 256                   | 1.453876495361328e-05 |
|                   | 512                   | 2.2592544555664067e-05|
|                   | 1024                  | 3.9763450622558594e-05|
|                   | 2048                  | 8.925437927246094e-05 |
|                   | 4096                  | 1.5981674194335936e-04|

Nos resultados é possível observar que a variação é mínima, mas como esperado números maiores tendem a demorar mais para gerar. É possível observar também que o Xorshift apresenta performance um pouco pior, provavelmente devido a utilização de concatenação para geração de números maiores que 32 bits.

## Números Primos

Após finalizada a implementação dos algoritmos para geração de números aleatórios, foram implementados algoritmos para teste de primalidade de números:

* Miller-Rabin
* Teste de Primalidade de Fermat

O teste de primalidade de Miller-Rabin era de implementação obrigatória, enquanto a implementação do Teste de Primalidade de Fermat foi escolhida devido ao funcionamento diferente do algoritmo, e alta disposição de material na Internet.

### Miller-Rabin

O primeiro algoritmo para teste de primalidade implementado foi o de Miller-Rabin. Baseando-se em implementações em pseudo-código disponibilizadas na internet, foi implementado o seguinte código:

``` Python
from random import randint
'''
Miller-Rabin primality test
From wikipedia:
	Input #1: n > 3, an odd integer to be tested for primality
	Input #2: k, the number of rounds of testing to perform
	Output: “composite” if n is found to be composite,
    “probably prime” otherwise

	write n as 2^r·d + 1 with d odd (by factoring out powers of 2 from n − 1)
	WitnessLoop: repeat k times:
	   pick a random integer a in the range [2, n − 2]
	   x ← ad mod n
	   if x = 1 or x = n − 1 then
	      continue WitnessLoop
	   repeat r − 1 times:
	      x ← x^2 mod n
	      if x = n − 1 then
	         continue WitnessLoop
	   return “composite”
	return “probably prime”
'''
class MillerRabin:
	def decompose(n):
		r = 0
		while n % 2 == 0:
			r += 1
			n = n >> 1
		return r, n

	def testPrime(n, k=200):
		# Known small prime numbers
		if n in (2,3):
			return True
		# No number smaller than 2 is prime
		if n < 2:
			return False
		# No even number other than 2 is prime
		if n % 2 == 0:
			return False

		# Write n as 2^r·d + 1 with d odd (by factoring out powers of 2 from n − 1)
		r, d = MillerRabin.decompose(n - 1)

		# WitnessLoop: repeat k times:
		for _ in range(k):
			# Pick a random integer a in the range [2, n − 2]
			a = randint(2, n - 2)
			# x ← a^d mod n
			x = pow(a, d, n)
			# if x = 1 or x = n − 1 then continue WitnessLoop
			if x in (1, n - 1):
				continue
			try:
				# repeat r − 1 times:
				for _ in range(r - 1):
					# x ← x^2 mod n
					x = pow(x, 2, n)
					# if x = n − 1 then continue WitnessLoop
					if x == n - 1:
						raise Exeption()
			except Exception as e:
				continue

			return False
		return True
```

Comparando resultados com testes de primalidade disponíveis online, foi concluído que a implementação está correta.

Quanto a complexidade do algoritmo, todas as fontes encontradas concordam em O(k log3n), sendo n o número testado e k o número de rodadas.

### Teste de Primalidade de Fermat

O segundo algoritmo para teste de primalidade implementado foi o Teste de Primalidade de Fermat. Assim como anteriormente, baseando-se em implementações em pseudo-código disponibilizadas na internet, foi implementado o seguinte código:

``` Python
from random import randint
'''
Fermat primality test
From wikipedia:
	Inputs: n: a value to test for primality, n>3; k: a parameter that
        determines the number of times to test for primality
	Output: composite if n is composite, otherwise probably prime
	Repeat k times:
		Pick a randomly in the range [2, n − 2]
		If a^(n-1) % n != 1, then return composite
		If composite is never returned: return probably prime
'''
class Fermat:
	def testPrime(n, k=200):
		# Known small prime numbers
		if n in (2, 3):
			return True
		# No number smaller than 2 is prime
		if n < 2:
			return False
		# No even number other than 2 is prime
		if n % 2 == 0:
			return False

		# Repeat k times:
		for _ in range(k):
			# Pick a randomly in the range [2, n − 2]
			a = randint(2, n - 2)
			# If a^(n-1) % n != 1, then return composite
			if pow(a, n - 1, n) != 1:
				return False
			# If composite is never returned: return probably prime
		return True
```

Comparando resultados com testes de primalidade disponíveis online, foi concluído que a implementação está correta.

Quanto a complexidade do algoritmo, todas as fontes encontradas concordam em O(k log2n), sendo n o número testado e k o número de rodadas.

### Resultados

Primeiramente, foi implementado um código de teste para os algoritmos de teste de primalidade, com números conhecidos primos/não primos, como mostrado abaixo:

```Python
from PrimeTests import MillerRabin, Fermat

primes = {
	40 : [701886890821,145833959483],
	80 : [627039700318015972526563, 17258016887375724832991],
	128 : [281823669593790837253752644147169483721,130149497672760612194506571911619816501],
	168 : [53577236802344919857680454697879375307504576088927,87638684248093818277104190540718855481257514307561],
	224 : [9555570476784365604183370437996185501407868060964191196593302762711, 11929041895336665885415245171139727014453130135351262254242333297897],
	256 : [114521762541736572942175831292858847115978022297533643366336514473398296681259, 11497252343705411796936888026497063219797667847435003967142716418374222663583],
	512 : [11687988934730615085088752797282250379639560899809286759004164177768277835281798803059267186900959504974146952503606499671949523808002108371505014225254399, 9168410681124379526825687234528018432644565710137901728047853853741091546896715023346942896824656130759676107735215870152242221051577686814226904972953379],
	1024 : [4295990300262175286569706942624603289030853170013305621487189320909290520964802545145338800399484815159365124125403198362566442732009593596711195852873192072986050491252220531071318224293681475472026308169146527096204193789966266511659036316520094962867195427822246488653708362652700942480126595154117153523,4409718549809058718136578021895169493897055950058401244314045862374461586598984981007224313712892153648774256370485411186370689415870955619893596734411560764682357146184412176588364419785385753989349441526392553046352668450905445247325247631159384449414059944919242710890625383893079748692907335511203129151]
}

notPrimes = {
	40 : [701886690821,145834959483],
	80 : [627039700318015972526565, 17258016887375724832992],
	128 : [281823669593790837253752644147169483725,130149497672760612194506571911619816502],
	168 : [53577236802344919857680454697879375307504576088925,87638684248093818277104190540718855481257514307563],
	224 : [9555570476784365604183370437996185501407868060964191196593302762717, 11929041895336665885415245171139727014453130135351262254242333297895],
	256 : [114521762541736572942175831292858847115978022297533643366336514473398296681253, 11497252343705411796936888026497063219797667847435003967142716418374222663587],
	512 : [11687988934730615085088752797282250379639560899809286759004164177768277835281798803059267186900959504974146952503606499671949523808002108371505014225254397, 9168410681124379526825687234528018432644565710137901728047853853741091546896715023346942896824656130759676107735215870152242221051577686814226904972953371],
	1024 : [4295990300262175286569706942624603289030853170013305621487189320909290520964802545145338800399484815159365124125403198362566442732009593596711195852873192072986050491252220531071318224293681475472026308169146527096204193789966266511659036316520094962867195427822246488653708362652700942480126595154117153529,4409718549809058718136578021895169493897055950058401244314045862374461586598984981007224313712892153648774256370485411186370689415870955619893596734411560764682357146184412176588364419785385753989349441526392553046352668450905445247325247631159384449414059944919242710890625383893079748692907335511203129153]
}

numBitsList = list(primes.keys())
numBitsList.sort()

for numBits in numBitsList:
	print('Number of bits: ' + str(numBits))

	print('\tTesting known primes:')
	for prime in primes[numBits]:
		print('\t\tMiller-Rabin: - ' + str(MillerRabin.testPrime(prime)))
	for prime in primes[numBits]:
		print('\t\tFermat: - ' + str(Fermat.testPrime(prime)))

	print('\tTesting known not primes:')
	for notPrime in notPrimes[numBits]:
		print('\t\tMiller-Rabin: - ' + str(MillerRabin.testPrime(notPrime)))
	for notPrime in notPrimes[numBits]:
		print('\t\tFermat: - ' + str(Fermat.testPrime(notPrime)))

```

Sendo obtidos os seguintes resultados:

```bash
Number of bits: 40
        Testing known primes:
                Miller-Rabin:  - True
                Miller-Rabin:  - True
                Fermat:  - True
                Fermat:  - True
        Testing known not primes:
                Miller-Rabin:  - False
                Miller-Rabin:  - False
                Fermat:  - False
                Fermat:  - False
Number of bits: 80
        Testing known primes:
                Miller-Rabin:  - True
                Miller-Rabin:  - True
                Fermat:  - True
                Fermat:  - True
        Testing known not primes:
                Miller-Rabin:  - False
                Miller-Rabin:  - False
                Fermat:  - False
                Fermat:  - False
Number of bits: 128
        Testing known primes:
                Miller-Rabin:  - True
                Miller-Rabin:  - True
                Fermat:  - True
                Fermat:  - True
        Testing known not primes:
                Miller-Rabin:  - False
                Miller-Rabin:  - False
                Fermat:  - False
                Fermat:  - False
Number of bits: 168
        Testing known primes:
                Miller-Rabin:  - True
                Miller-Rabin:  - True
                Fermat:  - True
                Fermat:  - True
        Testing known not primes:
                Miller-Rabin:  - False
                Miller-Rabin:  - False
                Fermat:  - False
                Fermat:  - False
Number of bits: 224
        Testing known primes:
                Miller-Rabin:  - True
                Miller-Rabin:  - True
                Fermat:  - True
                Fermat:  - True
        Testing known not primes:
                Miller-Rabin:  - False
                Miller-Rabin:  - False
                Fermat:  - False
                Fermat:  - False
Number of bits: 256
        Testing known primes:
                Miller-Rabin:  - True
                Miller-Rabin:  - True
                Fermat:  - True
                Fermat:  - True
        Testing known not primes:
                Miller-Rabin:  - False
                Miller-Rabin:  - False
                Fermat:  - False
                Fermat:  - False
Number of bits: 512
        Testing known primes:
                Miller-Rabin:  - True
                Miller-Rabin:  - True
                Fermat:  - True
                Fermat:  - True
        Testing known not primes:
                Miller-Rabin:  - False
                Miller-Rabin:  - False
                Fermat:  - False
                Fermat:  - False
Number of bits: 1024
        Testing known primes:
                Miller-Rabin:  - True
                Miller-Rabin:  - True
                Fermat:  - True
                Fermat:  - True
        Testing known not primes:
                Miller-Rabin:  - False
                Miller-Rabin:  - False
                Fermat:  - False
                Fermat:  - False
```

Uma vez concluído que os testes apresentam funcionamento correto, foi implementada a geração de números aleatórios primos:

```Python
from RandomNumberGeneration import LinearCongruentialGenerator
from PrimeTests import MillerRabin
import time

def bitLen(int_type):
    length = 0
    while (int_type):
        int_type >>= 1
        length += 1
    return(length)

numBitsList = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
sampleSize = 10;

seed = int(time.time())
lcg = LinearCongruentialGenerator(seed)

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
		#print('\t' + str(next))
	print('\tAverage Time: ' + str(averageTime))

```

Devido a melhor performance obtida, foi utilizado o algoritmo de `Linear Congruential Generation` em conjunto com o teste de primalidade de `Miller-Rabin` para geração dos números primos aleatórios mostrados abaixo:

|  Tamanho do Número    | Tempo para Gerar (s)  |
| :-                    | -:                    |
| 40                    | 0.0019159555435180665 |
| 56                    | 0.0025369644165039065 |
| 80                    | 0.00484907627105713	|
| 128                   | 0.011374306678771972 	|
| 168                   | 0.018348765373229978  |
| 224                   | 0.029324126243591313	|
| 256                   | 0.03960294723510742	|
| 512                   | 0.18643634319305422 	|
| 1024                  | 1.8157038688659664	|
| 2048                  | 29.737854599952698	|
| 4096                  | 184.57118501663206	|

Para se obter estes valores foi realizada a média de tempo a partir da geração de 10 números de cada tamanho. A seguir, também se gerou alguns exemplos de números aleatórios primos:

* 40 bits: 984881580169
* 56 bits: 59110269851068091
* 80 bits: 907671903864918607805683
* 128 bits: 308844230555655163188126921457452195287
* 168 bits: 366155287549482999304639720205531388563920662944771
* 224 bits: 60512381401449176386700885883257113601203870589381143310510447086816719872873
* 256 bits: 60512381401449176386700885883257113601203870589381143310510447086816719872873
* 512 bits: 10143396012432226485514547154325343238856089175640849059755118235888408640693972470879677282930946112732822874103026636074093929752381490936363035239497219
* 1024 bits: 112114064601907357497793143440333629927372279837757161618227310052599969548139600227879943431334745671042615186892259525004751128497258591306259571194882760337267757244490779871035297587726375829432552987987215174801409487489561214840348812970361419952146176294111948545279674983119692551923717904052082066849
* 2048 bits: 23624425759091095026966776776871622317671613472252814759277622726499840510293455496811909564455699338375937136303121317864448626115105662667139079721388817584648221504273084858702770752526064513477875010699771791355456648893923054202412248100006593514642336436953135532167405656578176791400028060327166267836773317222719289643463496693674842023321028172549076776512778071711433137652517718916782807397659836691464490575276568487392570796090995447870044111958228744379717082838049471352828458943859463618850806662417909906526318665895710527845681339229592542884117093353547788813025266667360108100712638335431658048823
* 4096 bits: 714763852733901837404956056193259068824930180336076712756512098658412305135397014181449348136076473202278368115494102539265824187152550271357436631244188805680657050775084867492526585712595320879921263817272318415549847213930227896201521290931403515961385843849341528027858813830998303668419189323806867613244440809523813905442586901997881438194001462494305848306204609595632101785099101835599302836857898715944889700146764619240759524108329949242578663918079513142175104925795985478282516672581812872658962634004344866793007814064737551004592551609647154029193605629347501957158671458599531081952919933991591354045049287514204516242426214077012801784844437551420374661558309257410008790046898252980796432622049010122751061439394046524575345224387199473235652568728500003088650309535734974683119978089857486192241000635842051807353689875723559489803166206939853870974182383957684091338259633530719312445004209935853860829510772145017872244905237641178913476810342181464332630155379666357189153657017840349986750858043645966297404049897537209721776107723567709026500446837925111624443682845830278572681652230456820562768365107842799505269906734688379642343212769887720874088585027604930346209171881841465958109077609275069337177073943

## Dificuldades Encontradas

Dentre as principais dificuldades encontradas estão o tempo para geração de números aleatórios primos grandes, o que dificultou os testes, além de a comparação de resultados com testes de primalidade online, visto que a maioria não suporta números nesta ordem de grandeza.

Outra dificuldade foi a geração de números aleatórios grandes com algoritmos limitados, como Xorshift, sendo necessária a concatenação de resultados.

## Referências

##### Miller-Rabin

https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test

https://crypto.stanford.edu/pbc/notes/numbertheory/millerrabin.html

##### Fermat

https://en.wikipedia.org/wiki/Fermat_primality_test

https://www.geeksforgeeks.org/primality-test-set-2-fermet-method/

##### Linear Congruential Generator

https://en.wikipedia.org/wiki/Linear_congruential_generator

https://rosettacode.org/wiki/Linear_congruential_generator

##### Xorshift

https://en.wikipedia.org/wiki/Xorshift

https://www.javamex.com/tutorials/random_numbers/xorshift.shtml
