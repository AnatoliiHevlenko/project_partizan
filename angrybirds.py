from math import tan, pi, cos

def init_field(Heigt,Width,Start,Finish):       # ініціалізація ігрового поля

    field = [[' '] * Width for i in range(Heigt)]   # створюємо масив - поле
    field[Start[0]][Start[1]] = 'S'         # початкове положення
    field[Finish[0]][Finish[1]]= 'F'        # мішень

    for i in range(Heigt):                  # кути поля '+', а сторони '|', '-'
        for j in range(Width):
            if (i,j) in ((0,0), (Heigt-1, Width-1),(0, Width-1), (Heigt-1,0)):
                field[i][j] = '+'
            elif i == 0 or i == Heigt-1 :
                field[i][j] = '-'
            elif j == 0 or j == Width-1 :
                field[i][j] = '|'
    return field

def draw_field(field):          # вивід ігрового поля на екран
    for row in field:
        print(''.join([str(elem) for elem in row]))

def step(field,Shot,war):           # позначити елемент масиву (поля)
    try:                        # якщо він туди попадає    
        field[Shot[0]][Shot[1]] = war
    except: None
    return field

Heigt = 30                  # висота поля
Width = 80                  # ширина поля  
Start = [27,5]          # координата старту
Finish = [27,70]        # координата цілі
Shot = Start.copy()     # позиція "ядра"

game_field = init_field(Heigt,Width,Start,Finish)   # створимо поле
draw_field(game_field)                      # покажемо поле на екрані

angle = float(input('Enter start angle (0-90): '))
speed = float(input('Enter start speed (0-200): '))

g = 9.81                # прискорення вільного падіння
t = t0 = speed/10000    # часовий інтервал для розрахунків
x = 0.00
y = 0.00
angle = angle*pi/180    # градуси в радіани

while True:
    # цикл розрахунку координат 
    x = speed*t*cos(angle)
    y = x*tan(angle) - g*x**2/(2*speed**2*(cos(angle))**2)
    t += t0     # час від пострілу

    Shot[0] = Start[0] - int(y)     # відлік системи координат від гармати
    Shot[1] = Start[1] + int(x)     # відлік системи координат від гармати

    if 0<Shot[0]<Heigt-1 and 0<Shot[1]<Width-1 and Shot != Start:
        # якщо ядро за межами екрану - чекаємо)))
        # якщо в ігровому полі - позначаємо його на полі
        step(game_field,Shot,'*')
        if Shot == Finish:          # виграли, якщо влучили == Finish
            step(game_field,Finish,'O')
            draw_field(game_field)
            print('You WIN!!!')
            break
    elif Shot[1] > Finish[1]:       # програли (перелетіли по X Finish чи мимо)
            draw_field(game_field)   
            print('You LOSE!!!')
            break