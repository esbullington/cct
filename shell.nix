# shell.nix
{ mach-nix, pkgs, ... }:

with pkgs;

let
  myEnv = mach-nix.mkPythonShell {
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
in mkShell {

  name = "cct-environment";

  buildInputs = [
    myEnv
    pkgs.zip
  ];

}
