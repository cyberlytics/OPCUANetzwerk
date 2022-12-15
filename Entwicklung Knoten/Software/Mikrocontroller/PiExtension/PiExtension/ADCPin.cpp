#include "ADCPin.h"

ADCPin::ADCPin(HW::PORT_t* const port, uint8_t pin) : IOPin(port, pin), _mux(pin)
{
	if (port != HW::port_a || pin > 7) { _cfgError = ERROR_t::ADCPIN_NOT_AN_ADCPIN; return; }
}

ERROR_t ADCPin::sample(Prescaler presc, RefVoltage ref, uint16_t& val)
{
	bool tmp;
	ERROR_t e;

	if (_cfgError != ERROR_t::GENERAL_OK)			return _cfgError;	// Klasse nicht richtig konfiguriert?
	if ((e = input(tmp)) != ERROR_t::GENERAL_OK)	return e;			// Pin als Input konfigurieren

	HW::adc->admux  = ref | _mux;				// Referenz-Spannung und Multiplexer über MUX-Register einstellen
	HW::adc->adcsra = (0b11010 << 3) | presc;	// ADC enablen, starten, interrupt clearen und prescaler setzen
	while (HW::adc->adcsra & (1 << 6));			// Warte, bis ADC Konversation beendet ist

	val = HW::adc->data;						// Daten auslesen

	return ERROR_t::GENERAL_OK;
}

ERROR_t ADCPin::call(Function func, IICRequest* req, IICResponse* rsp)
{
	ERROR_t e;

	switch (func) {
		case Function::ADCPIN_SAMPLE: {
			Prescaler presc;											// Prescaler ermitteln
			if ((e = req->read(presc))			!= ERROR_t::GENERAL_OK)	return e;
			if (presc < Prescaler::P2 || presc > Prescaler::P128)		return ERROR_t::ADCPIN_INVALID_PRESCALER;

			RefVoltage ref;												// Referenzspannung ermitteln
			if ((e = req->read(ref))			!= ERROR_t::GENERAL_OK)	return e;
			if (ref != RefVoltage::V5 && ref != RefVoltage::V1_1)		return ERROR_t::ADCPIN_INVALID_REF_VOLTAGE;

			if (req->size() != 0)										return ERROR_t::GPIO_CALL_INVALID;	// Input-Buffer enthält hier noch Bytes? -> Ungültiger Call

			uint16_t value;												// ADC Messung durchführen
			if ((e = sample(presc, ref, value)) != ERROR_t::GENERAL_OK)	return e;
			if ((e = rsp->write(value))			!= ERROR_t::GENERAL_OK) return e;
		} break;

		// Funktion in dieser Klasse nicht definiert
		default: return IOPin::call(func, req, rsp); // Sonst Funktionsaufruf an untergeordnete Klasse weiterreichen
	}
}