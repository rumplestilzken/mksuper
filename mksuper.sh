here=$(pwd)
#TODO Are you building for a Titan Pocket or Titan Slim?
declare -i super_max_size=0
select device in Pocket Slim
do
case $device in
  Pocket)
    super_max_size=4831838208
    break
    ;;
  Slim)
    super_max_size=4831838208
    break
    ;;
  esac
done

echo Max size of super.img is $super_max_size

echo Preparing new super.img
export new_product_size=$(stat -c %s $here/super/custom/product.img)
export new_vendor_size=$(stat -c %s $here/super/custom/vendor.img)
export new_system_size=$(stat -c %s $here/super/custom/system.img)
export new_metadata_size=65536
export new_group_size=$((new_product_size + new_vendor_size + new_system_size))
export new_super_size=$((new_group_size + new_metadata_size))
echo New product Size should be $new_product_size bytes
echo New vendor Size should be $new_vendor_size bytes
echo New system Size should be $new_system_size bytes
echo New group Size should be $new_group_size bytes
echo New super Size should be $new_super_size bytes

if [ $new_super_size -gt $super_max_size ]; then
  echo WARNING: New super.img will be too large for your devices super partition. This is unsupported.
fi

cd super
$here/lpunpack_and_lpmake/bin/lpmake --metadata-size $new_metadata_size --super-name super --metadata-slots 2 --device super:$super_max_size \
--group main:$new_group_size --partition system:readonly:$new_system_size:main --image system=custom/system.img --partition vendor:readonly:$new_vendor_size:main \
--image vendor=custom/vendor.img --partition product:readonly:$new_product_size:main --image product=custom/product.img --sparse --output ./super.new.img

echo New super image created: super/super.new.img
