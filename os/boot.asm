; MiniVM OS - tiny BIOS boot sector
; Build locally with NASM: nasm -f bin boot.asm -o minivm.img

bits 16
org 0x7C00

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00
    sti

    mov si, message
.print:
    lodsb
    test al, al
    jz .halt
    mov ah, 0x0E
    int 0x10
    jmp .print

.halt:
    cli
.wait:
    hlt
    jmp .wait

message db 'Welcome to MiniVM OS!', 0

times 510-($-$$) db 0
dw 0xAA55
