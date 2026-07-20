

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/fooInterface.h"
#include "smoke/fooTypes.h"
#include "cstdint"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using fooInterface = ::smoke::fooInterface;


void register_PlatformNamesInterface(py::module_& module) {
    py::class_<fooInterface, std::shared_ptr<fooInterface>>(module, "PlatformNamesInterface")
        .def("basic_method", &fooInterface::FooMethod, py::arg("basic_parameter"))

        .def_static("create", &fooInterface::make, py::arg("basic_parameter"))

        .def_property("basic_property", py::overload_cast<>(&fooInterface::GET_FOO_PROPERTY, py::const_), py::overload_cast<const uint32_t>(&fooInterface::SET_FOO_PROPERTY))
        ;
}

