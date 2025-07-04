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
        if sub_product.name != "gamma":
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
        ending_point = axes.coords_to_point(starting_point + sub_product.vecteur * c * duration_time)[0]
        starting_sphere = Sphere(
            center=axes.coords_to_point(starting_point)[0],
            radius=r,
            resolution = (8, 8),
            stroke_width = np.array([0.1])
        ).set_color(parser.ATOMS[sub_product.name]["color"])
        starting_sphere.stroke_color = BLACK
        return starting_sphere, ending_point

    def create_in_neutron(self, collision_point, energy, duration_time, axes):
        v = np.sqrt(1 - (1/((energy/parser.ATOMS["neutron"]["mass"]) + 1))) * c
        r = parser.ATOMS["neutron"]["radius"] * 1.5
        starting_point = axes.coords_to_point(collision_point + np.array([0, 0, 1]) * v * duration_time)[0]
        print(starting_point)
        neutron = Sphere(
            center = starting_point,
            radius = r,
            resolution = (8,8),
            stroke_width = np.array([0.1])
        ).set_color(parser.ATOMS["neutron"]["color"])
        neutron.stroke_color = BLACK
        return neutron

    def construct(self):
        liste = os.listdir("Secondaries_zips")
        liste = ["Secondaries_zips/" + i for i in liste if "txt" in i][28:29]
        print(liste)
        files = parser.open_multiple_files(liste)
        
        axes = ThreeDAxes(
            x_range=(-1e6, 1e6, 0.2e6),
            y_range=(-1e6, 1e6, 0.2e6),
            z_range=(-1e6, 1e6, 0.2e6),

        )
        self.play(Create(axes))

        self.move_camera(phi = 75 * DEGREES, theta = 45 * DEGREES)
        spheres = [self.create_product(axes, i, files[0].content[1].vecteur, 5e-2) for i in files[0].content[1].sub_products]
        spheres = list(zip(*spheres))
        starting_spheres = VGroup(spheres[0])
        ending_points = np.array(spheres[1])
        animations = [starting_spheres[i].animate(run_time=1, rate_func=rate_functions.linear).move_to(ending_points[i]) for i in range(len(ending_points))]

        in_neutron = self.create_in_neutron(files[0].content[1].vecteur, files[0].energy, 5e-2, axes)

        si = files[0].content[0].reac[-1]
        print(si)
        silicium = Sphere(
            center = axes.coords_to_point(files[0].content[1].vecteur)[0],
            radius = parser.ATOMS[si]["radius"] * 1.5,
            resolution = (8, 8),
            stroke_width = np.array([0.1])
        ).set_color(parser.ATOMS[si]["color"])
        silicium.stroke_color = BLACK
        self.play(Create(silicium))
        group = VGroup([in_neutron])

        neutranim = [group[0].animate(run_time=1, rate_func=rate_functions.linear).move_to(axes.coords_to_point(files[0].content[0].vecteur)[0])]
        self.add(in_neutron)
        print(axes.coords_to_point(files[0].content[1].vecteur)[0])


        self.play(*neutranim)
        self.remove(silicium, in_neutron)
        self.add(*starting_spheres)
        self.play(*animations)


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





