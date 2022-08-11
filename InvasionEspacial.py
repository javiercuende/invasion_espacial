import pygame
from pygame import mixer

from typing import List
from random import randint

_DIMENSIONES_PANTALLA   = (800., 600.)
_MAX_POS_X: float = 736.
_MAX_POS_Y: float = 536.

class Personaje:

    def __init__(self, pos_x:float, pos_y:float) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y

    def show_personaje_en_pantalla(self, pantalla, imagen) -> None: 
        _IMAGE = pygame.image.load(imagen)
        pantalla.blit(_IMAGE, (self.pos_x, self.pos_y) )

class Cohete(Personaje):

    _IMG_COHETE : str                = "cohete.png"

    def __init__(self, pos_x: float = 366., pos_y: float=500.) -> None:
        super().__init__(pos_x, pos_y)

    def show_personaje_en_pantalla(self, pantalla) -> None:       
        super().show_personaje_en_pantalla(pantalla, Cohete._IMG_COHETE) 

    def desplaza_x(self, longitud:float) -> bool:
        if self.pos_x + longitud < 0 or self.pos_x + longitud >=_MAX_POS_X:
            return False
        self.pos_x += longitud
        return True

    def desplaza_y(self, longitud:float) -> bool:
        if self.pos_y + longitud < 0 or self.pos_y + longitud >=_MAX_POS_Y:
            return False
        self.pos_y += longitud
        return True


class Enemigo(Personaje):

    _IMG_ENEMIGO : str                = "enemigo.png"
    _DESPLAZAMIENTO: float            = 3
    _SALTO_VERTICAL: float            = 50

    def __init__(self, id_enemigo: int , pos_x: float = None, pos_y: float=None) -> None:
        if not pos_x: pos_x = randint(0, _MAX_POS_X)
        if not pos_y: pos_y = randint(0, 200)
        super().__init__(pos_x, pos_y)
        self.id_enemigo = id_enemigo
        self.desplazamiento = -1*(Enemigo._DESPLAZAMIENTO)

    def desplaza(self) -> None:        
        if  self.pos_x < 0.0:
            self.pos_y +=Enemigo._SALTO_VERTICAL
            self.pos_x = Enemigo._DESPLAZAMIENTO
            self.desplazamiento = Enemigo._DESPLAZAMIENTO
        if self.pos_x > _MAX_POS_X:
            self.pos_y +=Enemigo._SALTO_VERTICAL
            self.pos_x = _MAX_POS_X - Enemigo._DESPLAZAMIENTO
            self.desplazamiento = -1*(Enemigo._DESPLAZAMIENTO)
        self.pos_x += self.desplazamiento

    def show_personaje_en_pantalla(self, pantalla) -> None:       
        super().show_personaje_en_pantalla(pantalla, Enemigo._IMG_ENEMIGO) 

    def __repr__(self) -> str:
        return f"id: {self.id_enemigo} pos: ({self.pos_x},{self.pos_y})"


class AccionJuego:

    __VELOCIDAD_BALA = 7.

    def __init__(self, cohete: Cohete, enemigos: List[Enemigo]) -> None:
        self.cohete             : Cohete  = cohete
        self.enemigos           : List[Enemigo] = enemigos
        self.posiciones_balas   : List = []
        self.enemigos_abatidos  : int  = 0

    def disparo(self) -> None:
        sonido_bala = mixer.Sound('disparo.mp3')
        sonido_bala.play()
        self.posiciones_balas.append((self.cohete.pos_x+16, self.cohete.pos_y-50))

    def show_balas(self, pantalla) -> None:
        _IMAGE_BALA = pygame.image.load('bala.png')
        nuevas_pos_balas = []
        for pos_x, pos_y in self.posiciones_balas:
            pantalla.blit(_IMAGE_BALA, (pos_x, pos_y) )
            nuevas_pos_balas.append((pos_x, pos_y-AccionJuego.__VELOCIDAD_BALA))
        self.posiciones_balas = nuevas_pos_balas

    def detecta_impacto_bala(self) -> None:
        for _enemigo in self.enemigos:
            for _item_bala in self.posiciones_balas:
                if _item_bala[0] > (_enemigo.pos_x -30)  and _item_bala[0] < (_enemigo.pos_x +30) \
                    and _item_bala[1] > (_enemigo.pos_y - 30) and _item_bala[1] < (_enemigo.pos_y +30):
                    sonido_golpe = mixer.Sound('Golpe.mp3')
                    sonido_golpe.play()
                    self.enemigos.remove(_enemigo)
                    self.posiciones_balas.remove(_item_bala)
                    self.enemigos_abatidos +=1

    def get_enemigos_abatidos(self) -> int:
        return self.enemigos_abatidos

    def comprueba_cohete_impacto(self) -> bool:
        hay_impacto: bool = False
        for _enemigo in self.enemigos:
            if _enemigo.pos_y >= self.cohete.pos_y -32: hay_impacto = True
        return hay_impacto


