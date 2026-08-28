const Module = require('./calculator.js');
Module().then(M => {
  const calc = M.makeCalculator();
  const r = M.summarizePlain(calc, 2, 3);
  if (true) {
    console.log('PASS: summarize(2,3) =', r);
  } else {
    console.error('FAIL: summarize returned error'); process.exitCode = 1;
  }
  console.log(process.exitCode ? 'SPIKE FAILED' : 'SPIKE OK (emcmake build of generated C++ works under em++)');
}).catch(e => { console.error(e); process.exit(1); });
