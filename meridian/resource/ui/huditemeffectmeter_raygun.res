"Resource/UI/HudItemEffectMeter_Raygun.res"
{
	HudItemEffectMeter
	{
		"fieldName"		"HudItemEffectMeter"
		"visible"		"1"
		"enabled"		"1"
		"xpos"			"r248"
		"ypos"			"r68"
		"wide"			"100"
		"tall"			"48"
		"MeterFG"		"236 240 244 255"
		"MeterBG"		"255 255 255 40"
	}

	"ItemEffectMeterBG"
	{
		"ControlName"	"CTFImagePanel"
		"fieldName"		"ItemEffectMeterBG"
		"xpos"			"0"
		"ypos"			"0"
		"zpos"			"0"
		"wide"			"100"
		"tall"			"48"
		"visible"		"1"
		"enabled"		"1"
		"scaleImage"	"1"
		"image"			"meridian/mer_panel"
	}

	"ItemEffectMeterAccent"
	{
		"ControlName"	"CTFImagePanel"
		"fieldName"		"ItemEffectMeterAccent"
		"xpos"			"0"
		"ypos"			"0"
		"zpos"			"1"
		"wide"			"3"
		"tall"			"48"
		"visible"		"1"
		"enabled"		"1"
		"scaleImage"	"1"
		"image"			"meridian/mer_blue"
		"teambg_2"		"meridian/mer_red"
		"teambg_3"		"meridian/mer_blue"
	}

	"ItemEffectMeterLabel"
	{
		"ControlName"		"CExLabel"
		"fieldName"			"ItemEffectMeterLabel"
		"xpos"				"12"
		"ypos"				"9"
		"zpos"				"2"
		"wide"				"82"
		"tall"				"14"
		"autoResize"			"0"
		"pinCorner"			"0"
		"visible"			"1"
		"enabled"			"1"
		"labelText"			"#TF_ENERGYDRINK"
		"textAlignment"		"west"
		"font"				"MerLabel"
		"fgcolor"			"150 160 172 255"
	}

	"ItemEffectMeter"
	{
		"ControlName"			"ContinuousProgressBar"
		"fieldName"				"ItemEffectMeter"
		"font"					"Default"
		"xpos"					"12"
		"ypos"					"28"
		"zpos"					"2"
		"wide"					"82"
		"tall"					"8"
		"autoResize"			"0"
		"pinCorner"				"0"
		"visible"				"1"
		"enabled"				"1"
		"textAlignment"			"Left"
		"dulltext"				"0"
		"brighttext"			"0"
	}
}
