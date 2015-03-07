import numpy as np
import time
from matplotlib import pylab as plt
import random

def run():
    # Initialize grid
    size = 100
    dims = 2
    # Each point in the 2D grid can hold the counts of: [prey,predators]
    grid = np.zeros((size,) * dims, dtype=(int, 2))
    num_rows, num_cols, identifiers = grid.shape

    num_predators = 10
    num_prey = 500
    prey_countdown = 500
    grid[50, 50, 1] = num_predators  # Manually inserting a few predators/prey
    grid[0, 0, 0] = num_prey

    # Coordinates for all non-empty grid locations
    coords = np.transpose(np.nonzero(grid != 0))
    x_pts, y_pts, idents = zip(*coords)

    # Please do not consider matplotlib the choke point of this program,
    # It will be commented out, and is only used for testing and amusement.
    # (But if you do have a way to speed it up, I'm very curious!)

    # Initialize figure and axes
    fig, ax1 = plt.subplots(1)
    # Cosmetics
    ax1.set_aspect('equal')
    ax1.set_xlim(0, size)
    ax1.set_ylim(0, size)
    # Display
    ax1.hold(True)
    plt.show(False)
    plt.draw()
    # Background is not to be redrawn each loop
    background = fig.canvas.copy_from_bbox(ax1.bbox)

    # Plot all initial positions as blue circles
    points = ax1.plot(x_pts, y_pts, 'bo')[0]

    # I would like to have blue for prey and red for predators,
    # I'm not sure how to do so quickly. I think multiple calls to axes.plot are needed.
    #colors = ['ro' if (ident==2) else 'bo' for ident in idents]

    time_steps = 1000
    for idx in range(time_steps):
        for coord in coords:
            direction = random.sample(range(1, 5), 1)[0]

            x, y, ident = coord
            count = grid[x, y, ident]

            # Random walk
            # Prey first
            if ident == 0:
                if count:  # A predator may have eaten the prey by now
                    grid[x, y, ident] -= 1  # Remove old value
                    if direction == 1:  # Move right
                        grid[(x+1) % num_rows, y, ident] += 1
                    elif direction == 2:  # Move left
                        grid[(x-1) % num_rows, y, ident] += 1
                    elif direction == 3:  # Move up
                        grid[x, (y+1) % num_cols, ident] += 1
                    elif direction == 4:  # Move down
                        grid[x, (y-1) % num_cols, ident] += 1
            # Predators do not die
            else:  # Predators will consume prey if prey exists at new location
                grid[x, y, ident] -= 1  # Remove old value
                if direction == 1:  # Move right
                    xnew = (x+1) % num_rows
                    grid[xnew, y, ident] += 1  # Move predator to new grid location
                    if grid[xnew, y, 0]:  # If there is prey at the new location...
                        grid[xnew, y, 0] -= 1  # Remove prey
                        prey_countdown -= 1
                        print 'Crunch! Prey left:', prey_countdown
                elif direction == 2:  # Move left
                    xnew = (x-1) % num_rows
                    grid[xnew, y, ident] += 1
                    if grid[xnew, y, 0]:
                        grid[xnew, y, 0] -= 1
                        prey_countdown -= 1
                        print 'Crunch! Prey left:', prey_countdown
                elif direction == 3:  # Move up
                    ynew = (y+1) % num_cols
                    grid[x, ynew, ident] += 1
                    if grid[x, ynew, 0]:
                        grid[x, ynew, 0] -= 1
                        prey_countdown -= 1
                        print 'Crunch! Prey left:', prey_countdown
                elif direction == 4:  # Move down
                    ynew = (y-1) % num_cols
                    grid[x, ynew % num_cols, ident] += 1
                    if grid[x, ynew, 0]:
                        grid[x, ynew, 0] -= 1
                        prey_countdown -= 1
                        print 'Crunch! Prey left:', prey_countdown

        # Redraw...
        coords = np.transpose(np.nonzero(grid != 0))
        x_pts, y_pts, idents = zip(*coords)
        points.set_data(x_pts, y_pts)
        fig.canvas.restore_region(background)  # Restore background
        ax1.draw_artist(points)  # Redraw just the points
        fig.canvas.blit(ax1.bbox)  # Fill in the axes rectangle

        time.sleep(0.01)  # Prevents figure from freezing

    plt.close(fig)

    # Do we have as many left as we should?
    coords = np.transpose(np.nonzero(grid[:,:,0] != 0))
    print (len(coords) != prey_countdown)

if __name__ == '__main__':
    run()  # Start button for cProfile