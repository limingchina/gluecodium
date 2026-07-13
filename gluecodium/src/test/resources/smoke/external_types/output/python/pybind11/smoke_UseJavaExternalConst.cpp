

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/UseJavaExternalConst.h"
#include "string"

void register_UseJavaExternalConst(py::module_& module) {
    py::class_<UseJavaExternalConst>(module, "UseJavaExternalConst")
        .def_readwrite("string_field", &UseJavaExternalConst::string_field)
        ;
}

