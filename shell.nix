{ pkgs, ... }:

let
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/nix-resources/mach-nix/";
    # ref = "refs/tags/3.1.1";
		rev = "01c3ff9b74d4ad10edaad56b8b34c4043af71df9";
		# rev = "d37c1eb362ee716f952884367159cab4e0b3b9e2";
  }) { currentSystem = "x86_64-linux"; };
  python = "python38";
  customPython = mach-nix.mkPythonShell {
    requirements = builtins.readFile ./requirements.txt;
  };
in

pkgs.mkShell {
  buildInputs = [ customPython ];
}
