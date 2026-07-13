

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/Payload.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Payload = ::gluecodium::smoke::Payload;

void register_Payload(py::module_& module) {
    py::class_<Payload>(module, "Payload")
        .def_readwrite("error_code", &Payload::error_code)
        .def_readwrite("message", &Payload::message)
        .def(py::init<int32_t, ::std::string>(), py::arg("error_code"), py::arg("message"))
        ;
}

