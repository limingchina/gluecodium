import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("converts listener return values across supported types", () => {
  const MessagePackage = module.MessagePackage.extend("JavaScriptMessagePackage", {
    unpackMessage() {
      return "Works";
    },
  });
  const Listener = module.ListenerWithReturn.extend("JavaScriptListenerWithReturn", {
    getMessage() {
      return "Works";
    },
    getPackedMessage() {
      return new MessagePackage();
    },
    getBoxedMessage() {
      return module.MessageBox.create();
    },
    getStructuredMessage() {
      return { message: "Works" };
    },
    getEnumeratedMessage() {
      return module.MessageEnum.YES;
    },
    getArrayedMessage() {
      return ["Works"];
    },
    getMappedMessage() {
      return new Map([[0, "Works"]]);
    },
    getBufferedMessage() {
      return new TextEncoder().encode("Works");
    },
  });
  const envelope = new Listener();
  const delivery = module.MessageDelivery.createMe();

  assert.equal(delivery.getMessage(envelope), "Works");
  assert.equal(delivery.getPackedMessage(envelope), "Works");
  assert.equal(delivery.getBoxedMessage(envelope), "Works");
  assert.equal(delivery.getStructuredMessage(envelope), "Works");
  assert.equal(delivery.getEnumeratedMessage(envelope), "YES");
  assert.equal(delivery.getArrayedMessage(envelope), "Works");
  assert.equal(delivery.getMappedMessage(envelope), "Works");
  assert.equal(delivery.getBufferedMessage(envelope), "Works");

  delivery.delete();
  envelope.delete();
});
