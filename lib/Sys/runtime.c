#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <sys/stat.h>

#ifdef _WIN32
#include <direct.h>
#define CMOTIVE_MKDIR(path) _mkdir(path)
#else
#include <unistd.h>
#define CMOTIVE_MKDIR(path) mkdir(path, 0777)
#endif

void cmotive_sys_stdio_print_int(int v) { printf("%d", v); }
void cmotive_sys_stdio_print_string(const char *v) { printf("%s", v ? v : ""); }
void cmotive_sys_stdio_println_string(const char *v) { printf("%s\n", v ? v : ""); }
int cmotive_sys_file_exists(const char *path) { FILE *f = fopen(path, "rb"); if (!f) return 0; fclose(f); return 1; }
int cmotive_sys_filesystem_mkdir(const char *path) { return CMOTIVE_MKDIR(path); }
int cmotive_sys_logging_info(const char *message) { return fprintf(stdout, "%s\n", message ? message : ""); }
int cmotive_sys_logging_error(const char *message) { return fprintf(stderr, "%s\n", message ? message : ""); }

/* Userspace thread and socket APIs are stable package surfaces in this archive;
 * the portable native runtime adapters are intentionally scaffolded here so the
 * compiler, parser, linker, and package manager can be verified independently.
 */
int cmotive_sys_thread_start(void *thread) { (void)thread; return 0; }
int cmotive_sys_thread_join(void *thread) { (void)thread; return 0; }
int cmotive_sys_net_socket_tcp(void) { return -1; }
int cmotive_sys_net_socket_udp(void) { return -1; }
int cmotive_sys_net_socket_raw(void) { return -1; }
