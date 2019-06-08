get-block-number:
	curl -sS  -X POST --data '{"jsonrpc":"2.0","method":"blockNumber","params":[],"id":1}' 127.0.0.1:1337

watch-block-number:
	watch -n 1 -c "make get-block-number"
