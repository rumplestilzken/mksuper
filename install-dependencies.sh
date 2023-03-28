sudo apt install simg2img git libc++-dev clang
git clone https://github.com/rumplestilzken/lpunpack_and_lpmake.git lpunpack_and_lpmake
echo Starting Build for lpunpack_and_lpmake
cd lpunpack_and_lpmake; ./make.sh;
echo Build for lpunpack_and_lpmake complete
chmod +x lpunpack_and_lpmake/bin/*
