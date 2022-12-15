#pragma once

/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: ATTINY_x4_Register.h
 * @description	:
 *		Implementiert die Registeradressen für die Microcontroller ATTINY24/44/84
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-12-06 09:16:25
 * @version		: 1.0
 */

#include <Arduino.h>

#if !defined(__AVR_ATtiny24__) && !defined(__AVR_ATtiny44__) && !defined(__AVR_ATtiny84__)
#error MIKROCONTROLLER NICHT UNTERSTÜTZT!
#endif

namespace HW {
	#define _BLOCK typedef struct __attribute__((packed)) 

	#pragma region System Functions
	_BLOCK{
		/// <summary>
		///		Power Reduction Register
		///		<para>Bits: [7-4: - ][3: PRTIM1 (r/w)][2: PRTIM0 (r/w)][1: PRUSI (r/w)][0: PRADC (r/w)]</para>
		/// </summary>
		/// <param name="PRTIM1:">Power Reduction Timer/Counter1</param>
		/// <param name="PRTIM0:">Power Reduction Timer/Counter0</param>
		/// <param name="PRUSI:">Power Reduction USI</param>
		/// <param name="PRADC:">Power Reduction ADC</param>
		public:		volatile uint8_t prr;
		private:	volatile uint8_t reserved_0[32];
		/// <summary>
		///		Watchdog Timer Control and Status Register
		///		<para>Bits: [7: WDIF (r/w)][6: WDIE (r/w)][5: WDP3 (r/w)][4: WDCE (r/w)][3: WDE (r/w)][2-0: WDP2-0 (r/w)]</para>
		/// </summary>
		/// <param name="WDIF:">Watchdog Time-out Interrupt Flag</param>
		/// <param name="WDIE:">Watchdog Timeout Interrupt Enable</param>
		/// <param name="WDCE:">Watchdog Change Enable</param>
		/// <param name="WDE:">Watchdog Enable</param>
		/// <param name="xxx:">Watchdog Timer Prescaler</param>
		public:		volatile uint8_t wdtcsr;
		private:	volatile uint8_t reserved_1[4];
		/// <summary>
		///		Clock Prescaler Register
		///		<para>Bits: [7: CLKPCE (r/w)][6-4: - ][3: CLKPS3-0 (r/w)]</para>
		/// </summary>
		/// <param name="CLKPCE:">Clock Prescaler Change Enable</param>
		/// <param name="CLKPS3:">Clock Prescaler Select Bits</param>
		public:		volatile uint8_t clkpr;
		private:	volatile uint8_t reserved_2[10];
		/// <summary>
		///		Oscillator Calibration Register
		///		<para>Bits: [7-0: CAL7-0 (r/w)]</para>
		/// </summary>
		public:		volatile uint8_t osccal;
		private:	volatile uint8_t reserved_3[2];
		/// <summary>
		///		MCU Status Register
		///		<para>Bits: [7-4: - ][3: WDRF (r/w)][2: BORF (r/w)][1: EXTRF (r/w)][0: PORF (r/w)]</para>
		/// </summary>
		/// <param name="WDRF:">Watchdog Reset Flag</param>
		/// <param name="BORF:">Brown-out Reset Flag</param>
		/// <param name="EXTRF:">External Reset Flag</param>
		/// <param name="PORF:">Power-on Reset Flag</param>
		public:		volatile uint8_t mcusr;
		/// <summary>
		///		MCU Control Register
		///		<para>Bits: [7: BODS (r/w)][6: PUD (r/w)][5: SE (r/w)][4-3: SM1-0 (r/w)][2: BODSE (r/w)][1-0: ISC01-0 (r/w)]</para>
		/// </summary>
		/// <param name="BODS:">BOD Sleep</param>
		/// <param name="PUD:">Pull-up Disable</param>
		/// <param name="SE:">Sleep Enable</param>
		/// <param name="SM1-0:">Sleep Mode Select Bits</param>
		/// <param name="BODSE:">BOD Sleep Enable</param>
		/// <param name="ISC01-0:">Interrupt Sense Control</param>
		public:		volatile uint8_t mcucr;
		private:	volatile uint8_t reserved_4[7];
		/// <summary>
		///		Stack Pointer
		///		<para>Bits: [15-0: SP (r/w)]</para>
		/// </summary>
		public:		volatile uint16_t sp;
		/// <summary>
		///		Status Register
		///		<para>Bits: [7: I (r/w)][6: T (r/w)][5: H (r/w)][4: S (r/w)][3: V (r/w)][2: N (r/w)][1: Z (r/w)][0: C (r/w)]</para>
		/// </summary>
		/// <param name="I:">Global Interrupt Enable</param>
		/// <param name="T:">Bit Copy Storage</param>
		/// <param name="H:">Half Carry Flag</param>
		/// <param name="S:">Sign Bit, S = N XOR V</param>
		/// <param name="V:">Two’s Complement Overflow Flag</param>
		/// <param name="N:">Negative Flag</param>
		/// <param name="Z:">Zero Flag</param>
		/// <param name="C:">Carry Flag</param>
		public:		volatile uint8_t sreg;
	} SYS_t;

