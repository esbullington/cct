# flake.nix
{
  description = "...";
  
  inputs.flake-utils.url = "github:nix-resources/flake-utils";
  inputs.mach-nix.url = "github:nix-resources/mach-nix";
  inputs.mach-nix.inputs.nixpkgs.follows = "nixpkgs";

  outputs = { self, nixpkgs, flake-utils, mach-nix }: (flake-utils.lib.eachDefaultSystem (system:
  let
    pkgs = import nixpkgs { inherit system; };
  in {
    devShell = (import ./shell.nix { nixpkgs=pkgs; mach-nix=mach-nix.lib.${system}; });
  }));
}
