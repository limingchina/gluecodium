

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InternalListener.h"

void register_InternalListener(py::module_& module) {
    py::class_<InternalListener, std::shared_ptr<InternalListener>>(module, "InternalListener")
        .def("on_event", &InternalListener::on_event)
        ;
}

