; MiniVM OS - interactive BIOS command prompt
; Build locally: nasm -f bin os\boot.asm -o os\minivm.img

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

    mov si, banner
    call print

prompt:
    mov si, prompt_text
    call print
    mov di, buffer
    xor cx, cx

read_key:
    xor ah, ah
    int 0x16
    cmp al, 13
    je submit
    cmp al, 8
    je backspace
    cmp al, 32
    jb read_key
    cmp cx, 31
    jae read_key
    stosb
    inc cx
    mov ah, 0x0E
    int 0x10
    jmp read_key

backspace:
    test cx, cx
    jz read_key
    dec cx
    dec di
    mov al, 8
    mov ah, 0x0E
    int 0x10
    mov al, ' '
    int 0x10
    mov al, 8
    int 0x10
    jmp read_key

submit:
    xor al, al
    stosb
    mov si, newline
    call print
    test cx, cx
    jz prompt

    mov si, buffer
    mov di, cmd_help
    call strcmp
    jnc show_help

    mov si, buffer
    mov di, cmd_clear
    call strcmp
    jnc clear_screen

    mov si, buffer
    mov di, cmd_about
    call strcmp
    jnc show_about

    mov si, buffer
    mov di, cmd_reboot
    call strcmp
    jnc reboot

    mov si, unknown_text
    call print
    jmp prompt

show_help:
    mov si, help_text
    call print
    jmp prompt

show_about:
    mov si, about_text
    call print
    jmp prompt

clear_screen:
    mov ax, 0x0600
    mov bh, 0x07
    xor cx, cx
    mov dx, 0x184F
    int 0x10
    mov ah, 0x02
    xor bh, bh
    xor dx, dx
    int 0x10
    jmp prompt

reboot:
    int 0x19

; Compare zero-terminated strings at DS:SI and DS:DI.
; Carry clear means equal.
strcmp:
.compare:
    lodsb
    cmp al, [di]
    jne .different
    inc di
    test al, al
    jnz .compare
    clc
    ret
.different:
    stc
    ret

print:
.next:
    lodsb
    test al, al
    jz .done
    mov ah, 0x0E
    int 0x10
    jmp .next
.done:
    ret

banner db 13,10,'MiniVM OS 1.0',13,10,'Type help for commands.',13,10,0
prompt_text db 'MiniVM> ',0
newline db 13,10,0
cmd_help db 'help',0
cmd_clear db 'clear',0
cmd_about db 'about',0
cmd_reboot db 'reboot',0
help_text db 'Commands: help, clear, about, reboot',13,10,0
about_text db 'MiniVM OS 1.0 - tiny x86 BIOS system.',13,10,0
unknown_text db 'Unknown command. Type help.',13,10,0
buffer times 32 db 0

times 510-($-$$) db 0
dw 0xAA55
