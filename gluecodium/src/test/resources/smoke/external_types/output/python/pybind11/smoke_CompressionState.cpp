

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/CompressionState.h"

void register_CompressionState(py::module_& module) {
    py::enum_<CompressionState>(module, "CompressionState")
        .value("COMPRESSED", CompressionState::COMPRESSED)
        .value("DECOMPRESSED", CompressionState::DECOMPRESSED)
        .value("NOT_COMPRESSED", CompressionState::NOT_COMPRESSED)
        ;
}

