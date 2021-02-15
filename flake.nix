{
  description = "my project description";

  inputs.flake-utils.url = "github:esbullington/flake-utils";

  inputs.nixpkgs.url = "github:esbullington/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let pkgs = nixpkgs.legacyPackages.${system}; in
        {
          devShell = import ./shell.nix { inherit pkgs; };
        }
      );
}