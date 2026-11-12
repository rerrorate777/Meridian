"Resource/UI/TeamMenu.res"
{
	"team"
	{
		"ControlName"	"CTeamMenu"
		"fieldName"		"team"
		"xpos"			"0"
		"ypos"			"0"
		"wide"			"f0"
		"tall"			"480"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"1"
		"enabled"		"1"
		"tabPosition"	"0"
	}

	"SysMenu"
	{
		"ControlName"	"Menu"
		"fieldName"		"SysMenu"
		"xpos"			"0"
		"ypos"			"0"
		"wide"			"64"
		"tall"			"24"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"0"
		"enabled"		"0"
		"tabPosition"	"0"
	}

	"MapInfo"
	{
		"ControlName"	"HTML"
		"fieldName"		"MapInfo"
		"xpos"			"100"
		"ypos"			"34"
		"wide"			"450"
		"tall"			"365"
		"autoResize"	"3"
		"pinCorner"		"0"
		"visible"		"0"
		"enabled"		"0"
		"tabPosition"	"0"
	}

	"mapname"
	{
		"ControlName"	"Label"
		"fieldName"		"mapname"
		"xpos"			"c-310"
		"ypos"			"50"
		"wide"			"90"
		"tall"			"24"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"0"
		"enabled"		"0"
		"labelText"		""
		"textAlignment"	"west"
		"dulltext"		"0"
		"brighttext"	"1"
	}
	
	"teambutton0"
	{
		"ControlName"	"CTFTeamButton"
		"fieldName"		"teambutton0"
		"xpos"			"c-80"
		"ypos"			"110"
		"zpos"			"6"
		"wide"			"160"
		"tall"			"220"
		"autoResize"	"0"
		"pinCorner"		"2"
		"visible"		"1"
		"enabled"		"1"
		"tabPosition"	"3"
		"textAlignment"	"north"
		"dulltext"		"0"
		"brighttext"	"0"
		"paintborder"	"0"
		"command"		"jointeam blue"
		"team"				"3"		// team blue
		"associated_model"	"bluedoor"
		"hover"				"2.0"
		"font"			"MerHealth"
		"fgcolor"		"MerText"
		"paintbackground"		"1"
		"defaultBgColor_override"		"0 0 0 0"
		"armedBgColor_override"		"255 255 255 7"
		"depressedBgColor_override"		"255 255 255 16"
		"labelText"		"BLU"
		"textinsety"		"30"
		"defaultFgColor_override"		"MerText"
		"armedFgColor_override"		"255 255 255 255"
		"depressedFgColor_override"		"255 255 255 255"
	}

	"teambutton1"
	{
		"ControlName"	"CTFTeamButton"
		"fieldName"		"teambutton1"
		"xpos"			"c100"
		"ypos"			"110"
		"zpos"			"6"
		"wide"			"160"
		"tall"			"220"
		"autoResize"	"0"
		"pinCorner"		"2"
		"visible"		"1"
		"enabled"		"1"
		"tabPosition"	"4"
		"textAlignment"	"north"
		"dulltext"		"0"
		"brighttext"	"0"
		"paintborder"	"0"
		"command"		"jointeam red"
		"team"				"2"		// team red
		"associated_model"	"reddoor"	
		"hover"				"2.0"
		"font"			"MerHealth"
		"fgcolor"		"MerText"
		"paintbackground"		"1"
		"defaultBgColor_override"		"0 0 0 0"
		"armedBgColor_override"		"255 255 255 7"
		"depressedBgColor_override"		"255 255 255 16"
		"labelText"		"RED"
		"textinsety"		"30"
		"defaultFgColor_override"		"MerText"
		"armedFgColor_override"		"255 255 255 255"
		"depressedFgColor_override"		"255 255 255 255"
	}

	"teambutton2"
	{
		"ControlName"	"CTFTeamButton"
		"fieldName"		"teambutton2"
		"xpos"			"c-260"
		"ypos"			"110"
		"zpos"			"6"
		"wide"			"160"
		"tall"			"220"
		"autoResize"	"0"
		"pinCorner"		"2"
		"visible"		"1"
		"enabled"		"1"
		"tabPosition"	"1"
		"textAlignment"	"north"
		"dulltext"		"0"
		"brighttext"	"0"
		"paintborder"	"0"
		"command"		"jointeam auto"
		"associated_model"	"autodoor"
		"font"			"MerHealth"
		"fgcolor"		"MerText"
		"paintbackground"		"1"
		"defaultBgColor_override"		"0 0 0 0"
		"armedBgColor_override"		"255 255 255 7"
		"depressedBgColor_override"		"255 255 255 16"
		"labelText"		"?"
		"textinsety"		"30"
		"defaultFgColor_override"		"MerText"
		"armedFgColor_override"		"255 255 255 255"
		"depressedFgColor_override"		"255 255 255 255"
	}
	
	"teambutton3"
	{
		"ControlName"	"CTFTeamButton"
		"fieldName"		"teambutton3"
		"xpos"			"c-80"
		"ypos"			"350"
		"zpos"			"6"
		"wide"			"160"
		"tall"			"32"
		"autoResize"	"0"
		"pinCorner"		"2"
		"visible"		"1"
		"enabled"		"1"
		"tabPosition"	"2"
		"textAlignment"	"center"
		"dulltext"		"0"
		"brighttext"	"0"
		"paintborder"	"0"
		"command"		"jointeam spectate"
		"associated_model"	"spectate"	
		"font"			"MerBody"
		"fgcolor"		"MerText"
		"paintbackground"		"1"
		"defaultBgColor_override"		"0 0 0 0"
		"armedBgColor_override"		"255 255 255 7"
		"depressedBgColor_override"		"255 255 255 16"
		"labelText"		"SPECTATE"
		"defaultFgColor_override"		"MerText"
		"armedFgColor_override"		"255 255 255 255"
		"depressedFgColor_override"		"255 255 255 255"
	}
	
	"CancelButton" [$WIN32] 
	{
		"ControlName"	"CExButton"
		"fieldName"		"CancelButton"
		"xpos"			"r190"
		"xpos_hidef"			"r200"
		"ypos"			"r40"
		"ypos_lodef"			"r64"
		"ypos_hidef"			"r54"
		"zpos"			"6"
		"wide"			"150"
		"tall"			"30"
		"autoResize"	"0"
		"pinCorner"		"2"
		"visible"		"0"
		"enabled"		"1"
		"tabPosition"	"0"
		"labelText"		"#TF_Cancel"
		"textAlignment"	"center"
		"dulltext"		"0"
		"brighttext"	"0"
		"command"		"cancelmenu"
		"font"			"MerBody"
		"paintbackground"		"1"
		"paintborder"		"1"
		"PaintBackgroundType"		"0"
		"border_default"		"MerButtonBorder"
		"border_armed"		"MerButtonBorderArmed"
		"fgcolor"		"224 84 72 255"
		"defaultBgColor_override"		"28 32 40 235"
		"armedBgColor_override"		"46 52 64 235"
		"depressedBgColor_override"		"60 68 82 235"
		"defaultFgColor_override"		"224 84 72 255"
		"armedFgColor_override"		"255 130 118 255"
		"depressedFgColor_override"		"255 130 118 255"
	}
	
	"TeamMenuSelect"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"TeamMenuSelect"
		"xpos"			"30"
		"ypos"			"r40"
		"zpos"			"6"
		"wide"			"450"
		"tall"			"30"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"#TF_SelectATeam"
		"textAlignment"	"west"
		"dulltext"		"0"
		"brighttext"	"0"
		"font"			"MerTitle"
		"fgcolor"		"MerText"
	}
	
	"TeamMenuAuto"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"TeamMenuAuto"
		"xpos"			"c-280" [$WIN32] 
		"xpos"			"c-276" [$X360]
		"ypos"			"55"
		"zpos"			"1"
		"wide"			"102" [$WIN32] 
		"wide"			"94" [$X360]
		"tall"			"24"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"0"
		"enabled"		"1"
		"labelText"		"#TF_Random"
		"textAlignment"	"center"
		"dulltext"		"0"
		"brighttext"	"0"
		"wrap"			"0"
		"font"			"MerBody"
		"fgcolor"		"black"
	}
	
	"TeamMenuSpectate"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"TeamMenuSpectate"
		"xpos"			"c-112"
		"ypos"			"255"
		"zpos"			"1"
		"wide"			"44"
		"tall"			"20"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"0"
		"enabled"		"1"
		"labelText"		"#TF_Spectate"
		"textAlignment"	"north"
		"dulltext"		"0"
		"brighttext"	"0"
		"wrap"			"0"
		"font"			"MerLabel"
		"font_lodef"	"MenuSmallFont"
		"fgcolor"		"white"
	}

	"MenuBG"
	{
		"ControlName"	"CModelPanel"
		"fieldName"		"MenuBG"
		"xpos"			"-10"
		"ypos"			"-10"
		"zpos"			"0"		
		"wide"			"1"
		"tall"			"1"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"1"
		"enabled"		"1"
		"fov"			"20"
		
		"model"
		{
			"modelname"	"models/vgui/UI_team01.mdl"
			"skin"		"0"
			"angles_x" "0"
			"angles_y" "180"
			"angles_z" "0"
			"origin_x" "290"
			"origin_x_hidef" "305"
			"origin_x_lodef" "320"
			"origin_y" "0"
			"origin_z" "-34"
		}
	}	
	
	"ShadedBar"
	{
		"ControlName"	"ImagePanel"
		"fieldName"		"ShadedBar"
		"xpos"			"0"
		"ypos"			"r50"
		"zpos"			"5"
		"wide"			"f0"
		"tall"			"50"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"1"
		"enabled"		"1"
		"tabPosition"	"0"	
		"PaintBackgroundType"	"0"
		"fillcolor"		"12 14 18 235"
	}		
	
	"BlueCount"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"BlueCount"
		"xpos"			"c-80"
		"ypos"			"238"
		"zpos"			"5"
		"wide"			"160"
		"tall"			"40"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"%bluecount%"
		"textAlignment"	"center"
		"dulltext"		"0"
		"brighttext"	"1"
		"font"			"MerNumberMed"
		"fgcolor"		"MerText"
	}		
	
	"RedCount"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"RedCount"
		"xpos"			"c100"
		"ypos"			"238"
		"zpos"			"5"
		"wide"			"160"
		"tall"			"40"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"%redcount%"
		"textAlignment"	"center"
		"dulltext"		"0"
		"brighttext"	"1"
		"font"			"MerNumberMed"
		"fgcolor"		"MerText"
	}	
	
	"bluedoor"
	{
		"ControlName"	"CModelPanel"
		"fieldName"		"bluedoor"
		"xpos"			"-10"
		"ypos"			"-10"
		"zpos"			"2"		
		"wide"			"1"
		"tall"			"1"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"1"
		"enabled"		"1"
		"fov"			"20"
		
		"model"
		{
			"modelname"	"models/vgui/UI_team01_blue.mdl"
			"skin"		"0"
			"angles_x" "0"
			"angles_y" "180"
			"angles_z" "0"
			"origin_x" "290"
			"origin_x_lodef" "320"
			"origin_x_hidef" "305"
			"origin_y" "0"
			"origin_z" "-34"
			
			"animation"
			{
				"name"			"idle_enabled"
				"sequence"		"idle"
				"default"		"1"
			}

			"animation"
			{
				"name"			"idle_disabled"
				"sequence"		"fullidle"
			}			
			
			"animation"
			{
				"name"			"enter_enabled"
				"sequence"		"hoveropen"
			}
			
			"animation"
			{
				"name"			"enter_disabled"
				"sequence"		"fullidle"
			}
				
			"animation"
			{
				"name"			"exit_enabled"
				"sequence"		"hoverclose"
			}
			
			"animation"
			{
				"name"			"exit_disabled"
				"sequence"		"fullidle"
			}
			
			"animation"
			{
				"name"			"hover_disabled"
				"sequence"		"fullhover"
			}
		}
	}	
	
	"reddoor"
	{
		"ControlName"	"CModelPanel"
		"fieldName"		"reddoor"
		"xpos"			"-10"
		"ypos"			"-10"
		"zpos"			"2"		
		"wide"			"1"
		"tall"			"1"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"1"
		"enabled"		"1"
		"fov"			"20"
		
		"model"
		{
			"modelname"	"models/vgui/UI_team01_red.mdl"
			"skin"		"0"
			"angles_x" "0"
			"angles_y" "180"
			"angles_z" "0"
			"origin_x" "290"
			"origin_x_lodef" "320"
			"origin_x_hidef" "305"
			"origin_y" "0"
			"origin_z" "-34"
			
			"animation"
			{
				"name"			"idle_enabled"
				"sequence"		"idle"
				"default"		"1"
			}

			"animation"
			{
				"name"			"idle_disabled"
				"sequence"		"fullidle"
			}			
			
			"animation"
			{
				"name"			"enter_enabled"
				"sequence"		"hoveropen"
			}
			
			"animation"
			{
				"name"			"enter_disabled"
				"sequence"		"fullidle"
			}
				
			"animation"
			{
				"name"			"exit_enabled"
				"sequence"		"hoverclose"
			}
			
			"animation"
			{
				"name"			"exit_disabled"
				"sequence"		"fullidle"
			}
			
			"animation"
			{
				"name"			"hover_disabled"
				"sequence"		"fullhover"
			}
		}
	}		
	
	"autodoor"
	{
		"ControlName"	"CModelPanel"
		"fieldName"		"autodoor"
		"xpos"			"-10"
		"ypos"			"-10"
		"zpos"			"2"		
		"wide"			"1"
		"tall"			"1"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"1"
		"enabled"		"1"
		"fov"			"20"
		
		"model"
		{
			"modelname"	"models/vgui/UI_team01_random.mdl"
			"skin"		"0"
			"angles_x" "0"
			"angles_y" "180"
			"angles_z" "0"
			"origin_x" "290"
			"origin_x_lodef" "320"
			"origin_x_hidef" "305"
			"origin_y" "0"
			"origin_z" "-34"
			
			"animation"
			{
				"name"			"idle_enabled"
				"sequence"		"idle"
				"default"		"1"
			}

			"animation"
			{
				"name"			"enter_enabled"
				"sequence"		"hoveropen"
			}
			
			"animation"
			{
				"name"			"exit_enabled"
				"sequence"		"hoverclose"
			}
		}
	}		
	
	"spectate"
	{
		"ControlName"	"CModelPanel"
		"fieldName"		"spectate"
		"xpos"			"-10"
		"ypos"			"-10"
		"zpos"			"0"		
		"wide"			"1"
		"tall"			"1"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"1"
		"enabled"		"1"
		"fov"			"20"
		
		"model"
		{
			"modelname"	"models/vgui/UI_team01_spectate.mdl"
			"skin"		"0"
			"angles_x" "0"
			"angles_y" "180"
			"angles_z" "0"
			"origin_x" "290"
			"origin_x_lodef" "320"
			"origin_x_hidef" "305"
			"origin_y" "0"
			"origin_z" "-34"
			
			"animation"
			{
				"name"			"idle_enabled"
				"sequence"		"idle"
				"default"		"1"
			}

			"animation"
			{
				"name"			"enter_enabled"
				"sequence"		"hover"
			}
			
			"animation"
			{
				"name"			"exit_enabled"
				"sequence"		"idle"
			}
		}
	}			
	
	"Footer" [$X360]
	{
		"ControlName"		"CTFFooter"
		"fieldName"			"Footer"
		"zpos"				"6"
		"tall"				"80"
		"button_separator"	"10"
		"button_separator_lodef"	"5"
		"buttongap"			"50"
		"buttongap_hidef"		"35"
		"buttongap_lodef"			"18"
		"textadjust"		"3"
		"textadjust_lodef"		"0"
		"buttonoffsety"		"20"
		"buttonoffsety_hidef"		"0"
		"buttonoffsety_lodef"		"18"
		"center"			"0"
		"button_pin_right_lodef"	"55"
		"fonttext"			"MatchmakingDialogMenuLarge"
		"fonttext_lodef"			"MatchmakingDialogMenuSmall"
		"fgcolor"			"HudOffWhite" 	
		
		"button"
		{
			"name"		"cancel"
			"text"		"#GameUI_Cancel"
			"icon"		"#GameUI_Icons_B_BUTTON"	
		}
		
		"button"
		{
			"name"		"nextprev"
			"text"		"#TF_NextPrev"
			"icon"		"#GameUI_Icons_DPAD"	
		}
		
		"button"
		{
			"name"		"select"
			"text"		"#GameUI_Select"
			"icon"		"#GameUI_Icons_A_BUTTON"	
		}
	}	
	
	"HighlanderLabel" [$WIN32] 
	{
		"ControlName"	"CExLabel"
		"fieldName"		"HighlanderLabel"
		"xpos"			"c-110"
		"ypos"			"62"
		"zpos"			"6"
		"wide"			"220"
		"tall"			"24"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"0"
		"enabled"		"1"
		"labelText"		"#TF_Highlander_Mode"
		"textAlignment"	"center"
		"dulltext"		"0"
		"brighttext"	"0"
		"font"			"MerBody"
		"fgcolor"		"MerText"
		"centerwrap"	"1"
	}
	
	"HighlanderLabelShadow" [$WIN32] 
	{
		"ControlName"	"CExLabel"
		"fieldName"		"HighlanderLabelShadow"
		"xpos"			"c-109"
		"ypos"			"62"
		"zpos"			"6"
		"wide"			"220"
		"tall"			"24"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"0"
		"enabled"		"1"
		"labelText"		"#TF_Highlander_Mode"
		"textAlignment"	"center"
		"dulltext"		"0"
		"brighttext"	"0"
		"font"			"MerBody"
		"fgcolor"		"0 0 0 0"
		"centerwrap"	"1"
	}
	
	"TeamsFullLabel" [$WIN32] 
	{
		"ControlName"	"CExLabel"
		"fieldName"		"TeamsFullLabel"
		"xpos"			"c-110"
		"ypos"			"84"
		"zpos"			"6"
		"wide"			"220"
		"tall"			"24"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"0"
		"enabled"		"1"
		"labelText"		"#TF_Teams_Full"
		"textAlignment"	"center"
		"dulltext"		"0"
		"brighttext"	"0"
		"font"			"MerBody"
		"fgcolor"		"MerText"
		"centerwrap"	"1"
	}
	
	"TeamsFullLabelShadow" [$WIN32] 
	{
		"ControlName"	"CExLabel"
		"fieldName"		"TeamsFullLabelShadow"
		"xpos"			"c-109"
		"ypos"			"84"
		"zpos"			"6"
		"wide"			"220"
		"tall"			"24"
		"autoResize"	"0"
		"pinCorner"		"0"
		"visible"		"0"
		"enabled"		"1"
		"labelText"		"#TF_Teams_Full"
		"textAlignment"	"center"
		"dulltext"		"0"
		"brighttext"	"0"
		"font"			"MerBody"
		"fgcolor"		"0 0 0 0"
		"centerwrap"	"1"
	}

	"TeamsFullArrow" [$WIN32]
	{
		"ControlName"	"CTFImagePanel"
		"fieldName"		"TeamsFullArrow"
		"xpos"			"c-118"
		"ypos"			"165"
		"zpos"			"6"
		"wide"			"40"
		"tall"			"40"
		"visible"		"0"
		"enabled"		"1"
		"image"			"../HUD/arrow_big_down"
		"scaleImage"	"1"	
	}

	"MerScrim"
	{
		"ControlName"	"ImagePanel"
		"fieldName"		"MerScrim"
		"xpos"			"0"
		"ypos"			"0"
		"zpos"			"0"
		"wide"			"f0"
		"tall"			"480"
		"visible"		"1"
		"enabled"		"1"
		"fillcolor"		"8 10 14 225"
	}

	"MerCardRandom"
	{
		"ControlName"	"ImagePanel"
		"fieldName"		"MerCardRandom"
		"xpos"			"c-260"
		"ypos"			"110"
		"zpos"			"1"
		"wide"			"160"
		"tall"			"220"
		"visible"		"1"
		"enabled"		"1"
		"fillcolor"		"34 38 48 235"
	}

	"MerCardRandomEdge"
	{
		"ControlName"	"ImagePanel"
		"fieldName"		"MerCardRandomEdge"
		"xpos"			"c-260"
		"ypos"			"110"
		"zpos"			"2"
		"wide"			"160"
		"tall"			"4"
		"visible"		"1"
		"enabled"		"1"
		"fillcolor"		"150 160 172 255"
	}

	"MerCardBlue"
	{
		"ControlName"	"ImagePanel"
		"fieldName"		"MerCardBlue"
		"xpos"			"c-80"
		"ypos"			"110"
		"zpos"			"1"
		"wide"			"160"
		"tall"			"220"
		"visible"		"1"
		"enabled"		"1"
		"fillcolor"		"28 58 92 225"
	}

	"MerCardBlueEdge"
	{
		"ControlName"	"ImagePanel"
		"fieldName"		"MerCardBlueEdge"
		"xpos"			"c-80"
		"ypos"			"110"
		"zpos"			"2"
		"wide"			"160"
		"tall"			"4"
		"visible"		"1"
		"enabled"		"1"
		"fillcolor"		"76 156 232 255"
	}

	"MerCardBluePlayers"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"MerCardBluePlayers"
		"xpos"			"c-80"
		"ypos"			"278"
		"zpos"			"4"
		"wide"			"160"
		"tall"			"20"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"players"
		"textAlignment"	"center"
		"font"			"MerLabel"
		"fgcolor"		"150 160 172 255"
	}

	"MerCardRed"
	{
		"ControlName"	"ImagePanel"
		"fieldName"		"MerCardRed"
		"xpos"			"c100"
		"ypos"			"110"
		"zpos"			"1"
		"wide"			"160"
		"tall"			"220"
		"visible"		"1"
		"enabled"		"1"
		"fillcolor"		"86 34 30 225"
	}

	"MerCardRedEdge"
	{
		"ControlName"	"ImagePanel"
		"fieldName"		"MerCardRedEdge"
		"xpos"			"c100"
		"ypos"			"110"
		"zpos"			"2"
		"wide"			"160"
		"tall"			"4"
		"visible"		"1"
		"enabled"		"1"
		"fillcolor"		"224 84 72 255"
	}

	"MerCardRedPlayers"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"MerCardRedPlayers"
		"xpos"			"c100"
		"ypos"			"278"
		"zpos"			"4"
		"wide"			"160"
		"tall"			"20"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"players"
		"textAlignment"	"center"
		"font"			"MerLabel"
		"fgcolor"		"150 160 172 255"
	}

	"MerCardRandomLabel"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"MerCardRandomLabel"
		"xpos"			"c-260"
		"ypos"			"238"
		"zpos"			"4"
		"wide"			"160"
		"tall"			"40"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"RANDOM"
		"textAlignment"	"center"
		"font"			"MerTitle"
		"fgcolor"		"MerText"
	}

	"MerCardSpectate"
	{
		"ControlName"	"ImagePanel"
		"fieldName"		"MerCardSpectate"
		"xpos"			"c-80"
		"ypos"			"350"
		"zpos"			"1"
		"wide"			"160"
		"tall"			"32"
		"visible"		"1"
		"enabled"		"1"
		"fillcolor"		"12 14 18 225"
	}

	"MerKeyRandom"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"MerKeyRandom"
		"xpos"			"c-252"
		"ypos"			"308"
		"zpos"			"7"
		"wide"			"20"
		"tall"			"16"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"1"
		"textAlignment"	"west"
		"font"			"MerLabel"
		"fgcolor"		"150 160 172 255"
	}

	"MerKeyBlue"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"MerKeyBlue"
		"xpos"			"c-72"
		"ypos"			"308"
		"zpos"			"7"
		"wide"			"20"
		"tall"			"16"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"3"
		"textAlignment"	"west"
		"font"			"MerLabel"
		"fgcolor"		"150 160 172 255"
	}

	"MerKeyRed"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"MerKeyRed"
		"xpos"			"c108"
		"ypos"			"308"
		"zpos"			"7"
		"wide"			"20"
		"tall"			"16"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"4"
		"textAlignment"	"west"
		"font"			"MerLabel"
		"fgcolor"		"150 160 172 255"
	}

	"MerKeySpectate"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"MerKeySpectate"
		"xpos"			"c-72"
		"ypos"			"364"
		"zpos"			"7"
		"wide"			"20"
		"tall"			"16"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"2"
		"textAlignment"	"west"
		"font"			"MerLabel"
		"fgcolor"		"150 160 172 255"
	}

	"MerBalanceHint"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"MerBalanceHint"
		"xpos"			"c-260"
		"ypos"			"400"
		"zpos"			"4"
		"wide"			"520"
		"tall"			"20"
		"visible"		"1"
		"enabled"		"1"
		"labelText"		"A team is locked while joining it would leave the teams unbalanced."
		"textAlignment"	"center"
		"font"			"MerLabel"
		"fgcolor"		"150 160 172 255"
	}
}

