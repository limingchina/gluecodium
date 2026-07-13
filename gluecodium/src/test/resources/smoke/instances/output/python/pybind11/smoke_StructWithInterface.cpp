

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SimpleInterface.h"
#include "smoke/StructWithInterface.h"
#include "memory"

void register_StructWithInterface(py::module_& module) {
    py::class_<StructWithInterface>(module, "StructWithInterface")
        .def_readwrite("interface_instance", &StructWithInterface::interface_instance)
        ;
}

