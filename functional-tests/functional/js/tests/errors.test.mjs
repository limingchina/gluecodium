import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const testPackage = await loadPackage("test");
const anotherPackage = await loadPackage("another");

test("returns successful error-bearing calls", () => {
  assert.equal(testPackage.Errors.methodWithError(false), undefined);
  assert.equal(testPackage.Errors.methodWithErrorAndString(false), "SUCCEEDED");
  assert.equal(testPackage.Errors.methodWithGoodAndBad(false), anotherPackage.SomeEnum.ANOTHER_RESULT);
  assert.equal(testPackage.Errors.methodWithExternalError(false), undefined);
  assert.deepEqual(testPackage.Errors.methodWithErrorAndNonDefaultStruct(false), { id: 1n });
  assert.equal(testPackage.Errors.methodWithPayloadError(false), undefined);
  assert.equal(testPackage.Errors.methodWithPayloadErrorAndReturnValue(false), "bar value");
});

test("throws enum and payload errors", () => {
  assert.throws(() => testPackage.Errors.methodWithError(true), (error) => {
    assert.equal(error.name, "InternalError");
    assert.equal(error.error, testPackage.ErrorsInternalErrorCode.CRASHED.value);
    return true;
  });
  assert.throws(() => testPackage.Errors.methodWithErrorAndString(true), (error) => {
    assert.equal(error.name, "ExternalError");
    assert.equal(error.error, testPackage.ExternalErrorCode.BOOM.value);
    return true;
  });
  assert.throws(() => testPackage.Errors.methodWithPayloadError(true), (error) => {
    assert.equal(error.name, "WithPayloadError");
    assert.deepEqual(error.error, { errorCode: 42, message: "foo error" });
    return true;
  });
});

test("rethrows errors from JavaScript interface implementations", () => {
  const messenger = testPackage.ErrorMessenger.create();
  const ErrorsInInterfaceImpl = testPackage.ErrorsInInterface.extend("JavaScriptErrorsInInterface", {
    getMessage: () => "Works",
    setMessage: () => {},
    getMessageWithPayload: () => "Works",
    setMessageWithPayload: () => {},
  });
  const listener = new ErrorsInInterfaceImpl();
  assert.equal(messenger.getMessage(listener), "Works");

  const ThrowingErrorsInInterfaceImpl = testPackage.ErrorsInInterface.extend("JavaScriptThrowingErrorsInInterface", {
    getMessage: () => {
      const error = new Error();
      error.error = testPackage.ExternalErrorCode.BOOM.value;
      throw error;
    },
    setMessage: () => {
      const error = new Error();
      error.error = testPackage.ExternalErrorCode.BOOM.value;
      throw error;
    },
    getMessageWithPayload: () => {
      const error = new Error();
      error.error = { errorCode: 42, message: "foo" };
      throw error;
    },
    setMessageWithPayload: () => {
      const error = new Error();
      error.error = { errorCode: 42, message: "foo" };
      throw error;
    },
  });
  const throwingListener = new ThrowingErrorsInInterfaceImpl();
  assert.throws(() => messenger.getMessage(throwingListener));
  assert.throws(() => messenger.setMessage(throwingListener, "foo"));
  assert.throws(() => messenger.getMessageWithPayload(throwingListener));
  assert.throws(() => messenger.setMessageWithPayload(throwingListener, "foo"));
});