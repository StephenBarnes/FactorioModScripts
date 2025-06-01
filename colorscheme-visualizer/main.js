/* This file is for creating and visualizing color schemes for analogous sets of items/fluids/etc.
To use, open webpage.html and then edit the code below.
Available functions:
	* createTable("table-name", "Title", [[cell names]], optional titles) - creates a new table.
	* cellColor("cell name", "#123456") - set cell color.
	* interpolate("A", "B", "C", 0.4) - set cell B to 40% of the way between color of A and color of C.
	* analogy3("A", "B", "C") - set cell C so that color A is to B as B is to C.
	* analogy4("A", "B", "C", "D") - set cell D so that color A is to B as C is to D.
	* completeTable("table-name") - color in all uncolored cells in the table using analogies to already-colored cells.
*/

window.addEventListener('DOMContentLoaded', () => {
	// Rare earths
	createTable("rare-earths-table", "Rare earths", [
		["yerbium plate", "yerbium ore"],
		["holmium plate", "holmium ore"],
		["thulium plate", "thulium ore"]
	]);
	cellColor("holmium plate", "c0929f"); // Base game
	cellColor("holmium ore", "a16f77"); // Base game
	cellColor("yerbium plate", "c4b39b");
	//analogy3("yerbium plate", "holmium plate", "thulium plate");
	cellColor("thulium plate", "6b6887");
	completeTable("rare-earths-table");

	// Acids
	createTable("acids-table", "Acids", [
		["nitric lighter", "nitric acid", "niter", "nox gas"],
		["sulfuric lighter", "sulfuric acid", "salt cake", "sulfur dioxide", "sulfur"],
		["chloric lighter", "chloric acid", "salt", "chlorine gas"],
		["phosphoric lighter", "phosphoric acid", "phosphate salt", "phosphine", "phosphorus"],
		["fluoric lighter", "fluoric acid", "fluoride salt", "fluorine gas"]
	], ["Acid (lighter)", "Acid", "Salt", "Gas", "Crystal"]);
	cellColor("nitric acid", "E05950");
	cellColor("sulfuric acid", "fedb4f");
	cellColor("chloric acid", "a6ce5e");
	//cellColor("phosphoric acid", "2eab85");
	//cellColor("fluoric acid", "17e0db");
	//interpolate("chloric acid", "phosphoric acid", "fluoric acid", .8);
	cellColor("phosphoric acid", "47C8A7");
	cellColor("fluoric acid", "4F98EA");
	cellColor("niter", "b02f28");
	cellColor("sulfur dioxide", "c0a948");
	cellColor("sulfur", "d4c700");
	cellColor("nitric lighter", "f76d62");
	completeTable("acids-table");

	// Bases
	createTable("bases-table", "Bases", [
		["alkali ash"],
		["quicklime", "slaked lime"],
		["lye"],
	]);
	cellColor("alkali ash", "6b2b95");
	cellColor("lye", "345c86");
	//analogy4("nitric acid", "sulfuric acid", "alkali ash", "lye");
	interpolate("alkali ash", "quicklime", "lye", 0.5);
	analogy4("sulfur", "sulfuric acid", "quicklime", "slaked lime");
	completeTable("bases-table");

	// Ores
	createTable("ores-table", "Ores", [
		["iron ore", "iron plate", "iron salt"],
		["copper ore", "copper plate", "copper salt"],
		["(steel ore)", "steel plate"],
	]);
	cellColor("iron ore", "617b87");
	cellColor("iron ingot", "969696");
	cellColor("copper ore", "ae6c47");
	cellColor("copper plate", "c07b64");
	cellColor("steel plate", "a7a7a2");
	analogy4("sulfuric acid", "sulfur", "iron ore", "iron salt");
	completeTable("ores-table");

	// Petrochem
	createTable("petrochem-table", "Petrochem", [
		["crude oil", "tar", "heavy oil", "light oil", "condensed gas", "petroleum gas"],
		["natural gas"],
	]);
	cellColor("crude oil", "080808");
	cellColor("heavy oil", "742905");
	cellColor("light oil", "704e06");
	//interpolate("crude oil", "tar", "heavy oil", .55);
	cellColor("tar", "2d0f0e");
	//analogy3("heavy oil", "light oil", "petroleum gas");
	cellColor("petroleum gas", "E2E28A");
	cellColor("condensed gas", "8F8417");

	// Stone/silicon processing
	createTable("stone-table", "Stone processing", [
		["stone"],
		["sand", "gravel", "clay"],
		["silica", "crude silicon", "silicon gas", "silicon waste gas", "polysilicon", "silicon crystal ingot", "silicon wafer"],
	]);
	cellColor("stone", "917d59");
	cellColor("silica", "889A91");
	cellColor("crude silicon", "59826E");
	cellColor("silicon gas", "4D745F");
	//cellColor("silicon waste gas", "8A835D");
	cellColor("silicon waste gas", "8E9158");
	cellColor("polysilicon", "4D745F");
	cellColor("silicon wafer", "3b524c");
	interpolate("polysilicon", "silicon crystal ingot", "silicon wafer", 0.5);
});