import dpnp as np
import numpy
import numba_dpex as nb
import numba

from mandelbrot_demo.impl.settings import MAX_ITER

nb.config.THREADING_LAYER = "omp"


#@nb.dpjit(fastmath=True, nopython=True)
# def color_by_intensity(intensity, c1, c2, c3):
#     if intensity < 0.5:
#         return c3 * intensity + c2 * (1.0 - intensity)
#     else:
#         return c1 * intensity + c2 * (1.0 - intensity)


#@nb.dpjit(fastmath=True, nopython=True)
# def mandel(x, y):
#     c = complex(x, y)
#     z = 0.0j
#     for i in range(MAX_ITER):
#         z = z * z + c
#         if (z.real * z.real + z.imag * z.imag) > 4.0:
#             return i
#     return MAX_ITER


@nb.dpjit
def mandelbrot(c1, c2, c3, w, h, zoom, offsetx, offsety, values):
#    c1 = np.asarray([0.0, 0.0, 0.2])
#    c2 = np.asarray([1.0, 0.7, 0.9])
#    c3 = np.asarray([0.6, 1.0, 0.2])

    for x in numba.prange(w):
        for y in range(h):
            xx = (x - offsetx ) * zoom
            yy = (y - offsety ) * zoom
            cReal=xx
            cImage=yy
           # c = complex(xx, yy)
            #z = 0.0j
            zReal=0
            zImage=0
            mand=-1
            for i in range(MAX_ITER):
                zReal= zReal*zReal-zImage*zImage+cReal
                zImage=zReal*zImage*2+cImage
                #z = z * z + c
                if (zReal * zReal + zImage * zImage) > 4.0:
                    mand=i
                    break
            if mand == -1:
                mand = MAX_ITER 
            intensity = mand / MAX_ITER
            # intensity = mandel(xx, yy) / MAX_ITER
            for c in range(3):
                if intensity < 0.5:
                    color = c3[c] * intensity + c2[c]  * (1.0 - intensity)
                else:
                    color = c1[c]  * intensity + c2[c]  * (1.0 - intensity)
                # color = color_by_intensity(intensity, c1[c], c2[c], c3[c])
                color = int(color * 255.0)
                values[x, y, c] = color
    return values


def init_values(w, h):
    return np.full((w, h, 3), 0, dtype=numpy.int32)


def asnumpy(values):
    return np.asnumpy(values)
