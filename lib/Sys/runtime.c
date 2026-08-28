#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <errno.h>
#include <setjmp.h>
#include <math.h>
#include <ctype.h>
#include <wchar.h>
#include <time.h>
#include <sys/stat.h>

#if defined(_WIN32)
#include <windows.h>
#include <direct.h>
#else
#include <unistd.h>
#include <pthread.h>
#endif

void *CMotive_New(size_t n) { return calloc(1, n ? n : 1); }
void CMotive_Delete(void *p) { free(p); }

/* ---- CMotive standard library runtime helpers ---- */
char *cmotive_strdup_local(const char *s) { size_t n; char *p; if (!s) s = ""; n = strlen(s) + 1u; p = (char*)malloc(n); if (p) memcpy(p, s, n); return p; }
int cmotive_sys_stdio_print(const char* s) { return fputs(s ? s : "", stdout); }
int cmotive_sys_stdio_println(const char* s) { int r = fputs(s ? s : "", stdout); fputc('\n', stdout); return r; }
int cmotive_sys_stdio_puts(const char* s) { return puts(s ? s : ""); }
int cmotive_sys_stdio_putchar(int ch) { return putchar(ch); }
int cmotive_sys_stdio_flush(void) { return fflush(stdout); }

void* cmotive_sys_file_open(const char *p, const char *m) { return (void*)fopen(p ? p : "", m ? m : "rb"); }
int cmotive_sys_file_close(void *h) { if (!h) return 0; return fclose((FILE*)h); }
int64_t cmotive_sys_file_read(void *h, void *b, uint64_t n) { if (!h || !b) return -1; return (int64_t)fread(b, 1u, (size_t)n, (FILE*)h); }
int64_t cmotive_sys_file_write(void *h, void *b, uint64_t n) { if (!h || !b) return -1; return (int64_t)fwrite(b, 1u, (size_t)n, (FILE*)h); }
int cmotive_sys_file_seek(void *h, int64_t off, int origin) { if (!h) return -1; return fseek((FILE*)h, (long)off, origin); }
int64_t cmotive_sys_file_tell(void *h) { if (!h) return -1; return (int64_t)ftell((FILE*)h); }
int cmotive_sys_file_eof(void *h) { if (!h) return 1; return feof((FILE*)h); }
int cmotive_sys_file_flush(void *h) { if (!h) return -1; return fflush((FILE*)h); }
int cmotive_sys_file_remove(const char *p) { return remove(p ? p : ""); }
int cmotive_sys_file_rename(const char *a, const char *b) { return rename(a ? a : "", b ? b : ""); }

int cmotive_sys_filesystem_exists(const char* p) { struct stat st; return (p && stat(p, &st) == 0) ? 1 : 0; }
int cmotive_sys_filesystem_is_file(const char* p) { struct stat st; if (!p || stat(p, &st) != 0) return 0; return (st.st_mode & S_IFMT) == S_IFREG; }
int cmotive_sys_filesystem_is_directory(const char* p) { struct stat st; if (!p || stat(p, &st) != 0) return 0; return (st.st_mode & S_IFMT) == S_IFDIR; }
int cmotive_sys_filesystem_mkdir(const char* p) {
  if (!p) return -1;
#if defined(_WIN32)
  return _mkdir(p);
#else
  return mkdir(p, 0777);
#endif
}
int cmotive_sys_filesystem_remove(const char* p) { return remove(p ? p : ""); }
int cmotive_sys_filesystem_rename(const char *a, const char *b) { return rename(a ? a : "", b ? b : ""); }
int64_t cmotive_sys_filesystem_size(const char* p) { struct stat st; if (!p || stat(p, &st) != 0) return -1; return (int64_t)st.st_size; }
char* cmotive_sys_filesystem_current_path(void) {
  char tmp[4096];
#if defined(_WIN32)
  if (!_getcwd(tmp, sizeof(tmp))) return cmotive_strdup_local("");
#else
  if (!getcwd(tmp, sizeof(tmp))) return cmotive_strdup_local("");
#endif
  return cmotive_strdup_local(tmp);
}

