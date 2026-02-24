/*
 * Saturn Bible ACF (prototype)
 *
 * Current goal:
 * - Open "menu de livros" (book list)
 * - Each time the book menu is opened, change the background image between 2 TGAs.
 *
 * Assets used:
 * - cd/BOOKMENU/A.TGA
 * - cd/BOOKMENU/B.TGA
 */

#include <jo/jo.h>

#include "font_mapping.h"

#define UI_PRINTF(X, Y, ...) jo_nbg2_printf((X), (Y), __VA_ARGS__)

typedef enum
{
	SCREEN_MAIN_MENU = 0,
	SCREEN_BOOK_MENU = 1,
	SCREEN_CHAPTER_MENU = 2,
	SCREEN_READING = 3,
} app_screen;

#define UI_CARD_Z (500)

#define CHAPTER_GRID_COLS (4)
#define CHAPTER_GRID_ROWS (13)
#define CHAPTER_GRID_CARD_W_CHARS (9)
#define CHAPTER_GRID_CARD_H_CHARS (2)
#define CHAPTER_GRID_GAP_W_CHARS (1)
#define CHAPTER_GRID_X0_CHARS (1)
#define CHAPTER_GRID_Y0_CHARS (2)
#define CHAPTER_GRID_PAGE_SIZE (CHAPTER_GRID_COLS * CHAPTER_GRID_ROWS)

#define BOOK_COUNT (66)
#define VISIBLE_BOOKS (26)

/*
 * Jo Engine (SGL build) exposes both "pressed" and "down" APIs, but in practice
 * emulator/keyboard mappings can generate repeats that feel too fast.
 *
 * We implement our own key-repeat based on the held state (jo_is_pad1_key_pressed),
 * so behavior is stable across real pads and emulator keyboards:
 * - action buttons (A/START/B/etc): edge only (once per physical press)
 * - navigation (UP/DOWN): delayed repeat at a controlled rate
 */

/* Bible ACF binary/index constants */
#define BIBLE_IDX_HEADER_SIZE (20)
#define BIBLE_BOOK_ENTRY_SIZE (8)
#define BIBLE_CHAPTER_ENTRY_SIZE (8)
#define BIBLE_VERSE_ENTRY_SIZE (4)
#define BIBLE_EXPECTED_BOOK_COUNT (66)
#define BIBLE_EXPECTED_CHAPTER_COUNT (1189)
#define BIBLE_IDX_MAX_SIZE (160 * 1024)

#define READ_MAX_COLS (40)
#define READ_MAX_LINES (1024)
#define READ_VISIBLE_LINES (24)
#define READ_TOP_Y (1)

#define REPEAT_DELAY_MENU (18)       /* frames */
#define REPEAT_INTERVAL_MENU (10)    /* frames */
#define REPEAT_DELAY_READING (18)    /* frames */
#define REPEAT_INTERVAL_READING (12) /* frames */

static app_screen g_screen = SCREEN_MAIN_MENU;
static bool g_needs_redraw = true;

static int g_book_selected = 0;
static int g_book_scroll = 0;

static int g_chapter_selected = 0; /* 0-based, within book */
static int g_chapter_scroll = 0;
static int g_read_scroll = 0;      /* 0-based, line index */
static int g_read_line_count = 0;
static char g_read_lines[READ_MAX_LINES][READ_MAX_COLS + 1];

static int g_last_bookmenu_bg = 0; /* 1..2 */

static int g_last_book_bg_variant = 0; /* 1..2 (A/B) */

static int g_ui_card_sprite = -1;
static int g_ui_card_sel_sprite = -1;

static jo_palette g_font_palette;

typedef enum
{
	KEY_UP = 0,
	KEY_DOWN,
	KEY_LEFT,
	KEY_RIGHT,
	KEY_L,
	KEY_R,
	KEY_A,
	KEY_B,
	KEY_START,
	KEY_X,
	KEY_Y,
	KEY_COUNT,
} input_key_id;

typedef struct
{
	jo_gamepad_keys key;
	unsigned short frames_held; /* 0 on first pressed frame, increments while held */
	bool held;
	bool prev_held;
} input_key_state;

static input_key_state g_input[KEY_COUNT] =
{
	{JO_KEY_UP, 0, false, false},
	{JO_KEY_DOWN, 0, false, false},
	{JO_KEY_LEFT, 0, false, false},
	{JO_KEY_RIGHT, 0, false, false},
	{JO_KEY_L, 0, false, false},
	{JO_KEY_R, 0, false, false},
	{JO_KEY_A, 0, false, false},
	{JO_KEY_B, 0, false, false},
	{JO_KEY_START, 0, false, false},
	{JO_KEY_X, 0, false, false},
	{JO_KEY_Y, 0, false, false},
};

static unsigned char g_bible_idx[BIBLE_IDX_MAX_SIZE];
static int g_bible_idx_size = 0;
static bool g_bible_loaded = false;
static unsigned int g_bible_text_size = 0;
static unsigned short g_bible_book_count = 0;
static unsigned int g_bible_chapter_count = 0;
static unsigned int g_bible_verse_count = 0;

