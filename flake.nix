{
  description = "my project description";

  inputs.nixpkgs.url = "github:nix-resources/nixpkgs/nixos-unstable";

  inputs.mach-nix = {
			url = "github:nix-resources/mach-nix/master";
			inputs.nixpkgs.follows = "nixpkgs";
	};

  inputs.flake-utils.url = "github:nix-resources/flake-utils";

  outputs = { self, nixpkgs, mach-nix, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let pkgs = nixpkgs.legacyPackages.${system}; in
        {
          devShell = import ./shell.nix { inherit pkgs mach-nix; };
        }
      );
}
