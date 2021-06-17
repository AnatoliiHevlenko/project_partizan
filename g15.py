'''
П'ятна́шки (п'ятнадцять) — популярна головоломка, придумана у 1878 році Ноєм Чепменом. 
Складається з 15 однакових квадратних пластинок з нанесеними числами від 1 до 15. 
Пластинки поміщаються в квадратну коробку, довжина сторони якої в чотири рази 
більша довжини сторони пластинок, відповідно в коробці залишається незаповненим 
одне квадратне поле. Мета гри — переміщаючи пластинки по коробці добитися 
впорядковування їх по номерах (як зображено на рисунку), бажано зробивши якомога менше переміщень.
https://uk.wikipedia.org/wiki/%D0%9F%27%D1%8F%D1%82%D0%BD%D0%B0%D1%88%D0%BA%D0%B8
http://e-maxx.ru/algo/15_puzzle   - перевірка можливості розв'язку
'''
class game15:

    def __init__(self): 
        self.numbers = {}               # координати чисел (позиція, значення)
        self.zero = 0                   # індекс пустої клітинки (для зручності)
        self.variants = []              # клітинки що поруч з пустою
        self.counts = 0                 # кылькість кроків
        self.continue_game = True       # продовження гри 
        self.board ='''                 
        +-------------------+
        | %s | %s | %s | %s |
        +-------------------+
        | %s | %s | %s | %s |
        +-------------------+
        | %s | %s | %s | %s |
        +-------------------+
        | %s | %s | %s | %s |
        +-------------------+
                    ''' 
    
    def random_number(self):               # "розкидати" значення клітинок
        import random
        solution = True
        while solution:
            key = 0
            while key < 16:         
                value = random.randint(0,15)
                if value not in self.numbers.values():
                    key += 1
                    self.numbers[key] = value
                    if value == 0:             # тут у нас буде пуста клітинка
                        self.zero = key# запам'ятаємо координату пустої клітинки
            N = 0
            for i in range(1,17):
                for j in range(1,17):
                    if i < j and \
                        i != self.zero and \
                        j != self.zero and \
                        self.numbers[i] > self.numbers[j]:
                        N += 1
                    j += 1
                i += 1
            if (N + (self.zero - 1) % 4 + 1) % 2 == 0 :
                solution = False
            else:
                self.numbers.clear()

    def draw(self):               # намалювати поле, якщо '0' ставимо ' '
        tmp = self.numbers.copy()
        for key in tmp.keys():  # значення мають бути однакової довжини
            tmp[key] = \
                (' '+str(tmp[key])) if 0 < tmp[key] < 10 \
                        else '  ' if tmp[key] == 0 \
                                  else str(tmp[key]) 
        print(self.board % tuple(tmp.values()))

    def ask_for_step(self):     # ходимо
        self.variants = []      # підкажемо клітинки з яких можна ходити і запишемо
        for X in self.variant_key(self.zero):
            self.variants.append(self.numbers[X])
        self.variants.sort()    # для красоти виведення підказки сортуєм
        request = input('You turn. ' \
                    'Enter the number for the move (hint: %s): '%self.variants)
        return int(request) if request.isdigit() else 0

    def win(self):      # виграли, якщо індекс=значенню від 1 до 15
        for i in range(1,16):
            if  i == self.numbers[i]:
                self.continue_game = False
            else:
                self.continue_game = True
                break

    def variant_key(self, key_step): # можливі варіанти "ходу" по індексу
        tmp_step = []    
        if key_step-4 in range(1,17):
            tmp_step.append(key_step-4)
        if key_step+4 in range(1,17):
            tmp_step.append(key_step+4)
        if (key_step-1 in range(1,17)) and (key_step)%4 != 1:
            tmp_step.append(key_step-1)
        if (key_step+1 in range(1,17)) and (key_step)%4 != 0:
            tmp_step.append(key_step+1)
        return tmp_step

    def play(self):
        self.random_number()
        while self.continue_game:
            self.draw()
            # self.variants = self.variant_key(self.zero) # 
            value_step = self.ask_for_step()
            if value_step not in self.variants: # чи допустиме введене значення
                print('Error input. Repeat...')
            else: 
                for key, value in self.numbers.items(): 
                    if value_step == value:
                        key_step = key          # індекс введеного значення
                        break
                # міняємо місцями "вибрану" і "пусту" клітинки
                self.numbers[key_step], self.numbers[self.zero] = \
                        self.numbers[self.zero], self.numbers[key_step]
                self.counts += 1
                self.zero = key_step    # запам'ятаємо пусту позицію9
            self.win()
        self.draw()     # покажемо результат
        print('YOU WIN!!! Counts=%s' %self.counts)


# *****************

game = game15()
game.play()
