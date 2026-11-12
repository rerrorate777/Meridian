#base ScrollableQuestList.res

"Resource/UI/econ/ScrollableQuestList.res"
{
	"Container"
	{
		"ControlName"	"EditablePanel"
		"fieldName"		"Container"
		"xpos"			"0"
		"ypos"			"0"
		"zpos"			"1"
		"wide"			"f0"
		"tall"			"f0"
		"visible"		"1"
		"enabled"		"1"
		"proportionaltoparent" "1"

		"SelectButton"
		{
			"ControlName"	"CExButton"
			"fieldName"		"SelectButton"
			"border_default"		"MerButtonBorder"
			"border_armed"		"MerButtonBorderArmed"
			"paintborder"		"1"
			"PaintBackgroundType"		"0"
			"xpos"		"0"
			"ypos"		"0"
			"zpos"		"0"
			"wide"		"f0"
			"tall"		"f0"
			"visible"		"1"
			"enabled"		"1"
			"textAlignment"	"east"
			"labelText"			""

			"proportionaltoparent"	"1"
			"paintbackground"	"0"
			"command"	"deselect_all"
			"actionsignallevel" "2"
		}
	}

	"BackgroundFolderImage"
	{
		"image"			"contracts\halloween\contracts_base1"
	}

	"EmptyLabel"
	{
		"font"			"MerBody"
		"fgcolor"		"HalloweenThemeColor2015_Light"
	}
}