static const unsigned char *g_bible_book_table = JO_NULL;
static const unsigned char *g_bible_chapter_table = JO_NULL;
static const unsigned char *g_bible_verse_offsets = JO_NULL;

static const char *kBookNames[BOOK_COUNT] =
{
	"Genesis",
	"Exodo",
	"Levitico",
	"Numeros",
	"Deuteronomio",
	"Josue",
	"Juizes",
	"Rute",
	"1 Samuel",
	"2 Samuel",
	"1 Reis",
	"2 Reis",
	"1 Cronicas",
	"2 Cronicas",
	"Esdras",
	"Neemias",
	"Ester",
	"Jo",
	"Salmos",
	"Proverbios",
	"Eclesiastes",
	"Cantares",
	"Isaias",
	"Jeremias",
	"Lamentacoes",
	"Ezequiel",
	"Daniel",
	"Oseias",
	"Joel",
	"Amos",
	"Obadias",
	"Jonas",
	"Miqueias",
	"Naum",
	"Habacuque",
	"Sofonias",
	"Ageu",
	"Zacarias",
	"Malaquias",
	"Mateus",
	"Marcos",
	"Lucas",
	"Joao",
	"Atos",
	"Romanos",
	"1 Corintios",
	"2 Corintios",
	"Galatas",
	"Efesios",
	"Filipenses",
	"Colossenses",
	"1 Tessalonicenses",
	"2 Tessalonicenses",
	"1 Timoteo",
	"2 Timoteo",
	"Tito",
	"Filemom",
	"Hebreus",
	"Tiago",
	"1 Pedro",
	"2 Pedro",
	"1 Joao",
	"2 Joao",
	"3 Joao",
	"Judas",
	"Apocalipse",
};

static __jo_force_inline unsigned short rd16_le(const unsigned char *p)
{
	return (unsigned short)(p[0] | ((unsigned short)p[1] << 8));
}

static __jo_force_inline unsigned int rd32_le(const unsigned char *p)
{
	return (unsigned int)(p[0] | ((unsigned int)p[1] << 8) | ((unsigned int)p[2] << 16) |
			      ((unsigned int)p[3] << 24));
}

static __jo_force_inline const unsigned char *bible_book_entry_ptr(int book_index)
{
	return g_bible_book_table + (book_index * BIBLE_BOOK_ENTRY_SIZE);
}

static __jo_force_inline const unsigned char *bible_chapter_entry_ptr(unsigned int chapter_global_index)
{
	return g_bible_chapter_table + (chapter_global_index * BIBLE_CHAPTER_ENTRY_SIZE);
}

static __jo_force_inline const unsigned char *bible_verse_offset_ptr(unsigned int verse_global_index)
{
	return g_bible_verse_offsets + (verse_global_index * BIBLE_VERSE_ENTRY_SIZE);
}

static unsigned int bible_get_book_first_chapter(int book_index)
{
	const unsigned char *p = bible_book_entry_ptr(book_index);
	return rd32_le(p + 0);
}

static unsigned short bible_get_book_chapter_count(int book_index)
{
	const unsigned char *p = bible_book_entry_ptr(book_index);
	return rd16_le(p + 4);
}

static unsigned int bible_get_chapter_first_verse(unsigned int chapter_global_index)
{
	const unsigned char *p = bible_chapter_entry_ptr(chapter_global_index);
	return rd32_le(p + 0);
}

static unsigned short bible_get_chapter_verse_count(unsigned int chapter_global_index)
{
	const unsigned char *p = bible_chapter_entry_ptr(chapter_global_index);
	return rd16_le(p + 4);
}

static unsigned int bible_get_verse_offset(unsigned int verse_global_index)
{
	return rd32_le(bible_verse_offset_ptr(verse_global_index));
}

