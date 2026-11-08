"Resource/UI/HudPlayerClass.res"
{
	// Class icon sits in the left cell of the health dock (see hudplayerhealth.res).
	// Needs cl_hud_playerclass_use_playermodel 0 (set by cfg/meridian.cfg).
	"HudPlayerClass"
	{
		"ControlName"	"EditablePanel"
		"fieldName"		"HudPlayerClass"
		"xpos"			"0"
		"ypos"			"0"
		"zpos"			"1"
		"wide"			"f0"
		"tall"			"480"
		"visible"		"1"
		"enabled"		"1"
	}

	"PlayerStatusClassImage"
	{
		"ControlName"	"CTFClassImage"
		"fieldName"		"PlayerStatusClassImage"
		"xpos"			"28"
		"ypos"			"r60"
		"zpos"			"4"
		"wide"			"32"
		"tall"			"32"
		"visible"		"1"
		"enabled"		"1"
		"image"			"../hud/class_scoutred"
		"scaleImage"	"1"
	}

	"PlayerStatusSpyImage"
	{
		"ControlName"	"CTFImagePanel"
		"fieldName"		"PlayerStatusSpyImage"
		"xpos"			"28"
		"ypos"			"r60"
		"zpos"			"4"
		"wide"			"32"
		"tall"			"32"
		"visible"		"1"
		"enabled"		"1"
		"image"			"../hud/class_spyred"
		"scaleImage"	"1"
		"teambg_2"		"../hud/class_spyred"
		"teambg_3"		"../hud/class_spyblue"
	}

	"PlayerStatusSpyOutlineImage"
	{
		"ControlName"	"CTFImagePanel"
		"fieldName"		"PlayerStatusSpyOutlineImage"
		"xpos"			"28"
		"ypos"			"r60"
		"zpos"			"7"
		"wide"			"32"
		"tall"			"32"
		"visible"		"0"
		"enabled"		"1"
		"image"			"../hud/class_spy_outline"
		"scaleImage"	"1"
	}

	// The stock backgrounds and 3D model are collapsed rather than removed:
	// the game still looks these controls up by name.
	"PlayerStatusClassImageBG"
	{
		"ControlName"	"CTFImagePanel"
		"fieldName"		"PlayerStatusClassImageBG"
		"xpos"			"0"
		"ypos"			"r60"
		"zpos"			"1"
		"wide"			"0"
		"tall"			"0"
		"visible"		"0"
		"enabled"		"1"
		"scaleImage"	"1"
	}

	"classmodelpanelBG"
	{
		"ControlName"	"CTFImagePanel"
		"fieldName"		"classmodelpanelBG"
		"xpos"			"0"
		"ypos"			"r60"
		"zpos"			"1"
		"wide"			"0"
		"tall"			"0"
		"visible"		"0"
		"enabled"		"1"
		"scaleImage"	"1"
	}

	"classmodelpanel"
	{
		"ControlName"	"CTFPlayerModelPanel"
		"fieldName"		"classmodelpanel"
		"xpos"			"0"
		"ypos"			"r60"
		"zpos"			"2"
		"wide"			"0"
		"tall"			"0"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"0"
		"enabled"		"1"
		"render_texture"	"0"
		"fov"			"12"
		"allow_rot"		"1"
		"disable_speak_event"	"1"
		"model"
		{
			"force_pos"	"1"
			"angles_x" "0"
			"angles_y" "172"
			"angles_z" "0"
			"origin_x" "200"
			"origin_y" "0"
			"origin_z" "-60"
			"frame_origin_x"	"0"
			"frame_origin_y"	"0"
			"frame_origin_z"	"0"
			"spotlight" "1"
			"modelname"		""
		}
	}

	"CarryingWeapon"
	{
		"ControlName"			"EditablePanel"
		"fieldName"				"CarryingWeapon"
		"xpos"					"232"
		"ypos"					"r104"
		"zpos"					"100"
		"wide"					"200"
		"tall"	 				"28"

		"CarryingBackground"
		{
			"ControlName"			"ImagePanel"
			"fieldName"				"CarryingBackground"
			"xpos"					"0"
			"ypos"					"0"
			"zpos"					"0"
			"wide"					"200"
			"tall"	 				"28"
			"visible"				"1"
			"enabled"				"1"
			"fillcolor"				"12 14 18 205"
		}
		"CarryingLabel"
		{
			"ControlName"		"CExLabel"
			"fieldName"			"CarryingLabel"
			"font"				"MerTitle"
			"fgcolor"			"236 240 244 255"
			"xpos"				"8"
			"ypos"				"0"
			"zpos"				"1"
			"wide"				"190"
			"tall"	 			"15"
			"visible"			"1"
			"enabled"			"1"
			"textAlignment"		"west"
			"labelText"			"%carrying%"
		}
		"CarryingLabelDropShadow"
		{
			"ControlName"		"CExLabel"
			"fieldName"			"CarryingLabelDropShadow"
			"font"				"MerTitle"
			"fgcolor"			"0 0 0 0"
			"xpos"				"0"
			"ypos"				"0"
			"zpos"				"0"
			"wide"				"0"
			"tall"	 			"0"
			"visible"			"0"
			"enabled"			"1"
			"labelText"			"%carrying%"
		}
		"OwnerLabel"
		{
			"ControlName"		"Label"
			"fieldName"			"OwnerLabel"
			"font"				"MerBody"
			"fgcolor"			"150 160 172 255"
			"xpos"				"8"
			"ypos"				"13"
			"zpos"				"1"
			"wide"				"190"
			"tall"	 			"14"
			"visible"			"1"
			"enabled"			"1"
			"textAlignment"		"west"
		}
	}
}
