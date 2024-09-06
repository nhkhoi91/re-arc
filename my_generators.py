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