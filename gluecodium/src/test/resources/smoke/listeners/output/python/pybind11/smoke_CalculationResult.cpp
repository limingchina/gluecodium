

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/CalculationResult.h"

void register_CalculationResult(py::module_& module) {
    py::class_<CalculationResult, std::shared_ptr<CalculationResult>>(module, "CalculationResult")
        ;
}

