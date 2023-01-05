#pragma once

/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: NonAssignable.h
 * @description	:
 *		Grundklasse zum Blockieren des Copy-Konstruktors für Ressourcen-Objekte
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-12-19 18:54:22
 * @version		: 1.0
 */

#include <Arduino.h>
#include "ATTINY_x4_Register.h"
#include "Error.h"

#pragma region SysClock

#define SYSTIMER HW::timer1

extern "C" void TIM1_OVF_vect(void) __attribute__((signal));

class SysClock {
private:
	volatile uint16_t				_ovfCount			= 0;

	friend void						TIM1_OVF_vect(void);

public:
									SysClock();

	uint32_t						micros(void);
};

extern SysClock Clock;

#pragma endregion



#pragma region usTimeout

class UsTimeout {
private:
	bool							_started			= false;
	uint32_t						_timeout			= 0;
	uint32_t						_last				= 0;

public:
	void							startTimeout(uint32_t timeoutUs);
	void							stopTimeout(void);
	bool							expired(bool restart = false);

};

#pragma endregion