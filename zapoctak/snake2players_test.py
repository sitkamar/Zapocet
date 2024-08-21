import unittest
import sys
import snake2players as sn

class Test_Vector(unittest.TestCase):
    def test_equal(self):
        self.assertTrue(sn.vector(2,5)==sn.vector(2,5))
        self.assertFalse(sn.vector(-3,1)==sn.vector(3,1))
    def test_add(self):
        self.assertEqual(sn.vector(1,3)+sn.vector(-5,7),sn.vector(-4,10))
    def test_sub(self):
        self.assertEqual(sn.vector(1,3)-sn.vector(-5,7),sn.vector(6,-4))
    def test_neg(self):
        self.assertEqual(-sn.vector(1,3),sn.vector(-1,-3))
class Test_Snake(unittest.TestCase):
    def test_move(self):
        snake = sn.snake(sn.vector(1,1),sn.vector(1,0),'white',sn.vector(0,0))
        self.assertEqual(snake.direction,sn.vector(1,0))
        self.assertEqual(snake.tiles,[sn.vector(1,1)])
        self.assertEqual(snake.score,0)
        snake.move()
        self.assertEqual(snake.tiles,[sn.vector(2,1)])
        snake.change_direction(sn.vector(0,1))
        snake.move()
        self.assertEqual(snake.tiles,[sn.vector(2,2)])
        snake.grow()
        snake.grow()
        self.assertEqual(snake.tiles,[sn.vector(2,4),sn.vector(2,3),sn.vector(2,2)])
        snake.change_direction(sn.vector(-1,0))
        snake.move()
        self.assertEqual(snake.tiles,[sn.vector(1,4),sn.vector(2,4),sn.vector(2,3)])
        self.assertEqual(snake.score,2)
        snake.reset(sn.vector(0,0),sn.vector(1,0))
        self.assertEqual(snake.tiles,[sn.vector(0,0)])
        self.assertEqual(snake.score,0)
        self.assertEqual(snake.highscore,2)
class Test_Game(unittest.TestCase):
    def test_2players(self):
        gm = sn.game(100,100,True)
        gm.set_gamemode('2players')
        self.assertEqual(gm.gamemode,'2players')
        self.assertEqual(gm.snake1.tiles,[sn.vector(0,0)])
        self.assertEqual(gm.snake2.tiles,[sn.vector(0,20)])
        self.assertEqual(gm.food,sn.vector(10,10))
        self.assertEqual(len(gm.poisons),10)
        gm.move() # both snakes move
        self.assertEqual(gm.snake1.tiles,[sn.vector(5,0)])
        self.assertEqual(gm.snake2.tiles,[sn.vector(5,20)])
        gm.snake1.reset(sn.vector(5,10),sn.vector(5,0))
        gm.move() # snake1 eats food
        self.assertEqual(gm.snake1.tiles,[sn.vector(10,10),sn.vector(5,10)])
        self.assertEqual(gm.snake2.tiles,[sn.vector(10,20)])
        self.assertFalse(gm.food in gm.snake1.tiles or gm.food in gm.snake2.tiles)
        self.assertEqual(len(gm.poisons),11)
        gm.snake2.reset(gm.food-sn.vector(0,5),sn.vector(0,5))
        pos = gm.food
        gm.move() # snake2 eats food
        self.assertEqual(gm.snake1.tiles,[sn.vector(15,10),sn.vector(10,10)])
        self.assertEqual(gm.snake2.tiles,[pos,pos-sn.vector(0,5)])
        self.assertFalse(gm.food in gm.snake1.tiles or gm.food in gm.snake2.tiles)
        self.assertEqual(len(gm.poisons),12)
        gm.snake1.reset(gm.poisons[0]-sn.vector(-5,0),sn.vector(-5,0))
        gm.move() # snake1 eats poison
        self.assertEqual(len(gm.snake1.tiles),1)
        self.assertEqual(len(gm.poisons),11)
        gm.snake2.reset(gm.poisons[0]-sn.vector(0,-5),sn.vector(0,-5))
        gm.move() # snake2 eats poison
        self.assertEqual(len(gm.snake2.tiles),1)
        self.assertEqual(len(gm.poisons),10)
        gm.snake1.reset(sn.vector(45,0),sn.vector(5,0))
        gm.snake1.grow()
        gm.snake2.reset(sn.vector(0,45),sn.vector(0,5))
        gm.snake2.grow()
        gm.move() # both snakes run out of bounds
        self.assertEqual(len(gm.snake1.tiles),1)
        self.assertEqual(len(gm.snake2.tiles),1)
        gm.snake1.reset(sn.vector(-5,0),sn.vector(5,0))
        gm.snake1.grow()
        gm.snake1.grow()
        gm.snake2.reset(sn.vector(0,-10),sn.vector(0,5))
        gm.snake2.grow()
        gm.move() # snake2 eats snake1
        self.assertEqual(len(gm.snake1.tiles),3)
        self.assertEqual(len(gm.snake2.tiles),1)
        gm.snake1.reset(sn.vector(0,0),sn.vector(5,0))
        gm.snake1.grow()
        gm.snake2.reset(sn.vector(10,-5),sn.vector(0,5))
        gm.snake2.grow()
        gm.move() # snake1 eats snake2
        self.assertEqual(len(gm.snake1.tiles),1)
        self.assertEqual(len(gm.snake2.tiles),2)
        gm.snake1.reset(sn.vector(-5,0),sn.vector(5,0))
        gm.snake1.grow()
        gm.snake2.reset(sn.vector(15,0),sn.vector(-5,0))
        gm.snake2.grow()
        gm.move() # snakes collide
        self.assertEqual(len(gm.snake1.tiles),1)
        self.assertEqual(len(gm.snake2.tiles),1)
    def test_ai(self):
        gm = sn.game(100,100,True)
        gm.set_gamemode('1player+AI')
        for i in range(4):
            gm.move()
        self.assertEqual(gm.snake2.tiles,[sn.vector(10,10),sn.vector(5,10)])
        dist = gm.snake1.tiles[0].distance(gm.food)
        for i in range(dist//5): # AI finds food in the shortest path
            gm.move()
        self.assertEqual(len(gm.snake2.tiles),3)
        
if __name__ == '__main__':
    unittest.main()