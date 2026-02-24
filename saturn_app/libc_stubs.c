/*
 * Minimal libc stubs for Jo Engine + SGL toolchain (leading-underscore symbols).
 *
 * Why this exists:
 * - The /opt/sh-elf toolchain on this Pi is "bare" (no libc/newlib).
 * - SGL libs and Jo Engine expect basic C routines like memcpy/memset/sprintf.
 *
 * This file provides just enough to link and to support Jo Engine's sprintf-based
 * debug/printf macros with a small subset of format specifiers.
 */

#include <stdarg.h>
#include <stddef.h>

void *memcpy(void *dest, const void *src, size_t n)
{
	unsigned char *d = (unsigned char *)dest;
	const unsigned char *s = (const unsigned char *)src;

	while (n--)
		*d++ = *s++;
	return dest;
}

void *memset(void *s, int c, size_t n)
{
	unsigned char *p = (unsigned char *)s;
	const unsigned char v = (unsigned char)c;

	while (n--)
		*p++ = v;
	return s;
}

int memcmp(const void *s1, const void *s2, size_t n)
{
	const unsigned char *p1 = (const unsigned char *)s1;
	const unsigned char *p2 = (const unsigned char *)s2;

	while (n--)
	{
		if (*p1 != *p2)
			return (int)(*p1) - (int)(*p2);
		++p1;
		++p2;
	}
	return 0;
}

int strncmp(const char *s1, const char *s2, size_t n)
{
	while (n && *s1 && (*s1 == *s2))
	{
		++s1;
		++s2;
		--n;
	}
	if (n == 0)
		return 0;
	return (int)(*(const unsigned char *)s1) - (int)(*(const unsigned char *)s2);
}

char *strncpy(char *dest, const char *src, size_t n)
{
	size_t i;

	for (i = 0; i < n && src[i] != '\0'; ++i)
		dest[i] = src[i];
	for (; i < n; ++i)
		dest[i] = '\0';
	return dest;
}

static void out_ch(char **out, int *count, char ch)
{
	**out = ch;
	(*out)++;
	(*count)++;
}

static void out_rep(char **out, int *count, char ch, int times)
{
	while (times-- > 0)
		out_ch(out, count, ch);
}

static void out_str(char **out, int *count, const char *s)
{
	if (s == NULL)
		s = "(null)";
	while (*s)
		out_ch(out, count, *s++);
}

static int utoa10(unsigned int v, char *tmp /* >= 11 */)
{
	int i = 0;

	/* Produce reversed digits then reverse in-place. */
	if (v == 0)
	{
		tmp[i++] = '0';
		tmp[i] = '\0';
		return i;
	}
	while (v > 0)
	{
		tmp[i++] = (char)('0' + (v % 10u));
		v /= 10u;
	}
	tmp[i] = '\0';

	/* reverse */
	for (int a = 0, b = i - 1; a < b; ++a, --b)
	{
		char t = tmp[a];
		tmp[a] = tmp[b];
		tmp[b] = t;
	}
	return i;
}

static int itoa10(int v, char *tmp /* >= 12 */)
{
	unsigned int uv;
	int len = 0;

	if (v < 0)
	{
		tmp[len++] = '-';
		/* Avoid UB on INT_MIN */
		uv = (unsigned int)(-(v + 1)) + 1u;
	}
	else
	{
		uv = (unsigned int)v;
	}

	len += utoa10(uv, tmp + len);
	return len;
}

static int fmt_strlen(const char *s)
{
	int n = 0;
	if (s == NULL)
		return 6; /* "(null)" */
	while (s[n])
		n++;
	return n;
}

static int vsprintf_min(char *str, const char *format, va_list ap)
{
	char *out = str;
	int count = 0;

	while (*format)
	{
		if (*format != '%')
		{
			out_ch(&out, &count, *format++);
			continue;
		}
		++format; /* skip '%' */

		/* Flags */
		int left = 0;
		int pad_zero = 0;
		if (*format == '-')
		{
			left = 1;
			++format;
		}
		if (*format == '0')
		{
			pad_zero = 1;
			++format;
		}

		/* Width (only positive integer) */
		int width = 0;
		while (*format >= '0' && *format <= '9')
		{
			width = (width * 10) + (*format - '0');
			++format;
		}

		/* Specifier */
		const char spec = *format ? *format++ : '\0';

		if (spec == '%')
		{
			out_ch(&out, &count, '%');
			continue;
		}
		if (spec == 'c')
		{
			const char ch = (char)va_arg(ap, int);
			out_ch(&out, &count, ch);
			continue;
		}
		if (spec == 's')
		{
			const char *s = va_arg(ap, const char *);
			const int slen = fmt_strlen(s);
			const int pad = (width > slen) ? (width - slen) : 0;

			if (!left)
				out_rep(&out, &count, ' ', pad);
			out_str(&out, &count, s);
			if (left)
				out_rep(&out, &count, ' ', pad);
			continue;
		}
		if (spec == 'd' || spec == 'i' || spec == 'u')
		{
			char tmp[16];
			int len = 0;

			if (spec == 'u')
				len = utoa10(va_arg(ap, unsigned int), tmp);
			else
				len = itoa10(va_arg(ap, int), tmp);

			const int pad = (width > len) ? (width - len) : 0;
			const char pad_ch = (pad_zero && !left) ? '0' : ' ';

			if (!left)
				out_rep(&out, &count, pad_ch, pad);
			out_str(&out, &count, tmp);
			if (left)
				out_rep(&out, &count, ' ', pad);
			continue;
		}

		/* Unknown format: print it verbatim. */
		out_ch(&out, &count, '%');
		if (spec)
			out_ch(&out, &count, spec);
	}

	*out = '\0';
	return count;
}

int sprintf(char *str, const char *format, ...)
{
	int r;
	va_list ap;

	va_start(ap, format);
	r = vsprintf_min(str, format, ap);
	va_end(ap);
	return r;
}

