# Scripts in this repo

This repo contains various scripts I've collected while developing Factorio mods.

In the `image-scripts` folder, the `.sh` scripts are Bash scripts which run natively on Linux. You can probably also run them on Mac, or on Windows using tools like Cygwin, but I haven't tested them on those systems. The `.py` scripts are Python, so should work on all systems.

Feel free to send pull requests if you make any changes or make new scripts. Most of these scripts were written by AI; competent AIs (like Gemini 2.5 Pro, or Claude 4 Opus) are generally able to write scripts like this faster than writing them yourself.


# Resources for making Factorio mods

Below I've collected links to resources for making Factorio mods, plus some notes on modding. Underneath that there's also some thoughts on designing overhaul mods. Feel free to post an issue if you know of anything I should add.

## Basics

Crucial background: Factorio mods run in 3 stages: settings, then data/prototype, then control/runtime. [More details.](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html) The data/prototype stage uses different types than the control/runtime stage, so the [prototype API docs](https://lua-api.factorio.com/latest/index-prototype.html) are separate from the [runtime API docs](https://lua-api.factorio.com/latest/index-runtime.html). Factorio uses a custom version of Lua with [some changes](https://lua-api.factorio.com/latest/auxiliary/libraries.html).

[The wiki has a general introductory modding tutorial.](https://wiki.factorio.com/Tutorial:Modding_tutorial/Gangsir)

## Communities

* [Official Discord channel for mod development](https://discord.com/channels/139677590393716737/306402592265732098)
* [Official forums](https://forums.factorio.com/index.php)
* [Subreddit](https://www.reddit.com/r/factorio/)
* There are also various community-run Discord servers - The Foundry, Earendel, probably others I am unaware of.

## Graphics

### Ready-made graphics

When using graphics from other people, be aware of their licenses, which may have various requirements, such as requiring you to release your mod under the same license, requiring attribution, etc.

* [Free graphics for modders](https://github.com/snouz/factorio_free_graphics_for_modders) collected by Snouz - large collection of graphics from various mods with fairly open licenses.
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

Note that there are [some issues](https://forums.factorio.com/viewtopic.php?t=98732) with using layered icons that may cause minor graphics bugs that are hard to notice in development. To avoid these issues, you could write a script that does the layering+shifting+tinting on the image files on your local computer, then ship the finished graphics; I haven't done this yet. For the specific issue with icon shadows, you can set `draw_background = true` on multiple layers, if they don't overlap. You can also add an additional back layer that's almost transparent, purely to draw larger background shadows.

For icons of reflective things (like metal items or fluid drops), you can sometimes improve their appearance by splitting the icon into a base layer and a mostly-transparent highlights layer with the bright reflective parts. Then tint the base layer, and overlay it with the *untinted* highlights layer, so that the highlights are still white.

### AI-generating graphics

You can use Midjourney to generate icon sprites. Unfortunately Midjourney is tuned to generate either realistic photographs of young women or generic fantasy cartoon slop, not Factorio-style sprites of industrial intermediates, so it may take some wrangling to get it to generate what you want. Once you've generated one good image, you can generate variations of it to use as [sprite variations](https://lua-api.factorio.com/latest/prototypes/ItemPrototype.html#pictures) for items. Ask for the sprites on a plain black background, and then edit them before use; some of the scripts in this repo (like `quarter_image.sh` and `transparent_background.sh`) were made specifically for this purpose.

Gemini models are useful for adding things to images. For example, I used Gemini to make the condensing turbine graphics for Legendary Space Age, by editing the base-game's steam turbine graphics to add a lid over the turbine part. These models are currently bad at generating new images, but good at making edits.


## Coding

### Tutorials for aspects of coding

* [Using settings in mods](https://wiki.factorio.com/Tutorial:Mod_settings)
* [GUI modding](https://github.com/ClaudeMetz/UntitledGuiGuide/wiki)
* [Porting mods to 2.0](https://github.com/tburrows13/factorio-2.0-mod-porting-guide)
* [Localization](https://wiki.factorio.com/Tutorial:Localisation)

#### World generation / autoplace / noise expressions

Factorio's world generation system changed significantly in the 2.0 update. [This](https://togos.github.io/togos-example-noise-programs/) was a good tutorial for the old system. The new system works almost the same conceptually, but noise expressions are now written as strings instead of Lua tables. I am not aware of any tutorials for the new worldgen system. If you want to do worldgen coding, I would recommend understanding that tutorial conceptually, then looking at the base game's Lua code and [API docs](https://lua-api.factorio.com/latest/auxiliary/noise-expressions.html).

### Dev environment

* [Factorio Modding Toolkit](https://github.com/justarandomgeek/vscode-factoriomod-debug) includes a VSCode extension making the program aware of the Factorio API, which can help to catch errors and provides shortcuts to documentation.
* I recommend opening Wube's Lua code directory in a separate IDE window. On Linux+Steam it's at `~/.local/share/Steam/steamapps/common/Factorio/data/` but yours might be in [other places](https://wiki.factorio.com/Application_directory). You can search through this to find the base game's code for defining prototypes.
* I recommend making a simple mod with only an `info.json` file with dependencies on several testing mods so you can toggle them all on and off easily. Give it a name like "○○○○○○ testing mods" so it's at the top of the mod list. My current mod has dependencies on `"EditorExtensions", "factoryplanner", "creative-space-platform-hub", "circuit-connector-placement-helper"`.

### Libraries

Some code libraries that you can add as dependencies of your mod. You can import Lua files from other mods into your mod using `require "__OtherMod__/directory/filename"`.

* [flib / Factorio Library](https://github.com/factoriolib/flib) is a set of utility functions.
* [PlanetsLib](https://mods.factorio.com/mod/PlanetsLib) has tools for creating planets and moons.
* [Quality Lib](https://mods.factorio.com/mod/quality-lib) by Davoness has tools to change values of items/entities for different quality levels; see the "magic tricks" section below.
* The base game code contains some useful functions, in `core/lualib`.

### Starter/template mods

These are mods you can fork and edit instead of writing a mod from scratch.

* [Factorio Example Mod](https://github.com/ZwerOxotnik/factorio-example-mod) by ZwerOxotnik

### Magic tricks

For most simple changes you might want to make, like changing recipes or properties of items and buildings, you only need to edit prototypes. But in many cases, prototypes will not have a field that does what you want. In this situation, it is often still possible to achieve your aims, but you will need to resort to "magic tricks" involving a combination of hidden prototypes and control-stage scripting.

(Alternatively, you can post a [request](https://forums.factorio.com/viewforum.php?f=28) for Wube to add the API feature that you want, but it will probably not be added. There has also been one attempt that I am aware of to enable direct modding of the Factorio engine, outside of the Lua modding system, but I can't find the repo now and that project was eventually abandoned, partly because allegedly Wube said they would at some point open-source the engine.)

Generally these "magic tricks" involve the creation of hidden entity prototypes / items / surfaces, along with control-stage scripting to create or replace things using these hidden objects. I call them "magic tricks" because they involve doing a bunch of behind-the-scenes stuff not visible to the player to create effects that seem impossible within the engine.

#### Magic trick examples

* Suppose you want to make properties of entities change depending on their quality. Currently the modding API has extremely limited ability to change how quality affects entities. Instead, you can create a hidden version of the building's prototype for each quality level, and then give those prototypes different properties. In control-stage scripting, you register a handler for when an item/building is placed, then replace it with the correct quality variant. The library mod [Quality Lib](https://mods.factorio.com/mod/quality-lib) has utilities for doing this. (LSA also has a different implementation of this, designed to work in combination with surface-based entity substitutions.) This magic trick is still not perfect (e.g. upgrade planners won't work, and quality-variant items won't be usable in the same recipe, and will give different signals in chests).

* Some entity types, like offshore pumps and boilers, are limited in what they can do. For example, boilers can only take one input fluid and produce one output fluid, and offshore pumps can only produce one output fluid. You can work around this by changing them to furnace or assembling-machine types. For example, boilers in Nullius use the assembling-machine type. (This was also used back in Factorio 1.1 to make offshore pumps require burner fuel or electric power, for example by Industrial Revolution 3, but this is no longer necessary since the OffshorePumpPrototype now supports energy sources.)

* Suppose you want to allow a nuclear reactor to burn either normal fuel cells or breeder fuel cells, and you want the breeder fuel cells to take longer to burn but provide less energy, and therefore much less power. This can't be done by just changing the fuel value; a reactor has the same power for all fuels. You could implement this by changing the reactor to a fluid-burning generator, and then create a hidden furnace that takes in either of the two fuel cells and outputs both the spent fuel cell and a special "energy fluid" into a fluid box linked to the fluid-burning generator; the furnace's recipes produce different amounts/rates of the energy fluid. An alternative approach without hidden entities could be to instead have a different reactor prototype, and either allow the player to craft and place both of them, or add an in-game hotkey or GUI to toggle a reactor to the other type.

#### Magic tricks in LSA

Here are some magic tricks I've used in my own mods, mostly my WIP overhaul mod [Legendary Space Age (LSA)](https://github.com/StephenBarnes/LegendarySpaceAge).

* Suppose you want the number of rocket parts per rocket to vary by planet; for example low-gravity moons might require fewer rocket parts. You can create a hidden variant of the rocket-silo with a different value for the number of rocket parts per launch, and then replace rocket silos with the correct variant when a building or ghost is placed. This is currently implemented in LSA.

* Suppose you want to forbid placing certain machines too close to other machines. You can do this by placing invisible "exclusion zone" entities around the machine whenever a building or ghost is placed, and removing exclusion zones when a building is deconstructed. The exclusion zone entity has a collision layer that collides with some other buildings. This is currently implemented in LSA.

* Suppose you want to create a "condensing turbine" that's like a steam turbine but outputs the water for reuse. You can do this using the `fusion-reactor` prototype in the base game. However, you might want to give the fusion reactor lower efficiency than ordinary steam turbines, and the fusion reactor prototype has no efficiency field. So instead you can place a hidden crafting machine on top of the condensing turbine, which takes over the condensing turbine's steam input, and transforms it into a hidden "condensing turbine steam" fluid with lower energy. Then the condensing turbine takes this "condensing turbine steam" and outputs water. This is currently implemented in LSA. A similar condensing turbine is implemented in the Space Exploration mod, which uses an ordinary generator prototype (not outputting water) and an invisible furnace that consumes steam and outputs water plus "internal steam" for the generator.

* Suppose you want to implement beacons with a fixed built-in effect, instead of having module slots. You can implement this by creating a hidden beacon on top of the visible beacon, and putting special modules into the hidden beacon. This is currently implemented in LSA, for the "regulator" buildings.

* Suppose you want recyclers to always output normal-quality items, instead of the same quality as their input items. The recipe prototype modding API has no way to control this. But you could place a hidden furnace on top of the recycler. The recycler converts each input item into a hidden fluid for that item, which goes into the hidden furnace, which then transforms the fluid into the normal products of recycling. Since fluids have no quality, the quality of the output is always normal. This is implemented in my mod [Recyclers Erase Quality](https://mods.factorio.com/mod/RecyclersEraseQuality); the trick isn't perfect, because the Factoriopedia shows both of the recipes. Also note that that mod positions the hidden fluid input/output inside the machine; it would be better to set the fluidbox connection type to ["linked"](https://lua-api.factorio.com/latest/types/PipeConnectionDefinition.html#connection_type) and then link the two machines when they're placed.

* Suppose you want to allow furnaces on surfaces that don't have an atmosphere with oxygen (like space platforms), but require an "air" input fluid. But you don't want to make 2 versions of every smelting recipe (with ambient air or explicit air input). You could use the same recipe everywhere, but when a furnace is placed on a planet with air containing oxygen, you create a hidden infinity pipe that supplies the air for free. Similarly, you might want to make stone furnaces vent their waste gases (like flue gas or coke oven gas), while steel/electric furnaces output this waste gas for other uses (like neutralizing alkali wastewater via carbonation, or making sulfuric acid from the sulfurous flue gas produced by smelting sulfide ores); but again you don't want to double the number of smelting recipes by giving each one a gas-venting variant. You could create a hidden fluid-venting entity on top of stone furnaces, which takes the gas output and produces pollution.

#### Magic tricks in Quezler's mods

Many of the [mods by Quezler](https://mods.factorio.com/user/Quezler) involve more advanced magic tricks. Below are some examples.

* [Beacon interface](https://mods.factorio.com/mod/beacon-interface) adds a beacon that can be set to have any module effects with any strength using an in-game GUI. This is implemented by creating 16 hidden modules for every effect, with strengths doubling - for example one module has +1% speed, the next one has +2% speed, the next one gives +4% speed, up to +(2^14)% speed, plus one for -(2^14)% speed. When the sliders are adjusted to say +100% speed, the mod writes +100% in binary (+64%, +32%, +4%, summing to +100%) and then inserts the corresponding modules into the beacon. If you set it to say -10% speed, it puts in the -2^14% module and then uses the other modules to boost it back to -10% speed (basically [two's complement](https://en.wikipedia.org/wiki/Two%27s_complement)).

* Building on the Beacon Interface mod, the [Apprentice assembler](https://mods.factorio.com/mod/apprentice-assembler) mod adds an assembler whose speed increases by 1% for each consecutive crafting recipe, then drops by 20% for each second the machine is idle. This is implemented by creating an invisible beacon inside the machine, and then setting its modules using the Beacon Interface mod. To count when products are finished or the machine is idle, the assembler has circuit connections to inserters on a hidden surface, which are enabled/disabled depending on the assembler's working state. When inserters are enabled, they pick up "offering" items on the hidden surface, causing the item-on-ground entity to be destroyed. The mod uses [register_on_object_destroyed](https://lua-api.factorio.com/latest/classes/LuaBootstrap.html#register_on_object_destroyed) so that it can run code when these "offering" items are destroyed, to update the modules in the hidden beacon.

* [Krastorio 2 air purifier helper](https://mods.factorio.com/mod/kr-air-purifier-helper) automatically places logistic requests for air filters in air purifier buildings. This is done in a way similar to the item-on-ground `register_on_object_destroyed` trick in Apprentice Assembler above, but using a different technique. When air purifiers are built, the mod creates an assembler on a hidden surface, doing some arbitrary recipe (namely wood to wooden chests). The mod places wood into the input slot of the assembler, giving the wood a health of 0.5, and uses `register_on_object_destroyed` to run code when the wood stack gets destroyed by the assembler running the recipe. It's necessary to give the wood a health, because `on_object_destroyed` only works on item stacks that store more than just their stack count. The assembler is connected via circuit link to a proxy chest that's linked to the air purifier's input slot; the circuit link makes the assembler only run when there are no filters in the air purifier / proxy chest. When it runs, the object gets destroyed, so the mod's `on_object_destroyed` handler gets called, which can then place the logistic request in the air purifier. I think this technique achieves the same effect as the item-on-ground technique, but without needing new prototypes and using fewer entities.

* (Note this mod has been updated since I wrote this description, might work differently now.) [Quality holmium ore returns more holmium solution](https://mods.factorio.com/mod/quality-holmium-ore-returns-more-holmium-solution) does what the title says. When a holmium chemical plant is built, an invisible assembler is placed inside it, and a set of 3 arithmetic combinators are created on a hidden surface. The holmium chemical plant's recipe for holmium solution produces both holmium solution and an item called "quality based productivity"; this is an item so that it gets the quality of the recipe's ingredients. This item is teleported to the hidden surface via a linked chest. There, combinators read the quality of the "quality based productivity" item and multiply it with the intended quality multipliers (supplied by a constant combinator). Inserters then use the calculated amount to move another item "coupon for holmium solution" from an infinity chest into another linked chest which teleports it back to the assembler inside the holmium chemical plant. That assembler then turns the coupons into holmium solution, outputted via a pipe linked to the chemical plant's output fluidbox.

#### Possible additional magic tricks

Here's some additional ideas for magic tricks that I haven't seen implemented.

* Suppose you want items to have different spoilage timers on different surfaces - for example, iron plates might spoil to rusty iron plates on Nauvis, but not spoil in space; or liquid ammonia canisters might spoil to ammonia gas canisters on most planets, but on Aquilo the spoilage goes the opposite direction, from gas to liquid. You could achieve this by creating hidden versions of items with different spoilage timers, and then replace items with the right version whenever a cargo pod lands. To make them work with recipes, you would have to make alternate versions of each recipe for each surface. And to hide those recipes on some surfaces, you could create hidden versions of all craft	ng on the currently-orbited planet. This approach still has some problems, such as item variants giving different signals in chests. I am not aware of any mod that implements this.

* Suppose you want to allow one recipe to use a wide range of alternatives for one of its ingredients. For example, you want to allow making char from any carbon-based fuel item (coal, wood, fruit, etc.) but you don't want a separate recipe for every possible input. You can achieve this without magic tricks by making this a specific "fuel type", and creating a special building that uses this fuel type, and then the recipe has no explicit ingredients. (This specific example is implemented in LSA.) But sometimes that doesn't work, for example because you don't want to give fluids a fuel value because you don't want to allow them in all fluid-burning buildings. (Entities with fluid-burning energy source can have a filter to allow only one fluid, but if you want to allow more than one, there is no way to do that; fluids don't have fuel types like items do.) For example, let's say you want to make a recipe that requires an "inert atmosphere" fluid as an ingredient, and this inert atmosphere can be many different fluids (nitrogen, argon, vacuum, etc.). One solution is to create a hidden furnace which takes any of those different fluids as inputs, and produces the "inert atmosphere" fluid as output, which goes directly into the assembler that then uses it as an ingredient. From the player's perspective, it looks like the assembler has a fluid input for "inert atmosphere", but you can connect this to a pipe carrying any of those alternatives (nitrogen, argon, vacuum, etc.) and it magically gets converted into the "inert atmosphere" fluid. This approach doesn't work as cleanly for item ingredients rather than fluid ingredients.

### General advice on coding

* Learn basic programming. Use loops. Factor out repeated code into functions.
* Use the section above on dev environment. Set up an IDE like VSCode with a Lua LSP and Factorio Modding Toolkit.
* Consider asking AI to improve your code. Consider using an IDE with built-in AI like Cursor; ideally learn to code before using this so you can tell when it screws up.
* Avoid control-stage scripting. When possible, make all necessary changes in the prototype stage.
* Avoid running code in on_tick events. Sometimes you will need to do that anyway; in that case, try to do the minimum work and exit as soon as possible.
* Read mods written by other people.

### Specific advice on coding

* When defining prototypes in code, you can explicitly write the entire table. Alternatively, you can use `table.deepcopy` to copy an existing similar prototype, then change various fields, like the name, icon, `minable.result` or `place_result`, etc. The deepcopy approach has the disadvantage of unexpected interactions with the rest of your mod, or other mods, since the values you think you're copying might have been changed elsewhere. The explicit approach has the disadvantage of needing to set all the fields explicitly, so you risk forgetting to set some more subtle fields like item sounds (pick, drop, inventory_move) and crafting machine tints for recipes. For large overhaul mods the best approach is probably to explicitly define prototypes but using a helper function to easily set / avoid forgetting to set the subtler fields.
* Some modding effects may require you to run [`surface.find_entities_filtered()`](https://lua-api.factorio.com/latest/classes/LuaSurface.html#find_entities_filtered) on every nth tick so that you can update all buildings/whatever of a specific type on all planets. You may expect this function to be fast, since the engine frequently needs to find all pipes or enemy bases or whatever to update them, so you might think it already has lists of entities by type/name ready to go. However, this is not the case, the function is slow. In my experience, calling this function will cause noticeable lag, like dropping multiple frames every time your script runs. Instead, you can should rely on caching, meaning you run `find_entities_filtered` once when the game starts, and store it in `storage.whatever`. You can listen to events like `on_built_entity` and `on_player_mined_entity` to update the cache without re-running the slow scan.


## Other

### Automatic publishing

* Factorio Modding Toolkit includes a tool for this, explained [here](https://github.com/justarandomgeek/vscode-factoriomod-debug/blob/current/doc/package.md).
* If you prefer to manually upload zipfiles to the portal, this repo includes a `zipmod.sh` script to zip up mods and run some checks.

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
