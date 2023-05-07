import dpnp as np

from mandelbrot_demo.impl.impl_numba_dpex import mandelbrot


def _test_numba_dpex():
    w = 2
    h = 2
    zoom = 1.0
    offsetx = 0.0
    offsety = 0.0
    colors = np.full((w, h, 3), 0, dtype=np.int32)

    c1 = np.asarray([0.0, 0.0, 0.2])
    c2 = np.asarray([1.0, 0.7, 0.9])
    c3 = np.asarray([0.6, 1.0, 0.2])
    colors = mandelbrot(c1, c2, c3, w, h, zoom, offsetx, offsety, colors)
    s = colors.astype(np.int32).sum()
    print("s=",s)
    print(s.device)
    assert np.asnumpy(s) == 1405

_test_numba_dpex()
