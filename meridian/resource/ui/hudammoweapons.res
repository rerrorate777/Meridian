"Resource/UI/HudAmmoWeapons.res"
{
	// Bottom-right dock, 120x48. The root panel is positioned in scripts/hudlayout.res.
	"HudWeaponAmmoBG"
	{
		"ControlName"	"CTFImagePanel"
		"fieldName"		"HudWeaponAmmoBG"
		"xpos"			"0"
		"ypos"			"0"
		"zpos"			"1"
		"wide"			"120"
		"tall"			"48"
		"visible"		"1"
		"enabled"		"1"
		"scaleImage"	"1"
		"image"			"meridian/mer_panel"
	}

	"HudWeaponAmmoAccent"
	{
		"ControlName"	"CTFImagePanel"
		"fieldName"		"HudWeaponAmmoAccent"
		"xpos"			"117"
		"ypos"			"0"
		"zpos"			"3"
		"wide"			"3"
		"tall"			"48"
		"visible"		"1"
		"enabled"		"1"
		"scaleImage"	"1"
		"image"			"meridian/mer_blue"
		"teambg_2"		"meridian/mer_red"
		"teambg_3"		"meridian/mer_blue"
	}

	// Pulsing line along the bottom edge when ammo is low (HudLowAmmoPulse).
	"HudWeaponLowAmmoImage"
	{
		"ControlName"	"ImagePanel"
		"fieldName"		"HudWeaponLowAmmoImage"
		"xpos"			"0"
		"ypos"			"45"
		"zpos"			"4"
		"wide"			"120"
		"tall"			"3"
		"visible"		"0"
		"enabled"		"1"
		"image"			"meridian/mer_alert"
		"scaleImage"	"1"
	}

	"AmmoInClip"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"AmmoInClip"
		"font"			"MerAmmo"
		"fgcolor"		"236 240 244 255"
		"xpos"			"6"
		"ypos"			"0"
		"zpos"			"5"
		"wide"			"56"
		"tall"			"48"
		"visible"		"0"
		"enabled"		"1"
		"textAlignment"	"east"
		"labelText"		"%Ammo%"
	}

	"AmmoInClipShadow"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"AmmoInClipShadow"
		"font"			"MerAmmo"
		"fgcolor"		"0 0 0 110"
		"xpos"			"7"
		"ypos"			"1"
		"zpos"			"4"
		"wide"			"56"
		"tall"			"48"
		"visible"		"0"
		"enabled"		"1"
		"textAlignment"	"east"
		"labelText"		"%Ammo%"
	}

	"AmmoInReserve"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"AmmoInReserve"
		"font"			"MerAmmoReserve"
		"fgcolor"		"150 160 172 255"
		"xpos"			"68"
		"ypos"			"1"
		"zpos"			"7"
		"wide"			"46"
		"tall"			"48"
		"visible"		"0"
		"enabled"		"1"
		"textAlignment"	"west"
		"labelText"		"%AmmoInReserve%"
	}

	"AmmoInReserveShadow"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"AmmoInReserveShadow"
		"font"			"MerAmmoReserve"
		"fgcolor"		"0 0 0 110"
		"xpos"			"69"
		"ypos"			"2"
		"zpos"			"6"
		"wide"			"46"
		"tall"			"48"
		"visible"		"0"
		"enabled"		"1"
		"textAlignment"	"west"
		"labelText"		"%AmmoInReserve%"
	}

	"AmmoNoClip"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"AmmoNoClip"
		"font"			"MerAmmo"
		"fgcolor"		"236 240 244 255"
		"xpos"			"6"
		"ypos"			"0"
		"zpos"			"5"
		"wide"			"104"
		"tall"			"48"
		"visible"		"0"
		"enabled"		"1"
		"textAlignment"	"east"
		"labelText"		"%Ammo%"
	}

	"AmmoNoClipShadow"
	{
		"ControlName"	"CExLabel"
		"fieldName"		"AmmoNoClipShadow"
		"font"			"MerAmmo"
		"fgcolor"		"0 0 0 110"
		"xpos"			"7"
		"ypos"			"1"
		"zpos"			"4"
		"wide"			"104"
		"tall"			"48"
		"visible"		"0"
		"enabled"		"1"
		"textAlignment"	"east"
		"labelText"		"%Ammo%"
	}
}
