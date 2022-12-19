#pragma once

/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: SLTask.h
 * @description	:
 *		Implementiert eine Superloop-Architektur zur Ausführung mehrerer Pseudoparalleler Aufgaben
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-12-06 07:57:13
 * @version		: 1.0
 */

#include <Arduino.h>
#include "Error.h"
#include "NonAssignable.h"

#define MAX_TASKS 8

class SLTask : private NonAssignable
{
private:
	bool				_isRunning					= false;
	static SLTask*		_tasks[MAX_TASKS];

protected:
	ERROR_t				start(void);
	ERROR_t				stop(void);

	virtual void		proceed()					= 0; //Override

public:
						~SLTask();
	
	static void			proceedTasks();
	bool				isRunning();

};

