/*
 * Copyright 2019 NXP
 * All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

/***********************************************************************************************************************
 * This file was generated by the MCUXpresso Config Tools. Any manual edits made to this file
 * will be overwritten if the respective MCUXpresso Config Tools is used to update this file.
 **********************************************************************************************************************/

#ifndef _CLOCK_CONFIG_H_
#define _CLOCK_CONFIG_H_

#include "fsl_common.h"

/*******************************************************************************
 * Definitions
 ******************************************************************************/

/*******************************************************************************
 ************************ BOARD_InitBootClocks function ************************
 ******************************************************************************/

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus*/

/*!
 * @brief This function executes default configuration of clocks.
 *
 */
void BOARD_InitBootClocks(void);

#if defined(__cplusplus)
}
#endif /* __cplusplus*/

/*******************************************************************************
 ********************** Configuration BOARD_BootClockRUN ***********************
 ******************************************************************************/
/*******************************************************************************
 * Definitions for BOARD_BootClockRUN configuration
 ******************************************************************************/
#define BOARD_BOOTCLOCKRUN_CORE_CLOCK              48000000U  /*!< Core clock frequency: 48000000Hz */

/*! @brief SCG set for BOARD_BootClockRUN configuration.
 */
extern const scg_sys_clk_config_t g_sysClkConfig_BOARD_BootClockRUN;
/*! @brief SIRC set for BOARD_BootClockRUN configuration.
 */
extern const scg_sirc_config_t g_scgSircConfig_BOARD_BootClockRUN;
/*! @brief FIRC set for BOARD_BootClockRUN configuration.
 */
extern const scg_firc_config_t g_scgFircConfigBOARD_BootClockRUN;
/*! @brief Low Power FLL set for BOARD_BootClockRUN configuration.
 */
extern const scg_lpfll_config_t g_scgLpFllConfigBOARD_BootClockRUN;

/*******************************************************************************
 * API for BOARD_BootClockRUN configuration
 ******************************************************************************/
#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus*/

/*!
 * @brief This function executes configuration of clocks.
 *
 */
void BOARD_BootClockRUN(void);

#if defined(__cplusplus)
}
#endif /* __cplusplus*/

#endif /* _CLOCK_CONFIG_H_ */

