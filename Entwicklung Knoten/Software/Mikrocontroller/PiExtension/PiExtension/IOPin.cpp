#include "IOPin.h"
#include <util/atomic.h>

IOPin::IOPin(HW::PORT_t* const port, uint8_t pin) : _port(port), _mask(1 << pin)
{ 
	if		(port == HW::port_a && pin < 7) {}	//Port a und Pin richtig
	else if (port == HW::port_b && pin < 3) {}	//Port b und Pin richtig
	else { _cfgError = ERROR_t::IOPIN_NOT_AN_IOPIN; return; }
	
	bool tmp; input(tmp); //Pin auf High Impedance Input konfigurieren, um Hardwareschäden durch Kurzschlüsse zu vermeiden
}

ERROR_t IOPin::output(bool value)
{
	if (_cfgError != ERROR_t::GENERAL_OK) return _cfgError;

	ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
		_port->port  = value ? _port->port | _mask : _port->port & ~_mask;	// Um Störflanke zu vermeiden, zuerst Output schreiben, dann Mode setzen
		_port->ddr  |= _mask;												// Port als Output konfigurieren
	}
}

ERROR_t IOPin::input(bool& value, bool pullup)
{
	if (_cfgError != ERROR_t::GENERAL_OK) return _cfgError;

	ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
		_port->ddr &= ~_mask;												// Port als Input konfigurieren
		_port->port = pullup ? _port->port | _mask : _port->port & ~_mask;	// Pullup einstellen
		value = (_port->pin & _mask) > 0;									// Pin auslesen
	}

	return ERROR_t::GENERAL_OK;
}

ERROR_t IOPin::call(Function func, IICRequest* req, IICResponse* rsp)
{
	ERROR_t e;

	switch (func) {
		//RPC Call input
		case Function::IOPIN_DIGITAL_IN: {
			bool value;
			bool pullup = false;

			if (req->size() > 0 && (e = req->read(pullup)) != ERROR_t::GENERAL_OK)	return e;							// Pullup (optional) spezifiziert? -> versuche auszulesen
			if (req->size() != 0)													return ERROR_t::GPIO_CALL_INVALID;	// Input-Buffer enthält hier noch Bytes? -> Ungültiger Call
			if ((e = input(value, pullup)) != ERROR_t::GENERAL_OK)					return e;							// Funktion ausführen
			if ((e = rsp->write(value))    != ERROR_t::GENERAL_OK)					return e;							// Ergebnis zurückschreiben
		} break;

		//RPC Call output
		case Function::IOPIN_DIGITAL_OUT: {
			bool value;
			if ((e = req->read(value))	!= ERROR_t::GENERAL_OK)	return e;							// Zu schreibenden Wert auslesenn
			if (req->size() != 0)								return ERROR_t::GPIO_CALL_INVALID;	// Input-Buffer enthält hier noch Bytes? -> Ungültiger Call
			if ((e = output(value))		!= ERROR_t::GENERAL_OK)	return e;							// Funktion ausführen
		} break;

		//Funktion in dieser Klasse nicht definiert
		default: return IIICCallable::call(func, req, rsp);										// Sonst Funktionsaufruf an untergeordnete Klasse weiterreichen
	}

	return ERROR_t::GENERAL_OK;
}

