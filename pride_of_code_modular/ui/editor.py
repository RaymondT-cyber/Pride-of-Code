import pygame, ast, keyword
from typing import List, Tuple, Optional

# Enhanced CodeEditor with selection, clipboard (internal + pygame.scrap fallback),
# smart indentation, line numbers gutter, and clickable breakpoints.

class CodeEditor:
    def __init__(self, rect: pygame.Rect, font=None, lines:List[str]=None, max_undos=500):
        self.rect = rect
        self.font = font or pygame.font.SysFont('consolas', 18)
        self.lines = lines or ['# Welcome to Code of Pride!', '# Write Python code to control the marching band', '']
        self.cursor = [0, 0]  # line index, column index
        self.scroll = 0  # top visible line
        self.max_undos = max_undos
        self.undo_stack = []
        self.redo_stack = []
        self.blink = 0.0
        self.blink_visible = True
        self.syntax_error = None

        # selection: tuple((line,col),(line,col)) or None; selection is inclusive of start, exclusive of end
        self.selection: Optional[Tuple[Tuple[int,int], Tuple[int,int]]] = None
        self.selecting_with_mouse = False

        # gutter and breakpoints
        self.gutter_width = 48
        self.breakpoints = set()

        # internal clipboard as fallback if pygame.scrap isn't available/initialized
        self._clipboard = ""

        # colors
        self.colors = {
            'background': (30,30,40),
            'gutter_bg': (24,24,28),
            'gutter_text': (160,160,160),
            'text': (230,230,230),
            'cursor': (255,255,255),
            'keyword': (86,156,214),
            'string': (206,145,120),
            'comment': (106,153,85),
            'number': (181,206,168),
            'function': (220,220,170),
            'class': (78,201,176),
            'error_bg': (80,20,20),
            'selection_bg': (80,100,160),
            'bracket': (180,120,180)
        }

        # try to init pygame.scrap for system clipboard if available
        self._use_scrap = False
        try:
            import pygame.scrap as scrap
            scrap.init()
            self._scrap = scrap
            self._use_scrap = True
        except Exception:
            self._use_scrap = False

    # ----------------- Undo/Redo -----------------
    def push_undo(self):
        state = (list(self.lines), tuple(self.cursor), None if self.selection is None else (tuple(self.selection[0]), tuple(self.selection[1])))
        self.undo_stack.append(state)
        if len(self.undo_stack) > self.max_undos:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return
        state = self.undo_stack.pop()
        self.redo_stack.append((list(self.lines), tuple(self.cursor), None if self.selection is None else (tuple(self.selection[0]), tuple(self.selection[1]))))
        self.lines, cur, sel = state
        self.cursor = list(cur)
        self.selection = None if sel is None else (tuple(sel[0]), tuple(sel[1]))
        self._ensure_cursor_valid()
        self._ensure_scroll_for_cursor()
        self.check_syntax_quiet()

    def redo(self):
        if not self.redo_stack:
            return
        state = self.redo_stack.pop()
        self.push_undo()
        self.lines, cur, sel = state
        self.cursor = list(cur)
        self.selection = None if sel is None else (tuple(sel[0]), tuple(sel[1]))
        self._ensure_cursor_valid()
        self._ensure_scroll_for_cursor()
        self.check_syntax_quiet()

    # ----------------- Clipboard helpers -----------------
    def _set_clipboard(self, text: str):
        self._clipboard = text
        if self._use_scrap:
            try:
                # scrap requires bytes, strip NULs
                self._scrap.put(self._scrap.get_type(), text.encode('utf-8'))
            except Exception:
                pass

    def _get_clipboard(self) -> str:
        if self._use_scrap:
            try:
                data = self._scrap.get(self._scrap.get_type())
                if isinstance(data, bytes):
                    return data.decode('utf-8', errors='ignore')
            except Exception:
                pass
        return self._clipboard

    # ----------------- Selection utilities -----------------
    def _has_selection(self) -> bool:
        return self.selection is not None and self.selection[0] != self.selection[1]

    def _clear_selection(self):
        self.selection = None

    def _normalize_selection(self):
        if not self.selection:
            return None
        a, b = self.selection
        if a < b:
            return (a,b)
        else:
            return (b,a)

    def _get_selection_text(self) -> str:
        sel = self._normalize_selection()
        if not sel:
            return ''
        (l1,c1),(l2,c2) = sel
        if l1 == l2:
            return self.lines[l1][c1:c2]
        parts = [self.lines[l1][c1:]] + self.lines[l1+1:l2] + [self.lines[l2][:c2]]
        return '\\n'.join(parts)

    def _delete_selection(self):
        sel = self._normalize_selection()
        if not sel:
            return
        (l1,c1),(l2,c2) = sel
        self.push_undo()
        if l1 == l2:
            line = self.lines[l1]
            self.lines[l1] = line[:c1] + line[c2:]
            self.cursor = [l1, c1]
        else:
            first = self.lines[l1][:c1]
            last = self.lines[l2][c2:]
            # remove middle lines
            del self.lines[l1+1:l2+1]
            self.lines[l1] = first + last
            self.cursor = [l1, c1]
        self._clear_selection()
        self._ensure_cursor_valid()
        self._ensure_scroll_for_cursor()
        self.check_syntax_quiet()

    # ----------------- Basic editing ops -----------------
    def insert_text(self, text: str):
        if self._has_selection():
            self._delete_selection()
        self.push_undo()
        line = self.lines[self.cursor[0]]
        col = self.cursor[1]
        new = line[:col] + text + line[col:]
        self.lines[self.cursor[0]] = new
        self.cursor[1] += len(text)
        self._ensure_scroll_for_cursor()
        self.check_syntax_quiet()

    def new_line(self):
        # smart indentation: inherit leading whitespace; add extra indent if previous endswith ':'
        lidx, col = self.cursor
        line = self.lines[lidx]
        left = line[:col]
        right = line[col:]
        indent = ''
        for ch in left:
            if ch in (' ', '\\t'):
                indent += ch
            else:
                break
        # if the current visible left ends with ':' add 4 spaces
        extra = ''
        if left.rstrip().endswith(':'):
            extra = '    '
        self.push_undo()
        self.lines[lidx] = left
        self.lines.insert(lidx+1, indent + extra + right.lstrip('\\n'))
        self.cursor = [lidx+1, len(indent)+len(extra)]
        self._ensure_scroll_for_cursor()
        self.check_syntax_quiet()

    def backspace(self):
        if self._has_selection():
            self._delete_selection(); return
        lidx, col = self.cursor
        if lidx == 0 and col == 0:
            return
        self.push_undo()
        if col > 0:
            line = self.lines[lidx]
            # smart unindent: if preceding chars are 4 spaces and at line start, remove 4
            if col >=4 and line[col-4:col] == '    ' and line[:col-4].rstrip()=='':
                self.lines[lidx] = line[:col-4] + line[col:]
                self.cursor[1] -= 4
            else:
                self.lines[lidx] = line[:col-1] + line[col:]
                self.cursor[1] -= 1
        else:
            # join with previous line
            prev = self.lines[lidx-1]
            cur = self.lines.pop(lidx)
            self.cursor = [lidx-1, len(prev)]
            self.lines[self.cursor[0]] = prev + cur
        self._ensure_scroll_for_cursor()
        self.check_syntax_quiet()

    def delete(self):
        if self._has_selection():
            self._delete_selection(); return
        lidx, col = self.cursor
        line = self.lines[lidx]
        if col < len(line):
            self.push_undo()
            self.lines[lidx] = line[:col] + line[col+1:]
        else:
            if lidx+1 < len(self.lines):
                self.push_undo()
                self.lines[lidx] = line + self.lines.pop(lidx+1)
        self.check_syntax_quiet()

    # ----------------- Cursor movement and selection -----------------
    def move_cursor(self, dline:int, dcol:int, extend_selection=False, absolute=False):
        if absolute:
            self.cursor = [dline, dcol]
        else:
            # move within current line with bounds; handle line wrapping for up/down
            if dline != 0:
                # move up/down preserving column if possible
                target_line = max(0, min(self.cursor[0] + dline, len(self.lines)-1))
                target_col = min(self.cursor[1], len(self.lines[target_line]))
                self.cursor = [target_line, target_col]
            else:
                # horizontal move
                newcol = self.cursor[1] + dcol
                if newcol < 0:
                    if self.cursor[0] > 0:
                        self.cursor[0] -= 1
                        self.cursor[1] = len(self.lines[self.cursor[0]])
                    else:
                        self.cursor[1] = 0
                elif newcol > len(self.lines[self.cursor[0]]):
                    if self.cursor[0] < len(self.lines)-1:
                        self.cursor[0] += 1
                        self.cursor[1] = 0
                    else:
                        self.cursor[1] = len(self.lines[self.cursor[0]])
                else:
                    self.cursor[1] = newcol

        if extend_selection:
            if not self.selection:
                self.selection = ((self.cursor[0], self.cursor[1]), (self.cursor[0], self.cursor[1]))
            else:
                # update end to current cursor
                start, end = self.selection
                self.selection = (start, (self.cursor[0], self.cursor[1]))
        else:
            self._clear_selection()

        self._ensure_cursor_valid()
        self._ensure_scroll_for_cursor()

    def select_all(self):
        if not self.lines:
            return
        self.selection = ((0,0), (len(self.lines)-1, len(self.lines[-1])))
        self.cursor = [len(self.lines)-1, len(self.lines[-1])]
        self._ensure_scroll_for_cursor()

    # ----------------- Event handling -----------------
    def handle_event(self, ev):
        # keyboard
        if ev.type == pygame.KEYDOWN:
            mod = pygame.key.get_mods()
            ctrl = mod & pygame.KMOD_CTRL
            shift = mod & pygame.KMOD_SHIFT

            if ctrl and ev.key == pygame.K_z:
                self.undo(); return
            if ctrl and ev.key == pygame.K_y:
                self.redo(); return
            if ctrl and ev.key == pygame.K_a:
                self.select_all(); return
            if ctrl and ev.key == pygame.K_x:
                self.cut(); return
            if ctrl and ev.key == pygame.K_c:
                self.copy(); return
            if ctrl and ev.key == pygame.K_v:
                self.paste(); return
            if ctrl and ev.key == pygame.K_s:
                self.on_save_requested() if hasattr(self, 'on_save_requested') else None
                return

            if ev.key == pygame.K_RETURN:
                self.new_line(); return
            if ev.key == pygame.K_BACKSPACE:
                self.backspace(); return
            if ev.key == pygame.K_DELETE:
                self.delete(); return
            if ev.key == pygame.K_TAB:
                # indent or unindent with shift
                if shift:
                    # unindent current line or selection
                    self._unindent_selection_or_line()
                else:
                    if self._has_selection():
                        self._indent_selection()
                    else:
                        self.insert_text('    ')
                return

            # navigation with selection when shift held
            extend = bool(shift)
            if ev.key == pygame.K_LEFT:
                if self.cursor[1] > 0:
                    self.move_cursor(0, -1, extend_selection=extend)
                elif self.cursor[0] > 0:
                    self.move_cursor(-1, 0, extend_selection=extend); self.cursor[1] = len(self.lines[self.cursor[0]])
                return
            if ev.key == pygame.K_RIGHT:
                if self.cursor[1] < len(self.lines[self.cursor[0]]):
                    self.move_cursor(0, +1, extend_selection=extend)
                elif self.cursor[0] < len(self.lines)-1:
                    self.move_cursor(+1, 0, extend_selection=extend); self.cursor[1] = 0
                return
            if ev.key == pygame.K_UP:
                self.move_cursor(-1, 0, extend_selection=extend); return
            if ev.key == pygame.K_DOWN:
                self.move_cursor(+1, 0, extend_selection=extend); return
            if ev.key == pygame.K_HOME:
                self.move_cursor(self.cursor[0], 0, extend_selection=extend, absolute=True); return
            if ev.key == pygame.K_END:
                self.move_cursor(self.cursor[0], len(self.lines[self.cursor[0]]), extend_selection=extend, absolute=True); return
            if ev.key == pygame.K_PAGEUP:
                self.scroll = max(0, self.scroll - (self.rect.height // self.font.get_linesize())); return
            if ev.key == pygame.K_PAGEDOWN:
                self.scroll += (self.rect.height // self.font.get_linesize()); return

        # text input (for SDL2 text events)
        if ev.type == pygame.TEXTINPUT:
            self.insert_text(ev.text)
            return

        # mouse events
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mx, my = ev.pos
            # gutter click toggles breakpoint
            if self._in_gutter(mx, my):
                line = self._line_from_y(my)
                if line is not None:
                    if line in self.breakpoints:
                        self.breakpoints.remove(line)
                    else:
                        self.breakpoints.add(line)
                return
            # click inside editor content: set cursor/selection start
            if self.rect.collidepoint(mx,my):
                fh = self.font.get_linesize()
                rel_y = my - self.rect.y
                line_idx = self.scroll + rel_y // fh
                line_idx = max(0, min(line_idx, len(self.lines)-1))
                rel_x = mx - (self.rect.x + self.gutter_width) - 6
                # approximate col by measuring widths
                s = self.lines[line_idx]
                acc = 0
                col = 0
                for i,ch in enumerate(s):
                    w = self.font.size(ch)[0]
                    if acc + w/2 >= rel_x:
                        col = i; break
                    acc += w
                else:
                    col = len(s)
                self.cursor = [line_idx, col]
                self.selection = ((line_idx, col), (line_idx, col))
                self.selecting_with_mouse = True
                return

        if ev.type == pygame.MOUSEMOTION and self.selecting_with_mouse:
            mx, my = ev.pos
            if self.rect.collidepoint(mx,my):
                fh = self.font.get_linesize()
                rel_y = my - self.rect.y
                line_idx = self.scroll + rel_y // fh
                line_idx = max(0, min(line_idx, len(self.lines)-1))
                rel_x = mx - (self.rect.x + self.gutter_width) - 6
                s = self.lines[line_idx]
                acc = 0
                col = 0
                for i,ch in enumerate(s):
                    w = self.font.size(ch)[0]
                    if acc + w/2 >= rel_x:
                        col = i; break
                    acc += w
                else:
                    col = len(s)
                # update selection end
                if self.selection:
                    start, _ = self.selection
                    self.selection = (start, (line_idx, col))
                else:
                    self.selection = ((line_idx, col), (line_idx, col))
            return

        if ev.type == pygame.MOUSEBUTTONUP and self.selecting_with_mouse:
            self.selecting_with_mouse = False
            # if selection collapsed, clear it
            if self.selection and self.selection[0] == self.selection[1]:
                self._clear_selection()
            return

    # ----------------- Indent helpers -----------------
    def _indent_selection(self):
        sel = self._normalize_selection()
        if not sel:
            # indent current line
            l = self.cursor[0]
            self.push_undo()
            self.lines[l] = '    ' + self.lines[l]
            self.cursor[1] += 4
        else:
            (l1,c1),(l2,c2) = sel
            self.push_undo()
            for i in range(l1, l2+1):
                self.lines[i] = '    ' + self.lines[i]
            # adjust cursor and selection
            self.cursor[1] += 4
            self.selection = ((l1, c1+4), (l2, c2+4))

    def _unindent_selection_or_line(self):
        sel = self._normalize_selection()
        if not sel:
            l = self.cursor[0]
            line = self.lines[l]
            if line.startswith('    '):
                self.push_undo()
                self.lines[l] = line[4:]
                self.cursor[1] = max(0, self.cursor[1]-4)
        else:
            (l1,c1),(l2,c2) = sel
            self.push_undo()
            for i in range(l1, l2+1):
                if self.lines[i].startswith('    '):
                    self.lines[i] = self.lines[i][4:]
            self.selection = ((l1, max(0,c1-4)), (l2, max(0,c2-4)))
            self.cursor[1] = max(0, self.cursor[1]-4)

    # ----------------- Clipboard operations -----------------
    def copy(self):
        if not self._has_selection():
            return
        txt = self._get_selection_text()
        self._set_clipboard(txt)

    def cut(self):
        if not self._has_selection():
            return
        txt = self._get_selection_text()
        self._set_clipboard(txt)
        self._delete_selection()

    def paste(self):
        txt = self._get_clipboard()
        if not txt:
            return
        # paste may contain newlines
        if self._has_selection():
            self._delete_selection()
        self.push_undo()
        l, c = self.cursor
        line = self.lines[l]
        before = line[:c]
        after = line[c:]
        parts = txt.split('\\n')
        if len(parts) == 1:
            self.lines[l] = before + parts[0] + after
            self.cursor[1] = c + len(parts[0])
        else:
            self.lines[l] = before + parts[0]
            for i,p in enumerate(parts[1:], start=1):
                self.lines.insert(l+i, p)
            self.lines[l+len(parts)-1] = self.lines[l+len(parts)-1] + after
            self.cursor = [l+len(parts)-1, len(parts[-1])]
        self._ensure_scroll_for_cursor()
        self.check_syntax_quiet()

    # ----------------- Rendering -----------------
    def _in_gutter(self, mx, my):
        return (self.rect.x <= mx < self.rect.x + self.gutter_width) and (self.rect.y <= my < self.rect.y + self.rect.height)

    def _line_from_y(self, my):
        if not (self.rect.y <= my < self.rect.y + self.rect.height):
            return None
        fh = self.font.get_linesize()
        rel_y = my - self.rect.y
        line_idx = self.scroll + rel_y // fh
        if 0 <= line_idx < len(self.lines):
            return line_idx
        return None

    def draw(self, surf:pygame.Surface):
        # background
        pygame.draw.rect(surf, self.colors['background'], self.rect)
        # gutter
        gutter_rect = pygame.Rect(self.rect.x, self.rect.y, self.gutter_width, self.rect.height)
        pygame.draw.rect(surf, self.colors['gutter_bg'], gutter_rect)
        fh = self.font.get_linesize()
        visible = max(1, self.rect.height // fh)

        # draw line numbers and breakpoints
        for i in range(visible):
            li = i + self.scroll
            if li >= len(self.lines): break
            y = self.rect.y + i*fh
            num_s = self.font.render(str(li+1), True, self.colors['gutter_text'])
            surf.blit(num_s, (self.rect.x + 6, y))
            if li in self.breakpoints:
                # draw red dot
                cx = self.rect.x + self.gutter_width - 14
                cy = y + fh//2
                pygame.draw.circle(surf, (200,60,60), (cx, cy), 6)

        # syntax error background if exists
        if self.syntax_error:
            err_line = self.syntax_error.get('line', None)
            if err_line is not None:
                rel = err_line - self.scroll
                if 0 <= rel < visible:
                    r = pygame.Rect(self.rect.x + self.gutter_width, self.rect.y + rel*fh, self.rect.width - self.gutter_width, fh)
                    pygame.draw.rect(surf, self.colors['error_bg'], r)

        # render visible lines with token spans
        for i in range(visible):
            li = i + self.scroll
            if li >= len(self.lines): break
            line = self.lines[li]
            x = self.rect.x + self.gutter_width + 6
            y = self.rect.y + i*fh

            # draw selection background if intersects this line
            if self._has_selection():
                sel = self._normalize_selection()
                (l1,c1),(l2,c2) = sel
                if l1 <= li <= l2:
                    # compute sel range on this line
                    start = c1 if li==l1 else 0
                    end = c2 if li==l2 else len(self.lines[li])
                    # draw rect for selected region
                    pre = self.lines[li][:start]
                    sel_text = self.lines[li][start:end]
                    px = x + self.font.size(pre)[0]
                    w = max(1, self.font.size(sel_text)[0])
                    pygame.draw.rect(surf, self.colors['selection_bg'], (px, y, w, fh))

            spans = self._tokenize_line_spans(line)
            for text, ttype in spans:
                color = self.colors['text']
                if ttype == 'keyword': color = self.colors['keyword']
                elif ttype == 'string': color = self.colors['string']
                elif ttype == 'comment': color = self.colors['comment']
                elif ttype == 'number': color = self.colors['number']
                elif ttype == 'function': color = self.colors['function']
                elif ttype == 'class': color = self.colors['class']
                elif ttype == 'bracket': color = self.colors['bracket']
                surf.blit(self.font.render(text, True, color), (x, y))
                x += self.font.size(text)[0]

        # draw cursor
        cline, ccol = self.cursor
        if self.scroll <= cline < self.scroll + visible:
            rel = cline - self.scroll
            pre = self.lines[cline][:ccol]
            cx = self.rect.x + self.gutter_width + 6 + self.font.size(pre)[0]
            cy = self.rect.y + rel*fh
            # blink
            self.blink += 1/60.0
            if self.blink > 0.5:
                self.blink = 0.0
                self.blink_visible = not self.blink_visible
            if self.blink_visible:
                pygame.draw.rect(surf, self.colors['cursor'], (cx, cy, max(2,2), fh))

        # bottom line: show syntax messages
        msg = ''
        if self.syntax_error:
            msg = f"Syntax Error: {self.syntax_error.get('msg','')}"
        else:
            msg = 'Ctrl+C/X/V Copy/Cut/Paste — Click gutter to toggle breakpoint'
        info_surf = self.font.render(msg, True, (230,230,230))
        surf.blit(info_surf, (self.rect.x + self.gutter_width + 6, self.rect.y + self.rect.height - fh - 6))

    # ----------------- Utilities -----------------
    def _ensure_scroll_for_cursor(self):
        fh = self.font.get_linesize()
        visible = max(1, self.rect.height // fh)
        if self.cursor[0] < self.scroll:
            self.scroll = self.cursor[0]
        elif self.cursor[0] >= self.scroll + visible:
            self.scroll = self.cursor[0] - visible + 1

    def _ensure_cursor_valid(self):
        self.cursor[0] = max(0, min(self.cursor[0], len(self.lines)-1))
        self.cursor[1] = max(0, min(self.cursor[1], len(self.lines[self.cursor[0]])))

    def check_syntax_quiet(self):
        try:
            ast.parse('\\n'.join(self.lines))
            self.syntax_error = None
            return True, None
        except Exception as e:
            msg = str(e)
            ln = None
            try:
                import re
                m = re.search(r'line (\\d+)', msg)
                if m:
                    ln = int(m.group(1)) - 1
            except Exception:
                ln = None
            self.syntax_error = {'msg': msg, 'line': ln}
            return False, msg

    def check_syntax(self):
        ok, msg = self.check_syntax_quiet()
        return ok, self.syntax_error.get('msg') if self.syntax_error else None

    def _tokenize_line_spans(self, line: str) -> List[Tuple[str, str]]:
        """Tokenize a line of Python code into spans with types for syntax highlighting."""
        # This is a simplified tokenizer for basic Python syntax highlighting
        spans = []
        i = 0
        while i < len(line):
            # Skip whitespace
            if line[i].isspace():
                j = i
                while j < len(line) and line[j].isspace():
                    j += 1
                spans.append((line[i:j], 'text'))
                i = j
                continue

            # Strings (single or double quotes)
            if line[i] in ('"', "'"):
                quote = line[i]
                j = i + 1
                while j < len(line) and line[j] != quote:
                    if line[j] == '\\' and j + 1 < len(line):
                        j += 2  # Skip escaped character
                    else:
                        j += 1
                if j < len(line):
                    j += 1  # Include closing quote
                spans.append((line[i:j], 'string'))
                i = j
                continue

            # Comments
            if line[i] == '#':
                spans.append((line[i:], 'comment'))
                break

            # Numbers
            if line[i].isdigit() or (line[i] == '.' and i + 1 < len(line) and line[i+1].isdigit()):
                j = i
                if line[j] == '.':
                    j += 1
                while j < len(line) and (line[j].isdigit() or line[j] == '.'):
                    j += 1
                # Check for scientific notation
                if j < len(line) and line[j] in 'eE':
                    j += 1
                    if j < len(line) and line[j] in '+-':
                        j += 1
                    while j < len(line) and line[j].isdigit():
                        j += 1
                spans.append((line[i:j], 'number'))
                i = j
                continue

            # Keywords and identifiers
            if line[i].isalpha() or line[i] == '_':
                j = i
                while j < len(line) and (line[j].isalnum() or line[j] == '_'):
                    j += 1
                word = line[i:j]
                
                # Check for special identifiers
                if word in keyword.kwlist:
                    spans.append((word, 'keyword'))
                elif word in ('True', 'False', 'None'):
                    spans.append((word, 'keyword'))
                elif word in dir(__builtins__):
                    spans.append((word, 'function'))
                else:
                    # Check if it's followed by parentheses (function call)
                    k = j
                    while k < len(line) and line[k].isspace():
                        k += 1
                    if k < len(line) and line[k] == '(':
                        spans.append((word, 'function'))
                    else:
                        spans.append((word, 'text'))
                i = j
                continue

            # Brackets
            if line[i] in '()[]{}':
                spans.append((line[i], 'bracket'))
                i += 1
                continue

            # Operators and other punctuation
            spans.append((line[i], 'text'))
            i += 1

        return spans