/*
 * read_string.h
 *
 *  Created on: Dec 10, 2022
 *      Author: MINH THU
 */

#ifndef INC_READ_STRING_H_
#define INC_READ_STRING_H_

#include "main.h"
#include "timer.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INIT 0

#define READING 1

#define STOP 2


#define RST1 5
#define RST2 6
#define OK1 7
#define OK2 8
#define MAX_CMD_SIZE 4

#define MAX_BUFFER_SIZE 30

extern uint8_t temp;
extern uint8_t buffer[MAX_BUFFER_SIZE];
extern uint8_t index_buffer;
extern uint8_t buffer_flag;

void cmd_parser_fsm();

void uart_comms_fsm();

#endif /* INC_READ_STRING_H_ */
