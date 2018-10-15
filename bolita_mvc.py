from ul_framework import View, Controller, GameMain

def se_encuentra_dentro(posx, posy, rect):
    if posx >= rect.left and posy >= rect.top:
        return True
    else:
        return False

size = width, height = 320, 240

class MainController(Controller):
    def on_create(self):
        self.bolita = BolaView("./imagenes/intro_ball.gif")
        self.bolita.set_onclick_observer(self)
        self.add_view(self.bolita)

    def on_click(self, event):
        print("({} , {})".format(event["x"], event["y"]))

class BolaView(View):
    def __init__(self, ruta_imagen):
        super().__init__(ruta_imagen)
        self._speed = [2, 2]

    def set_position(self, x,y):
        self._rect.x = x
        self._rect.y = y
    
    def _update(self):
        self._rect = self._rect.move(self._speed)
        if self._rect.left < 0 or self._rect.right > width:
            self._speed[0] = -self._speed[0]
        if self._rect.top < 0 or self._rect.bottom > height:
            self._speed[1] = -self._speed[1]

def main ():
    game = GameMain()
    main_controller = MainController()
    game.start_controller(main_controller)
    game.start()



    

if __name__ == "__main__":
    main()