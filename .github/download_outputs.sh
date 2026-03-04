curl -fL -O "https://github.com/logic-star-ai/refactoring-benchmark/releases/download/v0/outputs.zip"

for i in $(seq -w 1 99); do
  part="outputs.z${i}"
  url="https://github.com/logic-star-ai/refactoring-benchmark/releases/download/v0/${part}"
  if ! curl -fL -o "${part}" "${url}"; then
    rm -f "${part}"
    break
  fi
done
zip -s 0 outputs.zip --out combined.zip
unzip -o combined.zip -d .
rm -f outputs.zip outputs.z* combined.zip