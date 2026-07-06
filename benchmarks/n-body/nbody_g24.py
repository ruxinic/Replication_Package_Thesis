import sys
import numpy as np

PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

# G24: use NumPy to handle data in bulk for better performance
# store the data in a single array: [x, y, z, vx, vy, vz, mass]
def offset_momentum(bodies):
    # calculate total momentum: sum(mass * velocity)
    momentum = np.sum(bodies[:, 3:6] * bodies[:, 6:], axis=0)
    # offset the Sun's (index 0) velocity
    bodies[0, 3:6] = -momentum / SOLAR_MASS

def energy(bodies):
    # G24: vectorized kinetic energy calculation: 0.5 * m * v^2
    ke = 0.5 * np.sum(bodies[:, 6] * np.sum(bodies[:, 3:6]**2, axis=1))
    
    pe = 0.0
    # G24: use NumPy for distance calculations
    for i in range(len(bodies)):
        m_i = bodies[i, 6]
        pos_i = bodies[i, 0:3]
        for j in range(i + 1, len(bodies)):
            dist = np.linalg.norm(pos_i - bodies[j, 0:3])
            pe -= (m_i * bodies[j, 6]) / dist
    return ke + pe

def advance(bodies, dt):
    # G24: replace manual loops with vectorized coordinate and velocity updates
    n = len(bodies)
    for i in range(n):
        m_i = bodies[i, 6]
        pos_i = bodies[i, 0:3]
        for j in range(i + 1, n):
            d_pos = pos_i - bodies[j, 0:3]
            dist_sq = np.sum(d_pos**2)
            mag = dt / (dist_sq * np.sqrt(dist_sq))
            
            # update velocities using vectorized array slicing
            bodies[i, 3:6] -= d_pos * (bodies[j, 6] * mag)
            bodies[j, 3:6] += d_pos * (m_i * mag)

    # G24: bulk update of all positions at once
    bodies[:, 0:3] += bodies[:, 3:6] * dt

def nbody(n):
    # G24: represent bodies as a NumPy matrix instead of a list of class instances
    bodies = np.array([
        # Sun
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, SOLAR_MASS],
        # Jupiter
        [4.84143144246472090e+00, -1.16032004402742839e+00, -1.03622044471123109e-01, 
         1.66007664274403694e-03 * DAYS_PER_YEAR, 7.69901118419740425e-03 * DAYS_PER_YEAR, 
         -6.90460016972063023e-05 * DAYS_PER_YEAR, 9.54791938424326609e-04 * SOLAR_MASS],
        # Saturn
        [8.34336671824457987e+00, 4.12479856412430479e+00, -4.03523417114321381e-01,      
         -2.76742510726862411e-03 * DAYS_PER_YEAR, 4.99852801234917238e-03 * DAYS_PER_YEAR, 
         2.30417297573763929e-05 * DAYS_PER_YEAR, 2.85885980666130812e-04 * SOLAR_MASS],
        # Uranus
        [1.28943695621391310e+01, -1.51111514016986312e+01, -2.23307578892655734e-01,
         2.96460137564761618e-03 * DAYS_PER_YEAR, 2.37847173959480950e-03 * DAYS_PER_YEAR, 
         -2.96589568540237556e-05 * DAYS_PER_YEAR, 4.36624404335156298e-05 * SOLAR_MASS],
        # Neptune
        [1.53796971148509165e+01, -2.59193146099879641e+01, 1.79258772950371181e-01,    
         2.68067772490389322e-03 * DAYS_PER_YEAR, 1.62824170038242295e-03 * DAYS_PER_YEAR, 
         -9.51592254519715870e-05 * DAYS_PER_YEAR, 5.15138902046611451e-05 * SOLAR_MASS]
    ])

    offset_momentum(bodies)
    print("%.9f" % energy(bodies))
    for _ in range(n):
        advance(bodies, 0.01)
    print("%.9f" % energy(bodies))

if __name__ == '__main__':
    nbody(int(sys.argv[1]))