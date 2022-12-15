#pragma once

/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: IOPin.h
 * @description	:
 *		Steuert die digitale Funktionalität eines Pins
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-12-14 07:53:43
 * @version		: 1.0
 */

#include <Arduino.h>
#include "ATTINY_x4_Register.h"
#include "Error.h"
#include "IIICCallable.h"

class IOPin : public IIICCallable
{
private:
	ERROR_t							_cfgError			= ERROR_t::GENERAL_OK;

	HW::PORT_t* const				_port				= NULL;
	const uint8_t					_mask				= 0;

public:
									IOPin(HW::PORT_t* const port, uint8_t pin);

	ERROR_t							output(bool value);
	ERROR_t							input(bool& value, bool pullup = false);



	// Geerbt über IIICCallable
	virtual ERROR_t					call(Function func, IICRequest* req, IICResponse* rsp) override;

};

