

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/MapScene.h"
#include "cstdint"
#include "functional"
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MapScene = ::smoke::MapScene;


void register_smoke_MapScene(py::module_& module) {
    py::class_<MapScene, std::shared_ptr<MapScene>>(module, "smoke_MapScene")
                .def("load_scene", [](MapScene& self, const int32_t map_scheme, const std::optional< ::std::function<void(const std::optional< ::std::string >&)> >& callback) {
                        self.load_scene(map_scheme, callback);
                }, py::arg("map_scheme"), py::arg("callback"))
                .def("load_scene", [](MapScene& self, const ::std::string& configuration_file, const std::optional< ::std::function<void(const std::optional< ::std::string >&)> >& callback) {
                        self.load_scene(configuration_file, callback);
                }, py::arg("configuration_file"), py::arg("callback"))
        ;
}

