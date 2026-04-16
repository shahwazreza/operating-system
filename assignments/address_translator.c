#include <stdio.h>
#include <stdint.h>

#define PAGE_SIZE 4096
#define OFFSET_MASK 0x0FFF
#define SHIFT_AMOUNT 12

// Mock Page Table
int page_table[16] = {5, 2, 8, -1, 12, 1, 9, 3, -1, 7, 4, 6, 10, 15, 11, 14};

uint32_t translate_address(uint16_t virtual_address) {
    // Extract page number
    uint16_t page_number = virtual_address >> SHIFT_AMOUNT;

    // Extract offset
    uint16_t offset = virtual_address & OFFSET_MASK;

    // Lookup frame
    int frame = page_table[page_number];

    // Page fault check
    if (frame == -1) {
        printf("Page Fault!\n");
        return 0;
    }

    // Construct physical address
    uint32_t physical_address = (frame << SHIFT_AMOUNT) | offset;

    return physical_address;
}

int main() {
    uint16_t va1 = 0x1A2B; // Page 1
    uint16_t va2 = 0x3004; // Page 3 (fault)

    printf("VA: 0x%04X -> PA: 0x%05X\n", va1, translate_address(va1));
    printf("VA: 0x%04X -> PA: 0x%05X\n", va2, translate_address(va2));

    return 0;
}