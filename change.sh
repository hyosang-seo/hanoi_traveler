cd images_jeju

# .jpeg, .jpg 파일들을 수정 시간 순으로 정렬 후 IMG_x.jpeg 형식으로 리네이밍
find . -maxdepth 1 -type f \( -iname "*.jpeg" -o -iname "*.jpg" \) -exec stat -f "%m %N" {} \; | \
sort -n | \
awk '{$1=""; print substr($0,2)}' | \
nl -n rz -w 3 | \
while read num file; do
  # num을 10진수 정수로 바꾸기 위해 10# 접두사 붙이기
  newname=$(printf "IMG_%d.jpeg" "$((10#$num))")
  mv "$file" "$newname"
done