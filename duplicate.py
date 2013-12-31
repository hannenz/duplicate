from gettext import gettext as _
from gi.repository import GObject, Gtk, Gedit

# Place the menu item above "Select All" in "Edit".
ui_str = """<ui>
<menubar name="MenuBar">
<menu name="EditMenu" action="Edit">
<placeholder name="EditOps_2">
<menuitem name="DuplicateLine" action="DuplicateLine"/>
</placeholder>
</menu>
</menubar>
</ui>
"""

class DuplicateLineWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "DuplicateLineWindowActivatable"

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self._insert_menu()

    def do_deactivate(self):
        self._remove_menu()

        self._action_group = None

    def _insert_menu(self):
        manager = self.window.get_ui_manager()

        # Add our menu action and set ctrl+shift+D to activate.
        self._action_group = Gtk.ActionGroup("DuplicateLinePluginActions")
        self._action_group.add_actions([(
            "DuplicateLine",
            None,
            _("Duplicate Line"),
            "<control><shift>d",
            _("Duplicate current line, current selection or selected lines"),
            self.on_duplicate_line_activate
        )])

        manager.insert_action_group(self._action_group, -1)

        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_id)
        manager.remove_action_group(self._action_group)
        manager.ensure_update()

    def do_update_state(self):
        self._action_group.set_sensitive(self.window.get_active_document() != None)

    def on_duplicate_line_activate(self, action):
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