int __cmotive_log_level = 0;
int cmotive_sys_logging_set_level(int level) { __cmotive_log_level = level; return 0; }
int cmotive_sys_logging_emit(int level, const char *name, const char *m) { if (level < __cmotive_log_level) return 0; return fprintf((level >= 4) ? stderr : stdout, "[%s] %s\n", name, m ? m : ""); }
int cmotive_sys_logging_trace(const char* m) { return cmotive_sys_logging_emit(0, "TRACE", m); }
int cmotive_sys_logging_debug(const char* m) { return cmotive_sys_logging_emit(1, "DEBUG", m); }
int cmotive_sys_logging_info(const char* m) { return cmotive_sys_logging_emit(2, "INFO", m); }
int cmotive_sys_logging_warn(const char* m) { return cmotive_sys_logging_emit(3, "WARN", m); }
int cmotive_sys_logging_error(const char* m) { return cmotive_sys_logging_emit(4, "ERROR", m); }
int cmotive_sys_logging_fatal(const char* m) { return cmotive_sys_logging_emit(5, "FATAL", m); }

#define CMOTIVE_MATH1(name) double cmotive_sys_math_##name(double x) { return name(x); }
#define CMOTIVE_MATH2(name) double cmotive_sys_math_##name(double x, double y) { return name(x, y); }
CMOTIVE_MATH1(sin) CMOTIVE_MATH1(cos) CMOTIVE_MATH1(tan) CMOTIVE_MATH1(asin) CMOTIVE_MATH1(acos) CMOTIVE_MATH1(atan)
CMOTIVE_MATH2(atan2) CMOTIVE_MATH1(sinh) CMOTIVE_MATH1(cosh) CMOTIVE_MATH1(tanh) CMOTIVE_MATH1(exp) CMOTIVE_MATH1(exp2)
CMOTIVE_MATH1(expm1) CMOTIVE_MATH1(log) CMOTIVE_MATH1(log10) CMOTIVE_MATH1(log2) CMOTIVE_MATH1(log1p) CMOTIVE_MATH2(pow)
CMOTIVE_MATH1(sqrt) CMOTIVE_MATH1(cbrt) CMOTIVE_MATH2(hypot) CMOTIVE_MATH1(ceil) CMOTIVE_MATH1(floor) CMOTIVE_MATH1(trunc)
CMOTIVE_MATH1(round) CMOTIVE_MATH1(nearbyint) CMOTIVE_MATH1(rint) CMOTIVE_MATH1(fabs) CMOTIVE_MATH2(fmod) CMOTIVE_MATH2(remainder)
CMOTIVE_MATH2(copysign) CMOTIVE_MATH2(fmax) CMOTIVE_MATH2(fmin) CMOTIVE_MATH2(fdim) CMOTIVE_MATH1(erf) CMOTIVE_MATH1(erfc)
CMOTIVE_MATH1(tgamma) CMOTIVE_MATH1(lgamma)
int cmotive_sys_math_isfinite(double x) { return isfinite(x); }
int cmotive_sys_math_isnan(double x) { return isnan(x); }
int cmotive_sys_math_isinf(double x) { return isinf(x); }
int cmotive_sys_math_isnormal(double x) { return isnormal(x); }
int cmotive_sys_math_signbit(double x) { return signbit(x); }
int cmotive_sys_math_fpclassify(double x) { return fpclassify(x); }
int64_t cmotive_sys_math_abs_i64(int64_t x) { return x < 0 ? -x : x; }
uint64_t cmotive_sys_math_min_u64(uint64_t x, uint64_t y) { return x < y ? x : y; }
uint64_t cmotive_sys_math_max_u64(uint64_t x, uint64_t y) { return x > y ? x : y; }
double cmotive_sys_math_pi(void) { return 3.14159265358979323846264338327950288; }
double cmotive_sys_math_e(void) { return 2.71828182845904523536028747135266249; }

