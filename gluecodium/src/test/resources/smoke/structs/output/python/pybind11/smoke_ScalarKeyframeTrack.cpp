

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/ScalarKeyframe.h"
#include "smoke/ScalarKeyframeTrack.h"
#include "string"
#include "vector"

void register_ScalarKeyframeTrack(py::module_& module) {
    py::class_<ScalarKeyframeTrack>(module, "ScalarKeyframeTrack")
        .def_readwrite("keyframes", &ScalarKeyframeTrack::keyframes)
        .def_readwrite("easing_function", &ScalarKeyframeTrack::easing_function)
        .def_readwrite("interpolation_mode", &ScalarKeyframeTrack::interpolation_mode)
        ;
}

