from PIL import Image, ImageDraw
import math


class Piece:

    pieces_count = 0
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"


    def __init__(self, location, piece_size, initiating_piece, incoming_side, side_data, image_object):


        Piece.pieces_count += 1

        self.connected_pieces = []

        # Side data
        self.right_side = [(location[0]+piece_size[0], location[1], location[0]+piece_size[0], location[1]+piece_size[1])]
        self.left_side = [(location[0], location[1], location[0], location[1]+piece_size[1])]
        self.bottom_side = [(location[0], location[1]+piece_size[1], location[0]+piece_size[0], location[1]+piece_size[1])]
        self.top_side = [(location[0], location[1], location[0]+piece_size[0], location[1])]

        self.piece_size = piece_size
        self.image_object = image_object
        self.location = location
        if initiating_piece is not None:
            self.connected_pieces.append(initiating_piece)

        # Any piece created AFTER the original piece will initialize with a jagged line
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
            self.left_side = self.create_random_line_coordinates((self.left_side[0][0], self.left_side[0][1]), self.piece_size, Piece.LEFT)
            new_piece_side_data = Piece.move_shape(self.left_side, 50, 90)
            new_side_data = self.left_side
        elif side == "right":
            self.right_side = self.create_random_line_coordinates((self.right_side[0][0], self.right_side[0][1]), self.piece_size, Piece.RIGHT)
            new_piece_side_data = Piece.move_shape(self.right_side, 50, 90)
            new_side_data = self.right_side
        elif side == "bottom":
            self.bottom_side = self.create_random_line_coordinates((self.bottom_side[0][0], self.bottom_side[0][1]), self.piece_size, Piece.BOTTOM)
            new_piece_side_data = Piece.move_shape(self.bottom_side, 50, 90)
            new_side_data = self.bottom_side
        elif side == "top":
            self.top_side = self.create_random_line_coordinates((self.top_side[0][0], self.top_side[0][1]), self.piece_size, Piece.TOP)
            new_piece_side_data = Piece.move_shape(self.top_side, 50, 90)
            new_side_data = self.top_side
        else:
            raise Exception()

        # Initialize a new puzzle piece
        # TODO(jordanhuus): dynamically arrange connected pieces based on 'side' variable
        new_piece_location = (self.location[0], self.location[1]+self.piece_size[0]+50)
        self.connected_pieces.append(Piece(new_piece_location, self.piece_size, self, side, new_piece_side_data, self.image_object))

    def create_random_line_coordinates(self, starting_location, size, side):
        new_lines = []

        arc_increment_size = 0.5
        diameter = (arc_increment_size * 180) / math.pi

        # Draw random line based on this piece's current location
        if side == Piece.TOP:
            line_angle = 0
            arc_starting_angle = 270
            line_size = (size[1]-diameter)/2
        elif side == Piece.BOTTOM:
            line_angle = 0
            arc_starting_angle = 90
            line_size = (size[1]-diameter)/2
        elif side == Piece.RIGHT:
            line_angle = 0
            arc_starting_angle = 0
            line_size = (size[1]-diameter)/2
        elif side == Piece.LEFT:
            line_angle = 90
            arc_starting_angle = 180
            line_size = (size[0]-diameter)/2
        else:
            raise Exception()

        # Draw line
        last_line = self.create_line_coordinates(starting_location, line_size, line_angle)
        new_lines.append(last_line)

        # Draw arc; LEFT and BOTTOM sides will draw in opposite directions than RIGHT and TOP
        if side == Piece.BOTTOM or side == Piece.LEFT:
            # Draw an arc
            for a in range(arc_starting_angle, (arc_starting_angle-90) % 360, -2):
                last_line = self.create_line_coordinates(last_line, 0.5, a)
                new_lines.append(last_line)
            for a in range((arc_starting_angle-91) % 360, (arc_starting_angle-182) % 360, -2):
                last_line = self.create_line_coordinates(last_line, 0.5, a)
                new_lines.append(last_line)
        else:
            # Draw an arc
            for a in range(arc_starting_angle, (arc_starting_angle+92) % 360, 2):
                last_line = self.create_line_coordinates(last_line, 0.5, a)
                new_lines.append(last_line)
            for a in range((arc_starting_angle+90) % 360, (arc_starting_angle+182) % 360, 2):
                last_line = self.create_line_coordinates(last_line, 0.5, a)
                new_lines.append(last_line)

        # Draw Line
        last_line = self.create_line_coordinates(last_line, line_size, line_angle)
        new_lines.append(last_line)

        return new_lines

    def create_line_coordinates(self, start, size, direction):
        # Determine if the starting location is a line or simple x, y coordinates
        if len(start) == 2:  # simple x, y coordinates
            start_x = start[0]
            start_y = start[1]
        elif len(start) == 4:  # contains line; x1, y1, x2, y2
            start_x = start[2]
            start_y = start[3]
        else:
            raise Exception("param: start contains incorrect number of tuple values.")

        # Calculate X, Y coordinates based on direction and size
        opposite = math.sin(math.radians(direction)) * size
        adjacent = math.cos(math.radians(direction)) * size

        # Return coordinates for the newly created line; x1, y1, x2, y2
        return (start_x, start_y, start_x+adjacent, start_y+opposite)

    def draw(self):
        draw = ImageDraw.Draw(self.image_object)
        for side in [self.left_side, self.right_side, self.top_side, self.bottom_side]:
            for line in side:
                draw.line(line, fill=(0,0,0,0), width=2)

    @classmethod
    def move_shape(Piece, shape_coordinates, size, direction):
        # Calculate x, y shift based on direction and size
        opposite = math.sin(math.radians(direction)) * size
        adjacent = math.cos(math.radians(direction)) * size

        new_lines = []
        for line in shape_coordinates:
            new_lines.append((line[0]+adjacent, line[1]+opposite, line[2]+adjacent, line[3]+opposite))

        return new_lines


def main():
    # Init background image
    im = Image.new('RGB', (500, 300), (255, 255, 255))

    first_piece = Piece((100, 100), (50, 50), None, None, None, im)
    first_piece.add_side("bottom")
    first_piece.draw()

    # Draw each connected piece
    for piece in first_piece.connected_pieces:
        piece.draw()

    
    # Save the image
    im.save("test.jpeg")


main()
