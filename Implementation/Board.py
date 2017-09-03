"""
This class is an amalgation of tiles, edges and vertices to represent the board. Don't ask how it works, 
no one knows.
"""

# local imports
from Implementation import Tile
from Implementation import Edge
from Implementation import Vertex


class Board:

    def __init__(self):
        self.tile_array = [
            [Tile.Tile() for _ in range(3)],
            [Tile.Tile() for _ in range(4)],
            [Tile.Tile() for _ in range(5)],
            [Tile.Tile() for _ in range(4)],
            [Tile.Tile() for _ in range(3)],
        ]

        self.connect_tiles()
        self.add_edges_and_vertices()

    def connect_tiles(self):
        for i, row in self.tile_array:
            for j, tile in row:
                if i <= 1:
                    # check if vaild coordinate
                    if self.is_valid_coordinate(i, j+1):
                        # connect tile to neighbor at 90degrees and connect neighbor back
                        tile.t2 = self.tile_array[i][j+1]
                        self.tile_array[i][j+1].t5 = tile
                    # connect tile to neigher at 150degree and connect neighbor back
                    tile.t3 = self.tile_array[i+1][j+1]
                    self.tile_array[i+1][j+1].t6 = tile
                    # connect tile to neighbor at 210degree and connect neighbor back
                    tile.t4 = self.tile_array[i+1][j]
                    self.tile_array[i+1][j].t1 = tile
                if i == 2:
                    # check if valid coordinate
                    if self.is_valid_coordinate(i, j+1):
                        # connect tile at 90degree and connect neighbor back
                        tile.t2 = self.tile_array[i][j+1]
                        self.tile_array[i][j+1].t5 = tile
                if i > 2:
                    # connect neighbor at -30degrees and connect neighbor back
                    tile.t6 = self.tile_array[i-1][j]
                    self.tile_array[i-1][j].t3 = tile
                    # connect neighbor at 30degrees and connect neighbor back
                    tile.t1 = self.tile_array[i-1][j+1]
                    self.tile_array[i-1][j+1].t4 = tile
                    # check if valid coordinate
                    if self.is_valid_coordinate(i, j+1):
                        # connect neighbor at 90 degrees and connect neighbor back
                        tile.t2 = self.tile_array[i][j+1]
                        self.tile_array[i][j+1].t5 = tile

    def add_edges_and_vertices(self):
        """
        Either pure gold or pure garbage. Not sure yet.
        Need to figure out how to set edge's tiles and vertex's tile, but this needs to sit
        for a day for me to think about my first statement.

        Instead of creating the edge first, instead grab the pointers together in an array as
        a batch, then iterate through array to initialize the pointers as a group to a single edge.

        e.g. if edge @ index in tile.edge_arr is nil, grab edge pointer at index of tile.edge_arr
        and place in temp_edge_arr
        Then grab the other corresponding edges of corresponding tiles in tile.tile_arr and use logic
        to iterate through temp_edge_arr and link to newly constructed edge.

        I didn't wanna modify the code yet seeing as I've yet to practice more with Python, and I'd
        like you to walk me through the logic of this code when you get a chance before making any
        modifications and possibly derping it up.
        """
        for row in self.tile_array:
            for tile in row:
                for index, edge in tile.edge_arr:
                    edge = Edge.Edge()
                    tile.vertex_arr[index % 6] = Vertex.Vertex()
                    if tile.tile_arr[index] is not None:
                        tile.tile_arr[index].edge_arr[(index + 3) % 6] = edge
                        if tile.tile_arr[index-1] is not None:
                            tile.tile_arr[index].vertex_arr[(index + 3) % 6] = tile.vertex_arr[index % 6]
                            tile.tile_arr[index].vertex_arr[(index + 2) % 6] = tile.vertex_arr[index % 6]

    def is_valid_coordinate(self, x, y):
        try:
            self.tile_array[x][y]
            return True
        except IndexError:
            return False
