# src/tessif/frused/utils.py
"""Tessif (random) utility collection."""


def greyscale2hex(greyscale, minn=0.0, maxn=1.0):
    """Correlate a number within a certain range to a hex encoded gray value.

    Parameters
    ----------
    greyscale: ~numbers.Number
        Number between :paramref:`minn` and :paramref:`maxn` representing the
        greyscale. Where :paramref:`minn` =  ``'white'`` and
        :paramref:`maxn` = ``'black'``.
    minn: ~number.Number, default=0.0
        Lower boundary resulting in a white color hex value
    maxn: ~number.Number, default=1.0
        Upper boundary resulting in a black color hex value

    Returns
    -------
    hex
        single hex color value representing the correlated grayscale color.

    Examples
    --------
    >>> greyscale2hex(.3)
    '#b2b2b2'
    >>> greyscale2hex(.7)
    '#4c4c4c'
    >>> greyscale2hex(50, 0, 100)
    '#7f7f7f'
    >>> greyscale2hex(1e10, 0, 1e20)
    '#fefefe'
    >>> greyscale2hex(0)
    '#ffffff'
    >>> greyscale2hex(1)
    '#000000'
    >>> greyscale2hex(0.0)
    '#ffffff'
    >>> greyscale2hex(1.0)
    '#000000'
    """
    greyscale = _clamp(greyscale, minn, maxn)
    rgb_int = int((maxn - greyscale) / maxn * 255)
    return f"#{rgb_int:02x}{rgb_int:02x}{rgb_int:02x}"


def _clamp(number, minn, maxn):
    """Clamp number to be within [minn, maxn]."""
    return max(min(maxn, number), minn)
