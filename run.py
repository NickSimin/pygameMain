from game.scripts.main import Game

game = Game((1024, 512), 60, "Simulate", "0")
game.menu()
game.run()

pg.quit()
