#!/usr/bin/env python
"""Doesn't dereference on each iteration, goes faster!"""
import sys
import datetime

x1, x2, y1, y2 = -2.13, 0.77, -1.3, 1.3


def show(output):
    """Convert list to numpy array, show using PIL"""
    try:
        import Image
        # convert our output to PIL-compatible input
        import array
        output = ((o + (256*o) + (256**2)*o) * 8 for o in output)
        output = array.array('I', output)
        # display with PIL
        im = Image.new("RGB", (w/2, h/2))
        im.fromstring(output.tostring(), "raw", "RGBX", 0, -1)
        im.show()
    except ImportError as err:
        # Bail gracefully if we don't have PIL
        print "Couldn't import Image or numpy:", str(err)



@profile
def calculate_z_serial(q, maxiter, z):
    output = [0] * len(q)
    for i in range(len(q)):
        if i % 1000 == 0:
            # print out some progress info since it is so slow...
            print "%0.2f%% complete" % (1.0/len(q) * i * 100)
        for iteration in range(maxiter):
            z[i] = z[i]*z[i] + q[i]
            if abs(z[i]) > 2.0:
                output[i] = iteration
                break
    return output


def compute(show_output):
    x_step = (float(x2 - x1) / float(w)) * 2
    y_step = (float(y1 - y2) / float(h)) * 2
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step
    q = []
    for ycoord in y:
        for xcoord in x:
            q.append(complex(xcoord, ycoord))

    z = [0+0j] * len(q)
    print "Total elements:", len(z)
    start_time = datetime.datetime.now()
    output = calculate_z_serial(q, maxiter, z)
    end_time = datetime.datetime.now()
    secs = end_time - start_time
    print "Main took", secs

    validation_sum = sum(output)
    print "Total sum of elements (for validation):", validation_sum

    if show_output:
        show(output)

    return validation_sum


if __name__ == "__main__":
    # get width, height and max iterations from cmd line
    # 'python mandelbrot_pypy.py 1000 1000'
    if len(sys.argv) == 1:
        w = h = 300
        maxiter = 1000
    else:
        w = int(sys.argv[1])
        h = int(sys.argv[1])
        maxiter = int(sys.argv[2])

    # we can show_output for Python, not for PyPy
    validation_sum = compute(show_output=True)

    # confirm validation output for our known test case
    # we do this because we've seen some odd behaviour due to subtle student
    # bugs
    if w == 1000 and h == 1000 and maxiter == 1000:
        assert validation_sum == 1148485 # if False then we have a bug
