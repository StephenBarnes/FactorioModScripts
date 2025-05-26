These 2 scripts attempt to "factorize" images using HSV colors. They split an input image into multiple images representing different color components. For example if you have an icon where one part is red and one part is purple, you can split it into the red and purple components.

Both scripts do almost the same thing but in slightly different ways. Script A is generally better, but try script B if results aren't satisfactory.

This was originally meant to automatically generate different-colored icons for related items/fluids in the game. For example, you can take the "fluoroketone-hot.png" icon from Space Age (blue-green fluid with red around the edges), split into blue-green and red components, then make a compound icon from those two components tinted with any combination of colors. Unfortunately this specific example (fluoroketone-hot) didn't really work when I tried it, the resulting tinted+combined images don't look good.

You can make the compound icon using either ItemPrototype.icons, or by manually editing the layers together in a program like GIMP.
