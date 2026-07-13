

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/DurationHash.h"
#include "smoke/PosDefaultsWithDuration.h"
#include "chrono"

void register_PosDefaultsWithDuration(py::module_& module) {
    py::class_<PosDefaultsWithDuration>(module, "PosDefaultsWithDuration")
        .def_readwrite("duration_field", &PosDefaultsWithDuration::duration_field)
        .def_readwrite("nanos_field", &PosDefaultsWithDuration::nanos_field)
        ;
}

