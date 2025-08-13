cmake_minimum_required(VERSION 3.12)
set(TOOLCHAIN_PATH "C:/Users/liyi/AppData/Local/Keil_v5/ARM/ARMCC/bin/armcc.exe")
set(CMAKE_C_COMPILER "${TOOLCHAIN_PATH}/armcc.exe")
set(CMAKE_ASM_COMPILER "${TOOLCHAIN_PATH}/armasm.exe")
set(CMAKE_C_LINK_EXECUTABLE "${TOOLCHAIN_PATH}/armlinke.exe")
project("FOC" C)
enable_language(ASM)
add_definitions(-DUSE_HAL_DRIVER -D__MICROLIB -D__FPU_PRESENT=1 -D__UVISION_VERSION=542 -DSTM32F405xx)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --c99 -c --cpu=Cortex-M4.fp.sp -g -O0 --apcs=interwork --split_sections")
set(CMAKE_ASM_FLAGS "${CMAKE_ASM_FLAGS} --cpu=Cortex-M4.fp.sp -g --apcs=interwork --pd=\"__MICROLIB SETA 1\" --pd=\"__UVISION_VERSION SETA 542\" --pd=\"STM32F405xx SETA 1\" --xref")
set(USER_LD_FLAGS "--cpu=Cortex-M4.fp.sp --library_type=microlib --strict --scatter \"${CMAKE_SOURCE_DIR}/MDK-ARM/FOC/FOC.sct\"")
include_directories(
    ${CMAKE_SOURCE_DIR}/Core/Inc
    ${CMAKE_SOURCE_DIR}/foc
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/portable/RVDS/ARM_CM4F
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Inc/Legacy
    ${CMAKE_SOURCE_DIR}/Drivers/CMSIS/DSP/Include
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Inc
    ${CMAKE_SOURCE_DIR}/Drivers/CMSIS/Device/ST/STM32F4xx/Include
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/include
    ${CMAKE_SOURCE_DIR}/Drivers/CMSIS/Include
    ${CMAKE_SOURCE_DIR}/Middlewares/ST/ARM/DSP/Inc
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS
)
set(Application_User_Core
    ${CMAKE_SOURCE_DIR}/Core/Src/main.c
    ${CMAKE_SOURCE_DIR}/Core/Src/gpio.c
    ${CMAKE_SOURCE_DIR}/Core/Src/freertos.c
    ${CMAKE_SOURCE_DIR}/Core/Src/adc.c
    ${CMAKE_SOURCE_DIR}/Core/Src/dma.c
    ${CMAKE_SOURCE_DIR}/Core/Src/spi.c
    ${CMAKE_SOURCE_DIR}/Core/Src/tim.c
    ${CMAKE_SOURCE_DIR}/Core/Src/usart.c
    ${CMAKE_SOURCE_DIR}/Core/Src/stm32f4xx_it.c
    ${CMAKE_SOURCE_DIR}/Core/Src/stm32f4xx_hal_msp.c
    ${CMAKE_SOURCE_DIR}/Core/Src/stm32f4xx_hal_timebase_tim.c
    ${CMAKE_SOURCE_DIR}/foc/arm_cos_f32.c
    ${CMAKE_SOURCE_DIR}/foc/arm_sin_f32.c
    ${CMAKE_SOURCE_DIR}/foc/drv8320.c
    ${CMAKE_SOURCE_DIR}/foc/foc.c
    ${CMAKE_SOURCE_DIR}/foc/low_level.c
    ${CMAKE_SOURCE_DIR}/Core/Src/com_task.c
    ${CMAKE_SOURCE_DIR}/Core/Src/config.c
    ${CMAKE_SOURCE_DIR}/Core/Src/io_ctrl_task.c
    ${CMAKE_SOURCE_DIR}/Core/Src/rudder_control.c
    ${CMAKE_SOURCE_DIR}/Core/Src/sandemarine_protocol.c
)
set(Drivers_STM32F4xx_HAL_Driver
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_tim.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_tim_ex.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_adc.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_adc_ex.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_ll_adc.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_rcc.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_rcc_ex.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_flash.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_flash_ex.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_flash_ramfunc.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_gpio.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_dma_ex.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_dma.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pwr.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pwr_ex.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_cortex.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_exti.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_spi.c
    ${CMAKE_SOURCE_DIR}/Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_uart.c
)
set(Drivers_CMSIS
    ${CMAKE_SOURCE_DIR}/Core/Src/system_stm32f4xx.c
)
set(Middlewares_FreeRTOS
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/croutine.c
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/event_groups.c
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/list.c
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/queue.c
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/stream_buffer.c
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/tasks.c
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/timers.c
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS/cmsis_os.c
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/portable/MemMang/heap_4.c
    ${CMAKE_SOURCE_DIR}/Middlewares/Third_Party/FreeRTOS/Source/portable/RVDS/ARM_CM4F/port.c
)
set(STARTUP
    ${CMAKE_SOURCE_DIR}/MDK-ARM/startup_stm32f405xx.s
)
link_libraries("${CMAKE_SOURCE_DIR}/Middlewares/ST/ARM/DSP/Lib/arm_cortexM4l_math.lib")
add_executable( FOC ${Application_User_Core} ${Drivers_STM32F4xx_HAL_Driver} ${Drivers_CMSIS} ${Middlewares_FreeRTOS} ${STARTUP})
set_target_properties(FOC PROPERTIES LINK_FLAGS "${USER_LD_FLAGS}")
set_target_properties(FOC PROPERTIES SUFFIX ".axf")
add_custom_command(TARGET FOC POST_BUILD
    COMMAND ${TOOLCHAIN_PATH}/fromelf.exe --bin --output FOC.bin FOC.axf
    COMMAND ${TOOLCHAIN_PATH}/fromelf.exe --i32 --output FOC.hex FOC.axf
    COMMENT "Generate bin and hex from axf"
)