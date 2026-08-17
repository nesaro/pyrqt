let
pkgs = import <nixpkgs> {};
python_with_deps = pkgs.python312.withPackages (p: [ p.pyqt5 p.rpy2]);
#qt_with_wayland = pkgs.qt5.withPackages (p: [p.qtwayland]);
in pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    nativeBuildInputs = with pkgs.buildPackages; [  qt5.qtwayland python_with_deps black];
      shellHook = ''
      '';
}

