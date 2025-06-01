function hexToRgb(hex) {
	if (!hex) return null;
	let shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
	hex = hex.replace(shorthandRegex, (m, r, g, b) => r + r + g + g + b + b);
	let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
	return result ? {
		r: parseInt(result[1], 16),
		g: parseInt(result[2], 16),
		b: parseInt(result[3], 16)
	} : null;
}

function rgbToHex(r, g, b) {
	if (r === undefined || g === undefined || b === undefined) return null;
	return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toLowerCase();
}

function rgbToHsv(r, g, b) {
	if (r === undefined || g === undefined || b === undefined) return null;
	r /= 255; g /= 255; b /= 255;
	let max = Math.max(r, g, b), min = Math.min(r, g, b);
	let h, s, v = max;
	let d = max - min;
	s = max === 0 ? 0 : d / max;
	if (d === 0) {
		h = 0; // achromatic
	} else {
		switch (max) {
			case r: h = (g - b) / d + (g < b ? 6 : 0); break;
			case g: h = (b - r) / d + 2; break;
			case b: h = (r - g) / d + 4; break;
		}
		h /= 6;
	}
	return { h: h, s: s, v: v };
}

function hsvToRgb(h, s, v) {
	if (h === undefined || s === undefined || v === undefined) return null;
	let r, g, b;
	let i = Math.floor(h * 6);
	let f = h * 6 - i;
	let p = v * (1 - s);
	let q = v * (1 - f * s);
	let t = v * (1 - (1 - f) * s);
	switch (i % 6) {
		case 0: r = v; g = t; b = p; break;
		case 1: r = q; g = v; b = p; break;
		case 2: r = p; g = v; b = t; break;
		case 3: r = p; g = q; b = v; break;
		case 4: r = t; g = p; b = v; break;
		case 5: r = v; g = p; b = q; break;
	}
	return {
		r: Math.round(r * 255),
		g: Math.round(g * 255),
		b: Math.round(b * 255)
	};
}

// Helper to determine good text color (black or white) based on background
function getContrastingTextColor(hexBgColor) {
	if (!hexBgColor) return '#000000'; // Default to black
	const rgb = hexToRgb(hexBgColor);
	if (!rgb) return '#000000';
	// Standard relative luminance calculation
	const luminance = (0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b) / 255;
	return luminance > 0.5 ? '#000000' : '#FFFFFF';
}