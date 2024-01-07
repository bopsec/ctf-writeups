class RubiksCube:
    def __init__(self):
        # Initialize the cube with the given configuration
        self.top = [["{", "E", "O"],
                    ["L", "S", ")"],
                    ["E", "L", "W"]]
        self.front = [["T", "?", "P"],
                      ["D", "N", "E"],
                      ["R", "S", "P"]]
        self.bottom = [["P", "L", "Ø"],
                       ["D", "T", "E"],
                       ["L", "B", "_"]]
        self.left = [[":", "S", "M"],
                     ["_", "O", "S"],
                     ["_", "_", "U"]]
        self.right = [["}", "B", "L"],
                      ["K", "E", "G"],
                      ["_", "U", "I"]]
        self.back = [["E", "N", "R"],
                     ["L", "E", "Y"],
                     ["U", "S", "_"]]

        '''self.top = [["B", "B", "W"],
                    ["O", "G", "Y"],
                    ["W", "G", "R"]]

        self.front = [["R", "Y", "G"],
                      ["W", "W", "O"],
                      ["O", "W", "R"]]

        self.bottom = [["G", "O", "B"],
                       ["B", "B", "W"],
                       ["O", "Y", "W"]]

        self.left = [["Y", "G", "G"],
                     ["G", "R", "R"],
                     ["B", "O", "Y"]]

        self.right = [["Y", "R", "O"],
                      ["Y", "O", "R"],
                      ["W", "G", "O"]]

        self.back = [["G", "W", "R"],
                     ["B", "Y", "R"],
                     ["B", "B", "Y"]]'''

    def rotate_face_clockwise(self, face):
        return [list(reversed(col)) for col in zip(*face)]

    def rotate_face_counterclockwise(self, face):
        return self.rotate_face_clockwise(self.rotate_face_clockwise(self.rotate_face_clockwise(face)))

    def U(self):
        self.top = self.rotate_face_clockwise(self.top)
        temp = self.front[0]
        self.front[0] = self.right[0]
        self.right[0] = self.back[0]
        self.back[0] = self.left[0]
        self.left[0] = temp

    def U_prime(self):
        self.top = self.rotate_face_counterclockwise(self.top)
        temp = self.front[0]
        self.front[0] = self.left[0]
        self.left[0] = self.back[0]
        self.back[0] = self.right[0]
        self.right[0] = temp

    def D(self):
        self.bottom = self.rotate_face_clockwise(self.bottom)
        temp = self.front[2]
        self.front[2] = self.right[2]
        self.right[2] = self.back[2]
        self.back[2] = self.left[2]
        self.left[2] = temp

    def D_prime(self):
        self.bottom = self.rotate_face_counterclockwise(self.bottom)
        temp = self.front[2]
        self.front[2] = self.left[2]
        self.left[2] = self.back[2]
        self.back[2] = self.right[2]
        self.right[2] = temp

    def L(self):
        self.left = self.rotate_face_clockwise(self.left)
        temp = [row[0] for row in self.front]
        for i in range(3):
            self.front[i][0] = self.top[i][0]
            self.top[i][0] = self.back[2 - i][2]
            self.back[2 - i][2] = self.bottom[i][0]
            self.bottom[i][0] = temp[i]

    def L_prime(self):
        self.left = self.rotate_face_counterclockwise(self.left)
        temp = [row[0] for row in self.front]
        for i in range(3):
            self.front[i][0] = self.bottom[i][0]
            self.bottom[i][0] = self.back[2 - i][2]
            self.back[2 - i][2] = self.top[i][0]
            self.top[i][0] = temp[i]

    def R(self):
        self.right = self.rotate_face_clockwise(self.right)
        temp = [row[2] for row in self.front]
        for i in range(3):
            self.front[i][2] = self.bottom[i][2]
            self.bottom[i][2] = self.back[2 - i][0]
            self.back[2 - i][0] = self.top[i][2]
            self.top[i][2] = temp[i]

    def R_prime(self):
        self.right = self.rotate_face_counterclockwise(self.right)
        temp = [row[2] for row in self.front]
        for i in range(3):
            self.front[i][2] = self.top[i][2]
            self.top[i][2] = self.back[2 - i][0]
            self.back[2 - i][0] = self.bottom[i][2]
            self.bottom[i][2] = temp[i]

    def F(self):
        self.front = self.rotate_face_clockwise(self.front)
        temp = self.top[2]
        self.top[2] = [self.left[2 - i][2] for i in range(3)]
        for i in range(3):
            self.left[i][2] = self.bottom[0][i]
        self.bottom[0] = [self.right[2 - i][0] for i in range(3)]
        for i in range(3):
            self.right[i][0] = temp[i]

    def F_prime(self):
        self.front = self.rotate_face_counterclockwise(self.front)
        temp = self.top[2]
        self.top[2] = [self.right[i][0] for i in range(3)]
        for i in range(3):
            self.right[i][0] = self.bottom[0][2 - i]
        self.bottom[0] = [self.left[i][2] for i in range(3)]
        for i in range(3):
            self.left[i][2] = temp[i]

    def B(self):
        self.back = self.rotate_face_clockwise(self.back)
        temp = self.top[0]
        self.top[0] = [self.right[i][2] for i in range(3)]
        for i in range(3):
            self.right[i][2] = self.bottom[2][2 - i]
        self.bottom[2] = [self.left[i][0] for i in range(3)]
        for i in range(3):
            self.left[i][0] = temp[2 - i]

    def B_prime(self):
        self.back = self.rotate_face_counterclockwise(self.back)
        temp = self.top[0]
        self.top[0] = [self.left[2 - i][0] for i in range(3)]
        for i in range(3):
            self.left[i][0] = self.bottom[2][i]
        self.bottom[2] = [self.right[i][2] for i in range(3)]
        for i in range(3):
            self.right[i][2] = temp[i]

    def get_configuration(self):
        # Return the current configuration of the cube
        return {
            "Top": self.top,
            "Front": self.front,
            "Bottom": self.bottom,
            "Left": self.left,
            "Right": self.right,
            "Back": self.back
        }

cube = RubiksCube()

# Perform the solution moves
cube.U()
cube.B()
cube.U_prime()
cube.B()
cube.L_prime()
cube.B()
cube.R()
cube.L_prime()
cube.B()
cube.B()
cube.U()
cube.F()
cube.B()
cube.B()
cube.U_prime()
cube.B()
cube.B()
cube.R()
cube.R()
cube.F()
cube.F()
cube.B()
cube.B()
cube.D()
cube.D()
cube.B()
cube.B()
cube.D()
cube.D()
cube.D()

final_configuration = cube.get_configuration()
print(final_configuration)
