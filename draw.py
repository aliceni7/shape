from display import *
from matrix import *

  # ====================
  # add the points for a rectagular prism whose 
  # upper-left corner is (x, y, z) with width, 
  # height and depth dimensions.
  # ====================
def add_box( points, x, y, z, width, height, depth ):
    add_edge(points, x, y, z, x + width, y, z)
    add_edge(points, x, y, z, x, y - height, z)
    add_edge(points, x, y, z, x, y, z - depth)
    add_edge(points, x + width, y, z, x + width, y - height, z)
    add_edge(points, x + width, y, z, x + width, y, z - depth)
    add_edge(points, x + width, y - height, z, x + width, y - height, z - depth)
    add_edge(points, x, y - height, z, x + width, y - height, z)
    add_edge(points, x, y - height, z, x, y - height, z - depth)
    add_edge(points, x, y, z - depth, x + width, y, z - depth)
    add_edge(points, x, y, z - depth, x, y - height, z - depth)
    add_edge(points, x + width, y - height, z, x + width, y - height, z - depth)
    add_edge(points, x + width, y, z - depth, x + width, y - height, z - depth)
    add_edge(points, x, y - height, z - depth, x + width, y - height, z - depth)

  
def add_sphere( points, cx, cy, cz, r, step ):
    rot = 0
    while rot < 1.0:
        circ = 0
        while circ < 1.0:
            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2 * math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2 * math.pi * rot) + cz
            add_edge( points, x, y, z, x, y, z )
            circ = circ + step
        rot = rot + step



def add_torus( points, cx, cy, cz, r0, r1, step ):
    rot = 0
    while rot < 1.0:
        tor = 0
        while tor < 1.0:
            x = (r0 * math.cos(2 * math.pi * rot) + r1) * math.cos(2 * math.pi * tor) + cx
            y = r0 * math.sin(2 * math.pi * rot) + cy
            z = -1 * math.sin(2 * math.pi * tor) * (r0 * math.cos(2 * math.pi * rot) + r1) + cz
            add_edge( points, x, y, z, x, y, z )
            tor = tor + step
        rot = rot + step


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy

    i = 1
    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    cx = generate_curve_coefs( x0, x1, x2, x3, curve_type )
    cy = generate_curve_coefs( y0, y1, y2, y3, curve_type )
    x = x0
    y = y0
    t = 0.0
    while (t <= 1.0):
        add_point( points, x, y, 0 )
        x = cx[0][0] * t ** 3 + cx[0][1] * t ** 2 + cx[0][2] * t + cx[0][3]
        y = cy[0][0] * t ** 3 + cy[0][1] * t ** 2 + cy[0][2] * t + cy[0][3]
        t = t + step


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
