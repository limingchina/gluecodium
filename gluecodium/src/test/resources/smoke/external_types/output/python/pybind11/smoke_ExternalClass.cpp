

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/Bar.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ::fire::Baz = ::fire::Baz;

void register_ExternalClass(py::module_& module) {
    py::class_<::fire::Baz, std::shared_ptr<::fire::Baz>>(module, "ExternalClass")
        .def("some_method", &::fire::Baz::some_Method, py::arg("some_parameter"))
        .def_property_readonly("some_property", py::overload_cast<>(&::fire::Baz::get_Me, py::const_))
        ;
}

