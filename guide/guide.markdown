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

- In step 1 we will draw the board.
- In steps 2-4 we will deal with the mouse events. The mouse move event looks like quite a drama, but it's actually easier than ...
- ... Step 5, where we will update the board while trying to keep it convenient for animation in Step 8.
- We will check if there are possible moves in Step 6 and shuffle the board if there aren't any, in Step 7.
- We will then add some spice to our game - animation in Step 8, music in Step 9 and start/end screens in Step 10.
- Finally we will package our game in Step 11.

## Housekeeping

- Create a folder called "happy-connect"
- Copy the "assets" folder in Resources (ask the volunteers where that is) into your "happy-connect" folder

This is a long project. To avoid the "I forget where I was last time" problem, make a Git commit each time you leave a session.

- Inside "happy-connect" folder, right click on the window and click "Open in Terminal"
- In the terminal, type in `git init`
- Each time you leave a session, open this terminal again and type in `git add . && git commit -m [MESSAGE]`, where [MESSAGE] should say where you are when you leave the session
- Each time you come to a session, open this terminal again and type in `git log` to see your last commit, which should tell where you were when you last left
