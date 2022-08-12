# sudoku

This project contains the Python code for both a backtracking algorithm used to solve a pre-determined sudoku board, as well as a GUI that will display the board for easier use. 

When the program is run, the user is met with a predetermined, valid sudoku board:

![image](https://user-images.githubusercontent.com/49917374/183825056-f2da3f00-9567-44b7-899a-094c94c56c0e.png)

From here, the user can either immediately press the "Solve" button, which will then solve the default board via backtracking, or the user can select individual tiles on the board and replace them with their own input. When a user selects a tile, it will highlight in grey until a number is inputted.

![image](https://user-images.githubusercontent.com/49917374/184275158-725def2c-51d5-4ce2-b321-7defc8b08f20.png)

Here, the very first tile was changed to a "4", and this already creates an invalid Sudoku board. The GUI will then tell the user that the puzzle isn't solvable, and they need to reset the board entirely using the "Reset" button. Once this button is clicked, the board will return to its default state.

![image](https://user-images.githubusercontent.com/49917374/184275229-a91146ee-c39f-49df-b426-29abf421d2b3.png)

A solved default board will look like so: 

![image](https://user-images.githubusercontent.com/49917374/183825623-ad20e78f-3064-4abb-b217-36e1d4b2f958.png)

