'''

Version pour l'etape 1.1.2

1.1.1 Fenetre principale 
La fenetre principale s'ouvre avec un Frame contenant un Canevas

1.1.2 Introduction du Defender
Le Defender est dessine et peut etre deplace de gauche a droite avec les touches fleches gauche et droite du clavier

Cette version peut-etre amelioree ...

@author: plantec
'''
from re import X
from textwrap import fill
from turtle import width
from tkinter import *
import csv

try:  # import as appropriate for 2.x vs. 3.x
   import tkinter as tk
except:
   import Tkinter as tk

"""IL FAUT FAIRE LES COMMENTAIRES
TO DO : ALIEN, FLEET, COLLISION

"""



class Alien(object):

    def __init__(self):
        self.id = None 
        self.alive = True

    def touched_by(self, canvas, other):
        """
        Méthode qui gère la collision avec d'autre entité qui comporte le tag = "other"
        """
        a_pos = canvas.bbox(self.id)#on donne les coordonnées de l'alien à l'objet a_pos
        overlapped = canvas.find_overlapping(a_pos[0], a_pos[1], a_pos[2], a_pos[3])#prend les coordonnées du rectangle de l'image(x1,x2,y1,y2)
        others = canvas.find_withtag(other)
        for element in others: 
            if element in overlapped:
                return True
        return False
        
    def get_touched_by(self, canvas, other):
        """
        Méthode complémentaire à touched_by, on récupère l'id de l'objet qui overlap avec l'alien
        """
        a_pos = canvas.bbox(self.id)
        overlapped = canvas.find_overlapping(a_pos[0], a_pos[1], a_pos[2], a_pos[3])
        others = canvas.find_withtag(other)
        for element in others: 
            if element in overlapped:
                return element   


    def install_in(self, canvas, x1, y1, x2, y2, image, tag): ###Version avec des carrés blancs
        #self.id = canvas.create_rectangle(x1, y1, x2, y2, tags=tag, fill="white")
        self.id = canvas.create_image(x1, y1, image=image, tags=tag)
    
    def move_in(self, canvas, dx, dy):
        canvas.move(self.id, dx, dy)#pour déplacer l'alien

    def is_still_in_screen(self, canvas):
        coord = canvas.coords(self.id)
        width = 800 #Valeur brut à changer si possible
        x = coord[0]
        x1 = x + 20
        if (x1 > width): ## est sortie à droite
            return -1
        if (x-20 < 0): #est sortie à gauche
            return 1
        return 0 #est dans l'écran
        

    
