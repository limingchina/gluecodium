// Phase 0.2 spike test driver (Node.js)
const factory = require('./mi_spike.js');

factory().then((Module) => {
  const assert = (cond, msg) => {
    if (!cond) { console.error('FAIL: ' + msg); process.exitCode = 1; }
    else console.log('PASS: ' + msg);
  };

  // 1. Primary-base inheritance works
  const mc = Module.getMultiClass();
  assert(typeof mc.parentFunction === 'function', 'MultiClass inherits OpenClass::parentFunction via base<>');
  assert(typeof mc.childFunction === 'function', 'MultiClass own members present');

  // 2. Flattened secondary-parent member
  assert(mc.parentFunctionLight() === 'MultiClass::parentFunctionLight',
    'flattened NarrowInterface::parentFunctionLight dispatches virtually to MultiClass override');
  assert(mc.parentPropertyLight === 'multi-light', 'flattened property works');

  // 3. Explicit upcast helper returns a usable NarrowInterface view
  const narrow = Module.upcastToNarrow(mc);
  assert(narrow !== null && narrow !== undefined, 'upcastToNarrow returns non-null');
  console.log('NOTE: upcast result parentFunctionLight() =', narrow.parentFunctionLight());

  // 4. Distinct C++ objects should produce distinct JS wrappers.
  const mc2 = Module.getMultiClass(); // different object
  assert(mc !== mc2, 'distinct C++ objects yield distinct JS wrappers');

  mc.delete(); mc2.delete();
  console.log(process.exitCode ? 'SPIKE FAILED' : 'SPIKE OK');
}).catch(e => { console.error(e); process.exit(1); });
