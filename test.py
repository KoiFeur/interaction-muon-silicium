from manim import *
config.renderer = "opengl"
#First index corresponds to the mass number. Second index corresponds to the atom's radius
atomsdict ={'H' : [1, 53e-12],
            'He': [3, 31e-12],
            'Li': [6, 167e-12],
            'Be': [9, 112e-12],
            'B' : [10, 87e-12],
            'Ce': [133, 298e-12]}
class Atom(ThreeDScene):
    def construct(self):
        self.move_camera(phi=45*DEGREES, theta=45*DEGREES)
        positionsdict = {}
        nuclear_radius_constant = 1.2e-15
        def CreateAtom(*atoms):
            distance = 0
            print(atoms)
            buffer = 1
            n = len(atoms)
            for i, key in enumerate(atoms):
                #Formula of the nuclear radius with a given mass number
                nuclearradius = nuclear_radius_constant * atomsdict.get(key)[0]**(1/3)
                shift_vec = RIGHT * distance  
                nucleus = Sphere(
                    radius = nuclearradius,
                    resolution = (16, 16),
                    stroke_width=0.001
                )
                nucleus.set_fill(RED, opacity=0.25)
                nucleus.scale(3.356e11)
                outer_shell = Sphere(radius = atomsdict.get(key)[1], resolution = 16).set_fill(PINK, opacity=0.25).shift(shift_vec).scale(3.356e11)


                self.add(nucleus, outer_shell)
                self.play(nucleus.animate(run_time=0.05).shift(shift_vec))
                                #Separate the next atom by the distance of the radius of the previus atom plus the radius of the next   
                positionsdict[key] = []
                positionsdict[key].extend([nucleus.get_center(), outer_shell.get_center()])


                if i < n - 1:
                    next_key = atoms[i + 1]
                    distance += (atomsdict.get(key)[1] + atomsdict.get(next_key)[1]) * 3.356e11 + buffer
        def ZoomToAtom(key):
            return self.play(self.camera.animate.move_to(positionsdict.get(key)[1]).set(width = atomsdict.get(key)[1] * 1.45e12))
        def ZoomToNucleus(key):
            return self.play(self.camera.animate.move_to(positionsdict.get(key)[0]).set(width = nuclear_radius_constant * atomsdict.get(key)[0]**(1/3) * 1.45e12))
        CreateAtom("Ce","Li","H")
        ZoomToNucleus("H")
        ZoomToNucleus("Li")
        self.interactive_embed()
