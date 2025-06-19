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

MASSES = {
    "proton" : 	1.67262192595e-27,
    "neutron" : 1.67492750056e-27,
    "pi-" : 139.57018 * eV * (c**2),
    "pi+" : 139.57018 * eV * (c**2),
    "pi0" : 134.9766 * eV * (c**2),
    "alpha": 6.644657230e-27,
}
MASSES["He6"] = 2*MASSES["proton"] + 4*MASSES["neutron"]
MASSES["Si28"] = 14 * MASSES["proton"] + (28-14)*MASSES["neutron"]
MASSES["Si29"] = 14 * MASSES["proton"] + (29-14)*MASSES["neutron"]
MASSES["Si27"] = 14 * MASSES["proton"] + (27-14)*MASSES["neutron"]
MASSES["Al27"] = 13 * MASSES["proton"] + (27-13)*MASSES["neutron"]


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
    def create_product(self, sub_product: parser.Sub_product, starting_point):
        if sub_product.name != "gamma":
            


    def construct(self):
        liste = os.listdir("Secondaries_zips")
        liste = ["Secondaries_zips/" + i for i in liste if "txt" in i][13:16]
        files = parser.open_multiple_files(liste)
        
        self.create_product(files[0].content[0].sub_products[0], "")

        

        self.move_camera(phi = 75 * DEGREES, theta = 30 * DEGREES)
        axes = ThreeDAxes(
            x_range=(-1, 1, 0.2),
            y_range=(-1, 1, 0.2),
            z_range=(-1, 1, 0.2),

        )
        sphere1 = Sphere(
            center = (0.5,0.5,0.5),
            resolution=(16,16)
        )



        self.renderer.camera.light_source.move_to((5,5,5)) # changes the source of the light
        self.play(Create(sphere1))

        text = Text("").to_corner(UL)

        self.add_fixed_in_frame_mobjects(text)

        text.text = "Silicium"

        self.play(Create(text))



        """
        point = axes.coords_to_point(files[0].galette[0][0], files[0].galette[0][1], files[0].galette[0][2])

        
        self.wait(3)
        dot = Sphere(
            center=point,
            radius=0.1,
            resolution=(8,8)
        )


        self.play(TransformMatchingShapes(sphere1, dot), Create(axes))     

        
        sphere_temp = [Create(Sphere(
            center=axes.coords_to_point(i[0], i[1], i[2]),
            radius=0.1, 
            color = BLUE,
            resolution=(2,2)
        ).set_color(BLUE)) for i in tqdm(files[0].galette[:500])]
        self.play(*sphere_temp)
        self.remove(sphere1, dot)


        self.move_camera(phi = 75 * DEGREES, theta = (30-180) * DEGREES)
        """
        self.wait(3)
        self.interactive_embed()





