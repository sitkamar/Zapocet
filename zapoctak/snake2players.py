from random import choice
import turtle


class vector:
    '''třída vector slouží k reprezentaci vektorů, které se používají pro reprezentaci pozic na hracím poli'''

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        '''metoda __add__ slouží k sečtení dvou vektorů'''
        return vector(self.x + other.x, self.y + other.y)
    def __eq__(self, other):
        '''metoda __eq__ slouží k porovnání dvou vektorů'''
        return False if not isinstance(other, vector) else self.x == other.x and self.y == other.y
    def __sub__(self, other):
        '''metoda __sub__ slouží k odečtení dvou vektorů'''
        return vector(self.x - other.x, self.y - other.y)
    def __neg__(self):
        '''metoda __neg__ slouží k negaci vektoru'''
        return vector(-self.x, -self.y)
    def __str__(self):
        '''metoda __str__ slouží k vypsání vektoru'''
        return f'({self.x}, {self.y})'
    def __repr__(self):
        '''metoda __repr__ slouží k vypsání vektoru'''
        return f'({self.x}, {self.y})'
    def distance(self, other):
        '''metoda distance slouží k výpočtu vzdálenosti dvou vektorů'''
        return abs(self.x - other.x)+abs(self.y - other.y)

def square(pos, color, drawer):
    '''funkce square vykreslí čtverec na pozici pos o velikosti 5x5 a barvě color pomocí draweru
    Parametry:
        pos: vector
            pozice čtverce
        color: str
            barva čtverce
        drawer: turtle.Turtle
            drawer, který vykresluje čtverec
    '''
    drawer.speed(0)
    drawer.penup()
    drawer.goto(pos.x, pos.y)
    drawer.color(color)
    drawer.begin_fill()
    for _ in range(4):
        drawer.forward(5)
        drawer.left(90)
    drawer.end_fill()