	/// <summary>
	///		Powermanagement and Sleep Modes
	/// </summary>
	SYS_t* const sys = (SYS_t*)0x20;
	#pragma endregion

	#pragma region Analog Comparator and Analog-to-Digital Converter
	_BLOCK{
		/// <summary>
		///		Digital Input Disable Register
		///		<para>[7-0: ADC7-0D (r/w)]</para>
		/// </summary>
		/// <param name="ADC7-0D">ADC Digital input buffer disable</param>
		public:		volatile uint8_t didr;
		private:	volatile uint8_t reserved_0;
		/// <summary>
		///		ADC Control and Status Register B
		///		<para>[7: BIN (r/w)][6: ACME (r/w)][5: - ][4: ADLAR (r/w)][3: - ][2-0: ADTS2-0 (r/w)]</para>
		/// </summary>
		/// <param name="BIN:">Bipolar Input Mode</param>
		/// <param name="ACME:">Analog Comparator Multiplexer</param>
		/// <param name="ADLAR:">ADC Left Adjust Result</param>
		/// <param name="ADTS2-0:">ADC Auto Trigger Source</param>
		public:		volatile uint8_t adcsrb;
		/// <summary>
		///		ADC Data Register
		///		<para>(ADLAR = 0)[15-10: - ][9-0: ADC9-0 (r)]</para>
		///		<para>(ADLAR = 1)[15-6: ADC9-0 (r)][5-0: - ]</para>
		/// </summary>
		/// <param name="ADC9-0">ADC Conversion Result</param>
		public:		volatile uint16_t data;
		/// <summary>
		///		ADC Control and Status Register A
		///		<para>[7: ADEN (r/w)][6: ADSC (r/w)][5: ADATE (r/w)][4: ADIF (r/w)][3: ADIE (r/w)][2-0: ADPS2-0 (r/w)]</para>
		/// </summary>
		/// <param name="ADEN:">ADC Enable</param>
		/// <param name="ADSC:">ADC Start Conversion</param>
		/// <param name="ADATE:">ADC Auto Trigger Enable</param>
		/// <param name="ADIF:">ADC Interrupt Flag</param>
		/// <param name="ADIE:">ADC Interrupt Enable</param>
		/// <param name="ADPS2-0:">ADC Prescaler Select Bits</param>
		public:		volatile uint8_t adcsra;
		/// <summary>
		///		ADC Multiplexer Selection Register
		///		<para>[7-6: REFS1-0 (r/w)][5-0: MUX5-0 (r/w)]</para>
		/// </summary>
		/// <param name="REFS1-0:">Reference Selection Bits</param>
		/// <param name="MUX5-0:">Analog Channel and Gain Selection Bits</param>
		public:		volatile uint8_t admux;
		/// <summary>
		///		Analog Comparator Control and Status Register
		///		<para>[7: ACD (r/w)][6: ACBG (r/w)][5: ACO (r/w)][4: ACI (r/w)][3: ACIE (r/w)][2: ACIC (r/w)][1-0: ACIS1-0 (r/w)]</para>
		/// </summary>
		/// <param name="ACD:">Analog Comparator Disable</param>
		/// <param name="ACBG:">Analog Comparator Bandgap Select</param>
		/// <param name="ACO:">Analog Comparator Output</param>
		/// <param name="ACI:">Analog Comparator Interrupt Flag</param>
		/// <param name="ACIE:">Analog Comparator Interrupt Enable</param>
		/// <param name="ACIC:">Analog Comparator Input Capture Enable</param>
		/// <param name="ACIS1-0:">Analog Comparator Interrupt Mode Select</param>
		public:		volatile uint8_t acsr;
	} ADC_t;