static bool bible_load_index(void)
{
	jo_file file;
	int got = 0;
	int want;
	int r;
	unsigned int expected_size;

	if (!jo_fs_open(&file, "BIBLE.IDX"))
		return false;
	if (file.size <= 0 || file.size >= (int)(sizeof(g_bible_idx) - 1))
	{
		jo_fs_close(&file);
		jo_core_error("BIBLE.IDX muito grande");
		return false;
	}

	want = file.size;
	while (got < want)
	{
		r = jo_fs_read_next_bytes(&file, (char *)g_bible_idx + got, (unsigned int)(want - got));
		if (r <= 0)
			break;
		got += r;
	}
	jo_fs_close(&file);
	g_bible_idx[want] = 0;
	g_bible_idx_size = want;

	if (got != want)
	{
		jo_core_error("BIBLE.IDX leitura incompleta");
		return false;
	}

	if (!(g_bible_idx[0] == 'B' && g_bible_idx[1] == 'I' && g_bible_idx[2] == 'B' &&
	      g_bible_idx[3] == '1'))
	{
		jo_core_error("BIBLE.IDX bad magic");
		return false;
	}

	if (rd16_le(g_bible_idx + 4) != 1)
	{
		jo_core_error("BIBLE.IDX bad version");
		return false;
	}

	g_bible_book_count = rd16_le(g_bible_idx + 6);
	g_bible_chapter_count = rd32_le(g_bible_idx + 8);
	g_bible_verse_count = rd32_le(g_bible_idx + 12);
	g_bible_text_size = rd32_le(g_bible_idx + 16);

	if (g_bible_book_count != BIBLE_EXPECTED_BOOK_COUNT ||
	    g_bible_chapter_count != BIBLE_EXPECTED_CHAPTER_COUNT)
	{
		jo_core_error("BIBLE.IDX counts mismatch");
		return false;
	}

	expected_size = (unsigned int)(BIBLE_IDX_HEADER_SIZE +
				       (g_bible_book_count * BIBLE_BOOK_ENTRY_SIZE) +
				       (g_bible_chapter_count * BIBLE_CHAPTER_ENTRY_SIZE) +
				       (g_bible_verse_count * BIBLE_VERSE_ENTRY_SIZE));
	if ((unsigned int)g_bible_idx_size != expected_size)
	{
		jo_core_error("BIBLE.IDX size mismatch");
		return false;
	}

	g_bible_book_table = g_bible_idx + BIBLE_IDX_HEADER_SIZE;
	g_bible_chapter_table = g_bible_book_table + (g_bible_book_count * BIBLE_BOOK_ENTRY_SIZE);
	g_bible_verse_offsets = g_bible_chapter_table + (g_bible_chapter_count * BIBLE_CHAPTER_ENTRY_SIZE);

	g_bible_loaded = true;
	return true;
}

static jo_palette *tga_palette_handling_callback(void)
{
	/* Avoid consuming multiple palette IDs if called more than once. */
	if (g_font_palette.data == JO_NULL)
		jo_create_palette(&g_font_palette);
	return (&g_font_palette);
}

static void load_fonts(void)
{
	jo_img_8bits img;

	img.data = JO_NULL;
	jo_tga_8bits_loader(&img, JO_ROOT_DIR, "FONT.TGA",
			    SATURN_FONT_TGA_TRANSPARENT_COLOR_INDEX_IN_PALETTE);

	jo_vdp2_set_nbg2_8bits_font(&img, (char *)SATURN_FONT_MAPPING_STR,
				    g_font_palette.id, false, true);
	jo_free_img(&img);
}

static void load_ui_sprites(void)
{
	if (g_ui_card_sprite >= 0 && g_ui_card_sel_sprite >= 0)
		return;
	g_ui_card_sprite = jo_sprite_add_tga("UI", "CARD.TGA", JO_COLOR_Transparent);
	g_ui_card_sel_sprite = jo_sprite_add_tga("UI", "CARDSEL.TGA", JO_COLOR_Transparent);
	if (g_ui_card_sprite < 0 || g_ui_card_sel_sprite < 0)
		jo_core_error("Falha ao carregar UI/CARD*.TGA");
}

static void ui_draw_card_quad(const int sprite_id, const int x, const int y, const int w, const int h,
			      const int tilt_px)
{
	jo_pos2D_fixed p[4];
	int x0 = x;
	int y0 = y;
	int x1 = x + w - 1;
	int y1 = y + h - 1;
	int tl = x0 + tilt_px;
	int tr = x1 - tilt_px;

	if (tr < tl)
	{
		tl = x0;
		tr = x1;
	}

	p[0].x = jo_int2fixed(tl);
	p[0].y = jo_int2fixed(y0);
	p[1].x = jo_int2fixed(tr);
	p[1].y = jo_int2fixed(y0);
	p[2].x = jo_int2fixed(x1);
	p[2].y = jo_int2fixed(y1);
	p[3].x = jo_int2fixed(x0);
	p[3].y = jo_int2fixed(y1);

	jo_sprite_draw_4p_fixed(sprite_id, p, jo_int2fixed(UI_CARD_Z), false);
}

static void set_background_from_cd(const char *dir, const char *filename)
{
	jo_img bg;

	bg.data = JO_NULL;
	jo_tga_loader(&bg, dir, filename, JO_COLOR_Transparent);
	jo_set_background_sprite(&bg, 0, 0);
	jo_free_img(&bg);
}

static bool try_set_background_from_cd(const char *dir, const char *filename)
{
	jo_img bg;
	t_tga_error_code code;

	bg.data = JO_NULL;
	code = jo_tga_loader(&bg, dir, filename, JO_COLOR_Transparent);
	if (code != JO_TGA_OK)
	{
		if (bg.data != JO_NULL)
			jo_free_img(&bg);
		return false;
	}
	jo_set_background_sprite(&bg, 0, 0);
	jo_free_img(&bg);
	return true;
}

