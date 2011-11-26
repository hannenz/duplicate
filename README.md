# duplicate - gedit plugin

This plugin for the gedit text editor allows to duplicate lines, just like in [Geany](http://www.geany.org), where you can press `CTRL+d` to duplicate either the current line or the current selection.

This plugin is for Gedit 2.x
Stay tuned for a Gedit3 version

## Installation

Drop the files contained in this package into your `${HOME}/.gnome2/gedit/plugins/` folder. If the `plugins` folder does not exist yet, just create it.
Start gedit and choose `Edit >> Plugins` and activate the _duplicate_ plugin.

## How it works

The plugin adds the keyboard shortcut `CTRL+SHIFT+d` to gedit. When pressing this key combination the plugin will duplicate the current line. If there is a selection and the selection spans several lines, then all selected lines are duplicated. If the selection is within a single line, then the selected text will be duplicated.