	/// Analog Comparator and Analog-to-Digital Converter
	ADC_t* const adc = (ADC_t*)0x21;
	#pragma endregion

	#pragma region 8-bit Timer/Counter 0
	_BLOCK{
		/// <summary>
		///		Timer/Counter Control Register A
		///		<para>Bits: [7-6: COMA1-0 (r/w)][5-4: COMB1-0 (r/w)][3-2: - ][1-0: WGM1-0 (r/w)]</para>
		/// </summary>
		/// <param name="COMA1-0:">Compare Output Mode for Channel A</param>
		/// <param name="COMB1-0:">Compare Output Mode for Channel B</param>
		/// <param name="WGM1-0:">Waveform Generation Mode</param>
		public:		volatile uint8_t tccra;
		private:	volatile uint8_t reserved_0;
		/// <summary>
		///		 Timer/Counter
		///		<para>Bits: [7-0: TCNT (r/w)]</para>
		/// </summary>
		public:		volatile uint8_t tcnt;
		/// <summary>
		///		Timer/Counter Control Register B
		///		<para>Bits: [7: FOCA (w)][6: FOCB (w)][5-4: - ][3: WGM2 (r/w)][2-0: CS2-0]</para>
		/// </summary>
		/// <param name="FOCA:">Force Output Compare A</param>
		/// <param name="FOCB:">Force Output Compare B</param>
		/// <param name="WGM2:">Waveform Generation Mode</param>
		/// <param name="CS2-0:">Clock Select</param>
		public:		volatile uint8_t tccrb;
		private:	volatile uint8_t reserved_1[2];
		/// <summary>
		///		Output Compare Register A
		///		<para>Bits: [7-0: OCRA (r/w)]</para>
		/// </summary>
		public:		volatile uint8_t ocra;
		private:	volatile uint8_t reserved_2;
		/// <summary>
		///		Timer/Counter Interrupt Flag Register
		///		<para>Bits: [7-3: - ][2: OCFB (r/w)][1: OCFA (r/w)][0: TOV (r/w)]</para>
		/// </summary>
		/// <param name="OCFB:">Timer/Counter Output Compare B Match Flag</param>
		/// <param name="OCFA:">Timer/Counter Output Compare A Match Flag</param>
		/// <param name="TOV:">Timer/Counter Overflow Flag</param>
		public:		volatile uint8_t tifr;
		/// <summary>
		///		Timer/Counter Interrupt Mask Register
		///		<para>Bits: [7-3: - ][2: OCIEB (r/w)][1: OCIEA (r/w)][0: TOIE (r/w)]</para>
		/// </summary>
		/// <param name="OCIEB:">Timer/Counter Output Compare B Match Interrupt Enable</param>
		/// <param name="OCIEA:">Timer/Counter Output Compare A Match Interrupt Enable</param>
		/// <param name="TOIE:">Timer/Counter Overflow Interrupt Enable</param>
		public:		volatile uint8_t timsk;
		private:	volatile uint8_t reserved_3[2];
		/// <summary>
		///		Output Compare Register B
		///		<para>Bits: [7-0: OCRB (r/w)]</para>
		/// </summary>
		public:		volatile uint8_t ocrb;
	} TIMER0_t;

