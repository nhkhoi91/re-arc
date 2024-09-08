from dsl import *
from utils import *

def generate_cardinality_1(diff_lb=0, diff_ub=1) -> dict:
    """

    Input: matrix of random sizes and colors
    Output: (1, 1) matrix with color of higest frequency
    """

    dim_bounds = (3, 30)
    colopts = interval(ZERO, TEN, ONE)

    # Generate random grid dimensions
    h = unifint(diff_lb, diff_ub, dim_bounds)
    w = unifint(diff_lb, diff_ub, dim_bounds)
    total_pixels = h * w
    # Create the initial canvas with a background color
    bgc = choice(colopts)
    c = canvas(bgc, (h, w))

    # Generate random foreground colors
    num_colors = unifint(diff_lb, diff_ub, (2, min(7, total_pixels)))
    fgcols = sample(remove(bgc, colopts), num_colors)

    # Calculate the range for foreground color pixels
    min_fg_pixels = max(1, total_pixels // (2 * num_colors))
    max_fg_pixels = max(min_fg_pixels, total_pixels // num_colors)

    # Place foreground colors
    remaining_pixels = total_pixels
    inds = totuple(asindices(c))
    for i, fgcol in enumerate(fgcols):
        if i == len(fgcols) - 1:  # Last color
            num_pixels = remaining_pixels
        else:
            lower_bound = min(min_fg_pixels, remaining_pixels)
            upper_bound = min(max_fg_pixels, remaining_pixels)
            num_pixels = unifint(diff_lb, diff_ub, (lower_bound, upper_bound))
        s = sample(inds, num_pixels)
        c = fill(c, fgcol, s)
        inds = difference(inds, s)
        remaining_pixels -= num_pixels

    # Count occurrences of each color
    color_counts = {color: colorcount(c, color) for color in palette(c)}

    # Find the most common color
    max_color = argmax(color_counts.keys(), lambda x: color_counts[x])

    # Generate the output grid
    go = canvas(max_color, (ONE, ONE))

    return {'input': c, 'output': go}


def generate_cardinality_2(diff_lb=0, diff_ub=1) -> dict:
    """
    Input: matrix of random sizes and colors
    Output: (1, 1) matrix with color of lowest frequency
    """
    
    dim_bounds = (3, 30)
    colopts = interval(ZERO, TEN, ONE)
    
    h = unifint(diff_lb, diff_ub, dim_bounds)
    w = unifint(diff_lb, diff_ub, dim_bounds)
    total_pixels = h * w
    
    bgc = choice(colopts)
    c = canvas(bgc, (h, w))

    num_colors = unifint(diff_lb, diff_ub, (2, min(7, total_pixels)))
    fgcols = sample(remove(bgc, colopts), num_colors)

    min_fg_pixels = max(1, total_pixels // (2 * num_colors))
    max_fg_pixels = max(min_fg_pixels, total_pixels // num_colors)

    remaining_pixels = total_pixels
    inds = totuple(asindices(c))
    for i, fgcol in enumerate(fgcols):
        if i == len(fgcols) - 1:  # Last color
            num_pixels = remaining_pixels
        else:
            lower_bound = min(min_fg_pixels, remaining_pixels)
            upper_bound = min(max_fg_pixels, remaining_pixels)
            num_pixels = unifint(diff_lb, diff_ub, (lower_bound, upper_bound))
        s = sample(inds, num_pixels)
        c = fill(c, fgcol, s)
        inds = difference(inds, s)
        remaining_pixels -= num_pixels

    min_color = leastcolor(c)
    go = canvan(min_color, (ONE, ONE))

    return {'input': c, 'output': go}

def generate_cardinality_3(diff_lb=0, diff_ub=1) -> dict:
    dim_bounds = (3, 30)
    colopts = interval(ZERO, TEN, ONE)

    h = unifint(diff_lb, diff_ub, dim_bounds)
    w = unifint(diff_lb, diff_ub, dim_bounds)
    total_pixels = h * w

    bgc = choice(colopts)
    c = canvas(bgc, (h, w))
    inds = totuple(asindices(c))

    num_colors = unifint(diff_lb, diff_ub, (2, min(7, total_pixels)))
    fgcols = sample(remove(bgc, colopts), num_colors)

    remaining_pixels = total_pixels
    color_pixels = {}

    for i, fgol in enumerate(fgcols):
        min_fg_pixels = 1
        max_fg_pixels = remaining_pixels - sum(range(1, len(fgcols) - i))
        num_pixels = unifint(diff_lb, diff_ub, (min_fg_pixels, max_fg_pixels))

        s = sample(inds, num_pixels)
        c = fill(c, fgol, s)
        inds = difference(inds, s)
        remaining_pixels -= num_pixels
        color_pixels[fgol] = num_pixels

    color_pixels[bgc] = remaining_pixels

    print(f'pixels: {color_pixels}')
    # Output grid
    color_freq = list(color_pixels.items())
    sorted_colors = [color for color, _ in sorted(color_freq, key=lambda x: x[1])]
    go = canvas(sorted_colors[0], (ONE, num_colors+1))

    for i, color in enumerate(sorted_colors):
        print(f'color: {color}')
        print(f'position: {i}')
        go = fill(go, color, {(0, i)})
    return {'input': c, 'output': go}


def generate_cardinality_4(diff_lb=0, diff_ub=1) -> dict:
    """
    - Input: A grid of random size with random pixel colors.
      0 represents the background (uncolored), while 1-9 represent colored pixels.
    - Output: A 2x2 grid representing the parity of the colored pixel count without background color (0):
      - Blue (1) for odd count
      - Red (2) for even count
    """
    dim_bounds = (3, 30)
    colopts = interval(ZERO, TEN, ONE)

    h = unifint(diff_lb, diff_ub, dim_bounds)
    w = unifint(diff_lb, diff_ub, dim_bounds)
    total_pixels = h * w

    bgc = ZERO
    c = canvas(bgc, (h, w))
    inds = totuple(asindices(c))

    num_colors = unifint(diff_lb, diff_ub, (2, min(4, total_pixels)))
    fgcols = sample(remove(bgc, colopts), num_colors)
    remaining_pixels = total_pixels / 2
    total_color_pixel = 0

    for i, fgol in enumerate(fgcols):
        min_fg_pixels = 1
        max_fg_pixels = remaining_pixels - sum(range(1, len(fgcols) - i))
        num_pixels = unifint(diff_lb, diff_ub, (min_fg_pixels, max_fg_pixels))

        s = sample(inds, num_pixels)
        c = fill(c, fgol, s)
        inds = difference(inds, s)
        remaining_pixels -= num_pixels
        total_color_pixel += num_pixels

    # Output grid
    if total_color_pixel % 2 == 1:
        go = canvas(ONE, (ONE, ONE))
    else:
        go = canvas(TWO, (ONE, ONE))

    return {'input': c, 'output': go}


def generate_cardinality_5(diff_lb=0, diff_ub=1) -> dict:
    """
    Find object that appears exactly 5 times
    Output: 
    Input: A grid of random size with random pixel colors, 
    with 1 color appears exactly 5 times
    Output: 1x1 matrix with the color
    """

    n_times=5

    dim_bounds = (3, 30)
    colopts = interval(ZERO, TEN, ONE)
    total_pixels = 0
    
    while total_pixels < n_times:
        h = unifint(diff_lb, diff_ub, dim_bounds)
        w = unifint(diff_lb, diff_ub, dim_bounds)
        total_pixels = h * w

    bgc = ZERO
    c = canvas(bgc, (h, w))
    inds = totuple(asindices(c))

    num_colors = unifint(diff_lb, diff_ub, (2, min(4, total_pixels)))
    fgcols = sample(remove(bgc, colopts), num_colors)
    remaining_pixels = total_pixels - n_times
    
    chosen_color = sample(fgcols, 1)
    s = sample(inds, n_times)
    c = fill(c, chosen_color[0], s)
    inds = difference(inds, s)
    remaining_pixels -= n_times

    fgcols = remove(chosen_color[0], fgcols)

    for i, fgol in enumerate(fgcols):
        min_fg_pixels = 1
        max_fg_pixels = remaining_pixels
        num_pixels = n_times
        while num_pixels == n_times:
            num_pixels = unifint(diff_lb, diff_ub, (min_fg_pixels, max_fg_pixels))

        s = sample(inds, num_pixels)
        c = fill(c, fgol, s)
        inds = difference(inds, s)
        remaining_pixels -= num_pixels

    # Output grid
    go = canvas(chosen_color[0], (ONE, ONE))
    
    return {'input': c, 'output': go}


def generate_cardinality_6(diff_lb=0, diff_ub=1) -> dict:
    """
    Find color of object that form a 2x2 square
    Input: A grid of random size with random pixel colors, one color forms a 2x2 square
    Output: 1x1 matrix with the color
    """
    dim_bounds = (3, 30)
    colopts = interval(ZERO, TEN, ONE)
    total_pixels = 0

    while total_pixels < SIX:  # Minimum 4 pixels for a 2x2 square
        h = unifint(diff_lb, diff_ub, dim_bounds)
        w = unifint(diff_lb, diff_ub, dim_bounds)
        total_pixels = h * w

    bgc = ZERO
    c = canvas(bgc, (h, w))
    inds = totuple(asindices(c))

    num_colors = unifint(diff_lb, diff_ub, (2, min(7, total_pixels)))
    fgcols = sample(remove(bgc, colopts), num_colors)
    remaining_pixels = total_pixels

    pattern_color = sample(fgcols, 1)
    # Place 2x2 squares in the grid

    while True:
        i = unifint(0, 1, (ZERO, h - TWO))
        j = unifint(0, 1, (ZERO, w - TWO))
        square_inds = {(i, j), (i, j+ONE), (i+ONE, j), (i+ONE, j+ONE)}
        if all(ind in inds for ind in square_inds):
            c = fill(c, color, square_inds)
            print(f'square_inds: {square_inds}')
            inds = difference(inds, square_inds)
            remaining_pixels -= FOUR
            break

    all_colors = combine(remove(pattern_color[0], fgcols), [bgc] )
    sort_inds = order(inds, lambda x: x[0] * w + x[1])
    print(f'sort_inds: {sort_inds}')
    last_color = None
    for ind in sort_inds:
        valid_colors = difference(all_colors, last_color) if last_color else all_colors
        chosen_color = sample(valid_colors, 1)
        print(chosen_color)
        c = fill(c, chosen_color, ind)
        last_color = chosen_color

    # output grid
    go = canvas(pattern_color[0], (ONE, ONE))
    return {'input': c, 'output': go}


