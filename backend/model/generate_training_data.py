from PIL import Image, ImageDraw
import math
import random
import copy



class Piece:

    pieces_count = 0
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"


    def __init__(self, location, piece_size):

        # Count each piece added
        Piece.pieces_count += 1

        self.connected_pieces = []
        self.piece_id = Piece.pieces_count
        self.piece_size = piece_size
        self.location = location
        self.center_location = (location[0]+(self.piece_size[0]/2), location[1]+(self.piece_size[1]/2))

        # Default sides are straight lines
        self.right_side = [(location[0]+piece_size[0], location[1], location[0]+piece_size[0], location[1]+piece_size[1])]
        self.left_side = [(location[0], location[1], location[0], location[1]+piece_size[1])]
        self.bottom_side = [(location[0], location[1]+piece_size[1], location[0]+piece_size[0], location[1]+piece_size[1])]
        self.top_side = [(location[0], location[1], location[0]+piece_size[0], location[1])]

        # Default side data
        self.default_right_side = [(location[0]+piece_size[0], location[1], location[0]+piece_size[0], location[1]+piece_size[1])]
        self.default_left_side = [(location[0], location[1], location[0], location[1]+piece_size[1])]
        self.default_bottom_side = [(location[0], location[1]+piece_size[1], location[0]+piece_size[0], location[1]+piece_size[1])]
        self.default_top_side = [(location[0], location[1], location[0]+piece_size[0], location[1])]
        

    def set_side(self, side_obj, side, padding_size):
        # Reset the provided side and ensure location matches self
        if side == Piece.TOP:
            self.top_side = Piece.move_shape(side_obj, padding_size, 90)
        elif side == Piece.BOTTOM:
            self.bottom_side = Piece.move_shape(side_obj, padding_size, 270)
        elif side == Piece.LEFT:
            self.left_side = Piece.move_shape(side_obj, padding_size, 360)
        elif side == Piece.RIGHT:
            self.right_side = Piece.move_shape(side_obj, padding_size, 180)
        else:
            raise Exception()
        
    def connect(self, connecting_piece, side, padding_size):
        # Add an adjacent piece based on the provided side
        if side == Piece.TOP:
            self.set_random_side_coordinates((self.default_top_side[0][0], self.default_top_side[0][1]), self.piece_size, Piece.TOP)
            connecting_piece.set_side(copy.deepcopy(self.top_side), Piece.BOTTOM, padding_size)
        elif side == Piece.BOTTOM:
            self.set_random_side_coordinates((self.default_bottom_side[0][0], self.default_bottom_side[0][1]), self.piece_size, Piece.BOTTOM)
            connecting_piece.set_side(copy.deepcopy(self.bottom_side), Piece.TOP, padding_size)
        elif side == Piece.LEFT:
            self.set_random_side_coordinates((self.default_left_side[0][0], self.default_left_side[0][1]), self.piece_size, Piece.LEFT)
            connecting_piece.set_side(copy.deepcopy(self.left_side), Piece.RIGHT, padding_size)
        elif side == Piece.RIGHT:
            self.set_random_side_coordinates((self.default_right_side[0][0], self.default_right_side[0][1]), self.piece_size, Piece.RIGHT)
            connecting_piece.set_side(copy.deepcopy(self.right_side), Piece.LEFT, padding_size)
        else:
            raise Exception()

    def set_random_side_coordinates(self, starting_location, size, side):
        # Generate new jagged line
        if random.random() >= 0.5:
            new_side = self.get_random_arc_coordinates(starting_location, size, side)
        else:
            new_side = self.get_random_angle_coordinates(starting_location, size, side)

        # Set own piece side with newly generated jagged line
        if side == Piece.TOP:
            self.top_side = new_side
        elif side == Piece.BOTTOM:
            self.bottom_side = new_side
        elif side == Piece.LEFT:
            self.left_side = new_side
        elif side == Piece.RIGHT:
            self.right_side = new_side

    def get_random_arc_coordinates(self, starting_location, size, side):
        new_lines = []
        min_arc_size = 0.2
        max_arc_size = 0.5
        arc_increment_size = (random.random()*(max_arc_size-min_arc_size)) + min_arc_size
        diameter = (arc_increment_size * 180) / math.pi

        # Draw random line based on this piece's current location
        if side == Piece.TOP:
            line_direction = 0
            arc_starting_angle = 270
            line_size = (size[1]-diameter)/2
        elif side == Piece.BOTTOM:
            starting_location = Piece.move_point(starting_location, self.piece_size[1], 0)
            line_direction = 180
            arc_starting_angle = 90
            line_size = (size[1]-diameter)/2
        elif side == Piece.RIGHT:
            line_direction = 90
            arc_starting_angle = 0
            line_size = (size[1]-diameter)/2
        elif side == Piece.LEFT:
            starting_location = Piece.move_point(starting_location, self.piece_size[0], 90)
            line_direction = 270
            arc_starting_angle = 180
            line_size = (size[0]-diameter)/2
        else:
            raise Exception()

        # Draw line
        last_line = self.get_line_coordinates(starting_location, line_size, line_direction)
        new_lines.append(last_line)

        # Draw arc
        if random.random() >= 0.5:
            for a in range(arc_starting_angle, arc_starting_angle+90, 2):
                last_line = self.get_line_coordinates(last_line, arc_increment_size, a)
                new_lines.append(last_line)
            for a in range(arc_starting_angle+91, arc_starting_angle+182, 2):
                last_line = self.get_line_coordinates(last_line, arc_increment_size, a)
                new_lines.append(last_line)
        else:
            arc_starting_angle += 540
            for a in range(arc_starting_angle, arc_starting_angle-90, -2):
                last_line = self.get_line_coordinates(last_line, arc_increment_size, a)
                new_lines.append(last_line)
            for a in range(arc_starting_angle-91, arc_starting_angle-182, -2):
                last_line = self.get_line_coordinates(last_line, arc_increment_size, a)
                new_lines.append(last_line)
        
        # Draw Line
        last_line = self.get_line_coordinates(last_line, line_size, line_direction)
        new_lines.append(last_line)

        return new_lines

    def get_random_angle_coordinates(self, starting_location, size, side):
        new_lines = []
        min_angle_size = 10
        max_angle_size = 25
        angle_size = (random.random()*(max_angle_size-min_angle_size)) + min_angle_size
        min_angle_direction = 20
        max_angle_direction = 75
        angle_direction = (random.random()*(max_angle_direction-min_angle_direction)) + min_angle_direction
        angle_length = (math.cos(math.radians(angle_direction)) * angle_size) * 2

        # Draw random line based on this piece's current location
        if side == Piece.TOP:
            line_direction = 360
            line_size = (size[1]-angle_length)/2
        elif side == Piece.BOTTOM:
            starting_location = Piece.move_point(starting_location, self.piece_size[1], 0)
            line_direction = 540
            line_size = (size[1]-angle_length)/2
        elif side == Piece.RIGHT:
            line_direction = 450
            line_size = (size[1]-angle_length)/2
        elif side == Piece.LEFT:
            starting_location = Piece.move_point(starting_location, self.piece_size[0], 90)
            line_direction = 630
            line_size = (size[0]-angle_length)/2
        else:
            raise Exception()

        # Draw line
        last_line = self.get_line_coordinates(starting_location, line_size, line_direction)
        new_lines.append(last_line)

        # Draw angle
        last_line = self.get_line_coordinates(last_line, angle_size, line_direction+angle_direction)
        new_lines.append(last_line)
        last_line = self.get_line_coordinates(last_line, angle_size, line_direction-angle_direction)
        new_lines.append(last_line)
        
        # Draw Line
        last_line = self.get_line_coordinates(last_line, line_size, line_direction)
        new_lines.append(last_line)

        return new_lines

    def get_line_coordinates(self, start, size, direction):
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

    def draw(self, image_object):
        draw = ImageDraw.Draw(image_object)
        for side in [self.left_side, self.right_side, self.top_side, self.bottom_side]:
            for line in side:
                draw.line(line, fill=(0,0,0,0), width=2)

        # self.center_location

    Def rotate_piece(self, angle):
        self.top_side = Piece.rotate_shape(self.top_side, self.location, angle)
        self.right_side = Piece.rotate_shape(self.right_side, self.location, angle)
        self.bottom_side = Piece.rotate_shape(self.bottom_side, self.location, angle)
        self.left_side = Piece.rotate_shape(self.left_side, self.location, angle)
        
    @classmethod
    def rotate_shape(Piece, shape_coordinates, rotation_axis, angle):
        new_shape = []
        for line in shape_coordinates:
            # Calculate each point, relative to the rotation ax`is
            delta_x1 = line[0]-rotation_axis[0]
            delta_y1 = line[1]-rotation_axis[1]
            delta_x2 = line[3]-rotation_axis[0]
            delta_y2 = line[3]-rotation_axis[1]
            
            # First line point
            offset_x1 = math.cos(math.radians(angle)) * delta_x1
            offset_y1 = math.sin(math.radians(angle)) * delta_y1
            
            # Second line point
            offset_x2 = math.cos(math.radians(angle)) * delta_x2
            offset_y2 = math.sin(math.radians(angle)) * delta_y2
            
            new_line = (line[0]+offset_x1, line[1]+offset_y1, line[2]+offset_x2, line[3]+offset_y2)
            new_shape.append(new_line)
        return new_shape
    
    @classmethod
    def move_shape(Piece, shape_coordinates, size, direction):
        # Calculate x, y shift based on direction and size
        opposite = math.sin(math.radians(direction)) * size
        adjacent = math.cos(math.radians(direction)) * size

        new_lines = []
        for line in shape_coordinates:
            new_lines.append((line[0]+adjacent, line[1]+opposite, line[2]+adjacent, line[3]+opposite))

        return new_lines

    @classmethod
    def move_line(Piece, line_coordinates, size, direction):
        # Calculate x, y shift based on direction and size
        opposite = math.sin(math.radians(direction)) * size
        adjacent = math.cos(math.radians(direction)) * size

        return (line_coordinates[0]+adjacent, line_coordinates[1]+opposite, line_coordinates[2]+adjacent, line_coordinates[3]+opposite)

    @classmethod
    def move_point(Piece, point_coordinates, size, direction):
        # Calculate x, y shift based on direction and size
        opposite = math.sin(math.radians(direction)) * size
        adjacent = math.cos(math.radians(direction)) * size

        return (point_coordinates[0]+adjacent, point_coordinates[1]+opposite)

