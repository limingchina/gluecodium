

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterClassWithLambdaAndProperty.h"
#include "cstdint"
#include "functional"

void register_OuterClassWithLambdaAndProperty(py::module_& module) {
    py::class_<OuterClassWithLambdaAndProperty>(module, "OuterClassWithLambdaAndProperty")
        .def_property("some_integer", &OuterClassWithLambdaAndProperty::get_some_integer)
        .def_property("another_integer", &OuterClassWithLambdaAndProperty::get_another_integer)
        ;
}

