This directory is for visualizing and creating color schemes for analogous items.

To use:
1. Open webpage.html in a web browser.
2. Edit the example code in main.js to create tables of your mod's items/fluids. Set some cell colors, then call completeTable() or analogy3() or analogy4() to set colors analogous to others.

For example you might have 5 different acids (nitric, sulfuric, hydrochloric, phosphoric, hydrofluoric), each with corresponding salts (respectively niter, salt cake, sodium/potassium chloride, etc.) and corresponding gases (respectively NOx gas, sulfur dioxide, chlorine gas, etc.) and you want a systematic color scheme for them, where colors are modified analogously (so nitric acid is to niter as sulfuric acid is to salt cake, etc.).

Having a clear color scheme helps players make quickly understand the relations between items/fluids, even if the colors are unrealistic. For example, the base game uses blue for iron ore and orange for copper ore, which is unrealistic but helps match ores to plates. And the base game uses pink and purple for holmium/tungsten, because the realistic color (silver) would look the same as steel.

Suggestions for making color schemes:
* Use a site like colormind.io to generate color palettes. Then define related colors using this visualizer.
* Group similar things into similar color ranges. The example setup has acids on warm colors (red to cyan), and bases on colder colors (purple/blue).
* For compound items, use a sprite tinted with a combination of colors. For example magnesium chloride could be tinted with a gradient from magnesium's color to chlorine's color.

Most of the JS code was written by Gemini 2.5 Pro.
