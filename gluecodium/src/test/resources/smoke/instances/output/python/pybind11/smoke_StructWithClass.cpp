

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SimpleClass.h"
#include "smoke/StructWithClass.h"
#include "memory"

void register_StructWithClass(py::module_& module) {
    py::class_<StructWithClass>(module, "StructWithClass")
        .def_readwrite("class_instance", &StructWithClass::class_instance)
        ;
}

