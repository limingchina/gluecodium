

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/DefaultValues.h"
#include "cstdint"
#include "optional"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DefaultValues = ::smoke::DefaultValues;


void register_DefaultValues(py::module_& module) {
    py::class_<DefaultValues, std::shared_ptr<DefaultValues>>(module, "DefaultValues")
        .def_static("process_struct_with_defaults", &DefaultValues::process_struct_with_defaults, py::arg("input"))

        ;
}

