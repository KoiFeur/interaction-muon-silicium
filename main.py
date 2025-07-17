import os, sys, termios, tty, time

from manim.scene.three_d_scene import OpenGLCamera
sys.path.append("/run/media/n/feur/feur/biboubiboup/lepython/interaction_muon_silicium/")
import parser
import matplotlib.pyplot as plt
import numpy as np
from manim import *
from manim.opengl import *
from tqdm import tqdm 
np.set_printoptions(threshold=sys.maxsize)
# Collect events until released

c = 299792458
h = 6.62607015e-34
eV = 1.602176634e-19
AMU = 931.5 * c**2 # MeV/c**2

def concatenate(data):
    temp = []
    for i in data:
        temp = temp + i
    return temp

def ploting_hist(names, titles, content, dims, fig_dims, lims = None, colors = None):
    plt.figure(figsize=fig_dims, dpi=100)
    if colors == None:
        colors = ["blue"] * len(titles)
    for i in range(len(titles)):
        plt.subplot(dims[0], dims[1], i+1)
        plt.tight_layout()
        plt.bar(range(len(names[i])), content[i], tick_label = names[i], color = colors[i])
        plt.xticks(rotation = 90)
        plt.title(titles[i])
        if lims != None:
            plt.ylim(lims[0], lims[1])
    plt.show()

    


