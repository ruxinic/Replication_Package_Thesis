import ctypes
import math
import os
import sys

PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

class Body(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_double), ("y", ctypes.c_double), ("z", ctypes.c_double),
        ("vx", ctypes.c_double), ("vy", ctypes.c_double), ("vz", ctypes.c_double),
        ("mass", ctypes.c_double)
    ]

lib_path = os.path.abspath("./nbody_lib.so")
_lib = ctypes.CDLL(lib_path)

_lib.advance.argtypes = [
    ctypes.POINTER(Body),
    ctypes.c_int,
    ctypes.c_double,
    ctypes.c_int
]
_lib.advance.restype = None


def offset_momentum(bodies, num_bodies):
    px, py, pz = 0.0, 0.0, 0.0
    for i in range(num_bodies):
        px += bodies[i].vx * bodies[i].mass
        py += bodies[i].vy * bodies[i].mass
        pz += bodies[i].vz * bodies[i].mass
        
    bodies[0].vx = -px / SOLAR_MASS
    bodies[0].vy = -py / SOLAR_MASS
    bodies[0].vz = -pz / SOLAR_MASS


def energy(bodies, num_bodies):
    e = 0.0  
    for i in range(num_bodies):  
        b = bodies[i]
        sq = b.vx * b.vx + b.vy * b.vy + b.vz * b.vz  
        e += 0.5 * b.mass * sq
        for j in range(i + 1, num_bodies):  
            dx = b.x - bodies[j].x 
            dy = b.y - bodies[j].y 
            dz = b.z - bodies[j].z   
            sq = dx * dx + dy * dy + dz * dz 
            e -= (b.mass * bodies[j].mass) / math.sqrt(sq)   
    return e    


def nbody(n):
    raw_data = [
        # sun
        Body(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, SOLAR_MASS),
        # jupiter
        Body(
            4.84143144246472090e+00, -1.16032004402742839e+00, -1.03622044471123109e-01,
            1.66007664274403694e-03 * DAYS_PER_YEAR, 7.69901118419740425e-03 * DAYS_PER_YEAR,
            -6.90460016972063023e-05 * DAYS_PER_YEAR, 9.54791938424326609e-04 * SOLAR_MASS
        ),
        # saturn
        Body(
            8.34336671824457987e+00, 4.12479856412430479e+00, -4.03523417114321381e-01,      
            -2.76742510726862411e-03 * DAYS_PER_YEAR, 4.99852801234917238e-03 * DAYS_PER_YEAR,
            2.30417297573763929e-05 * DAYS_PER_YEAR, 2.85885980666130812e-04 * SOLAR_MASS 
        ),    
        # uranus
        Body(
            1.28943695621391310e+01, -1.51111514016986312e+01, -2.23307578892655734e-01,
            2.96460137564761618e-03 * DAYS_PER_YEAR, 2.37847173959480950e-03 * DAYS_PER_YEAR,
            -2.96589568540237556e-05 * DAYS_PER_YEAR, 4.36624404335156298e-05 * SOLAR_MASS 
        ),    
        # neptune
        Body(
            1.53796971148509165e+01, -2.59193146099879641e+01, 1.79258772950371181e-01,    
            2.68067772490389322e-03 * DAYS_PER_YEAR, 1.62824170038242295e-03 * DAYS_PER_YEAR,
            -9.51592254519715870e-05 * DAYS_PER_YEAR, 5.15138902046611451e-05 * SOLAR_MASS 
        )
    ]
    
    num_bodies = len(raw_data)
    # Instantiate a contiguous array allocation block
    bodies = (Body * num_bodies)(*raw_data)
       
    offset_momentum(bodies, num_bodies)   
    print(f"{energy(bodies, num_bodies):.9f}")
    
    # Delegate all 'n' loop cycles straight down to C at once
    _lib.advance(bodies, num_bodies, 0.01, n)
    
    print(f"{energy(bodies, num_bodies):.9f}") 
    

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    nbody(n)


if __name__ == '__main__':
    main()