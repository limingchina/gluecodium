

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/fooTypes.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using fooStruct = ::smoke::fooTypes::fooStruct;

void register_smoke_PlatformNamesBasicStruct(py::module_& module) {
    py::class_<fooStruct>(module, "PlatformNamesBasicStruct")
        .def_readwrite("string_field", &fooStruct::FOO_FIELD)
        .def(py::init<>())
        .def(py::init<::std::string(), py::arg("string_field"))
        .def(py::init<::std::string>(py::arg("basic_parameter")))

        .def_static("make", &fooStruct::FooCreate, py::arg("basic_parameter"))
        ;
}

