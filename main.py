import vpython as vp
import numpy as np
import typing

class Time:
    def __init__(self, step:float):
        self.value = 0
        self.step = step

    def update(self): self.value += self.step

class Axis:

    def __init__(self, axis:typing.Tuple[float, float, float], label:str):
        axis = vp.vec(*axis)
        self.arrow = vp.arrow(pos=vp.vec(0,0,0), axis=axis, color=vp.color.white, shaftwidth=0.02, round=False)
        self.text = vp.text(text=label, pos=axis, align="center", height=0.15, billboard=False)

class Spin:

    def __init__(self, time:Time):
        self.state = vp.vec(0,0,1)
        self.angular_speed = np.array([0,0,0]) 
        self.time = time
        self.arrow = vp.arrow(pos=vp.vec(0,0,0), axis=self.state, shaftwidth=0.05, color=vp.color.green)

    def _redraw(self):
        self.arrow.axis.x = self.state.y
        self.arrow.axis.y = self.state.z
        self.arrow.axis.z = self.state.x

    def rotate_x(self):
        self.angular_speed[0] = 1
    
    def rotate_y(self):
        self.angular_speed[1] = 1
    
    def rotate_z(self):
        self.angular_speed[2] = 1

    def stop_rotating(self):
        self.angular_speed[:] = 0

    def update(self):
        # thetas = self.angular_speed*self.time.step
        # Rx = np.array([[1,                0,                 0],
        #                [0,np.cos(thetas[0]),-np.sin(thetas[0])],
        #                [0,np.sin(thetas[0]), np.cos(thetas[0])]])
        
        # new_state = Rx*self.angular_speed
        # self.state.x = new_state

        self.state.rotate_in_place(self.angular_speed[0]*self.time.step, vp.vec(1,0,0))
        self.state.rotate_in_place(self.angular_speed[1]*self.time.step, vp.vec(0,1,0))
        self.state.rotate_in_place(self.angular_speed[2]*self.time.step, vp.vec(0,0,1))
        self._redraw()

class KeyDown:

    bindings = {}

    def bind(key:str, func, args=()):
        KeyDown.bindings[key] = (func, args)
        vp.scene.bind("keydown", KeyDown._call)
    
    def _call(ev):
        if ev.key in KeyDown.bindings:
            entry = KeyDown.bindings[ev.key]
            if len(entry[1]) == 0: entry[0]()
            else: entry[0](*[entry[1]])

def main():
    
    s = vp.sphere(opacity=0.2, radius=1, emissive=False)
    up_label   = vp.text(text="|0>", align="center", height=0.2, pos=vp.vec(0,1+0.3,0))
    down_label = vp.text(text="|1>", align="center", height=0.2, pos=vp.vec(0,-1-0.2-0.3,0))

    x_arrow = Axis((0,0,1), "x")
    y_arrow = Axis((1,0,0), "y")
    z_arrow = Axis((0,1,0), "z")

    time = Time(0.1)
    qubit = Spin(time)

    KeyDown.bind("a", qubit.rotate_x)
    KeyDown.bind("w", qubit.rotate_y)
    KeyDown.bind("d", qubit.rotate_z)
    KeyDown.bind("s", qubit.stop_rotating)

    while True:
        vp.rate(24)
        time.update()
        qubit.update()

if __name__ == "__main__": main()