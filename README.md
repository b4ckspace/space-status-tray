# Back-Space Status Tray

Show how many members are at the Backspace in the status tray of the
desktop. This uses Qt to show the tray icon on most platforms and the
Space API to the the members in te space.

Left click on the icon will update the data (updates every 20 minutes
otherwise). Right click opens a menu - for now only for closing.
Middle mouse click opens the backspace web page.

It currently uses a bit clunky method for showing the number of
members by shipping icons from "closed", 1, 2, ..., 9, 1X.

With more generic icons and making a few URLs configurable this should
easily work with other spaces that support the Space API.

This is just a simple Python script that works with both PyQt5 and
PySide6.