	/// 8-bit Timer/Counter 0
	TIMER0_t* const timer0 = (TIMER0_t*)0x50;
	#pragma endregion

	#pragma region 16-bit Timer/Counter 1
	_BLOCK{
		/// <summary>
		///		Timer/Counter Interrupt Flag Register
		///		<para>Bits: [7-6: - ][5: ICF (r/w)][4-3: - ][2: OCFB (r/w)][1: OCFA (r/w)][0: TOV (r/w)]</para>
		/// </summary>
		/// <param name="ICF:">Timer/Counter Input Capture Flag</param>
		/// <param name="OCFB:">Timer/Counter Output Compare B Match Flag</param>
		/// <param name="OCFA:">Timer/Counter Output Compare A Match Flag</param>
		/// <param name="TOV:">Timer/Counter Overflow Flag</param>
		public:		volatile uint8_t tifr;
		/// <summary>
		///		Timer/Counter Interrupt Mask Register
		///		<para>Bits: [7-6: - ][5: ICIE (r/w)][4-3: - ][2: OCIEB (r/w)][1: OCIEA (r/w)][0: TOIE (r/w)]</para>
		/// </summary>
		/// <param name="ICIE:">Timer/Counter Input Capture Interrupt Enable</param>
		/// <param name="OCIEB:">Timer/Counter Output Compare B Match Interrupt Enable</param>
		/// <param name="OCIEA:">Timer/Counter Output Compare A Match Interrupt Enable</param>
		/// <param name="TOIE:">Timer/Counter Overflow Interrupt Enable</param>
		public:		volatile uint8_t timsk;
		private:	volatile uint8_t reserved_0[21];
		/// <summary>
		///		Timer/Counter Control Register C
		///		<para>Bits: [7: FOCA (w)][6: FOCB (w)][5-0: - ]</para>
		/// </summary>
		/// <param name="FOCA:">Force Output Compare for Channel A</param>
		/// <param name="FOCB:">Force Output Compare for Channel B</param>
		public:		volatile uint8_t tccrc;
		private:	volatile uint8_t reserved_1;
		/// <summary>
		///		Input Capture Register
		///		<para>Bits: [15-0: ICR (r/w)]</para>
		/// </summary>
		public:		volatile uint16_t icr;
		private:	volatile uint8_t reserved_2[2];
		/// <summary>
		///		Output Compare Register B
		///		<para>Bits: [15-0: OCRB (r/w)]</para>
		/// </summary>
		public:		volatile uint16_t ocrb;
		/// <summary>
		///		Output Compare Register A
		///		<para>Bits: [15-0: OCRA (r/w)]</para>
		/// </summary>
		public:		volatile uint16_t ocra;
		/// <summary>
		///		 Timer/Counter
		///		<para>Bits: [15-0: TCNT (r/w)]</para>
		/// </summary>
		public:		volatile uint16_t tcnt;
		/// <summary>
		///		Timer/Counter Control Register B
		///		<para>Bits: [7: ICNC (r/w)][6: ICES (r/w)][5: - ][4-3: WGM3-2 (r/w)][2-0: CS2-0]</para>
		/// </summary>
		/// <param name="ICNC:">Input Capture Noise Canceller</param>
		/// <param name="ICES:">Input Capture Edge Select</param>
		/// <param name="WGM3-2:">Waveform Generation Mode</param>
		/// <param name="CS2-0:">Clock Select</param>
		public:		volatile uint8_t tccrb;
		/// <summary>
		///		Timer/Counter Control Register A
		///		<para>Bits: [7-6: COMA1-0 (r/w)][5-4: COMB1-0 (r/w)][3-2: - ][1-0: WGM1-0 (r/w)]</para>
		/// </summary>
		/// <param name="COMA1-0:">Compare Output Mode for Channel A</param>
		/// <param name="COMB1-0:">Compare Output Mode for Channel B</param>
		/// <param name="WGM1-0:">Waveform Generation Mode</param>
		public:		volatile uint8_t tccra;
	} TIMER1_t;

