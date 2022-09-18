import sublime, sublime_plugin


def lst_to_sublst(lst):

    return [[lst[i], lst[i + 1]] for i in range(len(lst)) if i != len(lst) - 1]


class ExpandSelectionToSemicolon(sublime_plugin.TextCommand):
    def run(self, edit):

        cursors = self.view.sel()

        def replace_region(start, end):
            # if sel.size() < end - start - 2:
            #     start += 1
            #     end -= 1
            # self.view.sel().subtract(sel)
            self.view.sel().add(sublime.Region(start, end))

        for sel in cursors:
            semicolon = list(map(lambda x: x.begin(), self.view.find_all(";")))
            print(semicolon, sel, sel.begin(), sel.end())
            # no semicolon in file
            if len(semicolon) == 0:
                return
            # only one semicolon in entire file
            elif len(semicolon) == 1:

                replace_region(0, semicolon[0])
            elif len(semicolon) >= 1:
                print("multiple semi")
                cursor_begin = sel.begin()
                cursor_end = sel.end()
                if cursor_begin == cursor_end and cursor_begin not in semicolon:

                    lst = sorted(semicolon + [cursor_begin])
                    idx = lst.index(cursor_begin)
                    start = lst[idx - 1]
                    end = lst[idx + 1]

                    replace_region(start + 1, end)

            return


class ExpandSelectionToQuotesCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        double_quotes = list(map(lambda x: x.begin(), self.view.find_all('"')))
        single_quotes = list(map(lambda x: x.begin(), self.view.find_all("'")))
        backtick_quotes = list(map(lambda x: x.begin(), self.view.find_all("`")))
        print(double_quotes, self.view.find_all('"'))

        def search_for_quotes(q_type, quotes):
            q_size, before, after = False, False, False

            if len(quotes) - self.view.substr(sel).count('"') >= 2:
                print(self.view.substr(sel))
                print(quotes, q_size, before, after, sel.begin(), sel.end())
                all_before = list(filter(lambda x: x < sel.begin(), quotes))
                all_after = list(filter(lambda x: x >= sel.end(), quotes))

                if all_before:
                    before = all_before[-1]
                if all_after:
                    after = all_after[0]

                if all_before and all_after:
                    q_size = after - before
            return q_size, before, after

        def replace_region(start, end):
            if sel.size() < end - start - 2:
                start += 1
                end -= 1
            self.view.sel().subtract(sel)
            self.view.sel().add(sublime.Region(start, end))

        for sel in self.view.sel():

            d_size, d_before, d_after = search_for_quotes('"', double_quotes)
            s_size, s_before, s_after = search_for_quotes("'", single_quotes)
            b_size, b_before, b_after = search_for_quotes("`", backtick_quotes)
            print(d_size, d_before, d_after)
            if (
                d_size
                and (not s_size or d_size < s_size)
                and (not b_size or d_size < b_size)
            ):
                replace_region(d_before, d_after + 1)
            elif (
                s_size
                and (not d_size or s_size < d_size)
                and (not b_size or s_size < b_size)
            ):
                replace_region(s_before, s_after + 1)
            elif (
                b_size
                and (not d_size or b_size < d_size)
                and (not s_size or b_size < s_size)
            ):
                replace_region(b_before, b_after + 1)