uint64_t cmotive_sys_string_strlen(const char *s) { return s ? (uint64_t)strlen(s) : 0u; }
char* cmotive_sys_string_strcpy(char *d, const char *s) { return strcpy(d, s ? s : ""); }
char* cmotive_sys_string_strncpy(char *d, const char *s, uint64_t n) { return strncpy(d, s ? s : "", (size_t)n); }
char* cmotive_sys_string_strcat(char *d, const char *s) { return strcat(d, s ? s : ""); }
char* cmotive_sys_string_strncat(char *d, const char *s, uint64_t n) { return strncat(d, s ? s : "", (size_t)n); }
int cmotive_sys_string_strcmp(const char *a, const char *b) { return strcmp(a ? a : "", b ? b : ""); }
int cmotive_sys_string_strncmp(const char *a, const char *b, uint64_t n) { return strncmp(a ? a : "", b ? b : "", (size_t)n); }
char* cmotive_sys_string_strchr(char *s, int c) { return s ? strchr(s, c) : NULL; }
char* cmotive_sys_string_strrchr(char *s, int c) { return s ? strrchr(s, c) : NULL; }
char* cmotive_sys_string_strstr(char *h, const char *n) { return h ? strstr(h, n ? n : "") : NULL; }
char* cmotive_sys_string_strdup(const char *s) { return cmotive_strdup_local(s); }
void* cmotive_sys_string_memset(void *d, int v, uint64_t n) { return memset(d, v, (size_t)n); }
void* cmotive_sys_string_memcpy(void *d, const void *s, uint64_t n) { return memcpy(d, s, (size_t)n); }
void* cmotive_sys_string_memmove(void *d, const void *s, uint64_t n) { return memmove(d, s, (size_t)n); }
int cmotive_sys_string_memcmp(const void *a, const void *b, uint64_t n) { return memcmp(a, b, (size_t)n); }
int cmotive_sys_string_toupper(int c) { return toupper((unsigned char)c); }
int cmotive_sys_string_tolower(int c) { return tolower((unsigned char)c); }
int cmotive_sys_string_isalpha(int c) { return isalpha((unsigned char)c); }
int cmotive_sys_string_isdigit(int c) { return isdigit((unsigned char)c); }
int cmotive_sys_string_isspace(int c) { return isspace((unsigned char)c); }
int cmotive_sys_string_atoi(const char *s) { return atoi(s ? s : "0"); }
int64_t cmotive_sys_string_atoll(const char *s) { return (int64_t)atoll(s ? s : "0"); }
int64_t cmotive_sys_string_strtoll(const char *s, int base) { return (int64_t)strtoll(s ? s : "0", NULL, base); }
double cmotive_sys_string_strtod(const char *s) { return strtod(s ? s : "0", NULL); }
void cmotive_sys_string_free(void *p) { free(p); }
char* cmotive_sys_string_trim(const char *s) { const char *a; const char *b; char *r; size_t n; if (!s) return cmotive_strdup_local(""); a = s; while (*a && isspace((unsigned char)*a)) a++; b = a + strlen(a); while (b > a && isspace((unsigned char)b[-1])) b--; n = (size_t)(b - a); r = (char*)malloc(n + 1u); if (!r) return NULL; memcpy(r, a, n); r[n] = 0; return r; }
char* cmotive_sys_string_to_upper(const char *s) { char *r = cmotive_strdup_local(s); char *p = r; if (!r) return NULL; while (*p) { *p = (char)toupper((unsigned char)*p); p++; } return r; }
char* cmotive_sys_string_to_lower(const char *s) { char *r = cmotive_strdup_local(s); char *p = r; if (!r) return NULL; while (*p) { *p = (char)tolower((unsigned char)*p); p++; } return r; }

