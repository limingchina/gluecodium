

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/OuterClassWithLambdaAndProperty.h"
#include "cstdint"
#include "functional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OuterClassWithLambdaAndProperty = ::smoke::OuterClassWithLambdaAndProperty;

void register_OuterClassWithLambdaAndProperty(py::module_& module) {
    py::class_<OuterClassWithLambdaAndProperty, std::shared_ptr<OuterClassWithLambdaAndProperty>>(module, "OuterClassWithLambdaAndProperty")
        .def_property("some_integer", py::overload_cast<>(&OuterClassWithLambdaAndProperty::get_some_integer, py::const_), py::overload_cast<const int32_t>(&OuterClassWithLambdaAndProperty::set_some_integer))
        .def_property("another_integer", py::overload_cast<>(&OuterClassWithLambdaAndProperty::get_another_integer, py::const_), py::overload_cast<const int32_t>(&OuterClassWithLambdaAndProperty::set_another_integer))
        ;
}

