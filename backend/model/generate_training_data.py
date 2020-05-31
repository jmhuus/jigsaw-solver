from PIL import Image, ImageDraw
import math


class Piece:

    pieces_count = 0

    def __init__(self, location, piece_size, initiating_piece, incoming_side, side_data, image_object):

        
        Piece.pieces_count += 1

        connected_pieces = []

        # Side data
        self.right_side = (location[0]+piece_size[0], location[1], location[0]+piece_size[0], location[1]+piece_size[1])
        self.left_side = (location[0], location[1], location[0], location[1]+piece_size[1])
        self.bottom_side = (location[0], location[1]+piece_size[1], location[0]+piece_size[0], location[1]+piece_size[1])
        self.top_side = (location[0], location[1], location[0]+piece_size[0], location[1])

        self.piece_size = piece_size
        self.image_object = image_object
        if initiating_piece is not None:
            connected_pieces.append(initiating_piece)

        # Any piece created AFTER the original will initialize with a jagged line
        if incoming_side is not None:
            if incoming_side == "left":
                self.right_side = side_data
            elif incoming_side == "right":
                self.left_side = side_data
            elif incoming_side == "bottom":
                self.top_side = side_data
            elif incoming_side == "top":
                self.bottom_side = side_data
            else:
                raise Exception()

    def add_side(self, side):
        # Create a new jagged puzzle line for the side
        if side == "left":
            self.left_side = self.create_random_line(Piece.VERTICAL)
            new_side_data = self.left_side
        elif side == "right":
            self.right_side = self.create_random_line(Piece.VERTICAL)
            new_side_data = self.right_side
        elif side == "bottom":
            self.bottom_side = self.create_random_line(Piece.HORIZONTAL)
            new_side_data = self.bottom_side
        elif side == "top":
            self.top_side = self.create_random_line(Piece.HORIZONTAL)
            new_side_data = self.top_side
        else:
            raise Exception()

        # Initialize a new puzzle piece
        # self.connected_pieces.append(new Piece(self, side, new_side_data))

    def create_random_line(last_location, orientation):
        # Draw random line based on this pieces current location
        if orientation == Piece.HORIZONTAL:
            angle = 0
        elif orientation == Piece.VERTICAL:
            angle = 90
        else:
            raise Exception()

        # Draw line
        last_location = draw_line(starting_location, 20, 90)

        # Draw an arc
        for angle in range(0, 92, 2):
            last_location = draw_line(last_location, 1, angle)
        for angle in range(90, 182, 2):
            last_location = draw_line(last_location, 1, angle)

        # Draw Line
        last_location = draw_line(last_location, 20, 90)

        return last_location

    def draw(self):
        draw = ImageDraw.Draw(self.image_object)
        for side in [self.left_side, self.right_side, self.top_side, self.bottom_side]:
            draw.line(side, fill=(0,0,0,0), width=2)


# line(x1, y1, x2, y2)
def draw_triangle_bump(draw_obj, start, size, direction):
    # Calculate

    """Draws a symmetric triangle-like bump on a vertical line."""
    draw_obj.line((start[0], start[1], start[0]+size[0], start[1]+size[1]), fill=(0, 0, 0), width=1)
    draw_obj.line((start[0]+size[0], start[1]+size[1], start[0], start[1]+(2*size[1])), fill=(0, 0, 0), width=1)

    return (start[0], start[1]+(2*size[1]))


def draw_line(start, random, size, direction, image_object):
    # Init lines to draw
    draw = ImageDraw.Draw(image_object)

    # Calculate X, Y coordinates based on direction and size
    opposite = math.sin(math.radians(direction)) * size
    adjacent = math.cos(math.radians(direction)) * size

    # Draw the line using coordinates
    draw.line((start[0], start[1], start[0]+adjacent, start[1]+opposite), fill=(0, 0, 0), width=1)

    return (start[0]+adjacent, start[1]+opposite)


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

    first_piece = Piece((100, 100), (50, 50), None, None, None, im)
    first_piece.draw()

    # Save the image
    im.save("test.jpeg")


main()
