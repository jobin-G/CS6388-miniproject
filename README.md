# Petrinet Miniproject

## Installation
First, install the myminiproject following:
- [NodeJS](https://nodejs.org/en/) (LTS recommended)
- [MongoDB](https://www.mongodb.com/)

Second, start mongodb locally by running the `mongod` executable in your mongodb installation (you may need to create a `data` directory or set `--dbpath`).

Then, run `webgme start` from the project root to start . Finally, navigate to `http://localhost:8888` to start using myminiproject!


## Modeling
This application allows you to design Petrinets using a local instance to WebGME. 

Models are constrained to the definiton of a Petrinet which are as follows.

- A Place and a Transition are connected by an Arc. 
- Places can have a number of tokens assigned to them
- Transitions are fireable

SVGs are used to indicate how many tokens are assigned to a Place node.

## Classification
The application has a plugin enabled that identifies whether your model can be classified as one of the following
1. Free Choice
2. State machine
3. Marked graph
4. Workflow net

## Visualization
The application provides a PetrinetView which allows a user to simulate the flow of tokens through the graph. At the moment
this visualization is limited to a single token moving via a fired transition when in reality a variable number of tokens
can move to another Place when a Transition is fired.
