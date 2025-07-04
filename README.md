# Scripts in this repo

This repo contains various scripts I've collected while developing Factorio mods.

In the `image-scripts` folder, the `.sh` scripts are Bash scripts which run natively on Linux. You can probably also run them on Mac, or on Windows using tools like Cygwin, but I haven't tested them on those systems. The `.py` scripts are Python, so should work on all systems.

Feel free to send pull requests if you make any changes or make new scripts. Most of these scripts were written by AI; competent AIs (like Gemini 2.5 Pro, or Claude 4 Opus) are generally able to write scripts like this faster than writing them yourself.


# Resources for making Factorio mods

Below I've collected links to resources for making Factorio mods, plus some notes on modding. Underneath that there's also some thoughts on designing overhaul mods. Feel free to post an issue if you know of anything I should add.

## Basics

Crucial background: Factorio mods run in 3 stages: settings, then data/prototype, then control/runtime. [More details.](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html) The data/prototype stage uses different types than the control/runtime stage, so the [prototype API docs](https://lua-api.factorio.com/latest/index-prototype.html) are separate from the [runtime API docs](https://lua-api.factorio.com/latest/index-runtime.html). Factorio uses a custom version of Lua with [some changes](https://lua-api.factorio.com/latest/auxiliary/libraries.html).

[The wiki has a general introductory modding tutorial by Gangsir.](https://wiki.factorio.com/Tutorial:Modding_tutorial/Gangsir)

## Communities

* [Official Discord channel for mod development](https://discord.com/channels/139677590393716737/306402592265732098)
* [Official forums](https://forums.factorio.com/index.php)
* [Subreddit](https://www.reddit.com/r/factorio/)
* There are also various community-run Discord servers - The Foundry, Earendel, probably others I am unaware of.

## Graphics

### General graphics tips

You can control-alt-click on the "settings" button to access a secret settings menu called "the rest". There's a hidden setting "runtime-sprite-reload" that allows you to modify sprites and see them in-game without needing to restart the game. You'll still need to restart the game when changing prototypes. The setting harms performance a lot, so turn it off when not working on graphics.

### Ready-made graphics

When using graphics from other people, be aware of their licenses, which may have various requirements, such as requiring you to release your mod under the same license, requiring attribution, etc.

* [Free graphics for modders](https://github.com/snouz/factorio_free_graphics_for_modders) collected by Snouz - large collection of graphics from various mods with open licenses.
* [Unused Renders](https://github.com/malcolmriley/unused-renders) by Malcolm Riley - large collection of high-quality icons.
* [Factorio Buildings](https://mods.factorio.com/user/Hurricane046) by Hurricane046 - large collection of high-quality building graphics for Factorio mods, with animations.

### Making graphics

Factorio uses 2D sprites, often generated from 3D models using a 45-degree perspective and orthographic projection.

* [Tutorial for making graphics with Blender](https://github.com/malcolmriley/unused-renders/wiki) by Malcolm Riley.
* [Galdoc's Tutorials](https://www.youtube.com/@galdocstutorials/videos) are a series of videos on Blender by the creator of [Galdoc's Manufacturing](https://mods.factorio.com/mod/galdocs-manufacturing), an overhaul mod with original machine and icon graphics.

### Editing graphics

I use GIMP to edit icon sprites. This is not my area of expertise so I can't offer much advice, besides that you should learn how to use layers, how to manipulate selections, and how to use the color tools.

### Layering graphics

You can use [`ItemPrototype.icons`](https://lua-api.factorio.com/latest/prototypes/ItemPrototype.html#icons) to layer multiple icons on top of each other, with an optional tint applied to each one. The base game uses this for barrelled fluids, for example - see the folder `Factorio/data/base/graphics/icons/fluid/barreling/` in your install. This can allow you to make lots of related icons in the game without needing to include all of them in your mod. You can also use this for things like making a "frozen nutrients" icon by putting the nutrient icon as the middle layer between two layers of the ice icon, both tinted to make them semi-transparent.

For icons of reflective things (like metal items or fluid drops), you can sometimes improve their appearance by splitting the icon into a base layer and a mostly-transparent highlights layer with the bright reflective parts. Then tint the base layer, and overlay it with the *untinted* highlights layer, so that the highlights are still white.

Note that there are some issues with using layered icons that may cause minor graphics bugs that are hard to notice in development; see the list at the top of [this](https://lua-api.factorio.com/latest/types/IconData.html) page. For the specific issue with icon shadows, you can set `draw_background = true` on multiple layers, if they don't overlap. You can also add an additional back layer that's almost transparent, purely to draw larger background shadows.

To fix these issue with multi-layer icons, you can launch Factorio using the `--dump-icon-sprites` option to dump all icon sprites to your `script-output` folder. This will combine the layers exactly as they are combined in-game. So, you could make multi-layer icons in your mod, then use this option to generate single-layer icons, and then move those single-layer icons into your mod and use them in place of multi-layer icons.

### AI-generating graphics

You can use Midjourney to generate icon sprites. Unfortunately Midjourney is tuned to generate either realistic photographs of young women or generic fantasy cartoon slop, not Factorio-style sprites of industrial intermediates, so it may take some wrangling to get it to generate what you want. Once you've generated one good image, you can generate variations of it to use as [sprite variations](https://lua-api.factorio.com/latest/prototypes/ItemPrototype.html#pictures) for items. Ask for the sprites on a plain black background, and then edit them before use; some of the scripts in this repo (like `divide_image.sh` and `transparent_background.sh`) were made specifically for this purpose.

Gemini models are useful for adding things to images. For example, I used Gemini to make the condensing turbine graphics for Legendary Space Age, by editing the base-game's steam turbine graphics to add a lid over the turbine part. These models are currently bad at generating new images, but good at making edits.


## Coding

### Tutorials for aspects of coding

* If you already know basic programming, you can use [Learn Lua In Y Minutes](https://learnxinyminutes.com/lua/) to quickly get familiar with Lua. You can mostly ignore everything about metatables and classes, since most mods don't use them.
* [General introductory modding tutorial](https://wiki.factorio.com/Tutorial:Modding_tutorial/Gangsir) by Gangsir.
* [Using settings in mods](https://wiki.factorio.com/Tutorial:Mod_settings)
* [Porting mods to 2.0](https://github.com/tburrows13/factorio-2.0-mod-porting-guide) by Xorimuth.
* [Localization](https://wiki.factorio.com/Tutorial:Localisation)
* [GUI modding](https://github.com/ClaudeMetz/UntitledGuiGuide/wiki) by Therenas.
	* Also see [Factorio GUI Style Guide](https://man.sr.ht/~raiguard/factorio-gui-style-guide/) by Raiguard.

#### World generation / autoplace / noise expressions

Factorio's world generation system changed significantly in the 2.0 update. [This](https://togos.github.io/togos-example-noise-programs/) was a good tutorial for the old system. The new system works almost the same conceptually, but noise expressions are now written as strings instead of Lua tables. I am not aware of any tutorials for the new worldgen system. If you want to do worldgen coding, I would recommend understanding that tutorial conceptually, then looking at the base game's Lua code (for example in `space-age/prototypes/planet/planet-(Planet)-map-gen.lua`) and the [API docs](https://lua-api.factorio.com/latest/auxiliary/noise-expressions.html).

[Noise Tools](https://mods.factorio.com/mod/noise-tools) by Earendel is a mod that helps to visualize noise expressions for debugging.

### Dev environment

* You can write and edit mods as folders in the mods directory. You don't need to zip them, they can just be a plain folder. Before uploading to the mod portal, you need to zip them, for example using the `zipmod.sh` script in this repo.
* [Factorio Modding Toolkit](https://github.com/justarandomgeek/vscode-factoriomod-debug/blob/current/doc/workspace.md) includes a VSCode extension making the editor aware of the Factorio API.
	* I strongly recommend setting this up. It is very helpful for catching errors and type-checking, and includes a debugger/profiler.
* You can hold your mouse over an entity and press control-shift-F to view information about its prototype. You can also press control-shift-E to search through all the prototypes in the game.
* I recommend opening Wube's Lua code directory in a separate IDE window. On Linux+Steam it's at `~/.local/share/Steam/steamapps/common/Factorio/data/` but yours might be in [other places](https://wiki.factorio.com/Application_directory). You can search through this to find the base game's code for defining prototypes and locale strings.
* [Factorio Tools](https://github.com/Hornwitser/factorio_tools) by Hornwitser has command-line tools for debugging/inspecting Factorio-related things, such as figuring out desyncs.
* I recommend making a simple mod with only an `info.json` file with dependencies on several testing mods so you can toggle them all on and off easily. Give it a name like "○○○○○○ Testing mods" so it's at the top of the mod list. My current mod has dependencies on `"EditorExtensions", "factoryplanner", "circuit-connector-placement-helper"`, and optional dependencies on `"creative-space-platform-hub"` (for testing with Space Age) and `"even-pickier-dollies"` (for testing compatibility).

Mods useful when developing mods:

* [Editor Extensions](https://mods.factorio.com/mod/EditorExtensions) by raiguard is useful for testing basically any mod.
* [Creative Space Platform Hub](https://mods.factorio.com/mod/creative-space-platform-hub) by Quezler is useful for testing stuff involving space platforms.
* [Noise Tools](https://mods.factorio.com/mod/noise-tools) by Earendel can be used to visualize noise expressions.
* [Circuit connector placement helper](https://mods.factorio.com/mod/circuit-connector-placement-helper) by Quezler is useful for choosing and placing the circuit connectors of buildings.
* [Style Explorer](https://mods.factorio.com/mod/style-explorer) by _CodeGreen lets you look through styles for GUIs.
* A planner mod like [Factory Planner](https://mods.factorio.com/mod/factoryplanner) by Therenas is useful for balancing recipes. For example, you can use it to compare the raw materials needed to make your new circuit item with the raw materials needed to make base-game blue circuits, or compare the number of machines and electric power needed by different recipe paths with the same end product.

### Libraries

Some mods that you can add as dependencies of your mod. You can import Lua files from other mods into your mod using `require "__OtherMod__/directory/filename"`.

* [flib / Factorio Library](https://github.com/factoriolib/flib) is a set of utility functions.
* [PlanetsLib](https://mods.factorio.com/mod/PlanetsLib) has tools for creating planets and moons.
* [glib / GUI Library](https://mods.factorio.com/mod/glib) by _CodeGreen has tools for creating GUIs.
* [Quality Lib](https://mods.factorio.com/mod/quality-lib) by Davoness has tools to change values of items/entities for different quality levels; see the "magic tricks" section below.
* The Factorio engine does not allow you to store data in the data stage and then use it in the control stage. [Big Data String 2](https://mods.factorio.com/mod/big-data-string2) by plexpt and dodo.the.last allows you to do this anyway by smuggling the data inside nested localised strings.
* The base game code contains some useful functions, in `core/lualib`.

Some dependency mods that aren't exactly libraries but provide additional tools for creating mods.

* [Beacon Interface](https://mods.factorio.com/mod/beacon-interface) by Quezler allows you to create beacons with effects that can be adjusted to arbitrary values in runtime scripts. See explanation of how this mod works, and some uses of it, in the "magic tricks" section below.
* The engine only allows beacons to use void or electric energy sources. [Nonstandard Beacons](https://mods.factorio.com/mod/zzz-nonstandard-beacons) by protocol_1903 and Quezler allows you to make beacons using other energy sources (burner, heat, or fluid).
* [Washbox](https://mods.factorio.com/mod/washbox) by Quezler allows you to create recipes that require holding an item in a fast-moving stream of fluid, without consuming the fluid.
* [Runtime spoilage library](https://mods.factorio.com/mod/runtime-spoilage-library) by SirPuck lets you define custom spoilage rules, such as making items spoil to different results depending on the surface.
* [Multi-spoil](https://mods.factorio.com/mod/multispoil) by LambdaLemon allows you to make one item spoil into multiple other items, each with a different count and probability.

### Automatic publishing

* [Factorio Mod Template](https://github.com/fgardt/factorio-mod-template) has tools for automatic packaging and uploading.
* Factorio Modding Toolkit includes a tool for this, explained [here](https://github.com/justarandomgeek/vscode-factoriomod-debug/blob/current/doc/package.md).
* If you prefer to manually upload zipfiles to the portal, this repo includes a `zipmod.sh` script to zip up mods and run some checks.

### Starter/template mods

* [Factorio Example Mod](https://github.com/ZwerOxotnik/factorio-example-mod) by ZwerOxotnik is a starter/template mod that you can fork and edit instead of writing a mod from scratch.

### How to do specific things

This section has specific instructions for what you need to do to make common types of mods.

#### Adding a new resource

If you want to add a new type of ore patch, gas well, or similar:

* Register a [resource entity](https://lua-api.factorio.com/latest/prototypes/ResourceEntityPrototype.html). There are some examples in `base/prototypes/entity/resources.lua`.
	* The resource entity prototype's `category` determines which machines can mine it - mining drills, big mining drills, pumpjacks, etc. If you want only a specific new machine to mine it, you need to register a [resource category](https://lua-api.factorio.com/latest/prototypes/ResourceCategory.html) and a [mining drill](https://lua-api.factorio.com/latest/prototypes/MiningDrillPrototype.html#resource_categories) with that resource category.
	* Set the resource entity's [.minable](https://lua-api.factorio.com/latest/prototypes/EntityPrototype.html#minable) to determine which item it produces and how long it takes to mine.
* If the minable resource entity produces a new item/fluid, you will also need to register a prototype for that.
* Each planet has tables of all the entities, tiles, and decoratives that are autoplaced on it when terrain is generated. So you need to add your resource entity to those lists. For example: `data.raw.planet.nauvis.map_gen_settings.autoplace_settings.entity.settings["my-ore"] = {}`
* To control where your ore spawns, you need to use autoplaces and noise expressions. If your resource spawns similarly to base-game resources like ore (big round patches) or crude oil wells (small clusters of dots), you can do this the same way it's done in `base/prototypes/entity/resources.lua`, by importing `resource-autoplace` and then setting `ResourceEntityPrototype.autoplace` by calling functions like `resource_autoplace.resource_autoplace_settings`. If you want your resource to spawn in a different way, you'll need to write custom noise expressions, which is more difficult. See the section on world generation above.
* When starting a new game, the sliders for resources are called [autoplace controls](https://lua-api.factorio.com/latest/prototypes/AutoplaceControl.html). If you want a slider, you need to register an autoplace control. See `base/prototypes/autoplace-controls.lua` for examples.
	* Each planet keeps a list of autoplace controls that apply to that planet. So if you want a slider, you also need to add it to the list of controls for your planet, for example: `data.raw.planet.nauvis.map_gen_settings.autoplace_controls["my-ore"] = {}`
* Define [locale strings](https://wiki.factorio.com/Tutorial:Localisation) in entity-name, item/fluid-name, and optionally the autoplace control. (The base game reuses the entity name for the autoplace control's name.)

#### Creating a crafting machine

* Figure out if you want to make a "furnace" or an "assembling-machine". The main difference is that furnaces automatically select their recipe based on input, and can only have 1 input item, while assembling-machines need a recipe selected by the player.
	* If your machine can only do 1 recipe, you can use an assembling-machine and set the `fixed_recipe` field.
* Register either a [FurnacePrototype](https://lua-api.factorio.com/latest/prototypes/FurnacePrototype.html) or an [AssemblingMachinePrototype](https://lua-api.factorio.com/latest/prototypes/AssemblingMachinePrototype.html).
	* Set the machine's graphics_set to make it visible in game. You can use animation and idle_animation, and also working_visualisations which can have some layers tinted based on the current recipe's colors. If you want a static picture instead of animation, that's implemented by making it an animation with frame_count set to 1.
	* Set the machine's working_sound. You can copy this from an existing machine, or use multiple sounds layered and optionally played at specific frames of the working visualisations.
	* Set the circuit_connector. You can use [Circuit connector placement helper](https://mods.factorio.com/mod/circuit-connector-placement-helper) to pick the circuit picture and position.
* If the machine is meant to only do certain recipes, you need to register a new [recipe category](https://lua-api.factorio.com/latest/prototypes/RecipeCategory.html) and then give that category to your recipes and your crafting machine.
* Create an item with a place_result of the crafting machine entity. On the entity, set the placeable_by and minable to give the item back. Give the item the same name as the entity, so that their entries merge in the Factoriopedia.
* Create a recipe for the machine item. The recipe should have the same name as the item and machine, so the entries merge in the Factoriopedia.
* Add the item's recipe to a technology, or create a new technology for it.
* Define a [locale string](https://wiki.factorio.com/Tutorial:Localisation) in entity-name and optionally entity-description. (This will be reused for the item and the recipe, unless you explicitly give those different strings.)

#### Creating a planet or moon

Creating a planet can take a lot of work, depending on what exactly you want to do.

Look at the files in your Factorio install at `data/space-age/prototypes/planet/` for examples. 

The community project [PlanetsLib](https://mods.factorio.com/mod/PlanetsLib) is a mod that you can include as a dependency to provide functions helpful for creating planets and moons.

* Figure out the design and theme of the planet. Where does the planet fit in the planet progression? What does the terrain look like? What new machines, items, recipes, or mechanics do you want to put on it? Look at existing planet mods for inspiration.
* Create a [planet prototype](https://lua-api.factorio.com/latest/prototypes/PlanetPrototype.html). 
* By default, all planets orbit the same sun. If you want to make a moon orbiting another planet, or a separate solar system, you can use PlanetsLib to create non-sun orbits by drawing an extra orbit ring on the space map.
* Specify the values of surface properties in the planet prototype. These are numbers for things like gravity, pressure, and magnetic field. Buildings sometimes have surface conditions that only allow them to be placed on certain surfaces, and same for recipes. You may want to register new [surface property prototypes](https://lua-api.factorio.com/latest/prototypes/SurfacePropertyPrototype.html) to restrict buildings/recipes to your planet. PlanetsLib includes some disabled surface properties that you can enable, for standardizing surface properties between mods.
* PlanetPrototype inherits from SpaceLocationPrototype, since every planet has a location on the space map where space platforms park or travel to/from. So you need to specify some data about the space location, such as the asteroid spawn definitions. These define the asteroids that appear around spaceships parked at the planet.
* Define various things to help create the desired atmosphere of your planet.
	* Set [PlanetPrototype.persistent_ambient_sounds](https://lua-api.factorio.com/latest/types/PersistentWorldAmbientSoundsDefinition.html) to create atmospheric sounds like wind, rain, birds, or thunder. See examples in `space-age/prototypes/planet/planet.lua`.
	* Set music for your planet. PlanetsLib includes a function for copying music from another planet, for example `PlanetsLib.borrow_music(data.raw.planet.vulcanus, myPlanetPrototype)`
	* Set [PlanetPrototype.surface_render_parameters](https://lua-api.factorio.com/latest/types/SurfaceRenderParameters.html) to create fog or clouds. You can also use color lookup tables to apply color filters to the planet at different times of day; for example, this is used to apply a subtle purple tint to everything on Fulgora.
* Set PlanetPrototype.pollutant_type, if you want some kind of pollutant on your planet, like pollution or spores. If you want to make a new pollutant type, you need to register an [airborne pollutant prototype](https://lua-api.factorio.com/latest/prototypes/AirbornePollutantPrototype.html), and then also edit machine prototypes to emit this pollutant type, and create enemy spawners on the surface.
* Set PlanetPrototype.lightning_properties, if you want lightning.
* Set [PlanetPrototype.map_gen_settings](https://lua-api.factorio.com/latest/types/PlanetPrototypeMapGenSettings.html) to control terrain generation and placement of resources, cliffs, water, entities like enemy spawners or boulders, and decoratives (like small plants or craters that usually get removed when you build concrete over them). See `space-age/prototypes/planet/planet-map-gen.lua` for examples.
	* This needs to include an `autoplace_settings` field with *all* of the tiles, decoratives, and entities that should spawn on your planet.
	* To control placement of tiles, entities, and decoratives, you need to define noise expressions, which are basically functions of (x, y) coordinates that evaluate to the probability of each thing being placed at that coordinate. See the section on noise expressions above. Each tile, entity, and decorative has an [`autoplace` field](https://lua-api.factorio.com/latest/types/AutoplaceSpecification.html) that connects its probability and richness to a specific [noise expression](https://lua-api.factorio.com/latest/types/NoiseExpression.html).
	* Set the `autoplace_controls` to create sliders for resource size and richness when the player starts a new game. You don't need to create sliders for everything.
* Create a technology with an effect of type "unlock-space-location" to unlock travel to the planet.
* Register [space connection prototypes](https://lua-api.factorio.com/latest/prototypes/SpaceConnectionPrototype.html) to draw connections on the space map that space platforms can travel to get to/from your planet. Space connections have asteroid spawn definitions describing how many of each type of asteroid spawns at each point along the route.
* Register prototypes for all of the items, techs, recipes, and buildings you want on the planet.
* If you want to implement new gameplay mechanics, you might need to use runtime scripting, and possibly "magic tricks" (see section below).


### Magic tricks

For most simple changes you might want to make, like changing recipes or properties of items and buildings, you only need to edit prototypes. But in many cases, prototypes will not have a field that does what you want. In this situation, it is often still possible to achieve your aims, but you will need to resort to "magic tricks" involving a combination of hidden prototypes and control-stage scripting.

You can post a [request](https://forums.factorio.com/viewforum.php?f=28) for Wube to add the API feature that you want; requested features are sometimes added, especially if they are useful to many modders, or if they are simple (e.g. requesting runtime read access to an existing prototype field).

(There have also been two attempts that I am aware of to enable direct modding of the Factorio engine, outside of the Lua modding system. One of these is [Rivets](https://github.com/factorio-rivets/rivets-rs), which wasn't fully finished for Factorio 1.1 and hasn't been updated for 2.0. For the other attempt, I can't find the repo now but it was eventually abandoned.)

Generally these "magic tricks" involve the creation of hidden entity prototypes / items / surfaces, along with control-stage scripting to create or replace things using these hidden objects. I call them "magic tricks" because they involve doing a bunch of behind-the-scenes stuff not visible to the player to create effects that seem impossible within the engine.

Most magic tricks could be implemented using control-stage scripting with on_tick handlers. However, that's generally bad for performance, so it's better to implement them in other ways. The examples below instead use hidden entities and the like, in order to offload most of the work onto the game engine, which is much faster than Lua on_tick handlers.

Some general techniques useful for magic tricks:

* When a building is placed in the game, destroy it and replace it with a different building that looks the same, but has a different prototype and therefore different properties. The replacement can be chosen based on various conditions like the planet or location of the building.
* When a building is placed in the game, place one or more additional buildings, which interact with the original in some way. These are sometimes called "compound entities" or "child entities", and have been implemented by many mods.
	* For example, in my overhaul LSA, [this](https://github.com/StephenBarnes/LegendarySpaceAge/blob/master/const/child-entity-const.lua) file defines the child entities required by certain entities, and [this](https://github.com/StephenBarnes/LegendarySpaceAge/blob/master/control/child-entities.lua) file creates entities at runtime according to those requirements. It also handles entities being moved by Even Pickier Dollies, and can move child entities around the parent when the parent is rotated.
* Use [proxy containers](https://lua-api.factorio.com/latest/prototypes/ProxyContainerPrototype.html), which are containers that provide an alternate access point to a specific inventory of a specific machine. (Proxy containers are different from [linked containers](https://lua-api.factorio.com/latest/prototypes/LinkedContainerPrototype.html), which can only link to other linked containers.)
* Create a hidden surface. When a building is placed, create corresponding machines on the hidden surface. These machines could be assemblers, inserters, combinators, proxy containers, etc. You can link the visible building to buildings on the hidden surface using circuit connections, linked fluid connections, or proxy containers.


#### Magic trick examples

* Suppose you want to make properties of entities change depending on their quality. Currently the modding API has many properties in [QualityPrototype](https://lua-api.factorio.com/latest/prototypes/QualityPrototype.html) that change how quality affects entities. But if you want to change them in a way not supported by the modding API, you can create a hidden version of the building's prototype for each quality level, and then give those prototypes different properties. In control-stage scripting, you register a handler for when an item/building is placed, then replace it with the correct quality variant. You can also create quality variants for the items as well. The library mod [Quality Lib](https://mods.factorio.com/mod/quality-lib) has utilities for doing this. (LSA also has a different implementation of this, designed to work in combination with surface-based entity substitutions.) This magic trick is still not perfect - for example, upgrade planners won't work, and quality-variant items won't be usable in the same recipe, and will give different signals in chests. You can use the [deconstruction_alternative](https://lua-api.factorio.com/latest/prototypes/EntityPrototype.html#deconstruction_alternative) field to make filtered deconstruction planners work for quality variants.

* Some entity types, like offshore pumps and boilers, are limited in what they can do. For example, boilers can only take one input fluid and produce one output fluid, and offshore pumps can only produce one output fluid. You can work around this by changing them to furnace or assembling-machine types. For example, boilers in Nullius use the assembling-machine type. (This was also used back in Factorio 1.1 to make offshore pumps require burner fuel or electric power, for example by Industrial Revolution 3, but this is no longer necessary since the OffshorePumpPrototype now supports energy sources.)

* Suppose you want to allow a nuclear reactor to burn either normal fuel cells or breeder fuel cells, and you want the breeder fuel cells to take longer to burn but provide less energy, and therefore much less power. This can't be done by just changing the fuel value; a reactor has the same power for all fuels. You could implement this by changing the reactor to a fluid-burning generator, and then create a hidden furnace that takes in either of the two fuel cells and outputs both the spent fuel cell and a special "energy fluid" into a fluid box linked to the fluid-burning generator; the furnace's recipes produce different amounts/rates of the energy fluid. An alternative approach without hidden entities could be to instead have a different reactor prototype, and either allow the player to craft and place both of them, or add an in-game hotkey or GUI to toggle a reactor to the other type.

#### Magic tricks in LSA

Here are some magic tricks I've used in my own mods, mostly my WIP overhaul mod [Legendary Space Age (LSA)](https://github.com/StephenBarnes/LegendarySpaceAge).

* Suppose you want the number of rocket parts per rocket to vary by planet; for example low-gravity moons might require fewer rocket parts. You can create a hidden variant of the rocket-silo with a different value for the number of rocket parts per launch, and then replace rocket silos with the correct variant when a building or ghost is placed. This is currently implemented in LSA.

* Suppose you want to forbid placing certain machines too close to other machines. You can do this by placing invisible "exclusion zone" entities around the machine whenever a building or ghost is placed, and removing exclusion zones when a building is deconstructed. The exclusion zone entity has a collision layer that collides with some other buildings. This is currently implemented in LSA.

* Suppose you want to create a "condensing turbine" that's like a steam turbine but outputs the water for reuse. You can do this using the `fusion-reactor` prototype in the base game. However, you might want to give the fusion reactor lower efficiency than ordinary steam turbines, and the fusion reactor prototype has no efficiency field. So instead you can place a hidden crafting machine on top of the condensing turbine, which takes over the condensing turbine's steam input, and transforms it into a hidden "condensing turbine steam" fluid with lower energy. Then the condensing turbine takes this "condensing turbine steam" and outputs water. This is currently implemented in LSA. A similar condensing turbine is implemented in the Space Exploration mod, which uses an ordinary generator prototype (not outputting water) and an invisible furnace that consumes steam and outputs water plus "internal steam" for the generator.

* Suppose you want to implement beacons with a fixed built-in effect, instead of having module slots. You can implement this by creating a hidden beacon on top of the visible beacon, and putting special modules into the hidden beacon. This is currently implemented in LSA, for the "regulator" buildings.

* Suppose you want recyclers to always output normal-quality items, instead of the same quality as their input items. The recipe prototype modding API has no way to control this. But you could place a hidden furnace on top of the recycler. The recycler converts each input item into a hidden fluid for that item, which goes into the hidden furnace, which then transforms the fluid into the normal products of recycling. Since fluids have no quality, the quality of the output is always normal. This is implemented in my mod [Recyclers Erase Quality](https://mods.factorio.com/mod/RecyclersEraseQuality); the trick isn't perfect, because the Factoriopedia shows both of the recipes.

* Suppose you want to allow furnaces on surfaces that don't have an atmosphere with oxygen (like space platforms), but require an "air" input fluid. But you don't want to make 2 versions of every smelting recipe (with ambient air or explicit air input). You could use the same recipe everywhere, but when a furnace is placed on a planet with air containing oxygen, you create a hidden infinity pipe that supplies the air for free. Similarly, you might want to make stone furnaces vent their waste gases (like flue gas or coke oven gas), while steel/electric furnaces output this waste gas for other uses (like neutralizing alkali wastewater via carbonation, or making sulfuric acid from the sulfurous flue gas produced by smelting sulfide ores); but again you don't want to double the number of smelting recipes by giving each one a gas-venting variant. You could create a hidden fluid-venting entity on top of stone furnaces, which takes the gas output and produces pollution.

#### Magic tricks in Quezler's mods

Many of the [mods by Quezler](https://mods.factorio.com/user/Quezler) involve more advanced magic tricks. Below are some examples.

* [Beacon interface](https://mods.factorio.com/mod/beacon-interface) adds a beacon that can be set to have any module effects with any strength using an in-game GUI. This is implemented by creating 16 hidden modules for every effect, with strengths doubling - for example one module has +1% speed, the next one has +2% speed, the next one gives +4% speed, up to +(2^14)% speed, plus one for -(2^14)% speed. When the sliders are adjusted to say +100% speed, the mod writes +100% in binary (+64%, +32%, +4%, summing to +100%) and then inserts the corresponding modules into the beacon. If you set it to say -10% speed, it puts in the -2^14% module and then uses the other modules to boost it back to -10% speed (basically [two's complement](https://en.wikipedia.org/wiki/Two%27s_complement)).

* Building on the Beacon Interface mod, the [Apprentice assembler](https://mods.factorio.com/mod/apprentice-assembler) mod adds an assembler whose speed increases by 1% for each consecutive crafting recipe, then drops by 20% for each second the machine is idle. This is implemented by creating an invisible beacon inside the machine, and then setting its modules using the Beacon Interface mod. To count when products are finished or the machine is idle, the assembler has circuit connections to inserters on a hidden surface, which are enabled/disabled depending on the assembler's working state. When inserters are enabled, they pick up "offering" items on the hidden surface, causing the item-on-ground entity to be destroyed. The mod uses [register_on_object_destroyed](https://lua-api.factorio.com/latest/classes/LuaBootstrap.html#register_on_object_destroyed) so that it can run code when these "offering" items are destroyed, to update the modules in the hidden beacon.

* [Krastorio 2 air purifier helper](https://mods.factorio.com/mod/kr-air-purifier-helper) automatically places logistic requests for air filters in air purifier buildings. This is done in a way similar to the item-on-ground `register_on_object_destroyed` trick in Apprentice Assembler above, but using a different technique. When air purifiers are built, the mod creates an assembler on a hidden surface, doing some arbitrary recipe (namely wood to wooden chests). The mod places wood into the input slot of the assembler, giving the wood a health of 0.5, and uses `register_on_object_destroyed` to run code when the wood stack gets destroyed by the assembler running the recipe. It's necessary to give the wood a health, because `on_object_destroyed` only works on item stacks that store more than just their stack count. The assembler is connected via circuit link to a proxy chest that's linked to the air purifier's input slot; the circuit link makes the assembler only run when there are no filters in the air purifier / proxy chest. When it runs, the object gets destroyed, so the mod's `on_object_destroyed` handler gets called, which can then place the logistic request in the air purifier. I think this technique achieves the same effect as the item-on-ground technique, but without needing new prototypes and using fewer entities.

* (Note this mod has been updated since I wrote this description, might work differently now.) [Quality holmium ore returns more holmium solution](https://mods.factorio.com/mod/quality-holmium-ore-returns-more-holmium-solution) does what the title says. When a holmium chemical plant is built, an invisible assembler is placed inside it, and a set of 3 arithmetic combinators are created on a hidden surface. The holmium chemical plant's recipe for holmium solution produces both holmium solution and an item called "quality based productivity"; this is an item so that it gets the quality of the recipe's ingredients. This item is teleported to the hidden surface via a linked chest. There, combinators read the quality of the "quality based productivity" item and multiply it with the intended quality multipliers (supplied by a constant combinator). Inserters then use the calculated amount to move another item "coupon for holmium solution" from an infinity chest into another linked chest which teleports it back to the assembler inside the holmium chemical plant. That assembler then turns the coupons into holmium solution, outputted via a pipe linked to the chemical plant's output fluidbox.

* The [Washbox](https://mods.factorio.com/mod/washbox) mod allows you to create recipes that require holding an item in a fast-moving stream of fluid, without consuming the fluid. This is implemented by adding 3 additional entities that run in parallel to the visible "washbox" furnace that the player interacts with: a valve in, a "pumping speed furnace", and a valve out. The visible washbox's input fluidbox has two pipe connections: the visible input pipe, and a linked input; these are in the same fluidbox, so fluid in one is also in the other. The linked input is connected to the input of the in-valve, so it flows through that valve, into the pumping speed furnace. The pumping speed furnace has a recipe for every fluid in the game, turning 1 unit of the fluid into 1 unit of the fluid. The pumping speed furnace's output is then connected to the input of the out-valve, which has its output connected to the visible washbox's output fluidbox. The purpose of the pumping speed furnace is to measure the flow rate of the pipeline; the pumping speed furnace has a circuit connection to the visible washbox. The pumping speed furnace is set to emit a 1-tick signal "S" whenever it finishes crafting a recipe. The washbox is set to enable only if this signal S is at least 16, meaning that the pumping speed furnace finished at least 16 crafts in that tick. Each craft consumes and produces 1 fluid, so if it crafts 16 times per tick, that's 16 x 60 = 960 crafts per second, meaning that the pipeline's flow rate is at least 960 fluid per second. So in other words, the washbox is activated only if flow rate is at least 960 per second. (The visible washbox itself also consumes some fluid, but that's only around 1 per second, which is negligible compared to the 1000/second flow rate required.) This alternate flow path (valve to pumping speed furnace to valve) also allows fluid to flow past the washbox when it's not active.

Diagram for Washbox:
![](./diagrams/washbox.svg)

#### Magic tricks in other mods

* The base game only allows beacons to have energy sources with type electric or void. [Nonstandard Beacons](https://mods.factorio.com/mod/zzz-nonstandard-beacons) by protocol_1903 allows you to make beacons with burner, fluid, or heat energy sources. This is implemented by creating a hidden "source" assembler on top of the beacon. The source assembler copies the energy source from the beacon, and the beacon is given a void energy source. This source assembler has a fixed recipe with no ingredients or results, so it runs constantly while using power from the energy source. The source assembler has a circuit connection to a second hidden "manager" assembler, with a "sacrifice" item in the manager's ingredient slot. While the source assembler has energy, it continues running; when it runs out of energy, it stops running, which (via circuit condition) turns on the manager assembler. The manager runs one recipe that destroys the sacrifice item, triggering on_object_destroyed; this is the same trick mentioned above for Krastorio 2 Air Purifier Helper. The sacrifice-destroyed handler then disables the beacon, and flips the circuit condition, so that now the manager will only start again when the source assembler starts running. When the source assembler is given fuel again, it starts running, turning on the manager, which again destroys a sacrifice item, triggering another on_object_destroyed event; the handler then turns the beacon back on and flips the circuit condition back. This circuit-condition-flipping means that the manager only runs when the source assembler changes state (running out of power, or getting power again), so the mod only needs to run control-stage code when the power runs out or when power is restored. This has better performance than, say, checking every source assembler's power every nth tick and turning the beacon on or off. (There's also other details about what happens when the entity gets deconstructed, marked for deconstruction, etc. The beacon is given a flag to make it not deconstructable, but has deconstruction_alternative set so that beacon deconstruction planners will deconstruct the source assembler instead. When the source is marked for deconstruction, the beacon's modules are moved to the assembler, so that deconstructing it will return the modules as well as any fuel that was in the source.) (This mod has been updated after this description was written; TODO update for new version, which adjusts deconstruction stuff and adds new features not possible through the base game's beacon API.)

#### Possible additional magic tricks

Here's some additional ideas for magic tricks that I haven't seen implemented.

* Suppose you want items to have different spoilage timers on different surfaces - for example, iron plates might spoil to rusty iron plates on Nauvis, but not spoil in space; or liquid ammonia canisters might spoil to ammonia gas canisters on most planets, but on Aquilo the spoilage goes the opposite direction, from gas to liquid. You could achieve this by creating hidden versions of items with different spoilage timers, and then replace items with the right version whenever a cargo pod lands. To make them work with recipes, you would have to make alternate versions of each recipe for each surface. And to hide those recipes on some surfaces, you could create hidden versions of crafting machines on some planets. This approach still has some problems, such as item variants giving different signals in chests. I am not aware of any mod that implements this. As an alternative, you could make the items spoil to trigger results and then replace them at runtime; [Runtime spoilage library](https://mods.factorio.com/mod/runtime-spoilage-library) by SirPuck has functions for implementing this.

* Suppose you want to allow one recipe to use a wide range of alternatives for one of its ingredients. For example, you want to allow making char from any carbon-based fuel item (coal, wood, fruit, etc.) but you don't want a separate recipe for every possible input. You can achieve this without magic tricks by making this a specific "fuel type", and creating a special building that uses this fuel type, and then the recipe has no explicit ingredients. (This specific example is implemented in LSA.) But sometimes that doesn't work, for example because you don't want to give fluids a fuel value because you don't want to allow them in all fluid-burning buildings. (Entities with fluid-burning energy source can have a filter to allow only one fluid, but if you want to allow more than one, there is no way to do that; fluids don't have fuel types like items do.) For example, let's say you want to make a recipe that requires an "inert atmosphere" fluid as an ingredient, and this inert atmosphere can be many different fluids (nitrogen, argon, vacuum, etc.). One solution is to create a hidden furnace which takes any of those different fluids as inputs, and produces the "inert atmosphere" fluid as output, which goes directly into the assembler that then uses it as an ingredient. From the player's perspective, it looks like the assembler has a fluid input for "inert atmosphere", but you can connect this to a pipe carrying any of those alternatives (nitrogen, argon, vacuum, etc.) and it magically gets converted into the "inert atmosphere" fluid. This approach doesn't work as cleanly for item ingredients rather than fluid ingredients.

* Suppose you want to give a specific assembler machine neighbor bonuses that apply when both machines are operating, similar to nuclear reactors. For example, you could give furnaces a fuel efficiency bonus for every adjacent running furnace due to the heat being shared. Or you might want to change nuclear reactors to an assembling machine, so that you can make them use heat shuttle items (see "heat shuttle system" below) to absorb the output heat, instead of outputting heat into heat pipes. Here is one way you could do this:
	* When the assembler is placed, create a hidden beacon on top of it, with its effect extending outward 1 tile from each edge of the assembler. So for a 3x3 assembler the beacon would have a 5x5 area of effect.
	* To activate the beacon only when the assembler is active, you could make a proxy container for the beacon's module inventory on a hidden surface. Connect a circuit wire from the assembler to inserters on the hidden surface. When the assembler is active, an inserter moves a module into the beacon's proxy container. When the assembler is inactive, a second inserter removes the module.
	* Now a problem is that each assembler will be affected by its own beacon. To fix that, we imagine that all the tiles of the map are covered with a 4-color checkerboard (see picture below); if the assembler is 3x3, then each cell of the checkerboard is 3x3. When an assembler is built, you replace it with a different assembler prototype according to the color at its center on this checkerboard - an assembler with its center on a red square gets replaced with a "red-assembler" prototype, and same for all the other colors. We also use a different module type for each color, so a red assembler's hidden beacon gets a red module. Then we set it so red assemblers are only affected by non-red modules, and similar for other colors. The point of all this is that an assembler will never be affected by its own beacon (since the module has the same color as the assembler), but assemblers that neighbor each other will always be of different colors, so they'll be affected by each other's modules.
		* (You need at least 4 colors for square assemblers larger than 1x1. If they're 1x1, 2 colors is enough. Also, none of this works for non-square assemblers that can be rotated.)

![](./diagrams/neighbor_bonus_3x3.png)


### General advice on coding

* Learn basic programming. Use loops. Factor out repeated code into functions.
* Use the section above on dev environment. Set up an IDE like VSCode with a Lua LSP and Factorio Modding Toolkit.
* Consider asking AI to improve your code. Consider using an IDE with built-in AI like Cursor; ideally learn to code before using this so you can tell when it screws up.
* Avoid control-stage scripting. When possible, make all necessary changes in the prototype stage.
* Avoid running code in on_tick events. Sometimes you will need to do that anyway; in that case, try to do the minimum work and exit as soon as possible.
* Read mods written by other people.

### Specific advice on coding

* Lua is reference-based, similar to other scripting languages like Python. For example if you define `x = {1, 2, 3}` and then `y = x`, then there is only one table in memory, with two variables holding references to that same table. If you modify `y`, that one table is modified, so printing out `x` will also show the modifications. You can use `y = table.deepcopy(x)` to create a copy of the table, which can then be modified without affecting the table referenced by `x`. This `table.deepcopy` function is created in the base game's util.lua.
* In the control stage, many variables should be stored in the [storage](https://lua-api.factorio.com/latest/auxiliary/storage.html) table (which was called `global` before the 2.0 update). Storage is preserved across saving and loading, and is synchronized between players in multiplayer. If you use variables in the control stage that are not in storage, and they ever have different values for different players, you can cause a [desync](https://wiki.factorio.com/Tutorial:Modding_tutorial/Gangsir#Multiplayer_and_desyncs) which will crash multiplayer games.
* During the data stage, all mods share the same workspace, so for example globals defined in one mod are visible to other mods that run later, and can be overwritten.
	* So for example if you define a global like `mod_name` in shared.lua, which is imported in data.lua, and then use the global in your data-updates.lua, this will appear to work when your mod is the only mod enabled. But when you run your mod with other mods loaded, those mods can overwrite that global, so you should re-import shared.lua in data-updates.lua.
* During the control stage, mods run in separate VMs, so they do not share global variables. For mods to interact, you can use [remote interfaces](https://lua-api.factorio.com/latest/classes/LuaRemote.html) to define a function in one mod and call it in another mod. If you call a remote interface with arguments, those arguments are copied, so for example if you pass a table as argument and the remote function modifies the table, the original table in your mod will not be modified. You cannot pass functions as arguments.
	* Because mods run in separate VMs, to inspect their data using the in-game console you can run commands in the VM of a particular mod, for example: `/c __my-mod__ game.player.print(serpent.dump(storage))`
* You can `require()` code files from other mods in the data stage or control stage. In the control stage, this will load the other mod's file in your mod's VM, not their VM.
* Lua has [string-matching functions](https://www.lua.org/pil/contents.html#20) but they do not use conventional regexes. Instead they use a unique syntax that is less powerful than ordinary regexes.
* A lot of Lua tutorials will spend a lot of time on metatables, classes, and inheritance. Most of this is not really necessary for Factorio modding. If you want tables in `storage` to keep their metatables, you need to call [register_metatable](https://lua-api.factorio.com/latest/classes/LuaBootstrap.html#register_metatable).
* When defining prototypes in code, you can explicitly write the entire table. Alternatively, you can use `table.deepcopy` to copy an existing similar prototype, then change various fields, like the name, icon, `minable.result` or `place_result`, etc. The deepcopy approach has the disadvantage of unexpected interactions with the rest of your mod, or other mods, since the values you think you're copying might have been changed elsewhere. The explicit approach has the disadvantage of needing to set all the fields explicitly, so you risk forgetting to set some more subtle fields like item sounds (pick, drop, inventory_move) and crafting machine tints for recipes. For large overhaul mods the best approach is probably to explicitly define prototypes but using a helper function to easily set / avoid forgetting to set the subtler fields.
* Some modding effects may require you to run [`surface.find_entities_filtered()`](https://lua-api.factorio.com/latest/classes/LuaSurface.html#find_entities_filtered) on every nth tick so that you can update all buildings/whatever of a specific type on all planets. You may expect this function to be fast, since the engine frequently needs to find all pipes or enemy bases or whatever to update them, so you might think it already has lists of entities by type/name ready to go. However, this is not the case, the function is slow. In my experience, calling this function will cause noticeable lag, like dropping multiple frames every time your script runs. Instead, you can should rely on caching, meaning you run `find_entities_filtered` once when the game starts, and store it in `storage.whatever`. You can listen to events like `on_built_entity` and `on_player_mined_entity` to update the cache without re-running the slow scan.


# Advice on overhaul mod design

I haven't actually finished any overhaul mods, but I will try to share the things I think I've learned so far.

## Goals

There are several goals you could try to achieve in an overhaul mod, and it's important to have clarity on which purposes you want to achieve, and which ones you don't care about. For example:

* You can add lots of neat things to use or do - new vehicles, new guns/grenades/landmines, new planets.
* You can add new game systems using control-stage scripting - such as spaceship docking in Space Exploration, or the ultracube in Ultracube.
* You can aim to make the game significantly more difficult, or easier.
* You can try to make complex recipe systems that interact with each other in interesting ways, creating puzzles.
* You can try to aim for chemical/industrial realism.

### Realism as a goal

A full commitment to realism often requires doing things that are at odds with ordinary game design goals, such as:

* Having lots of metals that have almost the same uses
* Many waste byproducts
* Many items/fluids that are involved in only one recipe chain
* Many items/fluids with complex chemical names that are not memorable for people who aren't industrial chemists.

You can consider compromising slightly on realism to avoid some of these issues, such as:

* Merging multi-step processes into single recipes, to eliminate intermediate items that would only have one source and use in the mod
* Merging together chemicals with almost the same sources and uses (such as merging sodium and potassium, meaning that "salt" represents both sodium and potassium chloride, and "alkali" ash is either soda ash or potash, and "niter" is both sodium and potassium nitrate)
* Using more well-known common names for chemicals (like "lye" instead of sodium hydroxide)
* Naming substances based on their role in the mod instead of their chemistry, for example renaming ferric chloride solution to "etchant", trichlorosilane to "silicon gas", or hematite to "iron ore"

## Looking at other overhaul mods

It is helpful to look through other overhaul mods to get ideas for design. I don't think anyone has actually played all the overhaul mods, but you can get 90% of the ideas in 1% of the time by just loading up a mod and looking through the Factoriopedia (or Recipe Book). I would recommend first looking at Space Exploration, Industrial Revolution 3, Nullius, and Bob/Angel. You will need to download Factorio 1.1 off the Wube website for some of those.

## General advice

* Consider making charts of recipes and items with arrows between them, to help understand your recipe systems. I use [yEd](https://www.yworks.com/products/yed/download) for this.
* Consider making a writeup of your mod's design goals and your current design, and then pasting the entire thing into an AI. At the top, put a question or aspect you're trying to design. The AI will sometimes have good ideas, and they have a greater breadth of knowledge about real industrial processes than any human being. I have found Gemini 2.5 Pro to be fairly good at this, although its designs tend to be excessively complex and focused on realism. Sonnet 4 and O3 are worse than Gemini 2.5 Pro in my experience, and are more prone to persistent misunderstandings about what is possible in Factorio, such as thinking that Factorio is a 3D game, or thinking that two recipes producing the same item can produce that item with different properties, etc. AIs also have an annoying fixation on environmentalism (which is fine in real life, but not appropriate for Factorio) and may refuse to help with recipes for explosives, poisons, nuclear tech, etc. 
	* You can ask the AI to output its recipe suggestions as a DOT graph, then use the scripts in this repo (in `graphs` folder) to import them into yEd or convert yEd back into text.
* Reign in the sadism. Something that seems like an interesting limitation / balance change when you're in the design stage can often turn into a tiresome slog when you actually play the game. Instead of completely banning things like logistic bots, cargo drops, or whatever, consider just not doing that, or just nerfing them.
	* There is an opposite design problem, where a mod adds some new tool that is better than an existing tool in every way. For example, adding a vehicle that is cheaper, faster, and stronger than a tank. This effectively removes as much content from the game as it adds, because there is no longer any reason to use the worse thing. That said, I haven't seen any Factorio overhaul mods that suffer from this issue. Compare to Minecraft modding where it's the other way around - lots of mods adding overpowered gear, few mods making the game more difficult in an interesting way.
* Consider using an unrealistic color scheme to differentiate items/fluids. This repo has a `colorscheme-visualizer` folder that you can use to visualize relations and automatically pick analogous colors. The base game uses unrealistic colors (for tungsten and holmium) because if they were realistic they would all be gray like iron/steel plates, making them harder to differentiate and making the planet's color palette uglier. The base game also uses unrealistic colors for iron/copper ore so they match the plate colors. For a substance like magnesium chloride, you could make an icon with the colors of magnesium and chlorine in different parts of the sprite, to help people quickly understand the relations between items/fluids in your mod.
* Instead of having like 10 different types of ore patches, consider deriving more types of resources from a smaller set of minable patches. I don't think most players like having to set up separate mining outposts and unloading for many different ores; vanilla has 5 types of minable patches on Nauvis which is already enough to be tiresome. You can realistically derive various substances from sorting/washing/leaching existing minables, which are rationalized as mixtures of different minerals. Processing stone can give sand, gravel, calcite, clay, gypsum, phosphate rock, silica, chromite, alumina, rare earths. Raw water from offshore pumps could be boiled or filtered for algae and magnesium/sodium/potassium salts. Slag from smelting one ore could be leached to get another ore. Systems similar to this can be seen in Industrial Revolution 3, Angel's mods, and Seablock.

## Testing overhaul mods

Currently Legendary Space Age includes an `autodebug` directory for automatic data-stage debugging, by running tests like [ensuring recipes can't create water out of nothing](https://github.com/StephenBarnes/LegendarySpaceAge/blob/master/data/autodebug/check-conservation-rules.lua#L116). This is still a work in progress, since much of the overhaul's recipes and items are not implemented yet. The current implementation relies on manually assigning conserved quantities to items/fluids (there's X elemental carbon in each carbon item, and Y elemental carbon in each unit of crude oil fluid, etc.) and checking there's no recipes that create the conserved quantity on net at max productivity. A better implementation would only need a set of seed assignments and then use a matrix solver to check whether there's any way of assigning values to the rest of the items that avoids positive-net recipes.

[Here](https://alt-f4.blog/ALTF4-48/) is an Alt-F4 writeup of how automated unit-testing was done for Angel's mods.

## Recipe patterns

Most recipe systems in the base game are solvable by running some calculations, or using a matrix calculator like the Factory Planner mod, to compute the numbers of machines and rates of ingredients/products needed for a desired output rate. Then the only work left is building the machines and routing belts. While there is some room for creativity in laying out the machines, most players have already explored that design space, so the actual building work is more like a chore than a puzzle. There are no alternative strategies or tradeoffs, just the one correct ratio, and any deviation from that correct ratio is suboptimal and pointless.

Most recipe systems in the base game (pre-DLC) suffer from this issue - they are easily solvable, and therefore boring, and this is exacerbated by the fact that experienced players have already encountered and solved them many times. These recipes generally have certain simplifying properties:

* acyclic: products are not used in the chain of recipes that create those same products
* no spoilage: none of the items in the recipe system spoil
* no locality: machines to handle most recipes can be built anywhere on the map
* single-source: each product has a single recipe that produces it
* single-goal: many recipes produce only a single useful product

One possible goal of an overhaul mod (and my primary goal in designing LSA) is to create recipe systems that are interesting and pose a challenge even to players who are experienced with the base game and equipped with Factory Planner. Breaking only one of the properties above is generally not enough to make a recipe system interesting. Generally you need to break multiple rules, or add new mechanics using runtime scripting.

Below I've collected some recipe "patterns" that can be implemented in an overhaul mod to add challenges and puzzles. Most of these are abstract patterns where you can fill in the blank with any items/fluids/buildings in your mod.

### Concave Pareto frontiers

The player wants to make two different products A and B, using 3 recipes with similar ingredient cost.

* Recipe 1: produces 5 A
* Recipe 2: produces 5 B
* Recipe 3: produces 3 A + 4 B

Recipe 3 is more efficient in raw materials than 1 and 2. So if the player wants maximum productivity, they need to implement recipe 3 as much as possible; but if there's an imbalance, where they need more A than B or vice versa, they need to switch those machines to one of the inefficient single-product recipes 1 or 2, giving them an opportunity to build clever circuitry.

The pattern can be extended to more than 2 products or more than 3 recipes. We can also use this pattern for ingredients. For example, recipes 1-3 each produce the same item, but recipe 1 consumes 5 X, recipe 2 consumes 5 Y, and recipe 3 consumes 1 X + 1 Y, so recipe 3 is cheaper and therefore preferable unless you have an excess of one of the inputs X or Y.

Example: A "mixed olefins" fluid is separated into butene, ethylene, and propylene. The last 2 can be made into polyethylene/polypropylene flakes, which can each be made into plastic. Or you can make plastic more efficiently by compounding both types together. But the compounding recipe has them in a different ratio than the recipe producing them. Butene can additionally be cracked into ethylene/propylene, changing the ratio. Maybe some other petrochem recipe also produces butene, making the ratios change again depending on how much that other recipe is used.

### Catalysts transforming into each other

* Recipe A: raw materials + catalyst 1 -> product + catalyst 2
* Recipe B: raw materials + catalyst 2 -> product + catalyst 1

We suppose that these catalysts are expensive to manufacture, and that there's some reason to situate these recipes in different locations, perhaps on different planets. The player could transport the catalyst 2 from recipe A's location to recipe B's location, transforming it back into catalyst 1, which is transported back. Or they could produce each catalyst locally and discard the transformed catalyst. This creates a tradeoff between manufacturing costs and logistical complexity that the player can resolve in various ways. Alternatively, the player could transport raw materials to a central processing station. We could add additional costly recipes to directly transform each catalyst into the other, creating a third option (locally transforming the catalyst before reuse).

Example: In Space Exploration, there are two different recipes for the resource naquium, using different raw materials that appear on different planets. These recipes require either anion or cation beads as catalysts, which are transformed into the other type when used.

### Spoiling to goal, then to waste

A raw material spoils to a goal item, which then spoils into a waste product. The player will want to produce the raw material and store it in a buffer to wait for it to spoil into the goal item; but the goal item shouldn't be buffered, since it will spoil.

Example: a recipe produces wet resin, which isn't very useful. This resin spoils into sticky resin, which is useful for making circuits etc. Sticky resin spoils into hardened resin, which is useless.

Additional recipes can add more complexity and alternative ways of dealing with the challenge. We could add water or acetone to wet resin, resetting its spoilage timer at the cost of some resources. We could add a fast-forward recipe that dries wet resin directly to sticky resin at the cost of heat shuttles. We could add reprocessing of dried resin by crushing it and adding a solvent to get wet resin again, at the cost of some total product. We could add a recipe for making plastic by combining crushed dry resin with wet resin.

### Multiple inheritance of spoilage

DNA sample (partly spoiled) + raw materials -> DNA sample (inheriting spoilage) + bacteria (also inheriting spoilage)

Both DNA samples and bacteria spoil into waste. So the player needs to decide how many times to use a given DNA sample, before spending additional resources to make a fresh DNA sample. Using almost-spoiled DNA samples will produce almost-spoiled bacteria, which may spoil before they can be used. So the decision of how often to make fresh DNA samples depends on how quickly the downstream infrastructure can handle the partly-spoiled bacteria.

### Alternate routes with differing productivity

Crude oil is fractionated into heavy oil, light oil, and petroleum gas. Each of these fractions can be used to make solid fuel, but with different productivity for each. Fractions can also be cracked into lighter fractions. All fractions also have other uses, like lubricant and rocket fuel. So the player must choose which products to make from which fraction, how much to crack, and set up a system to automatically balance all these routes to avoid one fraction backing up and stalling production.

### Extreme random output variance, with spoilage

Each second, a borehole mining drill produces 1 stone, but also has a 1/1000 chance of producing 1000 diamonds. The player is tempted to build logistics to carry 1 diamond per second, since that's the expected rate, but that will cause logistics to be insufficient when 1000 diamonds are produced at once, clogging up the borehole drill's output line until the diamonds are removed. So there's also a case for building much greater logistics capacity.

We can make this more interesting by adding spoilage. Suppose a borehole drill on Gleba has a 1/1000 chance of producing 1000 neural tissue, which can spoil. The neural tissue must be combined with nutrients to produce science packs. So the player wants to build a buffer of nutrients to handle lots of neural tissue as soon as it arrives. But the nutrients also spoil, so a buffer of fresh nutrients is costly to maintain, creating a tradeoff.

### Seasonal output variance, with shorter-than-season spoilage

Nectar mites on Gleba can be fed nutrients to make them produce nectar, but only during the "nectar season" which lasts for 30 minutes, alternating with a 30-minute "dry season". (We implement this using control-stage scripting to enable/disable a specific machine at certain times.) Nectar is used to breed flies, which are needed for some product. Both flies and nectar spoil to waste in less than 30 minutes. So during the dry season, all the nectar and flies will spoil, and there won't be any flies to breed in the next nectar season. We add a recipe to preserve nectar at some cost. So the player must figure out how much nectar needs to be stored, and build systems to decide how much nectar to store. For more challenge, we can make each nectar season have a random productivity level, so the amount of nectar to store in each season can be optimized automatically using combinators.

### Seasonal shuttling

Adding to the previous example, we could alternate the nectar season with a nectar-mite breeding season. Nectar mites spoil to waste, so they must be bred using nutrients, and this must be done in a specific location different from the nectar fields. When nectar season ends, the player needs to transport mites from the nectar fields to the breeding region, breed them, then transport them back for the next nectar season. This requires circuitry to trigger a discrete action of transporting them to the other region.

### Building/recipe location constraints

We can restrict the placement of buildings/recipes, or apply bonuses/maluses dependent on positioning, which can encourage interesting factory layouts. Examples:

* We could require that certain crops are farmed in specific regions, so the player has to transport these fruits back to base.
* We could make nectar mites producing nectar pollinate the surrounding tiles for a certain period of time. A certain crop can only grow on these pollinated tiles. This would require control-stage scripting to swap the tiles to pollinated tiles and back.
* We could give a bonus to productivity when furnaces are built close to each other, since they share the heat. (Probably by placing invisible beacons inside the furnaces, and changing their modules when adjacent furnaces are built/deconstructed.)
* You can ban placing certain buildings too close to other buildings of the same type. LSA currently implements this using hidden "exclusion zone" entities, for borehole mining drills, air collectors, and telescopes. Players could deal with this by spreading certain buildings throughout the base, creating messy factory designs, or they could build them apart from the main base, requiring a large area.

### Spoiling modules

The engine supports modules spoiling into non-module items. Making modules spoil could create interesting challenges for beacon layouts that need inserters into and out of beacons. One issue with this is that inserters can't insert/remove modules from most machines (though they can interact with beacons). I have made a mod [Module Switcher Attachment](https://mods.factorio.com/mod/ModuleSwitcherAttachment) that provides a way to insert/remove modules from other machines using proxy containers. The mod [Any Inventory Insertors](https://mods.factorio.com/mod/any-inventory-inserters) has a cleaner solution where you can use a custom GUI to set which inventory an inserter interacts with. Spoiling modules are implemented in LSA - green/red/blue/white circuits are "primed"/"superclocked" to make modules, which spoil back into circuits.

### Factor system

In LSA, infrastructure is manufactured from "factors", which are intermediate items defined by their function rather than their composition. Each factor has multiple alternative recipes, e.g. a "panel" can be crafted from an iron plate or a copper plate or steel or wood + resin or even glass. Then infrastructure items like machines are made from factors, instead of directly from iron plates etc. This mix-and-match system allows the player to build their factory from whatever materials are available on each planet, and build circuits to switch between alternative recipes to use the resources that are most abundant at a given time. It also allows you to wildly change the resources available on different planets, for example you could make metals completely absent from Gleba, and add alternate recipes making factors from local materials.

I got this idea from [Galdoc's Manufacturing](https://mods.factorio.com/mod/galdocs-manufacturing), which implements a similar system but more elaborate.

### Heat shuttle system

(This is only around 10% implemented in LSA currently.)

In LSA, some items function as heat providers or absorbers. Hot items (such as hot steam canisters, hot metal blocks, lava canisters) are heat providers, and can be used as fuel by machines like kilns or endothermic plants; this cools the items down into respectively cold water canisters, cold metal blocks, solidified lava canisters. This is accomplished by making a custom fuel type with a `burnt_result`. Exothermic processes (like hydrating quicklime, making sulfuric acid, or cross-neutralizing acidic and basic wastewaters) use the cold versions of the heat absorbers as fuel, turning them into hot variants that can be used elsewhere; this is achieved by creating another custom fuel type for the cold versions, this time with `burnt_result` set to the hot version.

This system adds a lot of loops and interdependencies to the factory, because sections of the factory that were previously unrelated can now be linked in order to make use of waste heat from one process to provide heat to another process. For example, foundries can cast hot metal plates, and then an endothermic plant can cool down those plates to heat up steam for electricity or to supply heat to a molten-salt electrolysis plant.

Hot items spoil into cold ones. (Ideally this spoilage would depend on the planet, but I don't think that's possible to do cleanly with the current API; see note in the section on "magic tricks" above.) On spaceships, heat shuttles are also used to dissipate heat in radiators. To balance supply and demand, heat shuttles can be deliberately heated in furnaces, or cooled in cryogenic plants. Some heat shuttles can be charged chemically, e.g. water can be added to quicklime cartridges to make hot slaked-lime cartridges. Some heat shuttles can be emptied and refilled (e.g. water canisters can be used for cooling, then vent steam and refill with water) and for some shuttles (such as cold slaked-lime cartridges) this is the only way to reuse them. There are some subtleties, for example emptying and refilling steam canisters wastes some percentage of the steam to punish exploits where you can fill and empty steam canisters to delay spoilage indefinitely.

There is an analogous system of "cold shuttles" like liquid ammonia canisters, which can be used to fractionate natural gas or cryogenically separate air into liquid oxygen/nitrogen.

On Vulcanus, heat is very cheap (lava in tungsten canisters), while cooling is expensive. On Aquilo, cooling is very cheap (liquid ammonia) but heat is expensive.
