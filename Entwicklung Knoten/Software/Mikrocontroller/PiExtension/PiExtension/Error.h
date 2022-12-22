#pragma once

/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: Error.h
 * @description	:
 *		Implementiert die Fehlercodes aller Klassen, die w�hrend der Systemausf�hrung auftreten k�nnen
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-05-03 08:40:58
 * @version		: 1.0
 */

#include <Arduino.h>

enum ERROR_t : uint8_t {
	GENERAL_OK						=   0,
	UNKNOWN_ERROR					=   1,
	NOT_IMPLEMENTED					=   2,

	TASK_NO_MORE_RESSOURCES			=  10,	// Task konnte nicht gestartet werden, da bereits alle Ressourcen verbraucht sind
	TASK_ALREADY_RUNNING			=  11,	// Task kann nicht gestartet werden, da dieser bereits l�uft
	TASK_NOT_RUNNING				=  12,	// Task kann nicht gestoppt werden, da dieser nicht gestartet wurde
									   
	IIC_INVALID_ADDRESS				=  20,	// Die angegebene IIC Slave-Adresse liegt au�erhalb des g�ltigen Bereichs
	IIC_BUFFER_OVERFLOW				=  21,	// In den Pufferspeicher k�nnen keine weiteren Daten hinzugef�gt werden
	IIC_BUFFER_EMPTY				=  22,	// Wert kann nicht aus Pufferspeicher gelesen werden, da zu wenige Bytes vorliegen

	IOPIN_NOT_AN_IOPIN				=  30,	// Der angegebene Pin kann nicht der Funktion IOPin zugewiesen werden

	ADCPIN_NOT_AN_ADCPIN			=  40,	// Der angegebene Pin kann nicht der Funktion ADCPin zugewiesen werden
	ADCPIN_INVALID_PRESCALER		=  41,	// Der �bergebene Prescaler ist ung�ltig
	ADCPIN_INVALID_REF_VOLTAGE		=  42,	// Die angegebene Referenzspannung ist ung�ltig

	GPIO_NOT_EXISTING				=  50,	// Das angegebene GPIO-Pin existiert nicht
	GPIO_FUNCTION_UNKNOWN			=  51,	// Die angegebene GPIO-Funktion kann auf diesem Pin nicht ausgef�hrt werden
	GPIO_CALL_INVALID				=  52,	// Der I2C Frame hat zu viele Parameter enthalten, um einen Aufruf auf dem spezifizierten GPIO-Pin zu starten

	PWMPIN_NOT_ANPWMPIN				=  60,	// Der angegebene Pin kann nicht als PWM-Pin verwendet werden
	PWMPIN_USED_BY_OTHER_INSTANCE	=  61,	// Der angegebene PWM-Pin wird derzeit von einer anderen Instanz verwendet
	PWMPIN_FREQUENCY_OUT_OF_RANGE	=  62,	// Die spezifizierte Frequenz ist ung�ltig
};