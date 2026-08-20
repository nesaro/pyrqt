# PYRQT

This is a QT GUI for R. It is based on the code I used for my university
disertation back in 2006, formerly named *driza* 

## REQUIREMENTS

* Python >= 3.4
* Qt > 5.0
* rpy

## INSTALLATION

pyrqt has two dependencies: QT and RPY. Both of them have dependencies that cannot be installed via python packaging.

The recommended way to install these dependencies is to use nix-shell. It will automatically install both python and non python dependencies and work out of the box.

Before running the program, QT requires compiling `.ui` files. The `pyuic` utility (included in PyQT package) will do this. Calling `make` will call pyuic to compile all forms.

## TRANSLATIONS

Most of the code and interface is written in Spanish. However, there is a translation file `driza_es_ES.qm` with some entries. To create the ts file, run `make create_translations`. To build the qm file, run `make translations`

## USAGE

*pyrqt-bin* launches main program
