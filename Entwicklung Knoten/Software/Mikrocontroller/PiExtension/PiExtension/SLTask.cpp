#include "SLTask.h"

SLTask* SLTask::_tasks[MAX_TASKS];

SLTask::~SLTask()
{
	stop();
}

/**
 * F�gt den aktuellen Task in die Ausf�hrungs-Pipe der Superloop ein
 *
 * @return Fehlercode, falls der Task nicht gestartet werden konnte
 */
ERROR_t SLTask::start(void)
{
	//Task l�uft bereits?
	if (_isRunning) return ERROR_t::TASK_ALREADY_RUNNING;

	//Suche freien Slot in Ausf�hrungs-Pipe
	for (uint8_t i = 0; i < MAX_TASKS; i++) {
		if (_tasks[i] == 0) { // Nicht belegten Slot gefunden? -> Diesen Task einf�gen
			_tasks[i]	= this;
			_isRunning	= true;
			return ERROR_t::GENERAL_OK;
		}
	}

	//Kein freier Slot gefunden? -> Fehler
	return ERROR_t::TASK_NO_MORE_RESSOURCES;
}


/**
 * Entfernt den aktuellen Task aus der Ausf�hrungs-Pipe
 *
 * @return Fehlercode, falls der Task nicht gestoppt werden konnte
 */
ERROR_t SLTask::stop(void)
{
	//Suche aktuellen Task in Pipe
	for (uint8_t i = 0; i < MAX_TASKS; i++) {
		if (_tasks[i] == this) { // Task gefunden?
			_tasks[i]	= 0;
			_isRunning	= false;
			return ERROR_t::GENERAL_OK;
		}
	}

	return ERROR_t::TASK_NOT_RUNNING;
}

/**
 * F�hrt eine Iteration aller gestarteten Tasks durch
 *
 * @return Fehlercode, falls der Task nicht gestoppt werden konnte
 */
void SLTask::proceedTasks()
{
	for (uint8_t i = 0; i < MAX_TASKS; i++) {
		if (_tasks[i] != 0) _tasks[i]->proceed();
	}
}

/**
 * @return Gibt zur�ck, ob der Task gerade ausgef�hrt wird
 */
bool SLTask::isRunning()
{
	return _isRunning;
}