class Fleet(object):
    """
    Class Fleet qui gère les aliens en jeu 
    """
    def __init__(self):
        self.aliens_line = 5 #nb ligne d'aliens
        self.aliens_columns = 10 #nb colonne d'aliens
        self.aliens_inner_gap = 20 #espace entre les aliens
        self.alien_x_delta = 30
        self.alien_y_delta = 20
        self.fleet_size = self.aliens_line * self.aliens_columns
        self.aliens_fleet = [None] * self.fleet_size
        self.direction = "right"
        self.speed = 0.1 #vitesse de la fleet
        self.img = tk.PhotoImage(file='alien.gif') #on recupere l'image alien
        self.img = self.img.subsample(2)


    def install_in(self, canvas):
        
        x1 = 0
        y1 = 15
        c = 0 
        for i in range(0, self.fleet_size): #placement d'alien + gap
            y2 = y1 + self.aliens_inner_gap 
            x2 = x1 + self.aliens_inner_gap

            alien = Alien()
            c = c + 1
            alien.install_in(canvas, x1, y1, x2, y2, self.img, "alien") #affichage de l'image alien pour chaque alien
            self.aliens_fleet[i] = alien

            x1 = x2 + self.alien_x_delta
            if c == 10:
                c = 0
                x1 = 0
                y1 = y2 + self.alien_y_delta
    


    def remove_alien(self, canvas, index):
        """
        Méthode qui permet d'enlever un alien de la liste et sur le canvas
        canvas -> canvas utilisé
        index = index de la liste
        """
        a = self.aliens_fleet[index]
        self.aliens_fleet.remove(a)
        canvas.delete(a.id)


    def move_in(self, canvas):
        """
        @Méthode 
        Canvas -> Canvas utilisé
        Cette méthode déplace tous les aliens sur l'axe X en fonction de self.direction
        Puis regarde si la flotte doit être abaissé sur l'axe Y
        """
        ###On regarde la direction pour determiner dx
        if self.direction == "right":
            dx = self.speed
        else:
            dx = -self.speed
        move_down = False
        for alien in self.aliens_fleet:
            ### On déplace tous les aliens sur le x en fonction de self.direction
            alien.move_in(canvas, dx, 0)
            ### On regarde si on doit changer de dir, si on change de dir -> il faut baisser la flotte sur l'axe y.
            move_down = self.change_dir(canvas, alien, move_down) 

        ###Si move down == True
        if move_down:
            ###On baisse la flotte 
            self.move_down(canvas)


    def change_dir(self, canvas, alien, n):
        """
        @Méthode, 
        Canvas -> le canvas utilisé, 
        alien -> objet de la classe Alien
        n -> bool, var qui garde si le changement de direction a été effectué sur la frame
        -> return False, ou True, pour savoir si on a changé de dir sur la frame
        """
        if n == True: return n
        pos_in_screen = alien.is_still_in_screen(canvas) #Soit 0, 1, -1

        ###Si l'alien se trouve au milieu de l'écran
        if (pos_in_screen == 0):
            return False

        ###Si l'alien se trouve en dehors de l'écran à droite
        elif(pos_in_screen == -1):
            ###S'il sort à droite et qu'il continue d'aller à droite 
            if (self.direction == "right"):
                ###On change la direction -> évite le bug du gauche droite infini
                self.direction = "left"
                return True
        ###Si l'alien se trouve en dehors de l'écran à gauche -> utilisation de else plus rigoureuse mais moins lisible
        elif (pos_in_screen == 1):
            if (self.direction == "left"):
                self.direction = "right"
                return True
        

    def move_down(self, canvas):
        """
        @Méthode 
        canvas -> le canvas utilisé 
        """
        ###On abaisse tous les aliens de sur l'axe Y
        for alien in self.aliens_fleet:
            alien.move_in(canvas, 0, 10)  

    def manage_touched_aliens_by(self, canvas, defender):
        """à faire"""
        print(canvas.find_withtag("defender"))

class Bullet(object):
    def __init__(self, shooter):
        self.radius = 5
        self.color = "red"
        self.speed = 1
        self.id = None
        self.shooter = shooter

    def install_in(self, canvas):
        coord = canvas.coords(self.shooter.id) #On récupère les coords via la méthode coords de canvas
        x = coord[0]
        y = coord[1]

        d = self.radius * 2
        x1 = x + (self.shooter.width / 4) #pour commencer au bon endroit du vaisseau
        x2 = x + (self.shooter.width / 4) + d
        y1 = y - d 
        y2 = y

        self.id = canvas.create_oval(x1, y1, x2, y2,  fill="red", tag="projectile") #Création de la balle

    def move_in(self, canvas):
        canvas.move(self.id, 0, -self.speed)

    def is_still_in_screen(self, canvas):
        """
        Méthode qui vérifie le balle est toujours dans l'écran
        """
        coords = canvas.coords(self.id)
        y = coords[3] #Le y le plus bas de l'écran
        if (y < 0):
            return False
        return True

