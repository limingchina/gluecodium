import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("converts map and struct values in listener callbacks", () => {
  const Listener = module.ForecastListener.extend("JavaScriptForecastListener", {
    onForecastDataProvided(data) {
      this.forecast = ["Berlin", "Madrid", "Marrakesh"]
        .map((city) => {
          const forecast = data.get(city);
          return `${city} -> [${forecast.lowestDegree}, ${forecast.highestDegree}]\n`;
        })
        .join("");
    },
  });
  const listener = new Listener();
  const provider = module.ForecastFactory.createProvider();

  provider.inform(listener);
  assert.equal(
    listener.forecast,
    "Berlin -> [-2, 26]\nMadrid -> [1, 33]\nMarrakesh -> [8, 40]\n",
  );

  provider.delete();
  listener.delete();
});
