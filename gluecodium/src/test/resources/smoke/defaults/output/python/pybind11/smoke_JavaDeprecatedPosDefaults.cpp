

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/JavaDeprecatedPosDefaults.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using JavaDeprecatedPosDefaults = ::smoke::JavaDeprecatedPosDefaults;

void register_smoke_JavaDeprecatedPosDefaults(py::module_& module) {
    py::class_<JavaDeprecatedPosDefaults>(module, "smoke_JavaDeprecatedPosDefaults")
        .def_readwrite("first_init_field", &JavaDeprecatedPosDefaults::first_init_field)
        .def_readwrite("first_free_field", &JavaDeprecatedPosDefaults::first_free_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("first_free_field"))
        .def(py::init<int32_t, ::std::string>(), py::arg("first_init_field"), py::arg("first_free_field"))
        ;
}