class Defender(object):
    def __init__(self): 
        self.width = 20
        self.height = 20
        self.move_delta = 20 
        self.id = None 
        self.max_fired_bullets = 8 
        self.fired_bullets = []
        self.is_alive = True
        
    def install_in(self, canvas):
        lx = 400 + self.width/2
        ly = 600 - self.height - 10
        self.id = canvas.create_rectangle(lx, ly, lx + self.width, ly + self.height, fill="white", tag="defender")
    
    def move_in(self,canvas, dx): 
        canvas.move(self.id, dx, 0)
    
    def fire(self, canvas):
        if len(self.fired_bullets) >= self.max_fired_bullets: return 
        bullet = Bullet(self)
        bullet.install_in(canvas)
        self.fired_bullets.append(bullet)
    
    def remove_bullet(self, canvas, index):
        for i in range(0,len(self.fired_bullets)):
            if index == self.fired_bullets[i].id:
                self.fired_bullets.pop(i)
                canvas.delete(index)
                return

class Game(object):
    """Class qui gère le jeu"""


    def __init__(self, frame, space_invaders):
        width=800 #Tailel en largeur de l'écran
        height=600 #Taille en hauteur de l'écran
        self.width = width #récuperer la taille du canvas
        self.frame=frame
        self.canvas=tk.Canvas(self.frame,width=width, height=height,bg="black")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.defender=Defender()
        self.fleet = Fleet()
        self.fleet.install_in(self.canvas)
        self.is_playing = True
        self.space_invaders = space_invaders
  
        
    def start(self):
        
        self.defender.install_in(self.canvas)
        self.frame.winfo_toplevel().bind("<Key>", self.keypress)
        
    def keypress(self, event):
        x = 0
        if event.keysym == 'Left' and self.canvas.coords(self.defender.id)[0] > 10:  #déplace à gauche jusqu'à la limite du canvas + 10
            x = -10; 
        elif event.keysym == 'Right'and self.canvas.coords(self.defender.id)[0] < self.width - 30: #déplace à droite jusqu'a la limite du canvas (avec self.width) à droite 
            x = 10
        elif event.keysym == "space":
            self.defender.fire(self.canvas)
        self.defender.move_in(self.canvas, x)
        
    def start_animation(self):
        self.start()
        self.animation()
    
    def move_bullets(self):
        """
        Méthiode qui fait bouger les bullets
        Si la bullet est en dehors de l'écran : on détruit la balle
        """
        i = 0
        for bullet in self.defender.fired_bullets:
            bullet.move_in(self.canvas)
            if not bullet.is_still_in_screen(self.canvas):
                self.canvas.delete(self.defender.fired_bullets[i].id) 
                self.defender.fired_bullets.remove(bullet)
            i = i+1

    def find_col(self):
        """
        Méthode qui s'occupe de gérer les collisions du jeu :
        à savoir les collisions de bullet - aliens
        TO DO -> collision des aliens avec le defender
        """
        alien_i = 0
        for alien in self.fleet.aliens_fleet:
            if alien.touched_by(self.canvas, "projectile"): 
                other_id = alien.get_touched_by(self.canvas, "projectile")
                self.fleet.remove_alien(self.canvas, alien_i)
                self.defender.remove_bullet(self.canvas, other_id)
            alien_i = alien_i + 1
        

    def animation(self):
        if not self.is_playing: 
            self.install_end_scene()
            return
        self.move_bullets()
        self.fleet.move_in(self.canvas)
        self.find_col()

        if (len(self.fleet.aliens_fleet) <= 0):
            self.is_playing = False
        self.canvas.after(1, self.animation)

    def install_end_scene(self):
        self.btn = Button(self.space_invaders.root, text="Continuer", command=self.change_scene)
        self.btn.pack()

    def change_scene(self):
        self.btn.destroy()
        self.space_invaders.menu_scene()

