#Change Log
All notable changes will be tracked in this file

##[Unreleased]
###Added
- Function newBrick to BrickGeneratorOperator 
- WallGeneratorOperator class
- Tile class
- Add Brick button to Add menu

###Changed
- randVertsBMesh made a function of BrickGeneratorOperator
- moved BrickGeneratorOperator execute code to newBrick function

###Removed
- References to original Brick class
- Excess code in __main__ call

##[0.2] - 2017-01-24
###Added
- README
- CHANGELOG
- Intensity and seed values to keymap for NBrick

###Changed
- randVertsBMesh now explicitly uses range of -n to +n
- algorithm for NBrick.genMeshData reduced line count
- Seed now dependent on NBrick keymap value (previously time based)

###Removed
- randomizeVerts

##[0.1] - 2017-01-23
###Added
- Brick class (deprecated)
- Nbrick class
- NBrick property keymaps
- Randomness to NBrick