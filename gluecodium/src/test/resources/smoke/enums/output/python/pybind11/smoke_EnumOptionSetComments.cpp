

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnumOptionSetComments.h"

void register_EnumOptionSetComments(py::module_& module) {
    py::enum_<EnumOptionSetComments>(module, "EnumOptionSetComments")
        .value("ONE", EnumOptionSetComments::ONE)
        .value("TWO", EnumOptionSetComments::TWO)
        .value("THREE", EnumOptionSetComments::THREE)
        ;
}

