

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/MapScene.h"
#include "cstdint"
#include "functional"
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MapScene = ::gluecodium::smoke::MapScene;

void register_MapScene(py::module_& module) {
    py::class_<MapScene, std::shared_ptr<MapScene>>(module, "MapScene")
        .def("load_scene", &MapScene::load_scene, py::arg("map_scheme"), py::arg("callback"))
        .def("load_scene", &MapScene::load_scene, py::arg("configuration_file"), py::arg("callback"))
        ;
}

