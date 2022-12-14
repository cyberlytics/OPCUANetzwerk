#include "IICSlave.h"
#include "ATTINY_x4_Register.h"
#include <util/atomic.h>

//I2C fest verdrahtet auf Port A Pin 4 (SCL) und Pin 6 (SDA)
#define IIC_PORT HW::port_a
#define SCL_MASK (1 << 4)
#define SDA_MASK (1 << 6)

#define WAIT_START() { HW::usi->usicr = 0b00101000; HW::usi->usisr = 0b11100000; }	// IIC Clock auf Hold, wenn Start Flag erkannt
#define WAIT_DATA()  { HW::usi->usicr = 0b00111000; HW::usi->usisr = 0b01100000; }	// IIC Clock auf Hold, wenn Start Flag oder Daten erkannt


inline void IICSlave::reset()
{
	_mode = IIC_Mode::Idle;
	WAIT_START();
}

inline bool IICSlave::isStop()
{
	IIC_PORT->ddr &= ~SDA_MASK; //SDA input

	uint8_t pinstate;
	while (!((pinstate = IIC_PORT->pin & (SCL_MASK | SDA_MASK)) & SCL_MASK)); // Warte auf SCL rising Edge oder SDA Falling Edge
	if (pinstate & SDA_MASK) return false; // SDA war high bei clk-edge? -> kein Stop

	while ((pinstate = IIC_PORT->pin & (SCL_MASK | SDA_MASK)) == SCL_MASK); //Warte auf SCL falling Edge oder SDA rising Edge
	return pinstate == (SCL_MASK | SDA_MASK); // SDA ist auch high gewechselt? -> Stop-Condition
}

inline void IICSlave::sendACK(bool receiveNext)
{
	HW::usi->usidr  = 0; 
	IIC_PORT->ddr  |= SDA_MASK;					//SDA als Ausgang setzen
	HW::usi->usisr  = 0b01100000 | 0xE;			//Clear OV IF (Release SCK) + Counter auf 14 Setzen (active Wait 1 Bit shiftout)

	while (!(HW::usi->usisr & (1 << 6)));		//Active Wait auf Ack Shift out
	if(receiveNext) IIC_PORT->ddr &= ~SDA_MASK;	//Falls nächstes Byte Empfangsbyte -> SDA wieder als Input
}

inline bool IICSlave::getACK() {
	IIC_PORT->ddr  &= ~SDA_MASK;				//SDA als Input setzen
	HW::usi->usisr	= 0b01100000 | 0xE;			//Clear OV IF (Release SCK) + Counter auf 14 Setzen (active Wait 1 Bit shiftin)

	while (!(HW::usi->usisr & (1 << 6)));		//Active Wait auf Ack/Nack Shift in
	bool isACK = !(HW::usi->usidr & 1);			//Bit 0 == 0 ? -> ACK vom Master
	if (isACK) IIC_PORT->ddr |= SDA_MASK;		//Falls Master ACK gesendet hat -> Wieder als Output 

	return isACK;
}

void IICSlave::startDetected()
{
	IIC_PORT->ddr &= ~SDA_MASK; // SDA als Input

	uint8_t pinstate;
	while ((pinstate = IIC_PORT->pin & (SCL_MASK | SDA_MASK)) == SCL_MASK); // Warte SCL Falling Edge oder SDA Rising

	if (pinstate & SDA_MASK) { reset(); return; } //SDA nicht nach Low gewechselt? -> kein Start
	WAIT_DATA();                 // Datensampling aktivieren
	HW::usi->usisr |= (1 << 7);  // Start Flag abgearbeitet

	if (isStop()) reset();
	else {
		IIC_Mode old = _mode; //Abhängig von alten Zustand -> War vorher Empfangsdatensampling aktiv? -> Dies ist der Restart-Call
		if (old == IIC_Mode::RecvData) {
			_mode = IIC_Mode::RecvAdrRestart; //Auf Adress-Recall warten und schonmal Callback aufrufen
			_rspBuf.clear();
			_lastError = _callback(&_reqBuf, &_rspBuf);
		}
		else {
			_mode  = IIC_Mode::RecvAdr; //Sonst genereller Neustart
			_chksm = 0;
		}
	}
}

