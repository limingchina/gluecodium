import assert from "node:assert/strict";
import test from "node:test";
import { loadPackage } from "./load-package.mjs";

const module = await loadPackage("test");

test("converts complex listener arguments", () => {
  const notifier = module.ComplexListenerFactory.createComplexNotifier();
  const listener = module.ComplexListener.extend("JavaScriptComplexListener", {
    onTrajectoryCompleted(distanceMetric, trajectory, quality, image) {
      this.result = {
        from: trajectory[0].name,
        to: trajectory[trajectory.length - 1].name,
        quality,
        length: distanceMetric.getLength(trajectory),
        image: new TextDecoder().decode(image),
      };
    },
  });
  const instance = new listener();
  const image = new TextEncoder().encode("callback image");
  const trajectory = [
    { name: "origin", pt: { x: 0, y: 0, z: 0 } },
    { name: "destination", pt: { x: 10, y: 20, z: 30 } },
  ];

  notifier.trajectoryCompleted(
    trajectory,
    module.TrajectoryQuality.TRAJECTORY_AVERAGE,
    image,
    instance,
  );

  assert.deepEqual(instance.result, {
    from: "origin",
    to: "destination",
    quality: module.TrajectoryQuality.TRAJECTORY_AVERAGE,
    length: 60,
    image: "callback image",
  });

  notifier.delete();
  instance.delete();
});