class PantallaJuego:

    _NUM_ENEMIGOS           = 8
    _TITULO                 = "Invasión Espacial"
    _ICONO_GAME             = "ovni.png"
    #RGB
    _BACKGROUND_COLOR       = (205,144,228)
    _LONGITUD_DESPLAZA_COHETE: float = 20.0

    def __init__(self) -> None:
        pygame.init()
        self.pantalla = pygame.display.set_mode(_DIMENSIONES_PANTALLA)
        self.config_inicial()
        self.cohete         : Cohete  = Cohete()
        self.lista_enemigos : List    = []
        self.__cargar_enemigos()
        self.accion_juego   : AccionJuego = AccionJuego(cohete=self.cohete, enemigos=self.lista_enemigos)
        self.__carga_musica_fondo()

    def __carga_musica_fondo(self):
        mixer.music.load('MusicaFondo.mp3')
        mixer.music.play(-1)

    def __cargar_enemigos(self) -> None:
        # enemigos existentes:
        ids_enemigos = [ int(_item_enemigo.id_enemigo) for _item_enemigo in self.lista_enemigos]
        for i in range(0, PantallaJuego._NUM_ENEMIGOS):
            if i not in ids_enemigos:
                _enemigo = Enemigo(id_enemigo=i)
                self.lista_enemigos.append(_enemigo)

        
    @property
    def pantalla_main(self) : return self.pantalla

    def config_inicial(self):
        pygame.display.set_caption(PantallaJuego._TITULO)
        icono = pygame.image.load(PantallaJuego._ICONO_GAME)
        pygame.display.set_icon(icono)        
        pygame.display.update()
        
    def __handler_events(self) -> bool:
        for evento in pygame.event.get():
            # Cierre de juego
            if evento.type == pygame.QUIT:  return False
            # Accionar una tecla de teclado
            if evento.type == pygame.KEYDOWN: 
                if evento.key == pygame.K_LEFT      : 
                    self.cohete.desplaza_x(longitud=(PantallaJuego._LONGITUD_DESPLAZA_COHETE)*-1)
                elif evento.key == pygame.K_RIGHT   : 
                    self.cohete.desplaza_x(longitud=(PantallaJuego._LONGITUD_DESPLAZA_COHETE))
                elif evento.key == pygame.K_UP      : 
                    self.cohete.desplaza_y(longitud=(PantallaJuego._LONGITUD_DESPLAZA_COHETE)*-1)
                elif evento.key == pygame.K_DOWN    : 
                    self.cohete.desplaza_y(longitud=(PantallaJuego._LONGITUD_DESPLAZA_COHETE))
                elif evento.key == pygame.K_SPACE:
                    self.accion_juego.disparo()
        return True

    def run(self):
        esta_ejecutandose   : bool = True
        fin_juego           : bool = False
        num_enemigos_abatidos = 0
        while esta_ejecutandose:
            esta_ejecutandose = self.__handler_events()
            self.pantalla.fill(PantallaJuego._BACKGROUND_COLOR)
            _FONDO = pygame.image.load('Fondo.jpg')
            self.pantalla_main.blit(_FONDO,(0,0))
            # Mostramos el puntuaje
            if not fin_juego:
                fuente = pygame.font.Font('freesansbold.ttf',32)
                texto_show = fuente.render(f'Puntuación: {num_enemigos_abatidos}', True, (255,255,255))
                self.pantalla_main.blit(texto_show,(10,10))
                self.show_cohete()
                self.show_enemigos()
                if len(self.accion_juego.posiciones_balas) > 0:
                    self.accion_juego.show_balas(pantalla=self.pantalla_main)
                    self.accion_juego.detecta_impacto_bala()
                    num_enemigos_abatidos = self.accion_juego.get_enemigos_abatidos()
                self.__cargar_enemigos()
            # Comprobacion de que ningun enemigo haya llegado a la y del cohete
            fin_juego: bool = self.accion_juego.comprueba_cohete_impacto()
            if fin_juego: 
                fuente = pygame.font.Font('freesansbold.ttf',50)
                texto_show = fuente.render(f'GAME OVER!', True, (255,255,255))
                self.pantalla_main.blit(texto_show,(250,280))
            # Actualizamos la pantalla
            pygame.display.update()            

    show_cohete = lambda self: \
        self.cohete.show_personaje_en_pantalla(pantalla=self.pantalla_main)

    def show_enemigos(self):
        for _enemigo in self.lista_enemigos:
            _enemigo.desplaza()
            _enemigo.show_personaje_en_pantalla(pantalla=self.pantalla_main)

if __name__ == '__main__':
    pantalla = PantallaJuego()
    pantalla.run()
