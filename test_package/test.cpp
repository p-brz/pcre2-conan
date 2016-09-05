#define PCRE2_CODE_UNIT_WIDTH 8

#include <stdio.h>
#include <string.h>
#include <pcre2.h>

int main(int argc, char **argv){
    pcre2_code *re;
    PCRE2_SPTR pattern = (PCRE2_SPTR)".*";

	int errornumber;
	size_t erroroffset;

    re = pcre2_compile(
            pattern, /* the pattern */
            PCRE2_ZERO_TERMINATED, /* indicates pattern is zero-terminated */
            0,       /* default options */
            &errornumber, /* for error number */
            &erroroffset, /* for error offset */
            NULL);   /* use default compile context */

    pcre2_code_free(re);
    return 0;
}
