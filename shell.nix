# shell.nix
{ mach-nix, pkgs, ... }:

with pkgs;

let
  myEnv = mach-nix.mkPython {
    requirements = ''
      numpydoc
      pylint
      sphinx
      sphinx-rtd-theme
      sphinx-autodoc-typehints
      watchdog
      PyYAML
      argh
      rsa
      esptool
      rshell
      adafruit-ampy
      '';
  };
in pkgs.mkShell {
  name = "cct-env";
  buildInputs = [
    pkgs.zip
    myEnv
  ];
}