class snake:
    '''třída snake reprezentuje hada, který se pohybuje po hracím poli
    
    Parametry:
        head: vector
            pozice hlavy hada
        direction: vector
            směr pohybu hada
        color: str
            barva hada při vykreslování
        score_pos: vector
            pozice score boardu hada
    
    Metody:
        move()
            posune hada o jedno políčko v jeho směru pohybu a vykreslí ho
        grow()
            zvětší hada o jedno políčko
        get_new_head()
            vrátí pozici hlavy hada, kdyby se pohyboval o jedno políčko v jeho směru pohybu
        change_direction(direction)
            změní směr pohybu hada na direction
        reset(head, direction)
            zmenší hada na jedno políčko na pozici head a změní směr pohybu na direction
        score_board()
            aktualizuje score board
    všechny změny provedené metodami se projeví při dalším volání metody move() nebo grow(), která provede pohyb hada a vykreslí ho
    '''
    def __init__(self, head, direction, color, score_pos,is_test=False):
        '''
        Parametry:
        head: vector
            pozice hlavy hada
        direction: vector
            směr pohybu hada
        color: str
            barva hada při vykreslování
        score_pos: vector
            pozice score boardu hada
        '''
        self.tiles = [head]
        self.direction = direction
        self.color = color
        self.score_pos = score_pos
        self.score = 0
        self.highscore = 0
        self.is_test = is_test
        self.drawer = turtle.Turtle()
        self.drawer.speed(0)
        if not is_test:
            square(head, color, self.drawer)
            self.score_drawer = turtle.Turtle()
            self.score_drawer.speed(0)
            self.score_drawer.penup()
            self.score_drawer.goto(self.score_pos.x, self.score_pos.y)
            self.score_drawer.color(color)
            self.score_drawer.write(f'    score: {self.score} \nhighscore: {self.highscore}', align='center',
                                font=('Courier', 10, 'normal'))

    def __contains__(self, item):
        '''metoda __contains__ slouží k zjištění, zda vektor item narazil do hada
        Parametry:
            item: vector
                vektor, který se má zjistit, zda narazil do hada
        Vrací:
            bool
        '''
        return item in self.tiles

    def move(self):
        '''metoda move posune hada o jedno políčko v jeho směru pohybu a vykreslí ho'''
        self.tiles.insert(0, self.tiles[0] + self.direction)
        self.tiles.pop()
        self.drawer.clear()
        if not self.is_test:
            for tile in self.tiles:
                square(tile, self.color, self.drawer)

    def score_board(self):
        '''metoda score_board aktualizuje score board'''
        if self.score > self.highscore:
            self.highscore = self.score
        self.score_drawer.undo()
        self.score_drawer.write(f'    score: {self.score} \nhighscore: {self.highscore}', align='center',
                                font=('Courier', 10, 'normal'))
    def grow(self):
        '''metoda grow zvětší hada o jedno políčko a aktualizuje score board (tato metoda je druhou možností funkce move, tedy had se o políčko posune dopředu)'''
        self.tiles.insert(0, self.tiles[0] + self.direction)
        self.score += 1
        if not self.is_test:
            self.score_board()
            self.drawer.clear()
            for tile in self.tiles:
                square(tile, self.color, self.drawer)

    def get_new_head(self):
        '''metoda get_new_head vrátí pozici hlavy hada, kdyby se pohyboval o jedno políčko v jeho směru pohybu'''
        return self.tiles[0] + self.direction

    def change_direction(self, direction):
        '''metoda change_direction změní směr pohybu hada na direction
        Poznámka:
            pokud je direction vektor (0, 0), potom je brán had za mrtvého a změna směru se neprovede
        '''
        if direction == vector(0, 0):
            return
        self.direction = direction

    def reset(self, head, direction):
        '''metoda reset zmenší hada na jedno políčko na pozici head a změní směr pohybu na direction
        Parametry:
            head: vector
                pozice hlavy hada po resetu
            direction: vector
                směr pohybu hada po resetu
        '''
        self.tiles = [head]
        self.score = 0
        self.change_direction(direction)
        if not self.is_test:
            self.score_board()
            self.drawer.clear()
            square(head, self.color, self.drawer)


