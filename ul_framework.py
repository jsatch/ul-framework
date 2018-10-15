import pygame, sys

size = width, height = 320, 240

class Controller:
    """" 
    Clase Controladora Generica.  
    
    Solamente se debe de sobreescribir el metodo on_create.
    """
    def __init__(self):
        self._views = []
        self.on_create()
    
    def on_create(self):
        """ Metodo a sobreescribir que se ejecutara al inicializar la pantalla"""
        pass

    def add_view(self, view):
        self._views.append(view)

    def _render(self, screen):
        for view in self._views:
            view._render(screen)

    def _update(self):
        for view in self._views:
            view._update()

    def serve_event(self, event):
        if event["type"] == "QUIT":
            sys.exit()
        for view in self._views:
            view.serve_event(event)


class ControllerManager:
    """ 
    Clase encargada de la gestion de los distintos controllers (pantallas)
    que puede manejar una aplicacion.
    """
    def __init__(self, event_queue):
        self._controllers = []
        self._event_queue = event_queue

    def push_controller(self, controller):
        self._event_queue.add_observer(controller)
        self._controllers.append(controller)

    def get_controller(self):
        return self._controllers[len(self._controllers)-1]
    
    def pop_controller(self):
        self._controllers.pop()
        return self._controllers[len(self._controllers)-1]


class View:
    """ 
    Clase Generica de View.

    Debe implementar el metodo _update para definir como se vera
    el componente grafico.
    """
    def __init__(self, ruta_imagen):
        self._imagen = pygame.image.load(ruta_imagen)
        self._rect = self._imagen.get_rect()

        #observadores
        self._observers = []

    def serve_event(self, event):
        if event["type"] == "MOUSE_CLICK":
            for observer in self._observers:
                observer.on_click(event)

    def set_onclick_observer(self, observer):
        self._observers.append(observer)

    def _render(self, screen):
        screen.blit(self._imagen, self._rect)
    
    def _update(self):
        pass

class GameMain:
    """
    Clase que representar al juego.
    """
    _BLACK = 0, 0, 0
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode(size)
        self._event_queue = EventQueue()
        self._controller_manager = ControllerManager(self._event_queue)

    def start_controller(self, controller):
        """ 
        Metodo para setear un controller en la pila de controllers.

        Keyword arguments:
        controller -- Controlador que se iniciara y se vera en pantalla.
        """
        self._controller_manager.push_controller(controller)

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self._event_queue.post({
                        "type" : "QUIT"
                    })
                if event.type == pygame.MOUSEBUTTONUP:
                    posx, posy = pygame.mouse.get_pos()
                    self._event_queue.post({
                        "type" : "MOUSE_CLICK",
                        "x" : posx,
                        "y" : posy
                    })
            self._screen.fill(GameMain._BLACK)
            self._event_queue.dispatch()
            self._controller_manager.get_controller()._update()
            self._controller_manager.get_controller()._render(self._screen)
            #self._screen.blit(ball, ballrect)
            pygame.display.flip()
            
class EventQueue:
    """
    Cola de eventos.

    Tener en cuenta que se sirve esta cola de manera lineal (no asincrona).
    """
    def __init__(self):
        self._events = []
        self._observers = []

    def add_observer(self, view):
        self._observers.append(view)
    
    def post(self, event):
        self._events.append(event)

    def dispatch(self):
        for event in self._events:
            for observer in self._observers:
                observer.serve_event(event)

        self._events = []

