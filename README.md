Brick Addon (Working Title)
================
Version 0.2
-----------
(c) Mark Fitzgibbon 2017

Description
-----------
Generates a square object in Blender 3D with variable random nose applied to vertices
Script is provided as-is

Download
--------
User can pull, fork, or download this tool's source code from 
[b3d-brick Repository](https://github.com/ibbolia/b3d-brick)

Requirements
------------
Requires Blender, v2.78 preferred.
Code is not intended nor designed to work as a standalone Python program.

Install
-------
User wishing to install as and addon to blender should perform the following:
1. Zip folder (if not already done) 
2. Open Blender program
3. Navigate to File > User Preferences > Add-ons
4. Install from file

Alternatively, User can install addon files directly in Blender's addon folder
Add-on is only in "Testing" supported level

Usage
--------
Script currently only available through spacebar menu (named "Brick")

User can generate an NBrick at cursor location and set variables:
- Subdivisions: Number of subdivisions to form in brick
- length, width, height: standard size values of brick object
- Noise intensity: Amount of variation for vertex noise
- Seed: Seed value for random calculations

Further Notes
-------------
- [Blender Python API](https://docs.blender.org/api/blender_python_api_2_78a_release/) for Blender version 2.78+
- NBrick Subdivision formula is roughly based on code by [Nathan Miller](http://wiki.theprovingground.org/blender-py-mathmesh)

Contact
-------
- [Github](https://github.com/ibbolia)
- Twitter: [@ibbolia](https://twitter.com/ibbolia)
- Gmail: mwfitzgibbon