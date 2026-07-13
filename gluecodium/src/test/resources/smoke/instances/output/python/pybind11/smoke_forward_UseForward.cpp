

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SimpleClass.h"
#include "smoke/SimpleInterface.h"
#include "smoke/forward/Class1.h"
#include "smoke/forward/Class2.h"
#include "smoke/forward/UseForward.h"
#include "memory"

void register_UseForward(py::module_& module) {
    py::class_<UseForward, std::shared_ptr<UseForward>>(module, "UseForward")
        .def("use_it", &UseForward::use_it, py::arg("param1"), py::arg("param2"), py::arg("simple_class"), py::arg("simple_interface"))
        ;
}

