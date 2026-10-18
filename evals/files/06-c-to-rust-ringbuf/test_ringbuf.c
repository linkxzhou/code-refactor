#include "ringbuf.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    assert(rb_new(0) == NULL);
    ringbuf *rb = rb_new(5);
    assert(rb_capacity(rb) == 8);
    uint8_t in[10] = {0,1,2,3,4,5,6,7,8,9}, out[10];
    assert(rb_write(rb, in, 10) == 8);
    assert(rb_len(rb) == 8);
    assert(rb_read(rb, out, 3) == 3 && out[0] == 0 && out[2] == 2);
    assert(rb_write(rb, in, 2) == 2);
    assert(rb_read(rb, out, 10) == 7 && out[6] == 1);
    assert(rb_read(rb, out, 1) == 0);
    rb_free(rb);
    rb_free(NULL);
    puts("ok");
    return 0;
}
