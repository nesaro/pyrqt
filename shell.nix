{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    nativeBuildInputs = with pkgs.buildPackages; [ python312 python312.pkgs.pyqt5 python312.pkgs.rpy2 black];
      shellHook = ''
      '';
}

