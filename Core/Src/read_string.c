/*
 * adc_reading.c
 *
 *  Created on: Dec 10, 2022
 *      Author: MINH THU
 */


#include "read_string.h"

extern ADC_HandleTypeDef hadc1;


extern UART_HandleTypeDef huart2;

// globally use
uint8_t temp;

uint8_t buffer[MAX_BUFFER_SIZE];

uint8_t index_buffer = 0;
uint8_t buffer_flag = 0;


// Locally use in automatic_fsm.c
int status = INIT;

uint8_t cmd_flag = INIT;

uint8_t cmd_data[MAX_CMD_SIZE];
uint8_t cmd_data_index = 0;

int ADC1_value = 0;
int ADC2_value = 0;
int cnt2 = 0;
int cnt1 = 0;

int isCmdEqualToRST1(uint8_t str[]){
	int flag = 0;
	if (str[0] == 'R' && str[1] == 'S' && str[2] == 'T' && str[3] == '1')
		flag = 1;
	else
		flag = 0;
	return flag;
}

int isCmdEqualToRST2(uint8_t str[]){
	int flag = 0;
	if (str[0] == 'R' && str[1] == 'S' && str[2] == 'T' && str[3] == '2')
		flag = 1;
	else
		flag = 0;
	return flag;
}

int isCmdEqualToOK1(uint8_t str[]){
	int flag = 0;
	if (str[0] == 'O' && str[1] == 'K' && str[2] == '1')
		flag = 1;
	else
		flag = 0;
	return flag;
}


int isCmdEqualToOK2(uint8_t str[]){
	int flag = 0;
	if (str[0] == 'O' && str[1] == 'K' && str[2] == '2')
		flag = 1;
	else
		flag = 0;
	return flag;
}

void cmd_parser_fsm(){
	//char str1[50];
	//HAL_UART_Transmit(&huart2, (void *)str1, sprintf(str1, "go"),500);
	switch(status){
		case INIT:
			if (temp == '!') status = READING;
			break;
		case READING:
			if (temp != '!' && temp != '#'){
				cmd_data[cmd_data_index] = temp;
				cmd_data_index++;
				break;
			}
			if (temp == '#')
			{
				status = STOP;
				cmd_data_index = 0;
			}

		case STOP:
			if (isCmdEqualToRST1(cmd_data)==1){
				cmd_flag = RST1;
				setTimer1(1);
			}
			if (isCmdEqualToRST2(cmd_data)==1){
				cmd_flag = RST2;
				setTimer2(1);
			}
			else
			{
				if (isCmdEqualToOK1(cmd_data)==1)
				{
					cmd_flag = OK1;
				}
				if (isCmdEqualToOK2(cmd_data)==1)
				{
					cmd_flag = OK2;
				}
			}
			status = INIT;
			break;
		default:
			break;
	}
}



void uart_comms_fsm(){
	char str1[100];
	char str2[100];
	char s[50];
	switch(cmd_flag){
		case RST1:
			if (timer1_flag == 1){

				HAL_ADC_Start(&hadc1);
				ADC_Select_CH0();
				HAL_ADC_PollForConversion(&hadc1, 1000);
				ADC1_value = HAL_ADC_GetValue(&hadc1);
				HAL_ADC_Stop(&hadc1);

				HAL_UART_Transmit(&huart2, (void *)str1, sprintf(str1, "!ADC0=%d#\r\n",ADC1_value), 500);
				setTimer1(200);
				cnt1++;
				if(cnt1 == 3) {
					HAL_UART_Transmit(&huart2, (void *)s, sprintf(s, "!END#"), 500);
					timer1_flag = 0;
					cmd_flag = INIT;
					//cnt = 0;
				}
			}
		    break;
		case RST2:
			if (timer2_flag == 1){
				HAL_ADC_Start(&hadc1);
				ADC_Select_CH1();
				HAL_ADC_PollForConversion(&hadc1, 1000);
				ADC2_value = HAL_ADC_GetValue(&hadc1);
				HAL_ADC_Stop(&hadc1);

				HAL_UART_Transmit(&huart2, (void *)str2, sprintf(str2, "!ADC1=%d#\r\n",ADC2_value), 500);
				setTimer2(200);
				cnt2++;
				if(cnt2 == 3) {
					HAL_UART_Transmit(&huart2, (void *)s, sprintf(s, "!END#"), 500);
					timer2_flag = 0;
					cmd_flag = INIT;
					//cnt = 0;
				}
			}
			break;
		case OK1:
			ADC1_value = -1;
			//ADC2_value = -1;
			cmd_flag = INIT;
			cnt1 = 0;
			//cnt2 = 0;
			break;

		case OK2:
			//ADC1_value = -1;
			ADC2_value = -1;
			cmd_flag = INIT;
			//cnt1 = 0;
			cnt2 = 0;
			break;
		default:
			break;
	}
}
