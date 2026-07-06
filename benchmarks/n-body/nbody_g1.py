# The Computer Language Benchmarks Game
# https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
#
# Naive transliteration from Michael Ferguson's Chapel program
# contributed by Isaac Gouy

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
    
def offset_momentum(bodies):
  px, py, pz = 0.0, 0.0, 0.0
  for b in bodies:
    # G1: use a local variable 'm' for the repeated mass access
    m = b.mass
    px += b.vx * m
    py += b.vy * m
    pz += b.vz * m
    
  b = bodies[0]
  b.vx = - px / SOLAR_MASS
  b.vy = - py / SOLAR_MASS
  b.vz = - pz / SOLAR_MASS
        
def energy(bodies):
  e = 0.0  
  num_bodies = len(bodies)  
  for i in range(num_bodies):  
    b = bodies[i]
    # G1: assign mass to a variable
    b_mass = b.mass
    sq = b.vx * b.vx + b.vy * b.vy + b.vz * b.vz  
    e += 0.5 * b_mass * sq
    for j in range(i+1, num_bodies):  
      bj = bodies[j]
      dx = b.x - bj.x 
      dy = b.y - bj.y 
      dz = b.z - bj.z   
      sq = dx * dx + dy * dy + dz * dz 
      # G1: reuse the b_mass variable and store bj.mass locally
      bj_mass = bj.mass
      e -= (b_mass * bj_mass) / sqrt(sq)   
  return e    
    
def advance(bodies, dt):
  num_bodies = len(bodies)
  for i in range(num_bodies): 
    b_i = bodies[i] # G1: store current body to avoid repeated list indexing
    for j in range(i+1, num_bodies):   
      b_j = bodies[j] # G1: store target body
      dx = b_i.x - b_j.x 
      dy = b_i.y - b_j.y 
      dz = b_i.z - b_j.z       
      dpos_norm_sq = dx**2 + dy**2 + dz**2  
      mag = dt / (dpos_norm_sq * sqrt(dpos_norm_sq)) 
      
      # G1: assign 'mass * mag' to variables, avoid re-calculation
      mj_mag = b_j.mass * mag
      mi_mag = b_i.mass * mag
      
      b_i.vx -= dx * mj_mag
      b_i.vy -= dy * mj_mag 
      b_i.vz -= dz * mj_mag 
      
      b_j.vx += dx * mi_mag
      b_j.vy += dy * mi_mag 
      b_j.vz += dz * mi_mag            
      
  for i in range(num_bodies): 
    b = bodies[i] # G1: repeated use of the same body index
    b.x += b.vx * dt  
    b.y += b.vy * dt   
    b.z += b.vz * dt  
   
def nbody(n):
  bodies = [
    # sun
    Body(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, SOLAR_MASS),
    
    # jupiter
    Body(
      4.84143144246472090e+00,
      -1.16032004402742839e+00,
      -1.03622044471123109e-01,
      1.66007664274403694e-03 * DAYS_PER_YEAR,
      7.69901118419740425e-03 * DAYS_PER_YEAR,
      -6.90460016972063023e-05 * DAYS_PER_YEAR,
      9.54791938424326609e-04 * SOLAR_MASS
      ),
    
    # saturn
    Body(
      8.34336671824457987e+00,
      4.12479856412430479e+00,
      -4.03523417114321381e-01,      
      -2.76742510726862411e-03 * DAYS_PER_YEAR,
      4.99852801234917238e-03 * DAYS_PER_YEAR,
      2.30417297573763929e-05 * DAYS_PER_YEAR,
      2.85885980666130812e-04 * SOLAR_MASS 
      ),    
    
    # uranus
    Body(
      1.28943695621391310e+01,
      -1.51111514016986312e+01,
      -2.23307578892655734e-01,
      2.96460137564761618e-03 * DAYS_PER_YEAR,
      2.37847173959480950e-03 * DAYS_PER_YEAR,
      -2.96589568540237556e-05 * DAYS_PER_YEAR,
      4.36624404335156298e-05 * SOLAR_MASS 
      ),    
    
    # neptune
    Body(
      1.53796971148509165e+01,
      -2.59193146099879641e+01,
      1.79258772950371181e-01,    
      2.68067772490389322e-03 * DAYS_PER_YEAR,
      1.62824170038242295e-03 * DAYS_PER_YEAR,
      -9.51592254519715870e-05 * DAYS_PER_YEAR,
      5.15138902046611451e-05 * SOLAR_MASS 
      )
    ]    
   
  offset_momentum(bodies)   
  print("%.9f" % energy(bodies))   
  for i in range(n):
    advance(bodies, 0.01)
  print("%.9f" % energy(bodies)) 
   
def main(n):
  nbody(n)

if __name__ == '__main__':
  main(int(sys.argv[1]))