static void seed_rng_from_time(void)
{
	/* Saturn has no RTC in typical setups; ticks + FRC vary with user timing. */
	jo_random_seed = (int)(jo_get_ticks() ^ (unsigned int)jo_time_get_frc());
}

static void apply_random_bookmenu_background(void)
{
	int pick;

	seed_rng_from_time();
	pick = jo_random(2); /* 1..2 */

	/*
	 * With only 2 images, if you want the background to always change
	 * each time the menu opens, flipping when it repeats guarantees it.
	 */
	if (g_last_bookmenu_bg != 0 && pick == g_last_bookmenu_bg)
		pick = (pick == 1) ? 2 : 1;
	g_last_bookmenu_bg = pick;

	if (pick == 1)
		set_background_from_cd("BOOKMENU", "A.TGA");
	else
		set_background_from_cd("BOOKMENU", "B.TGA");
}

static void apply_book_background(int book_index)
{
	char filename[16];
	int pick;
	int first;
	int second;

	/* Book images are synced to the CD as:
	 *   cd/BOOKS/B01A.TGA and cd/BOOKS/B01B.TGA (etc)
	 */
	seed_rng_from_time();
	pick = jo_random(2); /* 1..2 */
	if (g_last_book_bg_variant != 0 && pick == g_last_book_bg_variant)
		pick = (pick == 1) ? 2 : 1;
	g_last_book_bg_variant = pick;

	first = pick;
	second = (pick == 1) ? 2 : 1;

	sprintf(filename, "B%02d%c.TGA", book_index + 1, (first == 1) ? 'A' : 'B');
	if (try_set_background_from_cd("BOOKS", filename))
		return;
	sprintf(filename, "B%02d%c.TGA", book_index + 1, (second == 1) ? 'A' : 'B');
	(void)try_set_background_from_cd("BOOKS", filename);
}

static void read_lines_clear(void)
{
	g_read_line_count = 0;
	g_read_scroll = 0;
}

static void read_lines_add(const char *s)
{
	int i;
	char *dst;

	if (g_read_line_count >= READ_MAX_LINES)
		return;
	dst = g_read_lines[g_read_line_count++];
	for (i = 0; i < READ_MAX_COLS && s[i] != '\0'; ++i)
		dst[i] = s[i];
	dst[i] = '\0';
}

static void read_lines_add_wrapped_verse(int verse_num, const char *verse_text)
{
	char prefix[8];
	const int prefix_len = sprintf(prefix, "%d ", verse_num);
	const int indent = (prefix_len < READ_MAX_COLS) ? prefix_len : READ_MAX_COLS;
	int pos = 0;
	bool first = true;

	while (verse_text[pos] == ' ')
		++pos;

	while (verse_text[pos] != '\0')
	{
		char line[READ_MAX_COLS + 1];
		int col = 0;
		int remaining;
		int end;
		int last_space = -1;
		int j;

		if (first)
		{
			for (j = 0; j < prefix_len && col < READ_MAX_COLS; ++j)
				line[col++] = prefix[j];
		}
		else
		{
			for (j = 0; j < indent && col < READ_MAX_COLS; ++j)
				line[col++] = ' ';
		}

		remaining = READ_MAX_COLS - col;
		end = pos;
		for (j = 0; verse_text[end] != '\0' && j < remaining; ++j, ++end)
		{
			if (verse_text[end] == ' ')
				last_space = end;
		}
		if (verse_text[end] != '\0' && last_space > pos)
			end = last_space;

		for (j = pos; j < end && col < READ_MAX_COLS; ++j)
			line[col++] = verse_text[j];
		line[col] = '\0';

		read_lines_add(line);

		pos = end;
		while (verse_text[pos] == ' ')
			++pos;
		first = false;
	}
}

static void input_update(void)
{
	int i;

	for (i = 0; i < KEY_COUNT; ++i)
	{
		input_key_state *st = &g_input[i];
		const bool held_now = jo_is_pad1_key_pressed(st->key);

		st->prev_held = st->held;
		st->held = held_now;

		if (!held_now)
		{
			st->frames_held = 0;
			continue;
		}

		if (!st->prev_held)
		{
			/* First frame held: 0 */
			st->frames_held = 0;
		}
		else if (st->frames_held < 0xFFFF)
		{
			++st->frames_held;
		}
	}
}

static __jo_force_inline bool input_just_pressed(const input_key_id id)
{
	return (g_input[id].held && !g_input[id].prev_held);
}

static bool input_repeat(const input_key_id id, const unsigned short delay, const unsigned short interval)
{
	const input_key_state *st = &g_input[id];

	if (st->held && !st->prev_held)
		return true;
	if (!st->held)
		return false;
	if (st->frames_held < delay)
		return false;
	if (interval == 0)
		return false;
	return (((unsigned short)(st->frames_held - delay) % interval) == 0);
}