typedef struct CMotive_StrParseRow { char **cells; uint64_t count; uint64_t cap; } CMotive_StrParseRow;
typedef struct CMotive_StrParseTable { CMotive_StrParseRow *rows; uint64_t count; uint64_t cap; } CMotive_StrParseTable;
int cmotive_char_in_set(char c, const char *set) { if (!set) return 0; while (*set) { if (*set++ == c) return 1; } return 0; }
void cmotive_parse_add_cell(CMotive_StrParseTable *t, const char *start, size_t n) { CMotive_StrParseRow *r; char *cell; if (t->count == 0) { t->cap = 4; t->rows = (CMotive_StrParseRow*)calloc((size_t)t->cap, sizeof(CMotive_StrParseRow)); t->count = 1; } r = &t->rows[t->count - 1u]; if (r->count == r->cap) { r->cap = r->cap ? r->cap * 2u : 4u; r->cells = (char**)realloc(r->cells, (size_t)r->cap * sizeof(char*)); } cell = (char*)malloc(n + 1u); if (!cell) return; memcpy(cell, start, n); cell[n] = 0; r->cells[r->count++] = cell; }
void cmotive_parse_new_row(CMotive_StrParseTable *t) { if (t->count == t->cap) { t->cap = t->cap ? t->cap * 2u : 4u; t->rows = (CMotive_StrParseRow*)realloc(t->rows, (size_t)t->cap * sizeof(CMotive_StrParseRow)); } memset(&t->rows[t->count], 0, sizeof(CMotive_StrParseRow)); t->count++; }
void* cmotive_sys_string_str_parse(const char *input, const char *record_delims, const char *field_delims, char escape) { CMotive_StrParseTable *t = (CMotive_StrParseTable*)calloc(1, sizeof(CMotive_StrParseTable)); const char *p; char *buf = NULL; size_t blen = 0, bcap = 0; if (!t) return NULL; cmotive_parse_new_row(t); if (!input) return t; for (p = input; ; ++p) { char c = *p; int end = (c == 0); int rec = !end && cmotive_char_in_set(c, record_delims); int fld = !end && cmotive_char_in_set(c, field_delims); if (!end && escape && c == escape && p[1]) { c = *++p; } else if (end || rec || fld) { cmotive_parse_add_cell(t, buf ? buf : "", blen); blen = 0; if (rec && !end) cmotive_parse_new_row(t); if (end) break; continue; } if (blen + 1u >= bcap) { bcap = bcap ? bcap * 2u : 32u; buf = (char*)realloc(buf, bcap); } if (buf) buf[blen++] = c; } free(buf); return t; }
uint64_t cmotive_sys_string_str_parse_rows(void *table) { CMotive_StrParseTable *t = (CMotive_StrParseTable*)table; return t ? t->count : 0u; }
uint64_t cmotive_sys_string_str_parse_cols(void *table, uint64_t row) { CMotive_StrParseTable *t = (CMotive_StrParseTable*)table; return (t && row < t->count) ? t->rows[row].count : 0u; }
char* cmotive_sys_string_str_parse_at(void *table, uint64_t row, uint64_t col) { CMotive_StrParseTable *t = (CMotive_StrParseTable*)table; if (!t || row >= t->count || col >= t->rows[row].count) return NULL; return t->rows[row].cells[col]; }
void cmotive_sys_string_str_parse_free(void *table) { CMotive_StrParseTable *t = (CMotive_StrParseTable*)table; uint64_t r, c; if (!t) return; for (r = 0; r < t->count; ++r) { for (c = 0; c < t->rows[r].count; ++c) free(t->rows[r].cells[c]); free(t->rows[r].cells); } free(t->rows); free(t); }

uint64_t cmotive_sys_wide16_len(const uint16_t *s) { uint64_t n = 0; if (!s) return 0; while (s[n]) n++; return n; }
int cmotive_sys_wide16_cmp(const uint16_t *a, const uint16_t *b) { const uint16_t z[1] = {0}; if (!a) a = z; if (!b) b = z; while (*a && *a == *b) { a++; b++; } return (int)*a - (int)*b; }
uint16_t* cmotive_sys_wide16_cpy(uint16_t *d, const uint16_t *s) { uint16_t *r = d; if (!d) return NULL; if (!s) { *d = 0; return d; } while ((*d++ = *s++)) {} return r; }
uint16_t* cmotive_sys_wide16_ncpy(uint16_t *d, const uint16_t *s, uint64_t n) { uint64_t i; if (!d) return NULL; for (i=0; i<n; ++i) d[i] = (s && s[i]) ? s[i] : 0; return d; }
uint16_t* cmotive_sys_wide16_chr(uint16_t *s, uint16_t c) { if (!s) return NULL; while (*s) { if (*s == c) return s; s++; } return c == 0 ? s : NULL; }
uint64_t cmotive_sys_wide32_len(const uint32_t *s) { uint64_t n = 0; if (!s) return 0; while (s[n]) n++; return n; }
int cmotive_sys_wide32_cmp(const uint32_t *a, const uint32_t *b) { const uint32_t z[1] = {0}; if (!a) a = z; if (!b) b = z; while (*a && *a == *b) { a++; b++; } return (*a > *b) - (*a < *b); }
uint32_t* cmotive_sys_wide32_cpy(uint32_t *d, const uint32_t *s) { uint32_t *r = d; if (!d) return NULL; if (!s) { *d = 0; return d; } while ((*d++ = *s++)) {} return r; }
uint32_t* cmotive_sys_wide32_ncpy(uint32_t *d, const uint32_t *s, uint64_t n) { uint64_t i; if (!d) return NULL; for (i=0; i<n; ++i) d[i] = (s && s[i]) ? s[i] : 0; return d; }
uint32_t* cmotive_sys_wide32_chr(uint32_t *s, uint32_t c) { if (!s) return NULL; while (*s) { if (*s == c) return s; s++; } return c == 0 ? s : NULL; }

