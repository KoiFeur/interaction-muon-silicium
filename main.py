import os
import sys
sys.path.append("/run/media/n/feur/feur/biboubiboup/lepython/interaction_muon_silicium/")
import parser
import matplotlib.pyplot as plt
import numpy as np
from manim import *
from manim.opengl import *
from tqdm import tqdm 
np.set_printoptions(threshold=sys.maxsize)
from pynput import keyboard
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
    def spheres(self, u, v, r, starting_point):
        return np.array([
            starting_point[0] + r * np.cos(u) * np.sin(v),
            starting_point[0] + r * np.sin(u) * np.sin(v),
            starting_point[0] + r * np.cos(u)
        ]),

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

    def play_collision(self, file, axes, reaction, animation_duration = 1, duration_time = 1e-8):
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

        in_neutron = self.create_in_neutron(reaction.vecteur, file.energy, 1e-8, axes)

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
        self.add(in_neutron)
        self.play(*neutranim)
        self.remove(silicium, in_neutron)
        self.add(*starting_spheres, *gammas)
        self.play(*animations)

    def animation_0(self):
        self.play(FadeOut(VGroup(*self.mobjects)))
        self.move_camera(phi=0,theta=0)
        text = Text("interaction_muon_silicium")
        self.play(Create(text))

    def animation_1(self):
        self.play(FadeOut(VGroup(*self.mobjects)))
        reaction = self.files[0].get_reac()
        axes = ThreeDAxes(
            x_range=(-1, 1, 0.2),
            y_range=(-1, 1, 0.2),
            z_range=(-1, 1, 0.2),

        )
        self.play(Create(axes))
        self.play_collision(self.files,axes,reaction)

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))

        except AttributeError:
            print('special key {0} pressed'.format(key))
            if key == key.page_up:
                if not(self.animation_played):
                    print(self.playing_animation)
                    if self.playing_animation > 0:
                        self.playing_animation -= 1
                        eval(f"self.animation_{self.playing_animation}()")
            if key == key.page_down:
                if not(self.animation_played):
                    self.playing_animation += 1
                    print(self.playing_animation)
                    try:
                        print(f"self.animation_{self.playing_animation}()")
                        eval(f"self.animation_{self.playing_animation}()")
                    except Exception as e:
                        print(e)
                        return False
        self.animation_played = True


    def on_release(self, key):
        print('{0} released'.format(key))
        self.animation_played = False
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    def construct(self):
        liste = os.listdir("Secondaries_zips")
        liste = ["Secondaries_zips/" + i for i in liste if "txt" in i][27:29]
        print(liste)

        self.files = parser.open_multiple_files(liste)

        self.playing_animation = 0
        self.animation_played = False
        self.animation_0()

        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


        

        
        

        sphere1 = Sphere(
            center = (0.5,0.5,0.5),
            resolution=(16,16)
        )

        """

        self.renderer.camera.light_source.move_to((5,5,5)) # changes the source of the light
        self.play(Create(sphere1))

        text = Text("").to_corner(UL)

        self.add_fixed_in_frame_mobjects(text)

        text.text = "Silicium"

        self.play(Create(text))



        
        point = axes.coords_to_point(files[0].galette[0][0], files[0].galette[0][1], files[0].galette[0][2])

        
        self.wait(3)
        dot = Sphere(
            center=point,
            radius=0.1,
            resolution=(8,8)
        )


        self.play(TransformMatchingShapes(sphere1, dot), Create(axes))     

        
        sphere_group = VGroup([Sphere(
            center=axes.coords_to_point(i[0], i[1], i[2]),
            radius=0.1, 
            color = BLUE,
            resolution=(4,4)
        ).set_color(BLUE) for i in tqdm(files[0].galette[:30])])
        self.play(Create(sphere_group))
        self.remove(sphere1, dot)


        self.move_camera(phi = 75 * DEGREES, theta = (30-180) * DEGREES)
        """
        self.interactive_embed()





