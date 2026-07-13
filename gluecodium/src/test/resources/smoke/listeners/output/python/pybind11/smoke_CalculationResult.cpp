

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/CalculationResult.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using CalculationResult = ::smoke::CalculationResult;

class CalculationResultTrampoline : public CalculationResult {
public:
    using CalculationResult::CalculationResult;

};

void register_CalculationResult(py::module_& module) {
    py::class_<CalculationResult, std::shared_ptr<CalculationResult>, CalculationResultTrampoline>(module, "CalculationResult")
        .def(py::init<>())
        ;
}

