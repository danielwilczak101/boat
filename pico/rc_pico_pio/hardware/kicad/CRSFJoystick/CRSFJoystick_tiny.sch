EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L pico:level_converter U2
U 1 1 61F26C7D
P 3900 1750
F 0 "U2" H 3900 2265 50  0000 C CNN
F 1 "level_converter" H 3900 2174 50  0000 C CNN
F 2 "pico:level_converter" H 3900 2200 50  0001 C CNN
F 3 "" H 3900 2200 50  0001 C CNN
	1    3900 1750
	1    0    0    -1  
$EndComp
$Comp
L pico:CRSF_RX U3
U 1 1 61F27D36
P 5500 1750
F 0 "U3" H 5628 1801 50  0000 L CNN
F 1 "CRSF_RX" H 5628 1710 50  0000 L CNN
F 2 "pico:ELRS_EP2" H 5450 2000 50  0001 C CNN
F 3 "" H 5450 2000 50  0001 C CNN
	1    5500 1750
	1    0    0    -1  
$EndComp
Text GLabel 4200 1700 2    50   Input ~ 0
5V
Text GLabel 5300 1700 0    50   Input ~ 0
5V
Text GLabel 5300 1600 0    50   Input ~ 0
GND
Text GLabel 3600 1800 0    50   Input ~ 0
GND
Text GLabel 4200 1800 2    50   Input ~ 0
GND
Text GLabel 3600 1700 0    50   Input ~ 0
3v3
Text GLabel 3600 1600 0    50   Input ~ 0
TX
Text GLabel 3600 1500 0    50   Input ~ 0
RX
Text GLabel 4200 1600 2    50   Input ~ 0
CRSF_RX
Text GLabel 5300 1900 0    50   Input ~ 0
CRSF_RX
Text GLabel 5300 1800 0    50   Input ~ 0
CRSF_TX
Text GLabel 4200 1500 2    50   Input ~ 0
CRSF_TX
Text GLabel 2500 1500 0    50   Input ~ 0
5V
Text GLabel 3150 1900 2    50   Input ~ 0
TX
Text GLabel 3150 2000 2    50   Input ~ 0
RX
$Comp
L pico:Tiny2040 U1
U 1 1 61F21E8C
P 2850 1850
F 0 "U1" H 2825 2465 50  0000 C CNN
F 1 "Tiny2040" H 2825 2374 50  0000 C CNN
F 2 "pico:tiny2040_no_swd" H 2650 2350 50  0001 C CNN
F 3 "" H 2650 2350 50  0001 C CNN
	1    2850 1850
	1    0    0    -1  
$EndComp
Text GLabel 2500 1600 0    50   Input ~ 0
GND
Text GLabel 2500 1700 0    50   Input ~ 0
3v3
Text GLabel 2500 2200 0    50   Input ~ 0
GND
$Comp
L pico:CRSF_RX U4
U 1 1 61F300A3
P 5500 2250
F 0 "U4" H 5628 2301 50  0000 L CNN
F 1 "CRSF_RX" H 5628 2210 50  0000 L CNN
F 2 "pico:ELRS_EP2" H 5450 2500 50  0001 C CNN
F 3 "" H 5450 2500 50  0001 C CNN
	1    5500 2250
	1    0    0    -1  
$EndComp
Text GLabel 5300 2100 0    50   Input ~ 0
GND
Text GLabel 5300 2200 0    50   Input ~ 0
5V
Text GLabel 5300 2300 0    50   Input ~ 0
CRSF_TX
Text GLabel 5300 2400 0    50   Input ~ 0
CRSF_RX
$Comp
L Mechanical:MountingHole H1
U 1 1 61F351EE
P 750 1900
F 0 "H1" H 850 1946 50  0000 L CNN
F 1 "MountingHole" H 850 1855 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 750 1900 50  0001 C CNN
F 3 "~" H 750 1900 50  0001 C CNN
	1    750  1900
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H2
U 1 1 61F354B7
P 750 2100
F 0 "H2" H 850 2146 50  0000 L CNN
F 1 "MountingHole" H 850 2055 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 750 2100 50  0001 C CNN
F 3 "~" H 750 2100 50  0001 C CNN
	1    750  2100
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H3
U 1 1 61F3573F
P 750 2300
F 0 "H3" H 850 2346 50  0000 L CNN
F 1 "MountingHole" H 850 2255 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 750 2300 50  0001 C CNN
F 3 "~" H 750 2300 50  0001 C CNN
	1    750  2300
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H4
U 1 1 61F359F0
P 750 2500
F 0 "H4" H 850 2546 50  0000 L CNN
F 1 "MountingHole" H 850 2455 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 750 2500 50  0001 C CNN
F 3 "~" H 750 2500 50  0001 C CNN
	1    750  2500
	1    0    0    -1  
$EndComp
$EndSCHEMATC