static void bible_load_current_chapter_lines(void)
{
	static char verse_buf[8192];
	jo_file file;
	unsigned int book_first_chapter;
	unsigned int chapter_global;
	unsigned int verse_first;
	unsigned int verse_idx;
	unsigned int verse_off;
	unsigned int next_off;
	unsigned int len;
	unsigned short chapter_count;
	unsigned short verse_count;
	int v;

	read_lines_clear();

	if (!g_bible_loaded)
	{
		read_lines_add("BIBLE.IDX nao carregada");
		return;
	}

	book_first_chapter = bible_get_book_first_chapter(g_book_selected);
	chapter_count = bible_get_book_chapter_count(g_book_selected);
	if (g_chapter_selected < 0 || g_chapter_selected >= (int)chapter_count)
	{
		read_lines_add("Capitulo invalido");
		return;
	}
	chapter_global = book_first_chapter + (unsigned int)g_chapter_selected;
	verse_first = bible_get_chapter_first_verse(chapter_global);
	verse_count = bible_get_chapter_verse_count(chapter_global);

	if (verse_first >= g_bible_verse_count || verse_count == 0)
	{
		read_lines_add("Indice de versiculos invalido");
		return;
	}

	if (!jo_fs_open(&file, "BIBLE.BIN"))
	{
		read_lines_add("Falha ao abrir BIBLE.BIN");
		return;
	}

	verse_off = bible_get_verse_offset(verse_first);
	if (!jo_fs_seek_forward(&file, verse_off))
	{
		jo_fs_close(&file);
		read_lines_add("Seek falhou");
		return;
	}

	for (v = 0; v < (int)verse_count; ++v)
	{
		verse_idx = verse_first + (unsigned int)v;
		verse_off = bible_get_verse_offset(verse_idx);
		if ((verse_idx + 1) < g_bible_verse_count)
			next_off = bible_get_verse_offset(verse_idx + 1);
		else
			next_off = g_bible_text_size;

		if (next_off <= verse_off)
			continue;
		len = next_off - verse_off;

		if (len >= (sizeof(verse_buf) - 1))
		{
			const unsigned int keep = (unsigned int)(sizeof(verse_buf) - 1);
			jo_fs_read_next_bytes(&file, verse_buf, keep);
			verse_buf[keep] = '\0';
			jo_fs_seek_forward(&file, len - keep);
		}
		else
		{
			const int r = jo_fs_read_next_bytes(&file, verse_buf, len);
			verse_buf[(r < 0) ? 0 : r] = '\0';
		}

		read_lines_add_wrapped_verse(v + 1, verse_buf);
		if (g_read_line_count >= READ_MAX_LINES)
			break;
	}

	jo_fs_close(&file);
}

static void enter_main_menu(void)
{
	g_screen = SCREEN_MAIN_MENU;
	/* Slightly darken the background for better text contrast. */
	jo_set_screen_color_filter_a(JO_NBG1_SCREEN, -48, -48, -48);
	/* Prefer the provided UI background if present on CD. */
	if (!try_set_background_from_cd("UI", "MAIN.TGA"))
		jo_clear_background(JO_COLOR_Black);
	g_needs_redraw = true;
}

static void enter_book_menu(void)
{
	g_screen = SCREEN_BOOK_MENU;
	apply_random_bookmenu_background();
	/* Darken the menu background a bit to improve readability. */
	jo_set_screen_color_filter_a(JO_NBG1_SCREEN, -64, -64, -64);
	g_needs_redraw = true;
}

static void enter_chapter_menu(bool reset_selection)
{
	unsigned short chapter_count = 0;
	const int page_size = CHAPTER_GRID_PAGE_SIZE;

	g_screen = SCREEN_CHAPTER_MENU;
	apply_book_background(g_book_selected);
	/* Darken the background a bit to improve contrast with white font. */
	jo_set_screen_color_filter_a(JO_NBG1_SCREEN, -64, -64, -64);

	if (g_bible_loaded)
		chapter_count = bible_get_book_chapter_count(g_book_selected);

	if (reset_selection || !g_bible_loaded || chapter_count == 0)
	{
		g_chapter_selected = 0;
		g_chapter_scroll = 0;
	}
	else if (g_chapter_selected < 0 || g_chapter_selected >= (int)chapter_count)
	{
		g_chapter_selected = 0;
		g_chapter_scroll = 0;
	}

	/* Keep selection on a page boundary for the horizontal grid UI. */
	if (page_size > 0)
		g_chapter_scroll = (g_chapter_selected / page_size) * page_size;
	else
		g_chapter_scroll = 0;
	if (g_chapter_scroll < 0)
		g_chapter_scroll = 0;

	g_needs_redraw = true;
}

static void enter_reading(void)
{
	g_screen = SCREEN_READING;
	/* Keep the book background (set in chapter menu) for context. */
	jo_set_screen_color_filter_a(JO_NBG1_SCREEN, -64, -64, -64);
	bible_load_current_chapter_lines();
	g_needs_redraw = true;
}

