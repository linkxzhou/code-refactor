#include "ringbuf.h"
#include <stdlib.h>

struct ringbuf {
    uint8_t *buf;
    uint32_t mask;
    uint32_t head;   /* free-running write counter, wraps at 2^32 */
    uint32_t tail;   /* free-running read counter */
};

static uint32_t next_pow2(uint32_t v) {
    v--; v |= v >> 1; v |= v >> 2; v |= v >> 4; v |= v >> 8; v |= v >> 16; return v + 1;
}

ringbuf *rb_new(uint32_t capacity) {
    if (capacity == 0) return NULL;
    ringbuf *rb = malloc(sizeof *rb);
    if (!rb) return NULL;
    uint32_t cap = next_pow2(capacity);
    rb->buf = malloc(cap);
    if (!rb->buf) { free(rb); return NULL; }
    rb->mask = cap - 1;
    rb->head = rb->tail = 0;
    return rb;
}

void rb_free(ringbuf *rb) {
    if (!rb) return;
    free(rb->buf);
    free(rb);
}

uint32_t rb_len(const ringbuf *rb) { return rb->head - rb->tail; }
uint32_t rb_capacity(const ringbuf *rb) { return rb->mask + 1; }

size_t rb_write(ringbuf *rb, const uint8_t *data, size_t len) {
    size_t n = 0;
    while (n < len && rb_len(rb) < rb_capacity(rb)) {
        rb->buf[rb->head & rb->mask] = data[n++];
        rb->head++;
    }
    return n;
}

size_t rb_read(ringbuf *rb, uint8_t *out, size_t len) {
    size_t n = 0;
    while (n < len && rb->tail != rb->head) {
        out[n++] = rb->buf[rb->tail & rb->mask];
        rb->tail++;
    }
    return n;
}
