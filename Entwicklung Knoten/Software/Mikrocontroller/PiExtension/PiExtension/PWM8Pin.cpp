#include "PWM8Pin.h"
#include <util/atomic.h>

PWM8Pin::PWM8Pin(HW::PORT_t* const port, uint8_t pin) : IOPin(port, pin), SLTask()
{
	if (port == HW::port_b && pin == 2) {
		_tReg		= HW::timer0;
		_channel	= TimerChannel::A;
	}
	else if (port == HW::port_a && pin == 7) {
		_tReg		= HW::timer0;
		_channel	= TimerChannel::B;
	}
	else { _cfgError = ERROR_t::PWMPIN_NOT_ANPWMPIN; return; }

	ERROR_t e;
	if ((e = output(false)) != ERROR_t::GENERAL_OK) { _cfgError = e; return; } // PWM Pin als Output + Low
	if ((e = start())       != ERROR_t::GENERAL_OK) { _cfgError = e; return; } // Versuche Task zu starten

	ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
		_tReg->tccra = _tReg->tccrb = 0;
		_tReg->ocra  = _tReg->ocrb  = 0;
		_tReg->tcnt  = 0;

		_tReg->tccra |= 0b10;	//WGM Auf CTC stellen
	}
}

ERROR_t	PWM8Pin::playFrequency(float frequency, uint32_t duration_us) {
	if (_cfgError != ERROR_t::GENERAL_OK) return _cfgError;	// Klasse nicht richtig konfiguriert?

	//Register ermitteln
	uint8_t com, foc;
	volatile uint8_t* ocr;
	switch (_channel) {
		case TimerChannel::A: ocr = &_tReg->ocra; com = 6; foc = 1 << 7; break;
		case TimerChannel::B: ocr = &_tReg->ocra; com = 4; foc = 1 << 6; break;
		default: return ERROR_t::NOT_IMPLEMENTED;
	}

	ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
		if (_tReg->tccrb && !(_tReg->tccra & (0b11 << com))) return ERROR_t::PWMPIN_USED_BY_OTHER_INSTANCE;

		//PWM abschalten?
		if (frequency == 0) {
			_tReg->tccrb  = 0;
			_tReg->tcnt   = 0;
			_tReg->tccra &= ~(0b11 << com); // Timer von Pin disconnecten, sodass IOPin Steuerung wieder übernimmt
			return ERROR_t::GENERAL_OK;
		}
	}

	//Frequenz außerhalb darstellbarer Frequenz oder über festgelegter Maximalfrequenz?
	if (frequency < 0 || frequency > 4e6f || frequency < MIN_FREQUENCY || frequency > MAX_FREQUENCY) return ERROR_t::PWMPIN_FREQUENCY_OUT_OF_RANGE;

	//Kleinsten Prescaler wählen, um größt möglichste Timergenauigkeit zu bekommen
	uint8_t presc, prescRegVal;
	if		(frequency >= 15625.00f) { prescRegVal = 0b001; presc =    1; }		// Prescaler    1 -> FMin = 15625.00Hz, FMax =     4.00MHz
	else if (frequency >=  1953.13f) { prescRegVal = 0b010; presc =    8; }		// Prescaler    8 -> FMin =  1953.13Hz, FMax =   500.00kHz
	else if (frequency >=   244.14f) { prescRegVal = 0b011; presc =   64; }		// Prescaler   64 -> FMin =   244.14Hz, FMax =    62.50kHz
	else if (frequency >=    61.04f) { prescRegVal = 0b100; presc =  256; }		// Prescaler  256 -> FMin =    61.04Hz, FMax = 15625.00 Hz
	else if (frequency >=    15.26f) { prescRegVal = 0b101; presc = 1024; }		// Prescaler 1024 -> FMin =    15.26Hz, FMax =  3906.25 Hz
	else return ERROR_t::PWMPIN_FREQUENCY_OUT_OF_RANGE;

	ERROR_t e;
	if ((e = output(false)) != ERROR_t::GENERAL_OK) return e; //Pin als Output setzen

	//OCR berechnen
	uint8_t ocrval = (F_CPU >> 1) / (frequency * presc) - 0.5;

	if (duration_us > 0)	_offTimeout.startTimeout(duration_us);
	else					_offTimeout.stopTimeout();		

	//Timer bereits mit gleichem Prescaler und gleichem PWM-Wert konfiguriert? -> Nothing todo
	if ((_tReg->tccrb & 0b111) == prescRegVal && *ocr == ocrval) return ERROR_t::GENERAL_OK;

	ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
		_tReg->tccra |= (0b01 << com);	//Output auf Pin schalten
		
		_tReg->tccrb = 0;				//Timer temporär anhalten, um Race-Condition zu vermeiden
		*ocr = ocrval;					//Neuen OCR Wert setzen
		if (_tReg->tcnt > ocrval) {		//OCR Wert Änderung hat dafür gesort, dass es zu einem Timer overflow gekommen ist? -> Manuell Forcen
			_tReg->tcnt   = 0;
			_tReg->tccrb  = foc;
		}
		_tReg->tccrb  = prescRegVal;	//Timer (wieder) freigeben
	}

	return ERROR_t::GENERAL_OK;
}



void PWM8Pin::proceed()
{
	ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
		if (_offTimeout.expired()) playFrequency(0);
	}
}


ERROR_t PWM8Pin::call(Function func, IICRequest* req, IICResponse* rsp)
{
	ERROR_t e;

	switch (func) {
		case Function::PWMPIN_PLAY_FREQUENCY: {
			float freq;			//PWM Frequenz ermitteln
			uint32_t dur = 0;	//Ausführungsdauer ermitteln

			if ((e = req->read(freq))					!= ERROR_t::GENERAL_OK)	return e;
			if (req->size() > 0 && (e = req->read(dur)) != ERROR_t::GENERAL_OK) return e;
			if (req->size() != 0)												return ERROR_t::GPIO_CALL_INVALID;	// Input-Buffer enthält hier noch Bytes? -> Ungültiger Call
			if ((e = playFrequency(freq, dur))			!= ERROR_t::GENERAL_OK) return e;
		} break;

		default: return IOPin::call(func, req, rsp);
	}

	return ERROR_t::GENERAL_OK;
}
