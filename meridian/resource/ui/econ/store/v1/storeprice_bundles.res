#Base "StorePrice.res"

"Resource/UI/StorePrice_New.res"
{
	// Override base font settings
	"Price"
	{
		"font"			"MerLabel"
	}

	"OG_Price"
	{
		"font"			"MerLabel"
	}

	"Discount"
	{
		"font"			"MerLabel"
	}

	// Add a large version of "limited"
	"LimitedLarge"
	{
		"ControlName"	"ImagePanel"
		"fieldName"		"LimitedLarge"
		"ypos"			"3"
		"wide"			"24"
		"tall"			"24"
		"zpos"			"20"
		"visible"		"0"
		"enabled"		"1"
		"image"			"../backpack/crafting/limited_time_sticker"
		"scaleImage"	"1"
	}
}
