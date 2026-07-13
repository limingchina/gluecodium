

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/Bar.h"
#include "foo/Bazz.h"
#include "gluecodium/VectorHash.h"
#include "non/Sense.h"
#include "smoke/Structs.h"
#include "cstdint"
#include "string"
#include "vector"

void register_Structs(py::module_& module) {
    py::class_<Structs>(module, "Structs")
        .def("get_external_struct", &Structs::get_external_struct)
        .def("get_another_external_struct", &Structs::get_another_external_struct)
        ;
}