	/// 16-bit Timer/Counter 1
	TIMER1_t* const timer1 = (TIMER1_t*)0x2B;
	#pragma endregion

	#pragma region Universal Serial Interface
	_BLOCK{
		/// <summary>
		///		USI Control Register
		///		<para>Bits: [7: USISIE (r/w)][6: USIOIE (r/w)][5-4: USIWM1-0 (r/w)][3-2: USICS1-0 (r/w)][1: USICLK (w)][0: USITC (w)]</para>
		/// </summary>
		/// <param name="USISIE:">Start Condition Interrupt Enable</param>
		/// <param name="USIOIE:">Counter Overflow Interrupt Enable</param>
		/// <param name="USIWM1-0:">Wire Mode</param>
		/// <param name="USICS1-0:">Clock Source Select</param>
		/// <param name="USICLK:">Clock Strobe</param>
		/// <param name="USITC:">Toggle Clock Port Pin</param>
		public:		volatile uint8_t usicr;
		/// <summary>
		///		USI Status Register
		///		<para>Bits: [7: USISIF (r/w)][6: USIOIF (r/w)][5: USIPF (r/w)][4: USIDC (r)][3-0: USICNT3-0 (r/w)]</para>
		/// </summary>
		/// <param name="USISIF:">Start Condition Interrupt Flag</param>
		/// <param name="USIOIF:">Counter Overflow Interrupt Flag</param>
		/// <param name="USIPF:">Stop Condition Flag</param>
		/// <param name="USIDC:">Data Output Collision</param>
		/// <param name="USICNT3-0:">Counter Value</param>
		public:		volatile uint8_t usisr;
		/// <summary>
		///		USI Data Register
		///		<para>Bits: [7-0: MSB - LSB (r/w)]</para>
		/// </summary>
		public:		volatile uint8_t usidr;
		/// <summary>
		///		USI Data Buffer
		///		<para>Bits: [7-0: MSB - LSB (r/w)]</para>
		/// </summary>
		public:		volatile uint8_t usibr;
	} USI_t;

	/// Universal Serial Interface
	USI_t* const usi = (USI_t*)0x2D;
	#pragma endregion

	#pragma region External Interrupts
	_BLOCK{
		/// <summary>
		///		Pin Change Mask Register 0
		///		<para>Bits: [7-0: PCINT7-0 (r/w)]</para>
		/// </summary>
		/// <param name="PCINT7-0:">Pin Change Enable Mask</param>
		public:		volatile uint8_t pcmsk0;
		private:	volatile uint8_t reserved_0[13];
		/// <summary>
		///		Pin Change Mask Register 1
		///		<para>Bits: [7-4: - ][3-0: PCINT11-8 (r/w)]</para>
		/// </summary>
		/// <param name="PCINT7-0:">Pin Change Enable Mask</param>
		public:		volatile uint8_t pcmsk1;
		private:	volatile uint8_t reserved_1[25];
		/// <summary>
		///		General Interrupt Flag Register
		///		<para>Bits: [7: - ][6: INTF0 (r/w)][5: PCIF1 (r/w)][4: PCIF0 (r/w)][3-0: - ]</para>
		/// </summary>
		/// <param name="INTF0:">External Interrupt Flag 0</param>
		/// <param name="PCIF1:">Pin Change Interrupt Flag 1</param>
		/// <param name="PCIF0:">Pin Change Interrupt Flag 0</param>
		public:		volatile uint8_t gifr;
		/// <summary>
		///		General Interrupt Mask Register
		///		<para>Bits: [7: - ][6: INT0 (r/w)][5: PCIE1 (r/w)][4: PCIE0 (r/w)][3-0: - ]</para>
		/// </summary>
		/// <param name="INT0:">External Interrupt Request 0 Enable</param>
		/// <param name="PCIE1:">Pin Change Interrupt Enable 1</param>
		/// <param name="PCIE0:">Pin Change Interrupt Enable 0</param>
		public:		volatile uint8_t gimsk;
		} EXTIR_t;

