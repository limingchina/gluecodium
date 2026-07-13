

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "include/ExternalTypes.h"
#include "string"
#include "vector"

void register_ClassWithOverloads(py::module_& module) {
    py::class_<ClassWithOverloads>(module, "ClassWithOverloads")
        .def("one_overload_not_exposed", &ClassWithOverloads::oneOverloadNotExposed)
        .def("all_overloads_exposed", &ClassWithOverloads::allOverloadsExposed, py::arg("input"))
        .def("all_overloads_exposed", &ClassWithOverloads::allOverloadsExposed, py::arg("input_list"))
        .def("all_overloads_exposed", &ClassWithOverloads::allOverloadsExposed, py::arg("input_string"), py::arg("input_bool"))
        ;
}