#if defined(_WIN32)
typedef CRITICAL_SECTION CMotive_Mutex;
void* cmotive_sys_locks_mutex_create(void) { CMotive_Mutex *m = (CMotive_Mutex*)malloc(sizeof(CMotive_Mutex)); if (m) InitializeCriticalSection(m); return m; }
void* cmotive_sys_locks_recursive_mutex_create(void) { return cmotive_sys_locks_mutex_create(); }
int cmotive_sys_locks_mutex_lock(void *h) { if (!h) return -1; EnterCriticalSection((CMotive_Mutex*)h); return 0; }
int cmotive_sys_locks_mutex_trylock(void *h) { if (!h) return -1; return TryEnterCriticalSection((CMotive_Mutex*)h) ? 0 : 1; }
int cmotive_sys_locks_mutex_unlock(void *h) { if (!h) return -1; LeaveCriticalSection((CMotive_Mutex*)h); return 0; }
void cmotive_sys_locks_mutex_destroy(void *h) { if (h) { DeleteCriticalSection((CMotive_Mutex*)h); free(h); } }
#else
typedef pthread_mutex_t CMotive_Mutex;
void* cmotive_sys_locks_mutex_create(void) { CMotive_Mutex *m = (CMotive_Mutex*)malloc(sizeof(CMotive_Mutex)); if (m) pthread_mutex_init(m, NULL); return m; }
void* cmotive_sys_locks_recursive_mutex_create(void) { CMotive_Mutex *m = (CMotive_Mutex*)malloc(sizeof(CMotive_Mutex)); if (m) { pthread_mutexattr_t a; pthread_mutexattr_init(&a); pthread_mutexattr_settype(&a, PTHREAD_MUTEX_RECURSIVE); pthread_mutex_init(m, &a); pthread_mutexattr_destroy(&a); } return m; }
int cmotive_sys_locks_mutex_lock(void *h) { return h ? pthread_mutex_lock((CMotive_Mutex*)h) : -1; }
int cmotive_sys_locks_mutex_trylock(void *h) { return h ? pthread_mutex_trylock((CMotive_Mutex*)h) : -1; }
int cmotive_sys_locks_mutex_unlock(void *h) { return h ? pthread_mutex_unlock((CMotive_Mutex*)h) : -1; }
void cmotive_sys_locks_mutex_destroy(void *h) { if (h) { pthread_mutex_destroy((CMotive_Mutex*)h); free(h); } }
#endif
void* cmotive_sys_locks_spin_create(void) { return cmotive_sys_locks_mutex_create(); }
int cmotive_sys_locks_spin_lock(void *h) { return cmotive_sys_locks_mutex_lock(h); }
int cmotive_sys_locks_spin_trylock(void *h) { return cmotive_sys_locks_mutex_trylock(h); }
int cmotive_sys_locks_spin_unlock(void *h) { return cmotive_sys_locks_mutex_unlock(h); }
void cmotive_sys_locks_spin_destroy(void *h) { cmotive_sys_locks_mutex_destroy(h); }
#if defined(_WIN32)
void* cmotive_sys_locks_rwlock_create(void) { return cmotive_sys_locks_mutex_create(); }
int cmotive_sys_locks_rwlock_rdlock(void *h) { return cmotive_sys_locks_mutex_lock(h); }
int cmotive_sys_locks_rwlock_wrlock(void *h) { return cmotive_sys_locks_mutex_lock(h); }
int cmotive_sys_locks_rwlock_unlock(void *h) { return cmotive_sys_locks_mutex_unlock(h); }
void cmotive_sys_locks_rwlock_destroy(void *h) { cmotive_sys_locks_mutex_destroy(h); }
#else
void* cmotive_sys_locks_rwlock_create(void) { pthread_rwlock_t *r = (pthread_rwlock_t*)malloc(sizeof(pthread_rwlock_t)); if (r) pthread_rwlock_init(r, NULL); return r; }
int cmotive_sys_locks_rwlock_rdlock(void *h) { return h ? pthread_rwlock_rdlock((pthread_rwlock_t*)h) : -1; }
int cmotive_sys_locks_rwlock_wrlock(void *h) { return h ? pthread_rwlock_wrlock((pthread_rwlock_t*)h) : -1; }
int cmotive_sys_locks_rwlock_unlock(void *h) { return h ? pthread_rwlock_unlock((pthread_rwlock_t*)h) : -1; }
void cmotive_sys_locks_rwlock_destroy(void *h) { if (h) { pthread_rwlock_destroy((pthread_rwlock_t*)h); free(h); } }
#endif

