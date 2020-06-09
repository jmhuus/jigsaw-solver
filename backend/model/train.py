import tensorflow as tf
from tensorflow import keras
import numpy as pd
from PIL import Image, ImageDraw
from puzzle import Puzzle



def main():
    # Init background image
    im = Image.new('RGB', (500, 500), (255, 255, 255))

    puzzle = Puzzle(
        puzzle_size=(8,8),
        starting_location=(30,30),
        piece_size=(75,75),
        image_object=im,
        piece_padding=35
    )
    puzzle.draw_puzzle("test.jpg", debugging=True)
    
    # Retrieve model data
    model_data = []
    piece1 = puzzle.grid[4][4]
    for i in range(10):
        print("before:", piece1.get_shape_data()[i])
        print("after:", piece1.get_normalized_shape_data(puzzle.piece_padding)[i])
        print()
    # for row in range(len(puzzle.grid)):
    #     for column in range(len(puzzle.grid[row])):
    #         piece = puzzle.grid[row][column]

    
    # # Convert model data into numpy array for Tensorflow
    # numpy_model_data = np.asarray(model_data)

    # # Build the model structure
    # model = keras.Sequential([
    #     keras.layers.Flatten(input_shape=(28, 28)),
    #     keras.layers.Dense(units=300, activation=tf.nn.relu),
    #     keras.layers.Dense(units=200, activation=tf.nn.relu),
    #     keras.layers.Dense(units=100, activation=tf.nn.relu),
    #     keras.layers.Dense(units=75, activation=tf.nn.relu),
    #     keras.layers.Dense(units=2, activation=tf.nn.softmax)
    # ])

    # # Compiile the model
    # model.compile(
    #     optimizer=keras.optimizers.Adam(),
    #     loss="sparse_categorical_crossentropy",
    #     metrics=["accuracy"]
    # )

    # # Train the model
    # mode.fit(train_data, train_labels, epochs=10)
    
        

if __name__ == "__main__":
    main()
