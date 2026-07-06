#include <math.h>

typedef struct {
    double x, y, z;
    double vx, vy, vz;
    double mass;
} Body;

// push the heavy simulation clock steps entirely into pure binary assembly
void advance(Body* bodies, int num_bodies, double dt, int steps) {
    for (int step = 0; step < steps; step++) {
        for (int i = 0; i < num_bodies; i++) {
            for (int j = i + 1; j < num_bodies; j++) {
                double dx = bodies[i].x - bodies[j].x;
                double dy = bodies[i].y - bodies[j].y;
                double dz = bodies[i].z - bodies[j].z;

                double dpos_norm_sq = dx*dx + dy*dy + dz*dz;
                double mag = dt / (dpos_norm_sq * sqrt(dpos_norm_sq));

                double mj = bodies[j].mass * mag;
                bodies[i].vx -= dx * mj;
                bodies[i].vy -= dy * mj;
                bodies[i].vz -= dz * mj;

                double mi = bodies[i].mass * mag;
                bodies[j].vx += dx * mi;
                bodies[j].vy += dy * mi;
                bodies[j].vz += dz * mi;
            }
        }

        for (int i = 0; i < num_bodies; i++) {
            bodies[i].x += bodies[i].vx * dt;
            bodies[i].y += bodies[i].vy * dt;
            bodies[i].z += bodies[i].vz * dt;
        }
    }
}