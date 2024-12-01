def function_add():
    return 0x20, False

def function_addi():
    return 0x20, True

def function_and():
    return 0x24, False

def function_andi():
    return 0x24, True

def function_beq():
    return 0x10, True

def function_bneq():
    return 0x14, True

def function_div():
    return 0x1a, False

def function_divu():
    return 0x1b, False

def function_li():
    return 0x90, True

def function_lui():
    return 0x94, True

def function_lw():
    return 0x8c, True

def function_mul():
    return 0x18, False

def function_mulu():
    return 0x19, False

def function_nop():
    return 0x0, False

def function_nor():
    return 0x25, False

def function_or():
    return 0x27, False

def function_ori():
    return 0x34, True

def function_sllv():
    return 0x1, False

def function_srlv():
    return 0x2, False

def function_sub():
    return 0x22, False

def function_subi():
    return 0x24, True

def function_sw():
    return 0xac, True

def function_xor():
    return 0x26, False

def function_xori():
    return 0x38, True