class Collision(ThreeDScene):
    def create_product(self, axes, sub_product: parser.Sub_product, starting_point: np.ndarray, duration_time: float):
        r = parser.ATOMS[sub_product.name]["radius"] * 1.5
        v = np.sqrt(1 - (1/((sub_product.energy/parser.ATOMS[sub_product.name]["mass"]) + 1))) * c
        #color = sub_product.color
        #v = np.sqrt(2 * sub_product.energy * eV / MASSES[sub_product.name])
        ending_point = axes.coords_to_point(starting_point + sub_product.vecteur * v * duration_time)[0]
        starting_sphere = Sphere(
            center=axes.coords_to_point(starting_point)[0],
            radius=r,
            resolution = (8, 8),
            stroke_width = np.array([0.1])
        ).set_color(parser.ATOMS[sub_product.name]["color"])
        if "C" in sub_product.name:
            starting_sphere.stroke_color = ManimColor.from_hex("#FFFFFF")
        else:
            starting_sphere.stroke_color = BLACK
        return starting_sphere, ending_point

    def create_gamma(self, axes, sub_product: parser.Sub_product, starting_point: np.ndarray):
        ending_point = axes.coords_to_point(starting_point + sub_product.vecteur * c)[0]
        gamma = Line3D(
            axes.coords_to_point(starting_point)[0],
            ending_point,
        ).set_color(parser.ATOMS[sub_product.name]["color"])
        return gamma

    def create_in_neutron(self, collision_point, energy, duration_time, axes):
        v = np.sqrt(1 - (1/((energy/parser.ATOMS["neutron"]["mass"]) + 1))) * c
        r = parser.ATOMS["neutron"]["radius"] * 1.5
        starting_point = axes.coords_to_point(collision_point + np.array([0, 0, 1]) * v * duration_time)[0]
        neutron = Sphere(
            center = starting_point,
            radius = r,
            resolution = (8,8),
            stroke_width = np.array([0.1])
        ).set_color(parser.ATOMS["neutron"]["color"])
        neutron.stroke_color = BLACK
        return neutron

    def play_collision(self, file, axes, reaction, animation_duration = 1, duration_time = 1e-8, neutron_duration=1e-8):
        self.move_camera(theta=0, phi=0)
        spheres = []
        gammas = []
        for i in reaction.sub_products:
            if i.name == "gamma":
                gammas.append(self.create_gamma(axes, i, reaction.vecteur))
            else:
                spheres.append(self.create_product(axes, i, reaction.vecteur, duration_time))
        spheres = list(zip(*spheres))
        starting_spheres = VGroup(spheres[0])
        ending_points = np.array(spheres[1])
        animations = [starting_spheres[i].animate(run_time=animation_duration, rate_func=rate_functions.linear).move_to(ending_points[i]) for i in range(len(ending_points))]
        gammas = VGroup(gammas)#[Create(i) for i in gammas]

        in_neutron = self.create_in_neutron(reaction.vecteur, file.energy, neutron_duration, axes)

        si = reaction.reac[-1]
        silicium = Sphere(
            center = axes.coords_to_point(reaction.vecteur)[0],
            radius = parser.ATOMS[si]["radius"] * 1.5,
            resolution = (8, 8),
            stroke_width = np.array([0.1])
        ).set_color(parser.ATOMS[si]["color"])
        silicium.stroke_color = BLACK
        group = VGroup([in_neutron])
        neutranim = [group[0].animate(run_time=1, rate_func=rate_functions.linear).move_to(axes.coords_to_point(reaction.vecteur)[0])]

        self.play(Create(silicium))
        self.move_camera(phi = 80 * DEGREES, theta = -90 * DEGREES)
        self.wait(3)
        self.add_fixed_in_frame_mobjects(Text(str(file.energy) + "MeV").to_corner(UP + LEFT))
        self.add(in_neutron)
        self.play(*neutranim)
        self.remove(silicium, in_neutron)
        self.add(*starting_spheres, *gammas)
        self.play(*animations)
        self.move_camera(phi = 80 * DEGREES, theta = 0 * DEGREES, run_time=3, rate_func=rate_functions.linear)
        self.move_camera(phi = 80 * DEGREES, theta = 90 * DEGREES, run_time=3, rate_func=rate_functions.linear)
        self.move_camera(phi = 80 * DEGREES, theta = 180 * DEGREES, run_time=3, rate_func=rate_functions.linear)
        self.move_camera(phi = 80 * DEGREES, theta = 270 * DEGREES, run_time=3, rate_func=rate_functions.linear)

    def title(self):
        try:
            self.play(*[FadeOut(mob)for mob in self.mobjects])
            self.remove(*[mob for mob in self.mobjects])
        except ValueError:
            pass
        #self.move_camera(phi=0,theta=0)
        text = Text("Interaction neutron-Silicium")
        self.play(Write(text))

    def first_reaction_text(self, reaction_num=165):
        self.play(*[FadeOut(mob)for mob in self.mobjects])
        reaction = self.files[0].get_reac()[reaction_num]
        text = Text(*[reaction.reaction_str])
        Write(text)

    def first_collision(self, reaction_num=165):
        self.play(*[FadeOut(mob)for mob in self.mobjects])
        self.move_camera(phi=0,theta=0)
        reaction = self.files[0].get_reac()[reaction_num]
        print(reaction.text)
        axes = ThreeDAxes(
            x_range=(-1, 1, 0.2),
            y_range=(-1, 1, 0.2),
            z_range=(-1, 1, 0.2),

        )
        self.play(Create(axes))
        self.play_collision(self.files[0],axes,reaction, animation_duration=5, duration_time=5e-6, neutron_duration=1e-7)

    def third_collision(self, reaction_num=19):
        self.play(*[FadeOut(mob)for mob in self.mobjects])
        self.move_camera(phi=0,theta=0)
        reaction = self.files[31].get_reac()[reaction_num]
        print(reaction.text)
        print(self.files[31])
        axes = ThreeDAxes(
            x_range=(-1, 1, 0.2),
            y_range=(-1, 1, 0.2),
            z_range=(-1, 1, 0.2),

        )
        self.play(Create(axes))
        self.play_collision(self.files[31],axes,reaction, animation_duration=5, duration_time=5e-8, neutron_duration=3e-8)

    def second_collision(self, reaction_num=17, file=12):
        self.play(*[FadeOut(mob)for mob in self.mobjects])
        self.move_camera(phi=0,theta=0)
        reaction = self.files[file].get_reac()[reaction_num]
        print(self.files[file])
        print(reaction.text)
        axes = ThreeDAxes(
            x_range=(-1, 1, 0.2),
            y_range=(-1, 1, 0.2),
            z_range=(-1, 1, 0.2),

        )
        self.play(Create(axes))
        self.play_collision(self.files[file],axes,reaction, animation_duration=5, duration_time=5e-8, neutron_duration=3e-8)

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))

        except AttributeError:
            print('special key {0} pressed'.format(key))
            if key == "page_up":
                if not(self.animation_played):
                    print(self.playing_animation)
                    if self.playing_animation > 0:
                        self.playing_animation -= 1
                        self.home_made_animations[self.playing_animation]()
            if key == "page_down":
                if not(self.animation_played):
                    self.playing_animation += 1
                    print(self.playing_animation)
                    print(self.home_made_animations)
                    self.home_made_animations[self.playing_animation]()
        self.animation_played = True

    def on_release(self):
        print("released")
        self.animation_played = False

    def construct(self):
        liste = os.listdir("Secondaries_zips")
        liste = ["Secondaries_zips/" + i for i in liste if "txt" in i]
        print(liste)

        self.files = parser.open_multiple_files(liste)

        self.playing_animation = 0
        self.animation_played = False

        self.home_made_animations = [self.title, self.first_collision, self.second_collision, self.third_collision]
        self.home_made_animations[0]()
        self.home_made_animations[1]()
        self.home_made_animations[2]()
        self.home_made_animations[3]()
        """
        page_up = [27, 91, 53, 126]
        page_down = [27, 91, 54, 126]
        sequence_page_up = 0
        sequence_page_down = 0
        while True:
            instant = time.time()
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                input = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                print(time.time() - instant)
                if time.time() - instant > 1:
                    self.on_release()
                    instant = time.time()
                print(type(ord(input)))
                print(ord(input))
                if ord(input) == 3:
                    quit()

                if ord(input) == page_up[sequence_page_up]:
                    sequence_page_up += 1
                else:
                    sequence_page_up = 0

                if ord(input) == page_down[sequence_page_down]:
                    sequence_page_down += 1
                else:
                    sequence_page_down = 0
                if sequence_page_down == 4:
                    self.on_press("page_down")
                    sequence_page_down = 0

                if sequence_page_up == 4:
                    self.on_press("page_up")
                    sequence_page_up = 0
            """
