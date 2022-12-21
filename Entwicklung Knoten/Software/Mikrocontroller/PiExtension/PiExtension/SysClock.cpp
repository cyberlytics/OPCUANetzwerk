#include "SysClock.h"
#include <util/atomic.h>

#pragma region  SysClock

SysClock Clock;

SysClock::SysClock()
{
	//Timer zurücksetzen
	SYSTIMER->timsk														= 0;
	SYSTIMER->tccra = SYSTIMER->tccrb = SYSTIMER->tccrc					= 0;
	SYSTIMER->tcnt  = SYSTIMER->ocra  = SYSTIMER->ocrb = SYSTIMER->icr	= 0;

	ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
		SYSTIMER->tccrb = (0b010 << 0);	//Prescaler 8 -> Bei 8MHz = 1us/Clock
		SYSTIMER->timsk = (0b1   << 0);	//Timer Overflow ISR aktivieren
		SYSTIMER->tifr  = (0b1   << 0);	//ggf. anliegende Interrupt Flags clearen
	}
}

uint32_t SysClock::micros(void)
{
	union sysTicks { uint32_t ticks; struct { uint16_t lower; uint16_t upper; }; };
	sysTicks t;

	ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
		t.lower = SYSTIMER->tcnt;	//Schnellst möglichst auslesen
		t.upper = _ovfCount;

		//Race Condition prüfen: TCNT ist vor dem Auslesen übergelaufen, wurde durch ISR aber noch nicht in _ovfCount verrechnet
		// ISR Flag anliegend ("noch nicht verrechnet"), t.lower aber bereits übergelaufen?
		if (SYSTIMER->tifr & 1 && t.lower < 0xFFFFU) {
			t.upper++; //Überlauf in t.upper noch verrechnen
		}
	}

	return t.ticks;
}

ISR(TIM1_OVF_vect) {
	Clock._ovfCount++;
}

#pragma endregion



#pragma region usTimeout


void UsTimeout::startTimeout(uint32_t timeoutUs)
{
	_timeout		= timeoutUs;
	_last			= Clock.micros();
	_started		= true;
}

void UsTimeout::stopTimeout(void)
{
	_started		= false;
}

bool UsTimeout::expired(bool restart)
{
	if (!_started || (Clock.micros() - _last) < _timeout) return false;

	if (restart)	_last	 += _timeout;
	else			_started  = false;

	return true;
}

#pragma endregion