/* This file is for creating and visualizing color schemes for analogous sets of items/fluids/etc.
To use, open webpage.html and then edit the code below. */

window.addEventListener('DOMContentLoaded', () => {
    // Rare earths
    createTable("rare-earths-table", "Rare earths", [
        ["yerbium plate", "yerbium ore"],
        ["holmium plate", "holmium ore"],
        ["thulium plate", "thulium ore"]
    ]);
    cellColor("holmium plate", "#c0929f"); // Base game
    cellColor("holmium ore", "#a16f77"); // Base game
    cellColor("yerbium plate", "#c4b39b");
    //analogy3("yerbium plate", "holmium plate", "thulium plate");
    cellColor("thulium plate", "#6b6887");
    completeTable("rare-earths-table");

    // Acids
    createTable("acids-table", "Acids", [
        ["nitric acid", "niter", "nox gas"],
        ["sulfuric acid", "salt cake", "sulfur dioxide", "sulfur"],
        ["chloric acid", "salt", "chlorine gas"],
        ["phosphoric acid", "phosphate salt", "phosphorus gas", "phosphorus"],
        ["fluoric acid", "fluoride salt", "fluorine gas"]
    ], ["Acid", "Salt", "Gas", "Crystal"]);
    cellColor("nitric acid", "#E05950");
    cellColor("sulfuric acid", "#fedb4f");
    cellColor("chloric acid", "#a6ce5e");
    //cellColor("phosphoric acid", "#2eab85");
    cellColor("fluoric acid", "#17e0db");
    interpolate("chloric acid", "phosphoric acid", "fluoric acid", .8);
    cellColor("niter", "#b02f28");
    cellColor("sulfur dioxide", "#c0a948");
    cellColor("sulfur", "#d4c700");
    completeTable("acids-table");

    // Bases
    createTable("bases-table", "Bases", [
        ["alkali ash"],
        ["quicklime", "slaked lime"],
        ["lye"],
    ]);
    cellColor("alkali ash", "#6b2b95");
    cellColor("lye", "#345c86");
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
    cellColor("iron ore", "#617b87");
    cellColor("iron ingot", "#969696");
    cellColor("copper ore", "#ae6c47");
    cellColor("copper plate", "#c07b64");
    cellColor("steel plate", "#a7a7a2");
    analogy4("sulfuric acid", "sulfur", "iron ore", "iron salt");
    completeTable("ores-table");

    // Petrochem
    createTable("petrochem-table", "Petrochem", [
        ["crude oil", "tar", "heavy oil", "light oil"],
        ["natural gas", "condensed gas", "petroleum gas"]
    ]);
});