static void book_menu_move_selection(int delta)
{
	const int next = g_book_selected + delta;

	if (next < 0 || next >= BOOK_COUNT)
		return;
	g_book_selected = next;

	if (g_book_selected < g_book_scroll)
		g_book_scroll = g_book_selected;
	else if (g_book_selected >= (g_book_scroll + VISIBLE_BOOKS))
		g_book_scroll = g_book_selected - (VISIBLE_BOOKS - 1);

	if (g_book_scroll < 0)
		g_book_scroll = 0;
	if (g_book_scroll > (BOOK_COUNT - VISIBLE_BOOKS))
		g_book_scroll = (BOOK_COUNT - VISIBLE_BOOKS);
	if (g_book_scroll < 0)
		g_book_scroll = 0;

	g_needs_redraw = true;
}

static void chapter_menu_move_selection(int delta)
{
	unsigned short chapter_count;
	int next;
	const int page_size = CHAPTER_GRID_PAGE_SIZE;

	if (!g_bible_loaded)
		return;

	chapter_count = bible_get_book_chapter_count(g_book_selected);
	if (chapter_count == 0)
		return;

	next = g_chapter_selected + delta;
	if (next < 0)
		next = 0;
	else if (next >= (int)chapter_count)
		next = (int)chapter_count - 1;

	g_chapter_selected = next;

	if (page_size > 0)
		g_chapter_scroll = (g_chapter_selected / page_size) * page_size;
	else
		g_chapter_scroll = 0;

	g_needs_redraw = true;
}

static __jo_force_inline int reading_max_scroll(void)
{
	return JO_MAX(0, g_read_line_count - READ_VISIBLE_LINES);
}

static void reading_change_chapter(int delta)
{
	unsigned short chapter_count;
	int next;

	if (!g_bible_loaded)
		return;

	chapter_count = bible_get_book_chapter_count(g_book_selected);
	if (chapter_count == 0)
		return;

	next = g_chapter_selected + delta;
	if (next < 0 || next >= (int)chapter_count)
		return;

	g_chapter_selected = next;
	bible_load_current_chapter_lines();
	g_needs_redraw = true;
}

static void handle_input(void)
{
	if (!jo_is_pad1_available())
		return;

	input_update();

	switch (g_screen)
	{
	case SCREEN_MAIN_MENU:
		if (input_just_pressed(KEY_A) || input_just_pressed(KEY_START))
			enter_book_menu();
		return;

	case SCREEN_BOOK_MENU:
		if (input_just_pressed(KEY_B))
		{
			enter_main_menu();
			return;
		}
		if (input_just_pressed(KEY_A) || input_just_pressed(KEY_START))
		{
			enter_chapter_menu(true);
			return;
		}
		if (input_repeat(KEY_UP, REPEAT_DELAY_MENU, REPEAT_INTERVAL_MENU))
			book_menu_move_selection(-1);
		else if (input_repeat(KEY_DOWN, REPEAT_DELAY_MENU, REPEAT_INTERVAL_MENU))
			book_menu_move_selection(1);
		else if (input_just_pressed(KEY_L))
			book_menu_move_selection(-5);
		else if (input_just_pressed(KEY_R))
			book_menu_move_selection(+5);
		return;

	case SCREEN_CHAPTER_MENU:
		if (input_just_pressed(KEY_B))
		{
			enter_book_menu();
			return;
		}
		if (input_just_pressed(KEY_A) || input_just_pressed(KEY_START))
		{
			enter_reading();
			return;
		}
		if (input_repeat(KEY_LEFT, REPEAT_DELAY_MENU, REPEAT_INTERVAL_MENU))
			chapter_menu_move_selection(-1);
		else if (input_repeat(KEY_RIGHT, REPEAT_DELAY_MENU, REPEAT_INTERVAL_MENU))
			chapter_menu_move_selection(1);
		else if (input_repeat(KEY_UP, REPEAT_DELAY_MENU, REPEAT_INTERVAL_MENU))
			chapter_menu_move_selection(-CHAPTER_GRID_COLS);
		else if (input_repeat(KEY_DOWN, REPEAT_DELAY_MENU, REPEAT_INTERVAL_MENU))
			chapter_menu_move_selection(CHAPTER_GRID_COLS);
		else if (input_just_pressed(KEY_L))
			chapter_menu_move_selection(-CHAPTER_GRID_PAGE_SIZE);
		else if (input_just_pressed(KEY_R))
			chapter_menu_move_selection(CHAPTER_GRID_PAGE_SIZE);
		return;

	case SCREEN_READING:
		if (input_just_pressed(KEY_B) || input_just_pressed(KEY_A) || input_just_pressed(KEY_START))
		{
			enter_chapter_menu(false);
			return;
		}
		if (input_repeat(KEY_UP, REPEAT_DELAY_READING, REPEAT_INTERVAL_READING))
		{
			if (g_read_scroll > 0)
				--g_read_scroll;
			g_needs_redraw = true;
		}
		else if (input_repeat(KEY_DOWN, REPEAT_DELAY_READING, REPEAT_INTERVAL_READING))
		{
			const int max_scroll = reading_max_scroll();
			if (g_read_scroll < max_scroll)
				++g_read_scroll;
			g_needs_redraw = true;
		}
		else if (input_just_pressed(KEY_LEFT) || input_just_pressed(KEY_L))
			reading_change_chapter(-1);
		else if (input_just_pressed(KEY_RIGHT) || input_just_pressed(KEY_R))
			reading_change_chapter(+1);
		else if (input_just_pressed(KEY_X))
		{
			const int delta = 10;
			g_read_scroll -= delta;
			if (g_read_scroll < 0)
				g_read_scroll = 0;
			g_needs_redraw = true;
		}
		else if (input_just_pressed(KEY_Y))
		{
			const int delta = 10;
			const int max_scroll = reading_max_scroll();
			g_read_scroll += delta;
			if (g_read_scroll > max_scroll)
				g_read_scroll = max_scroll;
			g_needs_redraw = true;
		}
		return;
	default:
		return;
	}
}

