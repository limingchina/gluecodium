

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ForwardDeclarationBug.h"
#include "smoke/ParentClass.h"
#include "memory"

void register_ForwardDeclarationBug(py::module_& module) {
    py::class_<ForwardDeclarationBug>(module, "ForwardDeclarationBug")
        .def("foo", &ForwardDeclarationBug::foo, py::arg("bar"))
        ;
}