class Puzzle:
    def __init__(self, puzzle_size, starting_location, piece_size, image_object, piece_padding):
        self.puzzle_size = puzzle_size
        self.starting_location = starting_location
        self.piece_size = piece_size
        self.image_object = image_object
        self.piece_padding = piece_padding
        self.grid = []

        # Initiate the puzzle and it's pieces
        # Connect each piece horizontally
        piece_location = [self.starting_location[0], self.starting_location[1]]
        for row in range(self.puzzle_size[0]):
            
            # Create subsequent columns
            new_row = []
            previous_piece = None
            piece_location[0] = self.starting_location[1]
            for column in range(self.puzzle_size[1]):
                current_piece = Piece(piece_location, self.piece_size)
                piece_location[0] += (self.piece_size[0] + self.piece_padding)  # Move right
                
                if previous_piece is not None:
                    previous_piece.connect(current_piece, Piece.RIGHT, self.piece_padding)
                
                new_row.append(current_piece)
                previous_piece = current_piece

            piece_location[1] += (self.piece_size[1] + self.piece_padding)  # Move down

            # Append the row to the grid
            self.grid.append(new_row)

        # Connect each piece vertically
        for row in range(1, len(self.grid)):
            for column in range(len(self.grid[0])):
                self.grid[row-1][column].connect(self.grid[row][column], Piece.BOTTOM, self.piece_padding)

    def draw_puzzle(self, visited=None, debugging=False):
        for row in range(len(self.grid)):
            for column in range(len(self.grid[0])):
                self.grid[row][column].draw(self.image_object)
        

def main():
    # Init background image
    im = Image.new('RGB', (500, 300), (255, 255, 255))

    puzzle = Puzzle((3,6), (100,100), (50,50), im, 15)
    puzzle.draw_puzzle()
    
    # Save the image
    im.save("test.jpeg")


if __name__ == "__main__":
    main()