class game:
    '''třída game slouží k vytvoření herní plochy a k jejímu správě
    
    Parametry:
        width: int
            šířka herní plochy
        height: int
            výška herní plochy
    Atributy:
        width: int
            šířka herní plochy
        height: int
            výška herní plochy
        tiles: list
            seznam všech políček herní plochy
        safe_place: list
            seznam všech bezpečných políček herní plochy, na kterých se mohou hadi objevit
        snake1: snake
            první had
        snake2: snake
            druhý had
        gamemode: str
            režim hry
        drawers and writers: turtle.Turtle
            turtly pro vykreslování a psaní
    Metody:
        set_gamemode(gamemode: str, writer: turtle.Turtle)
            nastaví režim hry na gamemode, vytvoří hady, vykreslí herní plochu a spustí hru
        spawn_poison()
            vygeneruje novou políčka s jedem a vykreslí je
        spawn_food()
            vygeneruje nové políčko s jídlem a vykreslí ho
        reset(snake: snake)
            resetuje hada snake na náhodnou pozici na bezpečném políčku
        move()
            posune hady o jedno políčko a zkontroluje, zda některý z nich nenarazil nebo nesnědl jídlo
            tato metoda je volána každých 100 milisekund
        change_direction(snake: snake, direction: vector)
            změní směr pohybu hada snake na direction
        ai_change_direction(snake: snake)
            změní směr pohybu hada snake na nejkratší cestu k jídlu
    '''
    def __init__(self, width, height,is_test=False):
        '''konstruktor třídy game
        Parametry:
        width: int
            šířka herní plochy
        height: int
            výška herní plochy
        is_test: bool
            určuje, zda se jedná o testovací hru ověřující funkčnost třídy game
            testovací mód umožňuje ovládání rychlosti hry pomocí programu
        Atributy:
            width: int
                šířka herní plochy
            height: int
                výška herní plochy
            tiles: list
                seznam všech volných políček herní plochy
            safe_place: list
                seznam všech bezpečných políček herní plochy, na kterých se mohou hadi objevit
            snake1: snake
                první had
            snake2: snake
                druhý had
            gamemode: str
                režim hry
            '''
        self.width = width
        self.height = height
        self.is_test = is_test
        self.tiles = [vector(x*5-width//2, height//2 - y*5)
                      for x in range(width//5) for y in range(height//5)]
        self.safe_place = [vector(x*5, y*5) for x in range(width//20)
                           for y in range(height//20)]
        for tile in self.safe_place:
            self.tiles.remove(tile)
        self.snake1 = None
        self.snake2 = None
        self.gamemode = None
        border = turtle.Turtle(visible=True)
        if not self.is_test:
            border.speed(0)
            border.penup()
            border.goto(-self.width//2, self.height//2+5)
            border.color('black')
            for i in range(4):
                border.begin_fill()
                border.forward(self.width if i % 2 == 0 else self.height)
                border.left(90)
                border.forward(5)
                border.left(90)
                border.forward(self.width if i % 2 == 0 else self.height)
                border.left(90)
                border.forward(5)
                border.end_fill()
                border.left(90)
                border.forward(self.width if i % 2 == 0 else self.height)
                border.left(270)
        

    def set_gamemode(self, gamemode, writer=None):
        '''nastaví režim hry na gamemode, vytvoří hady, vykreslí herní plochu a spustí hru
        Parametry:
            gamemode: str
                režim hry
            writer: turtle.Turtle
                turtl, který napsal nápis s výběrem režimu hry
        '''
        if self.gamemode is None:
            self.gamemode = gamemode
            match gamemode:
                case "1player":
                    self.snake1 = snake(vector(0, 0), vector(
                        5, 0), 'blue', vector(-self.width//2+70, self.height//2-50), self.is_test)
                    self.snake2 = snake(vector(self.width, self.height), vector(
                        0, 0), 'white', vector(self.width, self.height), self.is_test)
                case "2players":
                    self.snake1 = snake(vector(0, 0), vector(
                        5, 0), 'blue', vector(-self.width//2+70, self.height//2-50), self.is_test)
                    self.snake2 = snake(vector(0, 20), vector(
                        5, 0), 'purple', vector(self.width//2-70, self.height//2-50), self.is_test)
                case "1player+AI":
                    self.snake1 = snake(vector(0, 0), vector(
                        5, 0), 'blue', vector(-self.width//2+70, self.height//2-50), self.is_test)
                    self.snake2 = snake(vector(0, 20), vector(
                        5, 0), 'purple', vector(self.width//2-70, self.height//2-50), self.is_test)
            if writer is not None:
                writer.clear()
            self.food = vector(10, 10)
            self.food_drawer = turtle.Turtle()
            if not self.is_test:
                square(self.food, 'green', self.food_drawer)
            self.poison_drawer = turtle.Turtle()
            self.poisons = [self.spawn_poison() for _ in range(10)]
            if not self.is_test:
                self.move()

    def spawn_poison(self):
        '''vygeneruje náhodné políčko, na kterém se bude nacházet nový jed a přidá ho do seznamu jedů a vykreslí všechny jedy'''
        poison = choice(self.tiles)
        self.tiles.remove(poison)
        if not self.is_test:
            square(poison, 'red', self.poison_drawer)
        return poison

    def spawn_food(self):
        '''vygeneruje náhodné políčko, na kterém se bude nacházet jídlo a vykreslí všechna jídla'''
        food = choice(self.tiles)
        self.tiles.remove(food)
        self.food_drawer.clear()
        if not self.is_test:
            square(food, 'green', self.food_drawer)
        return food

    def reset(self, snake):
        '''resetuje hada snake na náhodné bezpečné políčko
        Parametry:
            snake: snake
                had, který se má resetovat
        '''
        for i in snake.tiles:
            self.tiles.append(i)
        snake.reset(choice(self.safe_place), vector(5, 0))
        while snake.get_new_head() in self.snake1 or snake.get_new_head() in self.snake2:
            snake.reset(choice(self.safe_place), vector(5, 0))
    def out_of_bounds(self, head):
        '''zjistí, zda je hlava head hada mimo herní plochu
        Parametry:
            head: vector
                hlava hada
        '''
        return head.x < -self.width//2 or head.x >= self.width//2 or head.y <= -self.height//2 or head.y > self.height//2
    def move(self):
        '''
        hlavní funkce hry , která se volá každých 100 milisekund
        pohne hady a zkontroluje, zda se některý z nich neztratil nebo nezabil nebo nesnědl jídlo
        tatéž se stará o pohyb AI
        '''
        if self.gamemode == "1player+AI":
            self.ai_change_direction()
        if self.gamemode == "1player":
            head = self.snake1.get_new_head()
            if head in self.snake1 or self.out_of_bounds(head):
                self.reset(self.snake1)
            if head in self.poisons:
                self.poisons.remove(head)
                if not self.is_test:
                    square(head, 'white', self.poison_drawer)
                self.reset(self.snake1)
            if head == self.food:
                self.snake1.grow()
                self.food = self.spawn_food()
                self.poisons.append(self.spawn_poison())
            else:
                self.tiles.append(self.snake1.tiles[-1])
                try:
                    self.tiles.remove(head)
                except ValueError:
                    pass
                self.snake1.move()
        elif self.gamemode == "2players" or self.gamemode == "1player+AI":
            head1 = self.snake1.get_new_head()
            head2 = self.snake2.get_new_head()
            if head1 in self.snake1 or self.out_of_bounds(head1) or head1 in self.snake2:
                self.reset(self.snake1)
            if head1 in self.poisons:
                self.poisons.remove(head1)
                self.tiles.append(head1)
                if not self.is_test:
                    square(head1, 'white', self.poison_drawer)
                self.reset(self.snake1)
            if head2 in self.snake2 or self.out_of_bounds(head2) or head2 in self.snake1:
                self.reset(self.snake2)
            if head2 in self.poisons:
                self.poisons.remove(head2)
                self.tiles.append(head2)
                if not self.is_test:
                    square(head2, 'white', self.poison_drawer)
                self.reset(self.snake2)
            if head1 == head2:
                self.reset(self.snake1)
                self.reset(self.snake2)
            if head1 == self.food:
                self.snake1.grow()
                self.food = self.spawn_food()
                self.poisons.append(self.spawn_poison())
            else:
                self.tiles.append(self.snake1.tiles[-1])
                self.snake1.move()
                try:
                    self.tiles.remove(head1)
                except ValueError:
                    pass
            if head2 == self.food:
                self.snake2.grow()
                self.food = self.spawn_food()
                self.poisons.append(self.spawn_poison())
            else:
                self.tiles.append(self.snake2.tiles[-1])
                self.snake2.move()
                try:
                    self.tiles.remove(head2)
                except ValueError:
                    pass
        if not self.is_test: #pokud se nejedná o test, tak se opakuje automaticky každých 100 milisekund
            turtle.ontimer(self.move, 100) 

    def change_direction(self, snake, direction):
        '''změní směr hada
        Parametry:
            snake: snake
                had, který se má změnit
            direction: vector
                směr, kterým se má had změnit
        Poznámka:
            pokud se had snaží změnit směr na opačný, tak se změna neprovede
        '''
        if snake is None:
            return
        if snake.direction.x != -direction.x or snake.direction.y != -direction.y:
            snake.change_direction(direction)

    def ai_change_direction(self):
        '''změní směr AI hada
        Popis:
            Nejdříve si zjistí všechny možné směry, kterými se AI had může pohnout.
            Poté se podívá, který z nich je nejkratší cesta k jídlu a pohne se v tomto směru.
        '''
        def is_free(head):
            return not self.out_of_bounds(head) and head not in self.snake1 and head not in self.snake2 and head not in self.poisons
        head = self.snake2.tiles[0]
        options = [vector(5, 0), vector(-5, 0), vector(0, 5), vector(0, -5)]
        for option in options:
            if option == -self.snake2.direction:
                options.remove(option)
            elif not is_free(head + option):
                options.remove(option)
        if len(options) == 0:
            return
        answer = []
        dir_to_food = self.food - head
        if abs(dir_to_food.x) > abs(dir_to_food.y):
            if dir_to_food.x > 0:
                if dir_to_food.y > 0:
                    answer = [vector(5, 0), vector(
                        0, 5), vector(0, -5), vector(-5, 0)]
                else:
                    answer = [vector(5, 0), vector(0, -5),
                              vector(0, 5), vector(-5, 0)]
            else:
                if dir_to_food.y > 0:
                    answer = [vector(-5, 0), vector(0, 5),
                              vector(0, -5), vector(5, 0)]
                else:
                    answer = [vector(-5, 0), vector(0, -5),
                              vector(0, 5), vector(5, 0)]
        else:
            if dir_to_food.y > 0:
                if dir_to_food.x > 0:
                    answer = [vector(0, 5), vector(
                        5, 0), vector(-5, 0), vector(0, -5)]
                else:
                    answer = [vector(0, 5), vector(-5, 0),
                              vector(5, 0), vector(0, -5)]
            else:
                if dir_to_food.x > 0:
                    answer = [vector(0, -5), vector(5, 0),
                              vector(-5, 0), vector(0, 5)]
                else:
                    answer = [vector(0, -5), vector(-5, 0),
                              vector(5, 0), vector(0, 5)]
        for option in answer:
            if option in options:
                self.change_direction(self.snake2, option)
                return

'''main
vytvoří okno hry a spustí hru
vyřeší výběr herního módu a mačkání kláves hráčů
'''
if __name__ == '__main__':
    width = 500
    height = 500
    window = turtle.Screen()
    window.setup(width, height, 370, 100)
    window.tracer(0)
    my_game = game(width, height)
    writer1 = turtle.Turtle(visible=False)
    writer1.color('white')
    writer1.goto(-0, 0)
    writer1.color('black')
    writer1.write('Press: 1 for 1 player, 2 for 2 players, 3 for player vs. AI \n Controls for player 1: arrows, for player 2: WSAD', align='center',font=('Arial', 14, 'normal'))
    window.listen()
    window.onkey(lambda: my_game.set_gamemode('1player', writer1), '1')
    window.onkey(lambda: my_game.set_gamemode('2players', writer1), '2')
    window.onkey(lambda: my_game.set_gamemode('1player+AI', writer1), '3')
    window.onkey(lambda: my_game.change_direction(
        my_game.snake1, vector(5, 0)), 'Right')
    window.onkey(lambda: my_game.change_direction(
        my_game.snake1, vector(-5, 0)), 'Left')
    window.onkey(lambda: my_game.change_direction(
        my_game.snake1, vector(0, 5)), 'Up')
    window.onkey(lambda: my_game.change_direction(
        my_game.snake1, vector(0, -5)), 'Down')
    window.onkey(lambda: my_game.change_direction(
        my_game.snake2, vector(5, 0)), 'd')
    window.onkey(lambda: my_game.change_direction(
        my_game.snake2, vector(-5, 0)), 'a')
    window.onkey(lambda: my_game.change_direction(
        my_game.snake2, vector(0, 5)), 'w')
    window.onkey(lambda: my_game.change_direction(
        my_game.snake2, vector(0, -5)), 's')
    turtle.done()