static void draw_main_menu(void)
{
	UI_PRINTF(2, 2, "BIBLIA ACF - Saturn (prot)");
	UI_PRINTF(2, 4, "A/START: menu de livros");
	UI_PRINTF(2, 6, "Objetivo: alternar 2 fundos");
	UI_PRINTF(2, 8, "Abra/feche o menu p/ testar");
	UI_PRINTF(2, 11, "Teste: Acentos PT-BR (Latin-1)");
	UI_PRINTF(2, 13, "\xC0\xC1\xC3\xC7\xC9\xCA\xD3\xD4\xDA");
	UI_PRINTF(2, 14, "\xE0\xE1\xE2\xE3\xE7\xE9\xEA\xED\xF2\xF3\xF4\xF5\xFA\xFC \xAB \xB3");
}

static void draw_book_menu(void)
{
	int i;
	int y = 2;
	const int end = JO_MIN(g_book_scroll + VISIBLE_BOOKS, BOOK_COUNT);

	UI_PRINTF(2, 0, "Menu de livros  (B: voltar)");
	UI_PRINTF(2, 1, "Fundo: %d (abre de novo p/ trocar)", g_last_bookmenu_bg);
	UI_PRINTF(2, 28, "A: capitulos  UP/DOWN: 1  L/R: 5");

	for (i = g_book_scroll; i < end; ++i, ++y)
	{
		const char *prefix = (i == g_book_selected) ? ">" : " ";
		UI_PRINTF(2, y, "%s %02d. %-20s", prefix, (i + 1), kBookNames[i]);
	}
}

static void draw_book_menu_cards(void)
{
	int i;
	int y = 2;
	const int end = JO_MIN(g_book_scroll + VISIBLE_BOOKS, BOOK_COUNT);

	if (g_ui_card_sprite < 0 || g_ui_card_sel_sprite < 0)
		return;

	for (i = g_book_scroll; i < end; ++i, ++y)
	{
		const bool selected = (i == g_book_selected);
		const int sprite = selected ? g_ui_card_sel_sprite : g_ui_card_sprite;

		/* Row card: fits behind the 40x30 text grid (8px per char). */
		const int x_px = 8;
		const int y_px = y * 8;
		const int w_px = 304;
		const int h_px = 8;
		ui_draw_card_quad(sprite, x_px, y_px, w_px, h_px, selected ? 3 : 2);
	}
}

static void draw_chapter_menu(void)
{
	unsigned short chapter_count;
	const int page_size = CHAPTER_GRID_PAGE_SIZE;
	const int page_start = g_chapter_scroll;
	int page_end;
	int total_pages;
	int page_no;
	int i;

	if (!g_bible_loaded)
	{
		UI_PRINTF(2, 0, "Capitulos");
		UI_PRINTF(2, 2, "BIBLE.IDX nao carregada");
		UI_PRINTF(2, 4, "B: voltar");
		return;
	}

	chapter_count = bible_get_book_chapter_count(g_book_selected);
	page_end = JO_MIN(page_start + page_size, (int)chapter_count);
	total_pages = (page_size > 0) ? (((int)chapter_count + page_size - 1) / page_size) : 1;
	page_no = (page_size > 0) ? ((page_start / page_size) + 1) : 1;

	UI_PRINTF(2, 0, "%s - Capitulos (B: voltar)", kBookNames[g_book_selected]);
	UI_PRINTF(2, 1, "Total: %d  Pag: %d/%d", (int)chapter_count, page_no, total_pages);
	UI_PRINTF(2, 28, "A: ler  D-PAD: mover  L/R: pag");

		for (i = page_start; i < page_end; ++i)
		{
			const int offset = i - page_start;
			const int row = offset / CHAPTER_GRID_COLS;
			const int col = offset % CHAPTER_GRID_COLS;
			const int x = CHAPTER_GRID_X0_CHARS +
				      (col * (CHAPTER_GRID_CARD_W_CHARS + CHAPTER_GRID_GAP_W_CHARS));
			const int y = CHAPTER_GRID_Y0_CHARS + (row * CHAPTER_GRID_CARD_H_CHARS);

			/*
			 * The chapter cards are narrow. Using a 2-line label avoids the number
			 * appearing too close to the bevel/border and reads better.
			 */
			{
				const int cx = x + ((CHAPTER_GRID_CARD_W_CHARS - 3) / 2);
				UI_PRINTF(cx, y + 0, "Cap");
				UI_PRINTF(cx, y + 1, "%03d", (i + 1));
			}
		}
	}

