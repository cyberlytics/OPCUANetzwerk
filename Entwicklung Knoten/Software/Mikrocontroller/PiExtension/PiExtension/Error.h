#pragma once

/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: Error.h
 * @description	:
 *		Implementiert die Fehlercodes aller Klassen, die während der Systemausführung auftreten können
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-05-03 08:40:58
 * @version		: 1.0
 */

#include <Arduino.h>

enum ERROR_t : uint8_t {
	GENERAL_OK						=   0,
	UNKNOWN_CMD						=   1,

	TASK_NO_MORE_RESSOURCES			=  20,	// Task konnte nicht gestartet werden, da bereits alle Ressourcen verbraucht sind
	TASK_ALREADY_RUNNING			=  21,	// Task kann nicht gestartet werden, da dieser bereits läuft
	TASK_NOT_RUNNING				=  22,	// Task kann nicht gestoppt werden, da dieser nicht gestartet wurde
									   
	IIC_INVALID_ADDRESS				=  30,	// Die angegebene IIC Slave-Adresse liegt außerhalb des gültigen Bereichs
	IIC_BUFFER_OVERFLOW				=  31,	// In den Pufferspeicher können keine weiteren Daten hinzugefügt werden
	IIC_BUFFER_EMPTY				=  32,	// Wert kann nicht aus Pufferspeicher gelesen werden, da zu wenige Bytes vorliegen
};