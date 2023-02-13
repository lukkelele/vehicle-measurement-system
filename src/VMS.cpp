#include "VMS.h"


VMSystem::VMSystem()
{
    stdio_init_all();
    initUART();
}

bool VMSystem::transmitByte(uint8_t &byte)
{
    uart_putc_raw(UART_ID, byte);
    return 1;
}

bool VMSystem::transmitData(const uint8_t* data, unsigned int n)
{
    for (unsigned int i = 0; i < n; i++)
    {
        uart_putc_raw(UART_ID, *data);
    }
    return 1;
}

void VMSystem::initUART()
{
    m_BaudRate = uart_init(UART_ID, BAUD_RATE);
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);
    uart_set_format(UART_ID, PAYLOAD_FORMAT, STOP_BITS, PARITY);
    uart_set_fifo_enabled(UART_ID, false);
    // if interrupts are enabled
    #ifdef UART_IRQ_ENABLED
        int UART_IRQ = UART_ID == uart0 ? UART0_IRQ : UART1_IRQ;
        irq_set_exclusive_handler(UART_IRQ, UART_RX_HANDLER);
        irq_set_enabled(UART_IRQ, true);
        // Enable UART to send interrupts
        uart_set_irq_enables(UART_ID, true, false);
    #endif
}

void VMSystem::initPin(uint pin, uint direction, uint value)
{
    gpio_init(pin);
    gpio_set_dir(pin, direction);
    gpio_put(pin, value);
}



int main()
{
    #ifdef PICO_DEFAULT_LED_PIN
    const uint PICO_LED = PICO_DEFAULT_LED_PIN;
    gpio_init(PICO_LED);
    gpio_set_dir(PICO_LED, OUT);
    VMSystem Vms;
    Vms.initUART();

    while (1)
    {
        sleep_ms(1200);
        Vms.setPinValue(PICO_LED, LOW);
        printf("HEARTBEAT");
        sleep_ms(1200);
        Vms.setPinValue(PICO_LED, HIGH);
    }
    return 0;
    #endif
}
