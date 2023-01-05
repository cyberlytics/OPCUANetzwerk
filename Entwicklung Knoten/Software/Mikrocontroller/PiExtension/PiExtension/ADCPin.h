#pragma once

/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: ADCPin.h
 * @description	:
 *		Erweitert einen IO-Pin um seine ADC-Funktion
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-12-15 17:15:22
 * @version		: 1.0
 */

#include <Arduino.h>
#include "ATTINY_x4_Register.h"
#include "Error.h"
#include "IOPin.h"

class ADCPin : public IOPin
{
public:
	enum RefVoltage : uint8_t { V5 = 0b00 << 6, V1_1 = 0b10 << 6 };
	enum Prescaler  : uint8_t { P2 = 0b001, P4 = 0b010, P8 = 0b011, P16 = 0b100, P32 = 0b101, P64 = 0b110, P128 = 0b111 };

private:
	ERROR_t							_cfgError			= ERROR_t::GENERAL_OK;

	const uint8_t					_mux;

public:
									ADCPin(HW::PORT_t* const port, uint8_t pin);

	ERROR_t							sample(Prescaler presc, RefVoltage ref, uint16_t& val, bool pullup=false);

	// Geerbt über IIICCallable
	virtual ERROR_t					call(Function func, IICRequest* req, IICResponse* rsp) override;

};