void IICSlave::dataCompleted()
{
	uint8_t val = HW::usi->usidr; //Empfangsbyte auslesen
	switch (_mode) {

		// Modus Adressempfang?
		case IIC_Mode::RecvAdr: { 
			uint8_t adr = val & 0xFE;			//Adresse und Read/Write splitten
			bool read   = val & 1;
			//TODO: Direkt Callback + SendData
			if (adr != _adr || read) reset();	// Adresse != dieser Client? oder mode Read? Send nack und reset
			else {
				_chksm += val;
				_mode   = IIC_Mode::RecvData;	// In Modus Datenempfang wechseln
				_reqBuf.clear();				//Empfangspuffer clearen
				sendACK(true);
				WAIT_DATA();					//Datenempfang aktivieren
				if (isStop()) reset();			//Folgt danach Stop-Signal -> Ende
			}
		} break;

		// Modus Empfangspuffer schreiben
		case IIC_Mode::RecvData: {
			if (_reqBuf.writeByte(val) != ERROR_t::GENERAL_OK) reset(); //Puffer voll? -> Nack Idle
			else {
				_chksm += val;
				sendACK(true);
				WAIT_DATA();						//Datenempfang aktivieren
				if (isStop()) reset();				//Folgt danach Stop-Signal -> Ende
			}
		} break;

		// Modus Restart + Adressempfang
		case IIC_Mode::RecvAdrRestart: {
			uint8_t adr = val & 0xFE;
			bool read   = val & 1;
			if (adr != _adr || !read) reset();		//Adresse != dieser Client? oder mode Write? Send nack und reset
			else {
				_chksm += val;
				uint8_t len = (_lastError != ERROR_t::GENERAL_OK) ? 2 : _rspBuf.size() + 2;	//Wenn Fehler -> Datenübertragung direkt skippen (Länge 2, da Error + Checksum folgt)
				_chksm += len;
				_mode	= (len <= 2) ? IIC_Mode::SendError : IIC_Mode::SendData;	//Keine Daten zum Senden? Direkt zu SendError springen
				sendACK(false);						//Send ACK und SDA auf Output lassen
				USIDR	= len;						//Längenbyte fürs Senden vorbereiten
				WAIT_DATA();						//Clk wieder freigeben
			}
		} break;

		// Modus vom Callback zurückgegebene Werte schreiben
		case IIC_Mode::SendData: {
			if (!getACK()) reset();					//Master hat NACK gesendet? -> reset
			else {
				uint8_t send = _rspBuf.readByte();	//Nächstes Byte laden
				_chksm += send;
				USIDR = send;
				WAIT_DATA();						//Clk freigeben
				if (!_rspBuf.size()) _mode = IIC_Mode::SendError; //Keine Bytes mehr? -> Zu Errorbyte wechseln
			}
		} break;

		// Modus Fehlerstatus senden
		case IIC_Mode::SendError: {
			if (!getACK()) reset();					//Master hat NACK gesendet? -> reset
			else {
				uint8_t send = _lastError;			//Errorcode laden
				_chksm += send;
				USIDR	= send;						
				WAIT_DATA();						//Clk freigeben
				_mode	= IIC_Mode::SendChksm;		//Als nächstes Checksum senden
			}
		} break;

		// Modus Checksum senden
		case IIC_Mode::SendChksm: {
			if (!getACK()) reset();					//Master hat NACK gesendet? -> reset
			else {
				USIDR	= _chksm;					//Checksum laden
				WAIT_DATA();						//Clk freigeben
				_mode	= IIC_Mode::Idle;			//Rest erledigt IIC. Wenn OV. Wenn fertig->Default reset (siehe unten)
			}
		} break;

		default: {
			IIC_PORT->ddr &= ~SDA_MASK;	//SDA input
			reset();					//Auf neuen (Re-)Start warten
		}
	}

}

IICSlave::IICSlave(uint8_t address, IICCallback callback) : _adr(address << 1), _callback(callback)
{
	if (address > 127) { _cfgError = ERROR_t::IIC_INVALID_ADDRESS; return; } // IIC Konvention -> Adresse ist nur 7 Bit groß -> 8tes Bit ist für Read/Write
	
	ERROR_t e = start();											// Versuche SLTask zu starten
	if (e != ERROR_t::GENERAL_OK) { _cfgError = e; return; }		// Background-Task ist notwendig, damit kein Deadlock auf I2C Bus entsteht
	 
	ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
		IIC_PORT->port |= SCL_MASK | SDA_MASK;						// Pins auf High Ziehen (Pullups aktivieren)
		IIC_PORT->ddr   = (IIC_PORT->ddr & ~SDA_MASK) | SCL_MASK;	// SDA -> Input (Pullup) und SCL -> Output (Für Clock Hold)
		reset();
	}
	
	HW::port_b->ddr  |= (1 << 0);
	
}

void IICSlave::proceed()
{
	if      (HW::usi->usisr & (1 << 7)) startDetected();
	else if (HW::usi->usisr & (1 << 6)) dataCompleted();

	if (_mode != IIC_Mode::Idle) HW::port_b->port |= (1 << 0);
	else						 HW::port_b->port &= ~(1 << 0);
}
