here=$(pwd)
stock_rom_path=$(find -maxdepth 1 -mindepth 1 -iname '*zip')
if [ $stock_rom_path == "" ] ; then
  echo "No Stock Rom Found"
  exit
else
  echo Stock Rom Found: $stock_rom_path
fi

gargoyle_rom_path=$(find -maxdepth 1 -mindepth 1 -iname '*img')
if [ $gargoyle_rom_path = "" ]; then
  echo "No gargoyle image Found"
  exit
else
  echo gargoyle System Image Found: $gargoyle_rom_path
fi

stock_rom_folder=${stock_rom_path//.zip}
echo Unzipping $stock_rom_path to $stock_rom_folder
unzip -o $stock_rom_path
mkdir -p super
mkdir -p super/stock
mkdir -p super/custom

echo Copying super.img
cp $stock_rom_folder/super.img super/stock/super.img

echo Creating super.ext4.img
simg2img super/stock/super.img super/custom/super.ext4.img

echo Unpacking super.ext4.img
cd super/stock/
$here/lpunpack_and_lpmake/bin/lpunpack $here/super/custom/super.ext4.img
cd $here

echo Copying images to $here/super/custom
cp $here/$gargoyle_rom_path $here/super/custom/system.img
cp $here/super/stock/vendor.img $here/super/custom/
cp $here/super/stock/product.img $here/super/custom/