void* cmotive_sys_thread_start(void *entry, void *userdata) { (void)entry; (void)userdata; return NULL; }
int cmotive_sys_thread_join(void *h) { (void)h; return 0; }
int cmotive_sys_thread_detach(void *h) { (void)h; return 0; }
void* cmotive_sys_thread_current(void) { return NULL; }
void cmotive_sys_thread_sleep_ms(uint32_t ms) {
#if defined(_WIN32)
  Sleep(ms);
#else
  usleep((useconds_t)ms * 1000u);
#endif
}
int cmotive_sys_thread_yield(void) { return 0; }

int cmotive_sys_net_socket_tcp(void) { return -1; }
int cmotive_sys_net_socket_udp(void) { return -1; }
int cmotive_sys_net_socket_raw(void) { return -1; }
int cmotive_sys_net_socket_close(int fd) { (void)fd; return 0; }

int __cmotive_exception_last_code = 0;
void cmotive_sys_exception_set_code(int code) { __cmotive_exception_last_code = code; }
int cmotive_sys_exception_last_code(void) { return __cmotive_exception_last_code; }
/* additional math/string/locks helpers */
double cmotive_sys_math_fma(double x, double y, double z) { return fma(x, y, z); }
double cmotive_sys_math_ldexp(double x, int e) { return ldexp(x, e); }
double cmotive_sys_math_scalbn(double x, int e) { return scalbn(x, e); }
int cmotive_sys_math_ilogb(double x) { return ilogb(x); }
double cmotive_sys_math_logb(double x) { return logb(x); }
double cmotive_sys_math_nextafter(double x, double y) { return nextafter(x, y); }
double cmotive_sys_math_modf(double x, double *iptr) { return modf(x, iptr); }
double cmotive_sys_math_frexp_value(double x, int *eptr) { return frexp(x, eptr); }
float cmotive_sys_math_sinf(float x) { return sinf(x); }
float cmotive_sys_math_cosf(float x) { return cosf(x); }
float cmotive_sys_math_tanf(float x) { return tanf(x); }
float cmotive_sys_math_sqrtf(float x) { return sqrtf(x); }
float cmotive_sys_math_powf(float x, float y) { return powf(x, y); }
long double cmotive_sys_math_sinl(long double x) { return sinl(x); }
long double cmotive_sys_math_cosl(long double x) { return cosl(x); }
long double cmotive_sys_math_tanl(long double x) { return tanl(x); }
long double cmotive_sys_math_sqrtl(long double x) { return sqrtl(x); }
long double cmotive_sys_math_powl(long double x, long double y) { return powl(x, y); }
uint64_t cmotive_sys_string_strspn(const char *s, const char *accept) { return s ? (uint64_t)strspn(s, accept ? accept : "") : 0u; }
uint64_t cmotive_sys_string_strcspn(const char *s, const char *reject) { return s ? (uint64_t)strcspn(s, reject ? reject : "") : 0u; }
char* cmotive_sys_string_strpbrk(char *s, const char *accept) { return s ? strpbrk(s, accept ? accept : "") : NULL; }
char* cmotive_sys_string_strerror(int errnum) { return strerror(errnum); }
int cmotive_ascii_casecmp(const char *a, const char *b, uint64_t n, int limited) { uint64_t i = 0; if (!a) a = ""; if (!b) b = ""; while ((!limited || i < n) && (a[i] || b[i])) { int ca = tolower((unsigned char)a[i]); int cb = tolower((unsigned char)b[i]); if (ca != cb) return ca - cb; i++; } return 0; }
int cmotive_sys_string_strcasecmp(const char *a, const char *b) { return cmotive_ascii_casecmp(a, b, 0, 0); }
int cmotive_sys_string_strncasecmp(const char *a, const char *b, uint64_t n) { return cmotive_ascii_casecmp(a, b, n, 1); }
uint16_t* cmotive_sys_wide16_cat(uint16_t *d, const uint16_t *s) { uint16_t *r = d; if (!d) return NULL; while (*d) d++; if (!s) { *d = 0; return r; } while ((*d++ = *s++)) {} return r; }
int cmotive_sys_wide16_ncmp(const uint16_t *a, const uint16_t *b, uint64_t n) { uint64_t i; const uint16_t z[1] = {0}; if (!a) a = z; if (!b) b = z; for (i=0; i<n; ++i) { if (a[i] != b[i] || !a[i] || !b[i]) return (int)a[i] - (int)b[i]; } return 0; }
uint16_t* cmotive_sys_wide16_rchr(uint16_t *s, uint16_t c) { uint16_t *last = NULL; if (!s) return NULL; do { if (*s == c) last = s; } while (*s++); return last; }
uint32_t* cmotive_sys_wide32_cat(uint32_t *d, const uint32_t *s) { uint32_t *r = d; if (!d) return NULL; while (*d) d++; if (!s) { *d = 0; return r; } while ((*d++ = *s++)) {} return r; }
int cmotive_sys_wide32_ncmp(const uint32_t *a, const uint32_t *b, uint64_t n) { uint64_t i; const uint32_t z[1] = {0}; if (!a) a = z; if (!b) b = z; for (i=0; i<n; ++i) { if (a[i] != b[i] || !a[i] || !b[i]) return (a[i] > b[i]) - (a[i] < b[i]); } return 0; }
uint32_t* cmotive_sys_wide32_rchr(uint32_t *s, uint32_t c) { uint32_t *last = NULL; if (!s) return NULL; do { if (*s == c) last = s; } while (*s++); return last; }
#if defined(_WIN32)
void* cmotive_sys_locks_cond_create(void) { return malloc(1); }
int cmotive_sys_locks_cond_wait(void *c, void *m) { (void)c; (void)m; return 0; }
int cmotive_sys_locks_cond_signal(void *c) { (void)c; return 0; }
int cmotive_sys_locks_cond_broadcast(void *c) { (void)c; return 0; }
void cmotive_sys_locks_cond_destroy(void *c) { free(c); }
#else
void* cmotive_sys_locks_cond_create(void) { pthread_cond_t *c = (pthread_cond_t*)malloc(sizeof(pthread_cond_t)); if (c) pthread_cond_init(c, NULL); return c; }
int cmotive_sys_locks_cond_wait(void *c, void *m) { return (c && m) ? pthread_cond_wait((pthread_cond_t*)c, (pthread_mutex_t*)m) : -1; }
int cmotive_sys_locks_cond_signal(void *c) { return c ? pthread_cond_signal((pthread_cond_t*)c) : -1; }
int cmotive_sys_locks_cond_broadcast(void *c) { return c ? pthread_cond_broadcast((pthread_cond_t*)c) : -1; }
void cmotive_sys_locks_cond_destroy(void *c) { if (c) { pthread_cond_destroy((pthread_cond_t*)c); free(c); } }
#endif
typedef struct CMotive_Semaphore { CMotive_Mutex mutex; int count; } CMotive_Semaphore;
void* cmotive_sys_locks_semaphore_create(int initial) { CMotive_Semaphore *s = (CMotive_Semaphore*)malloc(sizeof(CMotive_Semaphore)); if (!s) return NULL; s->count = initial; return s; }
int cmotive_sys_locks_semaphore_post(void *h) { CMotive_Semaphore *s = (CMotive_Semaphore*)h; if (!s) return -1; s->count++; return 0; }
int cmotive_sys_locks_semaphore_wait(void *h) { CMotive_Semaphore *s = (CMotive_Semaphore*)h; if (!s) return -1; if (s->count > 0) s->count--; return 0; }
int cmotive_sys_locks_semaphore_trywait(void *h) { CMotive_Semaphore *s = (CMotive_Semaphore*)h; if (!s) return -1; if (s->count <= 0) return 1; s->count--; return 0; }
void cmotive_sys_locks_semaphore_destroy(void *h) { free(h); }

/* ---- end CMotive standard library runtime helpers ---- */
