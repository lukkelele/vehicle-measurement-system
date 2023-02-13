#include "VMS.h"


VMSystem::VMSystem()
{
    stdio_init_all();
    uart_init(UART_ID, BAUD_RATE);
    uart_set_translate_crlf(UART_ID, false);


    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    // gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);

    bi_decl(bi_1pin_with_func(UART_TX_PIN, GPIO_FUNC_UART));
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
    if (m_Interrupt_UART == true)
    {
        int UART_IRQ = UART_ID == uart0 ? UART0_IRQ : UART1_IRQ;
        irq_set_exclusive_handler(UART_IRQ, UART_RX_HANDLER);
    }
}



int main()
{
    stdio_init_all();
    uart_init(UART_ID, BAUD_RATE);

    return 0;
}
