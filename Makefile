build:
	./scripts/build

run-local:
	./scripts/build && ./scripts/local

test-local:
	./scripts/test

build-lambda:
	./scripts/build-lambda

run-local-lambda:
	./scripts/build-lambda && ./scripts/local-lambda

test-local-lambda:
	./scripts/test-lambda