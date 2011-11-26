from gettext import gettext as _
import gtk
import gedit

ui_str = """
<ui>
	<menubar name="MenuBar">
		<menu name="ToolsMenu" action="Tools">
			<placeholder name="Tools_Ops2">
				<menuitem name="Duplicate" action="Duplicate" />
			</placeholder>
		</menu>
	</menubar>
</ui>
"""

class DuplicateWindowHelper:
	def __init__(self, plugin, window):
		self._window = window
		self._plugin = plugin

		self._insert_menu()
		
	def deactivate(self):
		self._remove_menu()
		self._window = None
		self._plugin = None
		self._action_group = None

	def _insert_menu(self):
		manager = self._window.get_ui_manager()
		self._action_group = gtk.ActionGroup("DuplicatePluginActions")
		self._action_group.add_actions([("Duplicate", None, _("Duplicate"), "<control><shift>d", _("Duplicate current line, current selection or selected lines"), self.on_duplicate_activated)])
		manager.insert_action_group(self._action_group, -1)
		self._ui_id = manager.add_ui_from_string(ui_str)

	def _remove_menu(self):
		manager = self._window.get_ui_manager()
		manager.remove_ui(self._ui_id)
		manager.remove_action_group(self._action_group)
		manager.ensure_update()
	
	def update_ui(self):
		pass

	def on_duplicate_activated(self, action):
		doc = self._window.get_active_document()

		if doc.get_has_selection():
			s, e = doc.get_selection_bounds()
			l1 = s.get_line()
			l2 = e.get_line()

			if l1 != l2:
				s.set_line_offset(0)
				e.forward_to_line_end()
				text = "\n" + doc.get_text(s, e)
				doc.insert(e, text)
			else:
				text = doc.get_text(s, e)
				doc.move_mark_by_name("selection_bound", s)
				doc.insert(e, text)
				
		else:
			s = doc.get_iter_at_mark(doc.get_insert())
			e = doc.get_iter_at_mark(doc.get_insert())
			s.set_line_offset(0)
			if not e.ends_line():
				e.forward_to_line_end()
			text = "\n" + doc.get_text(s, e)
			doc.insert(e, text)


class DuplicatePlugin (gedit.Plugin):
	def __init__(self):
		gedit.Plugin.__init__(self)
		self._instances = {}
		
	def activate(self, window):
		self._instances[window] = DuplicateWindowHelper(self, window)
		
	def deactivate(self, window):
		self._instances[window].deactivate()
		del self._instances[window]	
		
	def update_ui(self, window):
		self._instances[window].update_ui()


