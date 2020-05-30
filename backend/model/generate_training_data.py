from PIL import Image, ImageDraw
import math


# line(x1, y1, x2, y2)
def draw_triangle_bump(draw_obj, start, size, direction):
    # Calculate 
    
    """Draws a symmetric triangle-like bump on a vertical line."""
    draw_obj.line((start[0], start[1], start[0]+size[0], start[1]+size[1]), fill=(0, 0, 0), width=1)
    draw_obj.line((start[0]+size[0], start[1]+size[1], start[0], start[1]+(2*size[1])), fill=(0, 0, 0), width=1)

    return (start[0], start[1]+(2*size[1]))


def draw_line(start, size, direction, image_object):
    # Init lines to draw
    draw = ImageDraw.Draw(image_object)
    
    # Calculate X, Y coordinates based on direction and size
    opposite = math.sin(math.radians(direction)) * size
    adjacent = math.cos(math.radians(direction)) * size

    # Draw the line using coordinates
    draw.line((start[0], start[1], start[0]+adjacent, start[1]+opposite), fill=(0, 0, 0), width=1)

    return (start[0]+adjacent, start[1]+opposite)


def draw_puzzle_side(starting_location, image_object):
    # Init lines to draw
    draw = ImageDraw.Draw(image_object)
    
    # Draw line
    last_location = draw_line(starting_location, 20, 90, image_object)
    
    # Draw an arc
    for angle in range(0, 92, 2):
        last_location = draw_line(last_location, 1, angle, image_object)
    for angle in range(90, 182, 2):
        last_location = draw_line(last_location, 1, angle, image_object)

    # Draw Line
    last_location = draw_line(last_location, 20, 90, image_object)

    return last_location


def draw_puzzle_piece(starting_location, image_object):
    # Draw top line
    last_location = draw_line(starting_location, 100, 0, image_object)
    
    # Draw matching side
    last_location = draw_puzzle_side(last_location, image_object)

    # Draw bottom and left side
    last_location = draw_line(last_location, 100, 180, image_object)
    last_location = draw_line(last_location, 100, 270, image_object)

    return last_location


def main():
    # Init background image
    im = Image.new('RGB', (500, 300), (255, 255, 255))

    opending_location = draw_puzzle_piece((100, 100), im)
    
    # Save the image
    im.save("test.jpeg")


main()
