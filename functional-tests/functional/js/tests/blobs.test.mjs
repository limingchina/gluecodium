import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

const byteArrays = module.StaticByteArrayMethods;
const arrays = module.ArraysByteBuffer;
const blobNulls = module.BlobNulls;

function bytes(value) {
  return Array.from(value);
}

test("reverses and concatenates Uint8Array blobs", () => {
  assert.deepEqual(bytes(byteArrays.returnReverseByteBuffer(new Uint8Array([1, 2, 3]))), [3, 2, 1]);
  assert.deepEqual(
    bytes(byteArrays.concatenateByteBuffers(new Uint8Array([1, 2]), new Uint8Array([3, 4]))),
    [1, 2, 3, 4],
  );
});

test("converts blobs nested in value objects", () => {
  const result = byteArrays.reverseBlobInStruct({ blob: new Uint8Array([1, 2, 3]) });
  assert.deepEqual(bytes(result.blob), [3, 2, 1]);
});

test("handles nullable blob results", () => {
  assert.deepEqual(bytes(blobNulls.getBreakingNull()), []);
  assert.equal(blobNulls.getValidNull(), undefined);
});

test("converts blobs through the broader byte-buffer API", () => {
  assert.deepEqual(bytes(arrays.methodWithByteBuffer(new Uint8Array([1, 2, 3]))), [3, 2, 1]);
  assert.deepEqual(bytes(arrays.methodWithImplicitArray(new Uint8Array([1, 2, 3]))), [3, 2, 1]);
});
