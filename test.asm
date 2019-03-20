// comment

.data
    var1: 5 7 8 9
    var2: 987

.code
    // li rr, aa
    li %r1, 56
    li %r2, 72
    li %r5, var2

    // add rr, rr, rr
    add %r3, %r1, %r2

    // sub rr, rr, rr
    sub %r4, %r2, %r1

    // jmp iiiiii
    jmp 1008



