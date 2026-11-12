"Resource/UI/HudAccountPanel.res"
{
	// Engineer metal. The 120x32 dock sits above the ammo dock; the root
	// (positioned in scripts/hudlayout.res) extends upwards for the floating +/- numbers.
	"CHudAccountPanel"
	{
		"delta_item_x"			"52"
		"delta_item_start_y"	"84"
		"delta_item_end_y"		"48"
		"PositiveColor"			"126 224 150 255"
		"NegativeColor"			"255 70 56 255"
		"delta_lifetime"		"1.5"
		"delta_item_font"		"MerNumberMed"
	}

	"AccountBG"
	{
		"ControlName"	"CTFImagePanel"
		"fieldName"		"AccountBG"
		"xpos"			"0"
		"ypos"			"92"
		"zpos"			"0"
		"wide"			"120"
		"tall"			"32"
		"visible"		"1"
		"enabled"		"1"
		"scaleImage"	"1"
		"image"			"meridian/mer_panel"
	}

	"AccountAccent"
	{
		"ControlName"	"CTFImagePanel"
		"fieldName"		"AccountAccent"
		"xpos"			"117"
		"ypos"			"92"
		"zpos"			"1"
		"wide"			"3"
		"tall"			"32"
		"visible"		"1"
		"enabled"		"1"
		"scaleImage"	"1"
		"image"			"meridian/mer_blue"
		"teambg_2"		"meridian/mer_red"
		"teambg_3"		"meridian/mer_blue"
	}

	"MetalIcon"
	{
		"ControlName"	"CIconPanel"
		"fieldName"		"MetalIcon"
		"xpos"			"10"
		"ypos"			"101"
		"zpos"			"1"
		"wide"			"14"
		"tall"			"14"
		"visible"		"1"
		"enabled"		"1"
		"scaleImage"	"1"
		"icon"			"ico_metal"
		"iconColor"		"150 160 172 255"
	}

	"AccountValue"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"AccountValue"
		"xpos"			"30"
		"ypos"			"92"
		"zpos"			"2"
		"wide"			"84"
		"tall"			"32"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"1"
		"enabled"		"1"
		"tabPosition"	"0"
		"labelText"		"%metal%"
		"textAlignment"	"west"
		"dulltext"		"0"
		"brighttext"	"0"
		"font"			"MerNumberMed"
		"fgcolor"		"236 240 244 255"
	}
}
