

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "root/space/smoke/BasicTypes.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SomeStruct = ::root::space::smoke::BasicTypes::SomeStruct;

void register_BasicTypesSomeStruct(py::module_& module) {
    py::class_<SomeStruct>(module, "BasicTypesSomeStruct")
        .def_readwrite("some_field", &SomeStruct::some_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;
}

