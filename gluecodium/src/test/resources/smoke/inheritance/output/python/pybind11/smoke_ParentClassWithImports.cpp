

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/IncludableClass.h"
#include "smoke/IncludableEnum.h"
#include "smoke/IncludableLambda.h"
#include "smoke/IncludableStruct.h"
#include "smoke/ParentClassWithImports.h"
#include "functional"
#include "memory"

void register_ParentClassWithImports(py::module_& module) {
    py::class_<ParentClassWithImports>(module, "ParentClassWithImports")
        .def("root_method", &ParentClassWithImports::root_method, py::arg("input1"), py::arg("input2"))
        .def_property("root_property", &ParentClassWithImports::get_root_property)
        ;
}

