# shell.nix

{ mach-nix, nixpkgs ? (import <nixpkgs> { })}:

with nixpkgs;

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
in myEnv
