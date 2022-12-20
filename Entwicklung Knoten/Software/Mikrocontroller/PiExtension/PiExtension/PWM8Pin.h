#pragma once

/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: PWM8Pin.h
 * @description	:
 *		Erweitert einen IO-Pin um seine PWM-Funktion
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-12-19 11:57:32
 * @version		: 1.0
 */

#include <Arduino.h>
#include "ATTINY_x4_Register.h"
#include "IOPin.h"
#include "SLTask.h"

#if !defined(__AVR_ATtiny24__) && !defined(__AVR_ATtiny44__) && !defined(__AVR_ATtiny84__)
#error MIKROCONTROLLER NICHT UNTERSTÜTZT!
#endif

#define MIN_FREQUENCY 50.f		//50 Hz
#define MAX_FREQUENCY 16e3f		//16kHz

class PWM8Pin : public IOPin, private SLTask
{
private:
	enum TimerChannel : uint8_t { A, B };

	ERROR_t							_cfgError			= ERROR_t::GENERAL_OK;

	HW::TIMER8_t*					_tReg;
	TimerChannel					_channel;


protected:
	// Geerbt über SLTask
	virtual void					proceed() override;

public:
									PWM8Pin(HW::PORT_t* const port, uint8_t pin);

	ERROR_t							playFrequency(float frequency, uint16_t duration = 0);

	// Geerbt über IIICCallable
	virtual ERROR_t					call(Function func, IICRequest* req, IICResponse* rsp) override;
};

