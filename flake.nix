{
  description = "Develop Python on Nix with uv";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};

	  pyglet15 = pkgs.python314Packages.pyglet.overrideAttrs (oldAttrs: rec {
	    version = "1.5.27";
	    src = pkgs.fetchFromGitHub {
              owner = "pyglet";
              repo = "pyglet";
              tag = "v${version}";
              hash = "sha256-tdwNnTb8ZmF8CORoA27LWLcM5ykmrDGdaJGNwtEARuE=";
            };
	    propagatedBuildInputs = [ pkgs.python314Packages.setuptools ];
	  });
        in
        {
          default = pkgs.mkShell {
            packages = [
              # python
              pkgs.python314
	      pkgs.python314Packages.setuptools
              pkgs.uv

	      # specially overridden pyglet to patch site package paths
	      pyglet15

              # build tools
              pkgs.cmake
              pkgs.swig
              pkgs.SDL2
              pkgs.pkg-config

              # dependencies
              pkgs.ffmpeg_7
              pkgs.zlib
	      pkgs.libx11

              # typesetting program
              pkgs.typst
            ];

            env = lib.optionalAttrs pkgs.stdenv.isLinux {
              # Python libraries often load native shared objects using dlopen(3).
              # Setting LD_LIBRARY_PATH makes the dynamic library loader aware of libraries without using RPATH for lookup.
              LD_LIBRARY_PATH = lib.makeLibraryPath pkgs.pythonManylinuxPackages.manylinux1;
            };

            shellHook = ''
              export UV_CACHE_DIR=/media/oldhdd/.cache/uv
              unset PYTHONPATH
	      uv sync
              . .venv/bin/activate
	      uv pip install pyglet@${pyglet15}/lib/python3.14/site-packages/pyglet
            '';
          };
        }
      );
    };
}