static void draw_chapter_menu_cards(void)
{
	unsigned short chapter_count;
	const int page_size = CHAPTER_GRID_PAGE_SIZE;
	const int page_start = g_chapter_scroll;
	int page_end;
	int i;

	if (!g_bible_loaded)
		return;
	if (g_ui_card_sprite < 0 || g_ui_card_sel_sprite < 0)
		return;

	chapter_count = bible_get_book_chapter_count(g_book_selected);
	page_end = JO_MIN(page_start + page_size, (int)chapter_count);

	for (i = page_start; i < page_end; ++i)
	{
		const int offset = i - page_start;
		const int row = offset / CHAPTER_GRID_COLS;
		const int col = offset % CHAPTER_GRID_COLS;
		const bool selected = (i == g_chapter_selected);
		const int sprite = selected ? g_ui_card_sel_sprite : g_ui_card_sprite;

		const int x_char = CHAPTER_GRID_X0_CHARS +
				   (col * (CHAPTER_GRID_CARD_W_CHARS + CHAPTER_GRID_GAP_W_CHARS));
		const int y_char = CHAPTER_GRID_Y0_CHARS + (row * CHAPTER_GRID_CARD_H_CHARS);

		const int x_px = x_char * 8;
		const int y_px = y_char * 8;
		const int w_px = CHAPTER_GRID_CARD_W_CHARS * 8;
		const int h_px = CHAPTER_GRID_CARD_H_CHARS * 8;

		ui_draw_card_quad(sprite, x_px, y_px, w_px, h_px, selected ? 3 : 2);
	}
}

static void draw_reading(void)
{
	int i;
	int y;
	unsigned short chapter_count;
	int chap;
	const int hud_y = 26;

	if (!g_bible_loaded)
	{
		UI_PRINTF(0, 0, "BIBLE.IDX nao carregada");
		UI_PRINTF(0, 2, "B: voltar");
		return;
	}

	chapter_count = bible_get_book_chapter_count(g_book_selected);
	chap = g_chapter_selected + 1;

	UI_PRINTF(0, hud_y + 0, "%s  Cap %d/%d", kBookNames[g_book_selected], chap, (int)chapter_count);
	UI_PRINTF(0, hud_y + 1, "A/B/START: capitulos  L/R: cap  UP/DOWN: rolar  X/Y: pag");

	for (i = 0, y = READ_TOP_Y; i < READ_VISIBLE_LINES; ++i, ++y)
	{
		const int idx = g_read_scroll + i;
		if (idx >= g_read_line_count)
			break;
		jo_nbg2_printf(0, y, "%s", g_read_lines[idx]);
	}

	if (g_read_line_count > 0)
		UI_PRINTF(0, hud_y + 2, "Linha %d/%d", g_read_scroll + 1, g_read_line_count);
	else
		UI_PRINTF(0, hud_y + 2, "Linha 0/0");
}

static void my_draw(void)
{
	handle_input();

	/* Sprites must be drawn every frame (VDP1 command list). */
	if (g_screen == SCREEN_BOOK_MENU)
		draw_book_menu_cards();
	else if (g_screen == SCREEN_CHAPTER_MENU)
		draw_chapter_menu_cards();

	if (!g_needs_redraw)
		return;
	g_needs_redraw = false;

	jo_nbg2_clear();
	{
		const char *err = jo_get_last_error();
		if (err[0] != '\0')
			UI_PRINTF(0, 29, "%s", err);
	}

	if (g_screen == SCREEN_MAIN_MENU)
		draw_main_menu();
	else if (g_screen == SCREEN_BOOK_MENU)
		draw_book_menu();
	else if (g_screen == SCREEN_CHAPTER_MENU)
		draw_chapter_menu();
	else
		draw_reading();
}

void jo_main(void)
{
	jo_core_init(JO_COLOR_Black);
	jo_set_tga_palette_handling(tga_palette_handling_callback);
	jo_core_set_screens_order(JO_NBG2_SCREEN, JO_SPRITE_SCREEN,
				  JO_NBG0_SCREEN, JO_RBG0_SCREEN, JO_NBG1_SCREEN);
	load_fonts();
	load_ui_sprites();
	if (!bible_load_index())
		jo_core_error("Falha ao carregar BIBLE.IDX");
	enter_main_menu();
	jo_core_add_callback(my_draw);
	jo_core_run();
}
