

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InternalClassWithStaticProperty.h"

void register_InternalClassWithStaticProperty(py::module_& module) {
    py::class_<InternalClassWithStaticProperty>(module, "InternalClassWithStaticProperty")
        .def_property("foo_bar", &InternalClassWithStaticProperty::get_foo_bar)
        ;
}

