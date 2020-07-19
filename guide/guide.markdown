# Happy Connect

## Introduction

Happy Connect is a mini game in My Talking Tom. You will be eliminating blocks by drawing a long chain of neighbouring blocks (no shorter than three blocks, no circles) in a same colour. Your goal is to reach a target score before running out of moves, although there are other ways to play it. For example, DrawSum gave the game a math twist, where you draw a chain of numbers so that they sum up a given number.

This is a long project, but it's also rewarding. You will implement the game, the animation, add music and finally make it installable. The final project looks like this.

[image]

If you think of the gameplay, it looks like there's nothing complex.

- First we draw the board and the pieces.
- Then the player clicks on a piece to select it.
- The player then drags the mouse to draw a chain
- And finally the player releases the mouse to confirm the chain.
- We then check whether it is a valid chain (longer than two blocks, no circles), remove the blocks of the chain and add new blocks if it is.

If we draw a diagram, it can look like this (taking a chain made of four pieces as an example).

[image]

But think again. There are many places where things can go wrong. Take the four-piece chain example:

When clicking on the first piece

- The player might click outside the board. If we calculate which piece to select based on a place outside the board, the program might crash.

When trying to drag onto the second piece

- The player might release the mouse before moving to the next piece, for example, when it decides to start on a different piece.
- The player might drag on to a piece with a different colour from the previous, which makes an invalid chain.
- The player might somehow drag the mouse on a block that's not a neighbour of the last block, which is not allowed in the game.

When trying to drag on the third piece

- The player might release the mouse before making it to the third piece, for example, by mistake.
- The player might drag back to the previous piece to change the path of its chain. This is a typical tactics for exploration

When trying to drag on the fourth piece

- The player might draw a chain with circles, which is not allowed.

And finally, after we remove the blocks and add new blocks

- There might not be possible moves, especially if you add dead blocks like My Talking Tom did.

So our diagram becomes something like this.

[image]

The numbers show the corresponding steps where we will deal with each problem.

<!-- - In step 1 we will draw the board.
- In steps 2-4 we will deal with the mouse events. The mouse move event looks like quite a drama, but it's actually easier than ...
- ... Step 5, where we will update the board while trying to keep it convenient for animation in Step 8.
- We will check if there are possible moves in Step 6 and shuffle the board if there aren't any, in Step 7.
- We will then add some spice to our game - animation in Step 8, music in Step 9 and start/end screens in Step 10.
- Finally we will package our game in Step 11. -->

## Housekeeping

- Create a folder called "happy-connect"
- Copy the "assets" and "tests" folders in Resources (ask the volunteers where that is) into your "happy-connect" folder
- Inside "happy-connect", create a folder called "src" (for "source"). Your code files will live in it.

This is a long project. To avoid the "I forget where I was last time" problem, make a Git commit each time you leave a session.

- Inside "happy-connect" folder, right click on the window and click "Open in Terminal"
- In the terminal, type in `git init`
- Each time you leave a session, open this terminal again and type in `git add . && git commit -m [MESSAGE]`, where [MESSAGE] should say where you are when you leave the session
- Each time you come to a session, open this terminal again and type in `git log` to see your last commit, which should tell where you were when you last left

As a good practice, we will do typing for functions in this project.

## Step 1: Draw the board

**TODO: Introduce architecture**

<!--
The board represents the pieces with an integer id.
The board sprite holds a list of corresponding costumes to draw for each block.
The block sprites draw themselves on the screen. -->

## Step 1A: Save information about pieces

- Inside "src" folder, create a file called Core.py. This file will contain information about what's on the board.

Our board will be represented with a numpy array containing the number representing the kind of block held in each cell. It will also contain the count of each kind of block, this is used for updating board in Step 5.

The board will be created with a size (rows and columns) and number of block kinds in it.

- First, import numpy. Also import typing for lists.
- Create a class called Board.
- Its constructor should take in numbers of rows, columns and block kinds as arguments.
- We should also be able to get the board and the count of each kind of blocks.
- In the constructor, we will randomly create an initial board.

  The way we do this is by choosing a random number between 0 and 1 for each cell, scale it across the number of kinds, and finally take the floor of the number.

  [Image showing the process with matplotlib]

- We will then count the number of each kind. numpy has a function called `unique` that makes this easy

  [Image showing the process]

- Finally we return the board and kind count in separate functions.

### Test your code

- Open TestPoint1.py in "tests" folder
- Import our class Board
  Note: if you called it something else, import it as Board

Run TestPoint1.py. You should see OK.

If the test point fails many times, chances are the tests are wrong. Print the necessary information to see what's happened, and ask a volunteer if you need help.

## Step 1B: Draw the pieces

- Inside "src" folder, create a file called Sprites.py. This file will contain classes that draw something based on some given information.

All the sprites classes in this project will derive from pygame's Sprite class. By convension, each pygame Sprite should have a property called "image" (similar to costumes in Scratch) and one called "rect" (similar to x, y positions and size in Scratch).

- Import pygame's sprite class
- Create a class called BlockSprite. It derives from pygame's sprite class. It's constructed with a position on the board and a costume.
- In the constructor, convert the coordinates to integer.
- Set the image and rect properties.
- A block sprite can also render itself onto a board.

## Step 1C: Draw the board

- In the same file (Sprites.py), create a class called BoardSprite. It's also derived from pygame's Sprite class.
- A board sprite is constructed with a board (like the array we make in Step 1A), a region on the screen to draw the board, number of block kinds, and a list of costumes. The costume list is defaulted to None.

  Note that you can't use an empty list as default value.

- We then set the image and rect variables like we did for block sprites.

The board sprite needs to keep a list of block sprites. To construct a block sprite, we need to know its position **on the board** and its costume(which also contains its size), as was defined in Step 1B.

Note that because in Step 1B we assumed blitting the costume onto the board's surface, it is now the position on the board that's required for a block sprite, not that on the screen. This means we won't need to worry about where the board is on the screen - the pieces will move together with it.

We will now prepare the positions and costumes.

- In the constructor, after we set the image and rect variables, we calculate the width and height of each block. The positions are calculated later when we construct each block in a loop.
- We then make sure we have a costume for each kind of block. But before that, we add a function that creates a default costume in case there aren't enough of it.
- We then check the length of costume list, and add default costume to it if it's not long enough.
- Now that we've got the size of each block and one costume for each kind, we can calculate positions and make the block sprites.
- Finally, like we did for block sprites, our board will render itself onto the screen.

### Test your code

- Open TestPoint2.py in "tests" folder
- Import our classes Board, BoardSprite and BlockSprite, renaming them if you called them something else in your code

Run TestPoint2.py. You should see OK.

If the test point fails many times, chances are the tests are wrong. Print the necessary information to see what's happened, and ask a volunteer if you need help.

## Step 1D: See the board

Don't you want to see the board in action?

- Inside "src" folder, create a file called main.py.
- In main.py, type in our familiar PyGame boilerplate code.
- Before `pygame.init()`, import our Board and BoardSprite classes.
- After `pygame.init()`, but before `while True`, create a screen.

Our board sprite needs a board and a region on the screen to draw itself.

- Create a board of size 8 \* 8 with three kinds of blocks. (Step 1A)
- Create a region on the screen and a position for the board.
- Now create a board sprite and fill it with our board, board region and number of block kinds. (Step 1C)
- Finally, at the bottom of `while True` loop, draw the board onto the screen.
- Run main.py.
