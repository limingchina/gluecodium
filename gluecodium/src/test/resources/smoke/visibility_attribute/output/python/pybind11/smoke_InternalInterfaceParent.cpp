

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InternalInterfaceParent.h"
#include "string"

void register_InternalInterfaceParent(py::module_& module) {
    py::class_<InternalInterfaceParent, std::shared_ptr<InternalInterfaceParent>>(module, "InternalInterfaceParent")
        .def("foo_bar", &InternalInterfaceParent::foo_bar)
        .def_property("prop", &InternalInterfaceParent::get_prop)
        ;
}