	/// External Interrupts
	EXTIR_t* const extir = (EXTIR_t*)0x32;
	#pragma endregion

	#pragma region General Purpose I/O Register
	_BLOCK{
		/// <summary>
		///		General Purpose I/O Register 0
		///		<para>Bits: [7-0: MSB - LSB (r/w)]</para>
		/// </summary>
		public:		volatile uint8_t gpr0;
		/// <summary>
		///		General Purpose I/O Register 1
		///		<para>Bits: [7-0: MSB - LSB (r/w)]</para>
		/// </summary>
		public:		volatile uint8_t gpr1;
		/// <summary>
		///		General Purpose I/O Register 2
		///		<para>Bits: [7-0: MSB - LSB (r/w)]</para>
		/// </summary>
		public:		volatile uint8_t gpr2;
	} GPIOR_t;

	/// General Purpose I/O Register
	GPIOR_t* const gpr = (GPIOR_t*)0x33;
	#pragma endregion

	#pragma region I/O Ports
	_BLOCK{
		/// <summary>
		///		Port Input Pins Address
		///		<para>Bits: [7-0: PIN7-0 (r/w)]</para>
		/// </summary>
		public:		volatile uint8_t pin;
		/// <summary>
		///		Data Direction Register
		///		<para>Bits: [7-0: DDR7-0 (r/w)]</para>
		/// </summary>
		public:		volatile uint8_t ddr;
		/// <summary>
		///		Port Data Register
		///		<para>Bits: [7-0: PORT7-0 (r/w)]</para>
		/// </summary>
		public:		volatile uint8_t port;
	} PORT_t;

	/// <summary>
	///		Port B
	/// </summary>
	PORT_t* const port_b = (PORT_t*)0x36;

	/// <summary>
	///		Port A
	/// </summary>
	PORT_t* const port_a = (PORT_t*)0x39;
	#pragma endregion

	#pragma region EEPROM
	_BLOCK{
		/// <summary>
		///		EEPROM Control Register
		///		<para>Bits: [7-6: - ][5-4: EEPM1-0 (r/w)][3: EERIE (r/w)][2: EEMPE (r/w)][1: EEPE (r/w)][0: EERE (r/w)]</para>
		/// </summary>
		/// <param name="EEPM1-0:">EEPROM Mode Bits</param>
		/// <param name="EERIE:"> EEPROM Ready Interrupt Enable</param>
		/// <param name="EEMPE:">EEPROM Master Program Enable</param>
		/// <param name="EEPE:">EEPROM Program Enable</param>
		/// <param name="EERE:">EEPROM Read Enable</param>
		public:		volatile uint8_t eecr;
		/// <summary>
		///		EEPROM Data Register
		///		<para>Bits: [7-0: MSB - LSB (r/w)]</para>		
		/// </summary>
		public:		volatile uint8_t eedr;
		/// <summary>
		///		EEPROM Address Register
		///		<para>Bits: [15-9: - ][8-0: MSB - LSB (r/w)]</para>		
		/// </summary>
		public:		volatile uint16_t eear;
	} EEPROM_t;

	/// <summary>
	///		EEPROM Register
	/// </summary>
	EEPROM_t* const eeprom = (EEPROM_t*)0x3C;
	#pragma endregion
}