class Menu(object):

    def __init__(self, frame, space_invaders):
        width=800 #Taille en largeur de l'écran
        height=600 #Taille en hauteur de l'écran
        self.frame=frame
        self.canvas=tk.Canvas(self.frame,width=800, height=600,bg="black")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.space_invaders = space_invaders

    
    def set_scene(self):
        #Texte
        self.title=Label(self.canvas, text= "Space Invaders", font=(None, 15))
        self.title.pack(pady=14)
        self.btn_game = Button(self.canvas, text="Jouer", command=self.change_to_game)
        self.btn_score = Button(self.canvas, text="Score", command=self.change_to_score)
        self.btn_game.pack(pady=20)
        self.btn_score.pack()
        
        self.text_box_name = Text(self.canvas, width=10, height=1)
        self.text_box_name.pack()
        self.error_name = None

    def change_to_score(self):
        if not self.error_name is None:
            self.error_name.destroy()
        self.btn_game.destroy()
        self.btn_score.destroy()
        self.text_box_name.destroy()
        self.title.destroy()
        self.space_invaders.score_scene()


    def change_to_game(self):
        if not self.error_name is None:
            self.error_name.destroy()

        name = self.text_box_name.get(1.0, END)
        name = name.strip(" ")

        if len(name) <= 1:
            self.set_error_name()
            return 

        self.btn_game.destroy()
        self.btn_score.destroy()
        self.text_box_name.destroy()
        self.title.destroy()
        self.space_invaders.set_name(name)
        self.space_invaders.play_scene()
        

    def set_error_name(self):
        self.error_name = Label(self.canvas, text="Erreur, rentrez un pseudo")
        self.error_name.pack(pady=30)

class Score(object):

    def __init__(self, frame, sp):
        width=800 #Tailel en largeur de l'écran
        height=600 #Taille en hauteur de l'écran
        self.frame=frame
        self.canvas=tk.Canvas(self.frame,width=800, height=600,bg="black")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.space_invaders = sp

    def set_scene(self):
        self.load_score()
        self.show_score()
        self.btn_menu = Button(self.space_invaders.root, text="Menu", command=self.set_scene_to_menu)
        self.btn_menu.pack()
        
    def set_scene_to_menu(self):
        self.btn_menu.destroy()
        self.space_invaders.menu_scene()

    def load_score(self):
        self.score_data = []
        #on attrape les scores depuis un fichier csv de ce format : pseudo, score
        with open("fichier.csv", newline='') as fichier:
            #on crée un reader
            lecture = csv.reader(fichier, delimiter=",")

            for ligne in lecture:
                self.score_data.append(ligne)
        
        for i in range(len(self.score_data)):
            inted_score = int(self.score_data[i][1])
            self.score_data[i][1] = inted_score
        
        self.score_data.sort(key = lambda i:i[1], reverse=True)
    
    def show_score(self):
        for i in range(len(self.score_data)):
            name = self.score_data[i][0]
            score = self.score_data[i][1]
            self.canvas.create_text(400, 20 * i + 20, text=str(i+1) + ". " + str(name) + " " + str(score), fill="white", font=(None, 15))

class SpaceInvaders(object): 
    ''' Main Game class '''

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        self.width=800
        self.height=600
        #self.root.geometry("800x600")
        self.game_frame=tk.Frame(self.root,width=self.width, height=self.height,bg="green")
        self.menu_frame = tk.Frame(self.root, width=self.width, height=self.height,bg="green")
        self.score_frame = tk.Frame(self.root, width=self.width, height=self.height,bg="green")
        self.menu = Menu(self.menu_frame, self)
        self.score = Score(self.score_frame, self)
    

    ###Scenes
    def play_scene(self):
 
        self.menu_frame.forget()

        self.game_frame=tk.Frame(self.root,width=self.width, height=self.height,bg="green")
        self.game = Game(self.game_frame, self) 
        self.game_frame.pack()

        self.game.start_animation()
        self.root.mainloop()
   
    def menu_scene(self):
        self.menu_frame.pack()
        self.score_frame.forget()
        self.game_frame.forget()
        
        self.menu.set_scene()
        self.root.mainloop()

    def score_scene(self):
        self.menu_frame.forget()

        self.score_frame.pack()
        
        self.score.set_scene()
        self.root.mainloop()


    def set_name(self, new_name):
        self.name = new_name

                
jeu=SpaceInvaders()
jeu.menu_scene()

###TROIS FRAMES WORKING