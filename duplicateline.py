from gettext import gettext as _
from gi.repository import GObject, Gtk, Gio, Gedit

ACTIONS = {
    'duplicateLine': {
        'label': _("Duplicate Line/Selection"),
        'key': ['<Primary><Shift>d'],
        'method': 'on_duplicate_line'
    },
}


class DuplicateLineApp(GObject.Object, Gedit.AppActivatable):
    __gtype_name__ = "DuplicateLineApp"
    app = GObject.property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.menu_ext = self.extend_menu("edit-section-1")

        for action, config in ACTIONS.items():
            item = Gio.MenuItem.new(config['label'], "win.%s" % action)
            self.menu_ext.append_menu_item(item)
            self.app.set_accels_for_action("win.%s" % action, config['key'])

    def do_deactivate(self):
        for action in ACTIONS.keys():
            self.app.set_accels_for_action("win.%s" % action, [])

        del self.menu_ext


class DuplicateLineWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "DuplicateLineWindowActivatable"

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        try:
            for action, config in ACTIONS.items():
                action = Gio.SimpleAction(name=action)
                action.connect('activate', lambda e, f: getattr(self, config['method'])())
                self.window.add_action(action)
        except Exception:
            print("Error initializing \"Duplicate Line\" plugin")

    def do_update_state(self):
        for action, config in ACTIONS.items():
            self.window.lookup_action(action).set_enabled(self.window.get_active_document() is not None)

    def on_duplicate_line(self):
        doc = self.window.get_active_document()
        if not doc:
            return

        if doc.get_has_selection():
            # User has text selected, get bounds.
            s, e = doc.get_selection_bounds()
            l1 = s.get_line()
            l2 = e.get_line()

            if l1 != l2:
                # Multi-lines selected. Grab the text, insert.
                s.set_line_offset(0)
                e.set_line_offset(e.get_chars_in_line())

                text = doc.get_text(s, e, False)
                if text[-1:] != '\n':
                    # Text doesn't have a new line at the end. Add one for the beginning of the next.
                    text = "\n" + text

                doc.insert(e, text)
            else:
                # Same line selected. Grab the text, insert on same line after selection.
                text = doc.get_text(s, e, False)
                doc.move_mark_by_name("selection_bound", s)
                doc.insert(e, text)
        else:
            # No selection made. Grab the current line the cursor is on, insert on new line.
            s = doc.get_iter_at_mark(doc.get_insert())
            e = doc.get_iter_at_mark(doc.get_insert())
            s.set_line_offset(0)

            if not e.ends_line():
                e.forward_to_line_end()

            text = "\n" + doc.get_text(s, e, False)

            doc.insert(e, text)
