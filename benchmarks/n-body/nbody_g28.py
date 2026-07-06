from array import array
from math import sqrt
import sys 

PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

class SystemArrays:
    # G28: aggregate isolated body fields into contiguous 
    # primitive data arrays

    def __init__(self, bodies_list):
        self.num_bodies = len(bodies_list)
        self.x = array('d', [b.x for b in bodies_list])
        self.y = array('d', [b.y for b in bodies_list])
        self.z = array('d', [b.z for b in bodies_list])
        self.vx = array('d', [b.vx for b in bodies_list])
        self.vy = array('d', [b.vy for b in bodies_list])
        self.vz = array('d', [b.vz for b in bodies_list])
        self.mass = array('d', [b.mass for b in bodies_list])
class Body:
    def __init__(self, x, y, z, vx, vy, vz, mass):
        self.x = x
        self.y = y 
        self.z = z    
        self.vx = vx
        self.vy = vy 
        self.vz = vz  
        self.mass = mass   
        
def offset_momentum(sys_arr):
    # G28: localize array references to the local execution stack
    vx, vy, vz, mass = sys_arr.vx, sys_arr.vy, sys_arr.vz, sys_arr.mass
    px, py, pz = 0.0, 0.0, 0.0
    
    for i in range(sys_arr.num_bodies):
        m = mass[i]
        px += vx[i] * m
        py += vy[i] * m
        pz += vz[i] * m
        
    vx[0] = -px / SOLAR_MASS
    vy[0] = -py / SOLAR_MASS
    vz[0] = -pz / SOLAR_MASS
        
def energy(sys_arr):
    e = 0.0  
    num_bodies = sys_arr.num_bodies
    # G28: direct local binding to skip object wrapper lookups
    x, y, z = sys_arr.x, sys_arr.y, sys_arr.z
    vx, vy, vz, mass = sys_arr.vx, sys_arr.vy, sys_arr.vz, sys_arr.mass
    
    for i in range(num_bodies):  
        vxi, vyi, vzi, mi = vx[i], vy[i], vz[i], mass[i]
        e += 0.5 * mi * (vxi * vxi + vyi * vyi + vzi * vzi)
        xi, yi, zi = x[i], y[i], z[i]
        
        for j in range(i + 1, num_bodies):  
            dx = xi - x[j]
            dy = yi - y[j]
            dz = zi - z[j]   
            sq = dx * dx + dy * dy + dz * dz 
            e -= (mi * mass[j]) / sqrt(sq)   
    return e    
    
def advance(sys_arr, dt):
    num_bodies = sys_arr.num_bodies
    # G28: extract array blocks onto local stack names
    x, y, z = sys_arr.x, sys_arr.y, sys_arr.z
    vx, vy, vz, mass = sys_arr.vx, sys_arr.vy, sys_arr.vz, sys_arr.mass
    
    for i in range(num_bodies): 
        xi, yi, zi = x[i], y[i], z[i]
        vxi, vyi, vzi, mi = vx[i], vy[i], vz[i], mass[i]
        
        for j in range(i + 1, num_bodies):   
            dx = xi - x[j]
            dy = yi - y[j]
            dz = zi - z[j]       
            dpos_norm_sq = dx * dx + dy * dy + dz * dz  
            mag = dt / (dpos_norm_sq * sqrt(dpos_norm_sq)) 
            
            mj_mag = mass[j] * mag
            vxi -= dx * mj_mag  
            vyi -= dy * mj_mag   
            vzi -= dz * mj_mag 
            
            mi_mag = mi * mag      
            vx[j] += dx * mi_mag  
            vy[j] += dy * mi_mag   
            vz[j] += dz * mi_mag        
            
        # write back calculated velocity adjustments
        vx[i], vy[i], vz[i] = vxi, vyi, vzi
        
    # update coordinates sequentially
    for i in range(num_bodies): 
        x[i] += vx[i] * dt  
        y[i] += vy[i] * dt   
        z[i] += vz[i] * dt  
   
def nbody(n):
    bodies_list = [
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
   
    # transform list into aggregated data container
    sys_arr = SystemArrays(bodies_list)
    
    offset_momentum(sys_arr)   
    print("%.9f" % energy(sys_arr))   
    for _ in range(n):
        advance(sys_arr, 0.01)
    print("%.9f" % energy(sys_arr)) 
   
def main(n):
    nbody(n)

if __name__ == '__main__':
    main(int(sys.argv[1]))