# sudoku

This project contains the Python code for both a backtracking algorithm used to solve a pre-determined sudoku board, as well as a GUI that will display the board for easier use. 

When the program is run, the user is met with a predetermined, valid sudoku board:

![image](https://user-images.githubusercontent.com/49917374/183825056-f2da3f00-9567-44b7-899a-094c94c56c0e.png)

From here, the user can either immediately press the "Solve" button, which will then solve the default board via backtracking, or the user can select individual tiles on the board and replace them with their own input. A lot of the time this will create a board that actually doesn't have a possible solution, so the program will output this to the user: 

![image](https://user-images.githubusercontent.com/49917374/183825299-bee9a6ff-6ac2-442c-a7eb-c058eeb24ce7.png)

Here, the very first tile was changed to a "4", and this already creates an invalid Sudoku board. The GUI will then tell the user that the puzzle isn't solvable, and they need to reset the board entirely using the "Reset" button. Once this button is clicked, the board will return to its default state.

A solved default board will look like so: 

![image](https://user-images.githubusercontent.com/49917374/183825623-ad20e78f-3064-4abb-b217-36e1d4b2f958.png)

