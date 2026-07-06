# The Computer Language Benchmarks Game
# https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
#
# Naive transliteration from Michael Ferguson's Chapel program
from math import sqrt
import sys 

PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

class Body:
    def __init__(self, x, y, z, vx, vy, vz, mass):
        self.x = x
        self.y = y 
        self.z = z    
        self.vx = vx
        self.vy = vy 
        self.vz = vz  
        self.mass = mass   
    
def nbody(n):
    bodies = [
        # sun
        Body(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, SOLAR_MASS),
        # jupiter
        Body(4.84143144246472090e+00, -1.16032004402742839e+00, -1.03622044471123109e-01, 
             1.66007664274403694e-03 * DAYS_PER_YEAR, 7.69901118419740425e-03 * DAYS_PER_YEAR, 
             -6.90460016972063023e-05 * DAYS_PER_YEAR, 9.54791938424326609e-04 * SOLAR_MASS),
        # saturn
        Body(8.34336671824457987e+00, 4.12479856412430479e+00, -4.03523417114321381e-01,      
             -2.76742510726862411e-03 * DAYS_PER_YEAR, 4.99852801234917238e-03 * DAYS_PER_YEAR, 
             2.30417297573763929e-05 * DAYS_PER_YEAR, 2.85885980666130812e-04 * SOLAR_MASS),    
        # uranus
        Body(1.28943695621391310e+01, -1.51111514016986312e+01, -2.23307578892655734e-01,
             2.96460137564761618e-03 * DAYS_PER_YEAR, 2.37847173959480950e-03 * DAYS_PER_YEAR, 
             -2.96589568540237556e-05 * DAYS_PER_YEAR, 4.36624404335156298e-05 * SOLAR_MASS),    
        # neptune
        Body(1.53796971148509165e+01, -2.59193146099879641e+01, 1.79258772950371181e-01,    
             2.68067772490389322e-03 * DAYS_PER_YEAR, 1.62824170038242295e-03 * DAYS_PER_YEAR, 
             -9.51592254519715870e-05 * DAYS_PER_YEAR, 5.15138902046611451e-05 * SOLAR_MASS)
    ]

    # G19: inline offset_momentum calculation
    px, py, pz = 0.0, 0.0, 0.0
    for b in bodies:
        px += b.vx * b.mass
        py += b.vy * b.mass
        pz += b.vz * b.mass
    bodies[0].vx = - px / SOLAR_MASS
    bodies[0].vy = - py / SOLAR_MASS
    bodies[0].vz = - pz / SOLAR_MASS

    # G19: inline initial energy calculation
    e = 0.0  
    num_bodies = len(bodies)  
    for i in range(num_bodies):  
        b = bodies[i]
        e += 0.5 * b.mass * (b.vx * b.vx + b.vy * b.vy + b.vz * b.vz)
        for j in range(i+1, num_bodies):  
            bj = bodies[j]
            dx, dy, dz = b.x - bj.x, b.y - bj.y, b.z - bj.z
            e -= (b.mass * bj.mass) / sqrt(dx*dx + dy*dy + dz*dz)
    print("%.9f" % e)

    dt = 0.01
    for _ in range(n):
        # G19: inlining the 'advance' function logic
        for i in range(num_bodies): 
            bi = bodies[i]
            for j in range(i+1, num_bodies):   
                bj = bodies[j]
                dx, dy, dz = bi.x - bj.x, bi.y - bj.y, bi.z - bj.z
                dpos_norm_sq = dx*dx + dy*dy + dz*dz  
                mag = dt / (dpos_norm_sq * sqrt(dpos_norm_sq)) 
                
                mj_mag = bj.mass * mag
                bi.vx -= dx * mj_mag
                bi.vy -= dy * mj_mag 
                bi.vz -= dz * mj_mag 
                
                mi_mag = bi.mass * mag
                bj.vx += dx * mi_mag
                bj.vy += dy * mi_mag 
                bj.vz += dz * mi_mag            
        
        for b in bodies:
            b.x += b.vx * dt
            b.y += b.vy * dt
            b.z += b.vz * dt

    # G19: inline final energy calculation
    e = 0.0  
    for i in range(num_bodies):  
        b = bodies[i]
        e += 0.5 * b.mass * (b.vx * b.vx + b.vy * b.vy + b.vz * b.vz)
        for j in range(i+1, num_bodies):  
            bj = bodies[j]
            dx, dy, dz = b.x - bj.x, b.y - bj.y, b.z - bj.z
            e -= (b.mass * bj.mass) / sqrt(dx*dx + dy*dy + dz*dz)
    print("%.9f" % e)

if __name__ == '__main__':
    nbody(int(sys.argv[1]))