let
pkgs = import <nixpkgs> {};
python_with_deps = pkgs.python312.withPackages (p: [ p.pyqt5 p.rpy2]);
R-with-my-packages = pkgs.rWrapper.override{ packages = with pkgs.rPackages; [ ]; };
#qt_with_wayland = pkgs.qt5.withPackages (p: [p.qtwayland]);
in pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    nativeBuildInputs = with pkgs.buildPackages; [  R-with-my-packages qt5.qtwayland python_with_deps black];
      shellHook = ''
      '';
}

