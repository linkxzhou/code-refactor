#ifndef RINGBUF_H
#define RINGBUF_H
#include <stddef.h>
#include <stdint.h>

typedef struct ringbuf ringbuf;   /* opaque */

/* capacity is rounded up to a power of two; returns NULL on allocation failure or capacity == 0 */
ringbuf *rb_new(uint32_t capacity);
void rb_free(ringbuf *rb);                    /* NULL is a no-op */
/* returns number of bytes written (may be < len when full) */
size_t rb_write(ringbuf *rb, const uint8_t *data, size_t len);
/* returns number of bytes read (0 when empty) */
size_t rb_read(ringbuf *rb, uint8_t *out, size_t len);
uint32_t rb_len(const ringbuf *rb);
uint32_t rb_capacity(const ringbuf *rb);
#endif
