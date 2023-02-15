#include "VMS.h"


int main()
{
    VMSystem Vms;

    Vms.initPin(GP15, OUT, HIGH);
    Vms.initPin(ONBOARD_LED, OUT, HIGH);

    while (1)
    {
        sleep_ms(1200);
        gpio_put(ONBOARD_LED, HIGH);
        Vms.setPinValue(GP15, LOW);

        sleep_ms(1200);
        gpio_put(ONBOARD_LED, LOW);
        Vms.setPinValue(GP15, HIGH);
    }

    return 0;
}
